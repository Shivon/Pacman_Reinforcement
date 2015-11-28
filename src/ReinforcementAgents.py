from game import Directions
from game import Agent
import game
import pacman
import random

class AbstractQState():
    def __init__(self, state, direction):
        self.state = state
        self.direction = direction
        
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.state == other.state and self.direction == other.direction
        else:
            return False
    def __hash__(self):
        return hash(hash(self.state) + hash(self.direction))    
        
class Saving():
    def __init__(self, evalFn="scoreEvaluation"):
        self.savedStates = {}
    
    def getValue(self, state, direction):
        abstractState = AbstractQState(state, direction)
        value = self.savedStates.get(abstractState)
        if value == None:
            return 0
        else:
            return value
            
    def setValue(self, state, direction, value):
        abstractState = AbstractQState(state, direction)
        self.savedStates[abstractState] = value
    
    def getBestDirection(self, state, directions):
        bestVal = float('-inf')
        bestDirection = None
        for direction in directions:
            tmpValue = self.getValue(state, direction)
            if bestVal < tmpValue:
                bestVal = tmpValue
                bestDirection = direction
        return bestDirection
        
    def getBestValue(self, state, directions):
        bestDirection = self.getBestDirection(state,directions)
        if bestDirection:
            return self.getValue(state,bestDirection)
        else:
            return 0.0
            
    def __repr__(self):
        return str(self.savedStates)
        
class ReinforcementTHAgent(game.Agent):
    def __init__(self, numTraining = 0):
         print "init"
         self.saving = Saving()
         self.random = random.Random()
         self.lastState = None
         self.lastAction = None
         self.alpha = 0.5
         self.gamma = 1
         self.epsilon = 0.5
         self.numTraining = int(numTraining)
         self.episodesSoFar = 0
         
    def getAction(self, state):
        actions = self.legalActions(state)
        rnd = self.random.random()
        if self.epsilon > rnd:
            #print "random " + str(rnd) + " gamma " + str(self.epsilon)
            self.lastAction = self.random.choice(actions)
        else:
            self.lastAction = self.saving.getBestDirection(self.lastState, actions)
        return self.lastAction
    
    def calcReward(self, state):
        return state.getScore() - self.lastState.getScore()
    
    def legalActions(self, state):
        actions = state.getLegalPacmanActions()
        self.safeListRemove(actions, Directions.LEFT)
        self.safeListRemove(actions, Directions.REVERSE)
        self.safeListRemove(actions, Directions.RIGHT)
        self.safeListRemove(actions, Directions.STOP)
        return actions
    
    def safeListRemove(self,lst,item):
        try:
            lst.remove(item)
        except ValueError: 
            pass
        
    def updater(self, state):
        reward = self.calcReward(state)
        currentQValue = self.saving.getValue(self.lastState, self.lastAction)
        maxPossibleFutureQValue = self.saving.getBestValue(state, self.legalActions(state))
        calcVal =  currentQValue + self.alpha * (reward + self.gamma * maxPossibleFutureQValue - currentQValue)
        self.saving.setValue(self.lastState, self.lastAction, calcVal)
        
    def observationFunction(self, state):
        if self.lastState:
            self.updater(state)
        self.lastState = state
        return state
        
    def final(self, state):
        self.updater(state)
        self.lastState = None
        self.lastAction = None
        if self.isInTraining():
            self.episodesSoFar += 1
            print "Training " + str(self.episodesSoFar) + " of " + str (self.numTraining)
        else:
            self.epsilon = 0.0 
            self.alpha = 0.0

    def isInTraining(self):
        return self.episodesSoFar < self.numTraining

    def isInTesting(self):
        return not self.isInTraining()
