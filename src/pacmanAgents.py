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
import ConfigParser

from bfsSearch import ReinforcementSearch
from ReinforcementState import ReinforcementDirection, ReinforcementState
from pacman import Directions
from game import Agent
import random
import game
import pacman
from ReinforcementSave import ReinforcementSave
from pacmanGlobals import PacmanGlobals
import util
import Queue
from ReinforcementSave import *

CONFIGURATIONSARSA_FILE = "sarsasettings.ini"

class LeftTurnAgent(game.Agent):
    "An agent that turns left at every opportunity"

    def getAction(self, state):
        legal = state.getLegalPacmanActions()
        current = state.getPacmanState().configuration.direction
        if current == Directions.STOP: current = Directions.NORTH
        left = Directions.LEFT[current]
        if left in legal: return left
        if current in legal: return current
        if Directions.RIGHT[current] in legal: return Directions.RIGHT[current]
        if Directions.LEFT[left] in legal: return Directions.LEFT[left]
        return Directions.STOP

class GreedyAgent(game.Agent):
    def __init__(self, evalFn="scoreEvaluation"):
        self.evaluationFunction = util.lookup(evalFn, globals())
        assert self.evaluationFunction != None

    def getAction(self, state):
        # Generate candidate actions
        legal = state.getLegalPacmanActions()
        if Directions.STOP in legal: legal.remove(Directions.STOP)

        successors = [(state.generateSuccessor(0, action), action) for action in legal]
        scored = [(self.evaluationFunction(state), action) for state, action in successors]
        bestScore = max(scored)[0]
        bestActions = [pair[1] for pair in scored if pair[0] == bestScore]
        return random.choice(bestActions)

class BfsAgent(game.Agent):
    def __init__(self, evalFn="scoreEvaluation"):
        self.rand = random.Random()
    
    def evade(self, direction, state):
        legal = state.getLegalPacmanActions()
        if Directions.STOP in legal: legal.remove(Directions.STOP)
        if direction in legal: legal.remove(direction)
        if (not legal):
            return Directions.STOP
        else:
            return self.rand.choice(legal)
        
    def goTo(self, direction, state):
        legal = state.getLegalPacmanActions()
        if direction in legal: return direction
        if (not legal):
            return Directions.STOP
        else:
            return self.rand.choice(legal)
    
    def getNearestEnermy(self, state, reinforcementState):
        nearestEnermy = None
        lastThreat = 9223372036854775807
        
        index = 1
        while index < state.getNumAgents():
            for ghostState in reinforcementState.ghosts:
                if (not ghostState.isEatable):
                    if (lastThreat > ghostState.threat):
                        lastThreat = ghostState.threat
                        nearestEnermy = ghostState
            index += 1
            
        return nearestEnermy
        
    def getNearestEatable(self, state, reinforcementState):
        nearestEnermy = None
        lastThreat = 9223372036854775807
        
        index = 1
        while index < state.getNumAgents():
            for ghostState in reinforcementState.ghosts:
                if (ghostState.isEatable):
                    if (lastThreat > ghostState.threat):
                        lastThreat = ghostState.threat
                        nearestEnermy = ghostState
            index += 1
            
        return nearestEnermy
    
    def getAction(self, state):
        evadeThreat = 2
        
        reinforcementState = ReinforcementSearch(state).getReinforcmentResult()
        # SarsaAgent.sarsaAlgo(reinforcementState)
        # EVADE UNEATABLE GHOST
        nearestEnermy = self.getNearestEnermy(state, reinforcementState)
        if (nearestEnermy != None):
            if (nearestEnermy.threat < evadeThreat):
                evadeDirection = ReinforcementDirection.toGameDirection(nearestEnermy.direction)
                return self.evade(evadeDirection, state)

        # GET NEAREST FOOD
        return ReinforcementDirection.toGameDirection(reinforcementState.bestDirection)

def scoreEvaluation(state):
    return state.getScore()


class SarsaAgent(game.Agent):

    def __init__(self, evalFn="scoreEvaluation"):
        self.steps = 4
        self.alpha = 0.2
        # Discount-rate
        self.gamma = 0.8
        self.epsilon = 0.1
        self.ourLambda = 0.9
        self.lastStateActionRating = None
        self.randomNum = random.Random()
        self.ringBuffer = []
        # self.ghostCount = PacmanGlobals.numGhostAgents
        self.ghostCount = 1
        self.ratingStorage = ReinforcementSave("ratingStorageFor" + str(self.ghostCount), self.ghostCount)
        self.prevState = None
        self.lastAction = None

    def getAction(self, state):
        reinforcementState = ReinforcementSearch(state).getReinforcmentResult()
        legalActions = state.getLegalPacmanActions()
        legalActions.remove('Stop')
        self.prevState = state
        if (self.epsilon * 100) > (self.randomNum.random() * 100 + 1):
            """ choose best next action. With 10% choose random action """
            index = int(self.randomNum.random() * len(legalActions))
            legalDirection = legalActions[index]
            bestRating = self.ratingStorage.getRatingForNextState(legalDirection, reinforcementState)
            nextBestAction = [legalDirection, bestRating, reinforcementState]
        else:
            nextBestAction = self.getBestAction(legalActions, reinforcementState)
        # print nextBestAction
        self.lastAction = nextBestAction
        return nextBestAction[0]
        # return self.sarsaAlgo(reinforcementState, legalActions, reward)


    """ choose best action for state """
    def getBestAction(self, directions, state):
        # getRatingForNextState(self, wentDirection, state):
        bestDirection = directions[0]
        bestRating = self.ratingStorage.getRatingForNextState(bestDirection, state)
        for direction in directions:
            ratingCurrDirection = self.ratingStorage.getRatingForNextState(direction, state)
            if (bestRating < ratingCurrDirection):
                bestDirection = direction
                bestRating = ratingCurrDirection
        # print "--- [bestDirection, bestRating, state] --- " + str([bestDirection, bestRating, state])
        return [bestDirection, bestRating, state]

    def sarsaAlgo(self, action, reward):
        self.updateRingBuffer(action, reward)

    """ update ringbuffer in which last stateActions are hold """
    def updateRingBuffer(self, nextBestAction, reward):
        # nextAction = nextBestAction[0]
        nextRating = nextBestAction[1]
        """ If ringBuffer has no items yet """
        if not self.ringBuffer:
            self.lastStateActionRating = 0

        """ Add new item """
        self.ringBuffer.insert(0, nextBestAction)
        """ if more than steps items in buffer remove last (oldest) one """
        if len(self.ringBuffer) >= self.steps:
            # deletes last element in list, returns it
            self.ringBuffer.pop()
        """ compute new rating """
        for index in range(0, len(self.ringBuffer)):
            delta = reward + (self.gamma * nextRating) - self.lastStateActionRating
            self.ringBuffer[index][1] = delta * self.alpha * pow(self.ourLambda, index)
            print self.ringBuffer[index][1]
            self.ratingStorage.setRatingForState(self.ringBuffer[index][0], self.ringBuffer[index][2], self.ringBuffer[index][1])
        # print "-- self.ringBuffer --- " + str(self.ringBuffer)
        """ choose first item from ringbuffer to be the last action """
        self.lastStateActionRating = self.ringBuffer[0][1]

    def calcReward(self, state):
        reward = 0
        # pos reward für Große Punkt
        # pos reward für Geister fressen wenn großer Punkt
        # pos reward win game
        # neg reward für Geist friss Pacman
        # neg reward loss game
        # neg reward gegen Wand laufen
        return reward

    """ Is called after each step """
    def observationFunction(self, state):
        if self.lastAction:
            # reward = -0.4
            reward = state.getScore() - self.prevState.getScore()
            print "--- reward --- " + str(reward)
            # print [method for method in dir(state) if callable(getattr(state, method))]
            # print self.prevState
            # print self.lastAction
            self.sarsaAlgo(self.lastAction, reward)
        return state

    """ Is calles at the end of game """
    def final(self, state):
        reward = state.getScore() - self.prevState.getScore()
        self.sarsaAlgo(self.lastAction, reward)
        self.lastAction = None
        self.ringBuffer = []
        self.prevState = None
        self.lastStateActionRating = None
        # print self.prevState
        # print state
        print state.isLose()
