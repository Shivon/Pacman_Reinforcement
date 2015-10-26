# pacmanAgents.py
# ---------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from pacman import Directions
from game import Agent
import random
import game
import util
import Queue

class NearestObjectSearchData:
    def __init__(self, direction, distance, eatable):
        self.direction = direction
        self.distance = distance
        self.eatable = eatable
    
    def getDirection(self):
        return self.direction
        
    def getDistance(self):
        return self.distance
    
    def isEatable(self):
        return self.eatable

class NearestObjectSearchResult:
    def __init__(self, nextFoodLocData, ghostsLocData):
        self.nextFoodLocData = nextFoodLocData
        self.ghostsLocData = ghostsLocData
    
    def getNextFoodLocData(self):
        return self.nextFoodLocData
        
    def getGhostsLocData(self):
        return self.ghostsLocData

class NearestObjectSearch:
    def __init__(self, state):
        self.state = state
        
    def isUnblocked(self, position):
        wallPositions = self.state.data.layout.walls.asList()
        minPosX = 0
        maxPosX = self.state.data.layout.getWidth()-1
        minPosY = 0
        maxPosY = self.state.data.layout.getHeight()-1
        
        if (position in wallPositions):
            return False
        if (position[0] < minPosX):
            return False
        if (position[0] > maxPosX):
            return False
        if (position[1] < minPosY):
            return False
        if (position[1] > maxPosY):
            return False
        
        return True
        
    def getChilds(self, position):
        childs = []
            
        top = (position[0], position[1]-1)
        if (self.isUnblocked(top)):
            childs.append(top)
        
        right = (position[0]+1, position[1])
        if (self.isUnblocked(right)):
            childs.append(right)
        
        bottom = (position[0], position[1]+1)
        if (self.isUnblocked(bottom)):
            childs.append(bottom)
            
        left = (position[0]-1, position[1])
        if (self.isUnblocked(left)):
            childs.append(left)
        
        return childs
    
    def getDirection(self, positionFrom, positionTo):
        if (positionFrom[1] > positionTo[1]):
            return Directions.SOUTH
            
        if (positionFrom[0] < positionTo[0]):
            return Directions.EAST
            
        if (positionFrom[1] < positionTo[1]):
            return Directions.NORTH
            
        if (positionFrom[0] > positionTo[0]):
            return Directions.WEST
            
        return Directions.STOP
    
    def getObjectData(self, position, previousNodes, eatable):
        node = (int(position[0]), int(position[1]))
        path = []
        while (node != None):
            path.append(node)
            node = previousNodes[node]
        
        direction = self.getDirection(path[-1], path[-2])
        length = len(path)-1
        
        result = NearestObjectSearchData(direction, length, eatable)
        return result

    def getResult(self):
        root = self.state.getPacmanPosition()
        foodPositions = self.state.getFood().asList() + []
        
        queue = Queue.Queue()
        visited = []
        queue.put(root)
        visited.append(root)
        
        previousNodes = {}
        previousNodes[root] = None
        
        nextFood = None
        
        while (not queue.empty()):
            node = queue.get()
            if ((nextFood == None) and (node in foodPositions)):
                nextFood = node
            
            childs = self.getChilds(node)
            random.shuffle(childs) # Shuffle position of elements
            
            for child in childs:
                if (not (child in visited)):
                    previousNodes[child] = node
                    queue.put(child)
                    visited.append(child)
        
        nextFoodLoc = self.getObjectData(nextFood, previousNodes, True)
        ghostsLoc = []
        index = 1
        while index < self.state.getNumAgents():
            ghostPosition = self.state.getGhostPosition(index)
            ghostEatable = self.state.getGhostState(index).isScared()
            ghostsLoc.append(self.getObjectData(ghostPosition, previousNodes, ghostEatable))
            index += 1
        
        return NearestObjectSearchResult(nextFoodLoc, ghostsLoc)
