from pacman import Directions
from game import Agent
from ReinforcementState import *
from types import *
import array
import random
import game
import util
import Queue

# BFS algorithm to get information about nearest way to ghosts and nearest food
class ReinforcementSearch:
    # Settings for algorithm
    ADD_CAPSULES_TO_FEED = True
    CHOOSE_RANDOM_IF_MULTIPLE_NEAREST = True
    
    # Constructor
    def __init__(self, state):
        self.rand = random.Random()
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

    # Converts a 2D position to a 1D position, depending on fields width
    def toPos1D(self, pos2D):
        return ((self.width * int(pos2D[1])) + int(pos2D[0]))
    
    # Initialize input for executeBFS method
    def initializeInput(self):
        # Save pacman's position
        self.pacmanPosition = self.toPos1D(self.state.getPacmanPosition())
        
        # Add wall positions
        walls = self.state.data.layout.walls.asList()
        for wall in walls:
            self.wallPostitions.append(self.toPos1D(wall))
        
        # Add feed positions
        foods = self.state.getFood().asList()
        for food in foods:
            self.foodPositions.append(self.toPos1D(food))
        
        # Add capsules (power food) positions to feed positions
        if (ReinforcementSearch.ADD_CAPSULES_TO_FEED):
            capsules = self.state.getCapsules()
            for capsule in capsules:
                self.foodPositions.append(self.toPos1D(capsule))
        
        # Save ghost states (position, eatable, processed and count)
        ghostStates = self.state.getGhostStates()
        for ghostState in ghostStates:
            self.ghostPositions.append(self.toPos1D(ghostState.getPosition()))
            self.ghostEatable.append(ghostState.isScared())
            self.ghostProcessed.append(False)
            self.numGhosts = self.numGhosts + 1
    
    # All ghosts processed?
    def isGhostsProcessed(self):
        return (not(False in self.ghostProcessed))
    
    # Get row of 1D position
    def getRow(self, position):
        return (position / self.width)
        
    # Get column of 1D position
    def getColumn(self, position):
        return (position % self.width)
    
    # Get accessable nearbours of passed 1D position
    # (returns a list of 1D positions)
    def getChilds(self, position):
        childs = []
        
        # Determine possible nearbours
        top = position - self.width
        bottom = position + self.width
        left = position - 1
        right = position + 1
        
        # Add top if not out of range and not a wall
        if ((top > 0) and (top < self.fieldSize)):
            if (not(top in self.wallPostitions)):
                childs.append(top)
        
        # Add bottom if not out of range and not a wall
        if ((bottom > 0) and (bottom < self.fieldSize)):
            if (not(bottom in self.wallPostitions)):
                childs.append(bottom)
        
        # Add left if not out of range and not a wall
        if (self.getRow(position) == self.getRow(left)):
            if (not(left in self.wallPostitions)):
                childs.append(left)
        
        # Add right if not out of range and not a wall
        if (self.getRow(position) == self.getRow(right)):
            if (not(right in self.wallPostitions)):
                childs.append(right)
        
        # Shuffle position of elements
        # Purpose: Choosing random food, if multiple food in same distance but with different directions
        if (ReinforcementSearch.CHOOSE_RANDOM_IF_MULTIPLE_NEAREST):
            self.rand.shuffle(childs)
        
        return childs
    
    # Executes a BFS algorithm until one feed is found and all ghosts are processed
    def executeBFS(self):
        INFINITY = 2147483647
        
        self.edgeTo = array.array('i', [-1] * (self.fieldSize))
        self.distTo = array.array('i', [INFINITY] * (self.fieldSize))
        marked = array.array('b', [False] * (self.fieldSize))
        
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
    
    # Get result path of BFS algorithm for target 1D Position
    # Returns a list of 1D position, which represent the path
    # The first element of the result path is the target position
    # The last element of the result path is pacman's position
    def getPath(self, targetPosition):
        path = []
        
        x = targetPosition
        while (self.distTo[x] != 0):
            path.append(x)
            x = self.edgeTo[x]
        path.append(x)
        
        return path;
    
    # Get direction of first step toward target position
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
    
    # Get distance (count of steps) toward target position
    def getDistance(self, targetPosition):
        return self.distTo[targetPosition]
    
    # Generates a ReinforcementState for the BFS algorithm result
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
    
    # Generates a ReinforcementState by using the BFS algorithm
    def getReinforcmentResult(self):
        self.initializeInput()
        self.executeBFS()
        return self.generateResult()


    def getPacmanPosition(self):
        return self.state.getPacmanPosition()