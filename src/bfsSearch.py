from pacman import Directions
from game import Agent
from ReinforcementState import *
from types import *
import random
import game
import util
import Queue

# BFS algorithm to get information about nearest way to ghosts and nearest food
class NearestObjectSearch:
    def __init__(self, state):
        self.state = state
        self.width = self.state.data.layout.getWidth()
        self.height = self.state.data.layout.getHeight()
        self.fieldSize = self.width * self.height
        self.numGhosts = 0
        self.nearestFoodPosition = None
        self.pacmanPosition = None
        self.wallPostitions = []
        self.foodPositions = []
        self.ghostPositions = []
        self.ghostEatable = []
        self.ghostProcessed = []

    def toPos1D(self, pos2D):
        #assert type(pos2D[0]) is IntType, "pos2D[0] is not an integer: %r" % pos2D[0]
        #assert type(pos2D[1]) is IntType, "pos2D[1] is not an integer: %r" % pos2D[1]
        return ((self.width * int(pos2D[1])) + int(pos2D[0]))
    
    def initializeInput(self):
        # initialize state data
        self.pacmanPosition = self.toPos1D(self.state.getPacmanPosition())
        
        walls = self.state.data.layout.walls.asList()
        for wall in walls:
            self.wallPostitions.append(self.toPos1D(wall))
        
        foods = self.state.getFood().asList()
        for food in foods:
            self.foodPositions.append(self.toPos1D(food))
        
        ghostStates = self.state.getGhostStates()
        for ghostState in ghostStates:
            self.ghostPositions.append(self.toPos1D(ghostState.getPosition()))
            self.ghostEatable.append(ghostState.isScared())
            self.ghostProcessed.append(False)
            self.numGhosts = self.numGhosts + 1
            
    def isGhostsProcessed(self):
        return (not(False in self.ghostProcessed))
    
    def getRow(self, position):
        assert type(position) is IntType, "position is not an integer: %r" % position
        assert type(self.width) is IntType, "self.width is not an integer: %r" % self.width
        assert type(self.height) is IntType, "self.height is not an integer: %r" % self.height
        return (position / self.width)
    
    def getChilds(self, position):
        childs = []
        
        top = position - self.width
        bottom = position + self.width
        left = position - 1
        right = position + 1
        
        if ((top > 0) and (top < self.fieldSize)):
            if (not(top in self.wallPostitions)):
                childs.append(top)
        
        if ((bottom > 0) and (bottom < self.fieldSize)):
            if (not(bottom in self.wallPostitions)):
                childs.append(bottom)
                
        if (self.getRow(position) == self.getRow(left)):
            if (not(left in self.wallPostitions)):
                childs.append(left)
                
        if (self.getRow(position) == self.getRow(right)):
            if (not(right in self.wallPostitions)):
                childs.append(right)
        
        # Shuffle position of elements
        # Purpose: Choosing random food, if multiple food in same distance but with different directions
        random.shuffle(childs)
        return childs
        
    def executeBFS(self):
        INFINITY = 9223372036854775807
        
        self.edgeTo = [None] * (self.fieldSize)
        self.distTo = [INFINITY] * (self.fieldSize)
        marked = [False] * (self.fieldSize)
        
        s = self.pacmanPosition
        q = Queue.Queue()
        
        self.distTo[s] = 0
        marked[s] = True
        q.put(s)
        
        while (not q.empty()):
            v = q.get()
            
            finished = True
            if (self.nearestFoodPosition == None):
                if (v in self.foodPositions):
                    self.nearestFoodPosition = v
                else:
                    finished = False
                    
            for i in range(0, self.numGhosts):
                if (not self.ghostProcessed[i]):
                    if (v == self.ghostPositions[i]):
                        self.ghostProcessed[i] = True
                    else:
                        finished = False
            
            if (finished):
                return
            
            for w in self.getChilds(v):
                if (not marked[w]):
                    self.edgeTo[w] = v
                    self.distTo[w] = self.distTo[v] + 1
                    marked[w] = True
                    q.put(w)
    
    def getPath(self, targetPosition):
        path = []
        
        x = targetPosition
        while (self.distTo[x] != 0):
            path.append(x)
            x = self.edgeTo[x]
        path.append(x)
        
        return path;
    
    def getDirection(self, targetPosition):
        path = self.getPath(targetPosition)
        
        positionFrom = self.pacmanPosition
        positionTo = path[-2]
        
        if (positionTo == (positionFrom - 1)):
            return ReinforcementDirection.WEST
            
        if (positionTo == (positionFrom + 1)):
            return ReinforcementDirection.EAST
            
        if (positionTo < positionFrom):
            return ReinforcementDirection.SOUTH
            
        if (positionTo > positionFrom):
            return ReinforcementDirection.NORTH
            
    def getDistance(self, targetPosition):
        return self.distTo[targetPosition]
    
    def generateResult(self):
        # generate food direction
        nearestFoodDirection = self.getDirection(self.nearestFoodPosition)
        
        # generate ghost state
        ghostStates = []
        for i in range(0, self.numGhosts):
            ghostPosition = self.ghostPositions[i]
            direction = self.getDirection(ghostPosition)
            threat = Threat.fromDistance(self.getDistance(ghostPosition))
            eatable = self.ghostEatable[i]
            ghostStates.append(GhostState(direction, threat, eatable))
        
        # return result
        return ReinforcementState(nearestFoodDirection, ghostStates)
    
    def getReinforcmentResult(self):
        self.initializeInput()
        self.executeBFS()
        return self.generateResult()
