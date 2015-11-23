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
        return ReinforcementDirection.toGameDirection(reinforcementState.nextFoodDirection)

def scoreEvaluation(state):
    return state.getScore()



class QLearningAgent(game.Agent):
    alphacounter = 0

    def __init__(self):
        QLearningAgent.alphacounter += (1)
        # learning rate (0 < alpha < 1)
        self.alpha = 0.3/QLearningAgent.alphacounter
        # Discount-rate
        self.gamma = 0.8
        self.epsilon = 0.1
        self.randomNum = random.Random()
        self.ghostCount = PacmanGlobals.numGhostAgents
        self.prevState = None
        self.bestRating = None
        self.lastAction = None
        self.ratingStorage = ReinforcementSave("ratingStorageFor" + str(self.ghostCount), self.ghostCount)

    def getAction(self, state):
        reinforcementState = ReinforcementSearch(state).getReinforcmentResult()
        legalActions = state.getLegalPacmanActions()
        legalActions.remove('Stop')
        # print "state " + str(state)
        # print state.getPacmanPosition()
        self.prevState = state
        if (self.epsilon * 100) > (self.randomNum.random() * 100 + 1):
            """ choose best next action. With 10% choose random action """
            index = int(self.randomNum.random() * len(legalActions))
            legalDirection = legalActions[index]
            self.bestRating = self.ratingStorage.getRatingForNextState(legalDirection, reinforcementState)
            nextBestAction = [legalDirection, self.bestRating, reinforcementState,  self.prevState]
        else:
            nextBestAction = self.getBestAction(legalActions, reinforcementState)
        self.lastAction = nextBestAction
        return nextBestAction[0]

    def qlearning(self, stateAction, reward):
        legalActions = stateAction[3].getLegalPacmanActions()
        legalActions.remove('Stop')
        bestNextAction = self.getBestAction(legalActions, stateAction[2])
        bestNextActionRate = bestNextAction[1]
        rating = self.bestRating + self.alpha * (reward + self.gamma * bestNextActionRate - self.bestRating)
        self.ratingStorage.setRatingForState(stateAction[0], stateAction[2], rating)


    """ choose best action for state """
    def getBestAction(self, directions, state):
        # getRatingForNextState(self, wentDirection, state):
        bestDirection = directions[0]
        self.bestRating = self.ratingStorage.getRatingForNextState(bestDirection, state)
        for direction in directions:
            ratingCurrDirection = self.ratingStorage.getRatingForNextState(direction, state)
            if (self.bestRating < ratingCurrDirection):
                bestDirection = direction
                self.bestRating = ratingCurrDirection
        return [bestDirection, self.bestRating, state, self.prevState]

    def calcReward(self, state):
        reward = -5
        rewardSmallPoints = (len(self.prevState.getFood().asList()) - len(state.getFood().asList())) * 20
        rewardEatablePoint = (len(self.prevState.getCapsules()) - len(state.getCapsules())) * 20
        rewardEatGhost = 0
        rewardLose = 0
        rewardWin = 0
        PacmanPos = state.getPacmanPosition()
        for ghostPos in state.getGhostPositions():
            if (not state.isLose()) and ((int(ghostPos[0]) == PacmanPos[0]) and (int(ghostPos[1]) == PacmanPos[1])):
                rewardEatGhost = 100

        if state.isLose():
            rewardLose = -300
        elif state.isWin():
            rewardWin = 300
        reward += rewardSmallPoints + rewardEatablePoint + rewardEatGhost + rewardWin + rewardLose
        # print reward
        return reward

    """ Is called after each step """
    def observationFunction(self, state):
        if self.lastAction:
            reward = self.calcReward(state)
            self.qlearning(self.lastAction, reward)
        return state

    """ Is calles at the end of game """
    def final(self, state):
        reward = self.calcReward(state)
        self.qlearning(self.lastAction, reward)
        self.prevState = None
        self.bestRating = None
        self.lastAction = None
        print state.isLose()


class SarsaAgent(game.Agent):

    def __init__(self, evalFn="scoreEvaluation"):
        # Number of indices in RingBuffer to save last StateActions
        self.steps = 4
        # learning rate (0 < alpha < 1)
        self.alpha = 0.4
        # Discount-rate
        self.gamma = 0.8
        # Exploration Rate
        self.epsilon = 0.1
        # decrease of qValues for older actions
        self.ourLambda = 0.9
        self.lastStateActionRating = None
        self.randomNum = random.Random()
        # ringbuffer indices: [bestDirection, bestRating, reinforcemenState, pacmansPosition]
        self.ringBuffer = []
        self.ghostCount = PacmanGlobals.numGhostAgents
        # self.ghostCount = 1
        self.ratingStorage = ReinforcementSave("ratingStorageFor" + str(self.ghostCount), self.ghostCount)
        self.prevState = None
        self.lastAction = None
        self.pacmanPos = None

    def getAction(self, state):
        reinforcementState = ReinforcementSearch(state).getReinforcmentResult()
        self.pacmanPos =  ReinforcementSearch(state).getPacmanPosition()
        legalActions = state.getLegalPacmanActions()
        legalActions.remove('Stop')
        # print "state " + str(state)
        # print state.getPacmanPosition()
        self.prevState = state
        if (self.epsilon * 100) > (self.randomNum.random() * 100 + 1):
            """ choose best next action. With 10% choose random action """
            index = int(self.randomNum.random() * len(legalActions))
            legalDirection = legalActions[index]
            bestRating = self.ratingStorage.getRatingForNextState(legalDirection, reinforcementState)
            nextBestAction = [legalDirection, bestRating, reinforcementState, self.pacmanPos]
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
        # print "--- [bestDirection, bestRating, state, self.pacmanPos] --- " + str([bestDirection, bestRating, state, self.pacmanPos])
        return [bestDirection, bestRating, state, self.pacmanPos]

    def sarsaAlgo(self, currentBestAction, reward):
        if not self.ringBuffer:
            """ If ringBuffer has no items yet """
            self.lastStateActionRating = 0
            # self.lastStateActionRating = currentBestAction[1]

        """ if more than steps items in buffer remove last (oldest) one """
        if len(self.ringBuffer) >= self.steps:
            self.ringBuffer.pop()

        """ Add new item """
        self.ringBuffer.insert(0, currentBestAction)
        delta = reward + (self.gamma * self.ringBuffer[0][1]) - self.lastStateActionRating
        self.updateRingBuffer(currentBestAction, delta)
        """ choose first item from ringbuffer to be the last action """
        self.lastStateActionRating = self.ringBuffer[0][1]


    """ update ringbuffer in which last stateActions are hold """
    def updateRingBuffer(self, currentBestAction, delta):
        currentPacmanPos = self.ringBuffer[0][3]
        # print currentPacmanPos
        # print " this is the state   " + str(self.ringBuffer[0][2])
        for index in range(1, len(self.ringBuffer)):
            """ compute new rating """
            self.ringBuffer[index][1] = delta * self.alpha * pow(self.ourLambda, index)
            # print " current pos in buffer " + str(self.ringBuffer[index][3])
            # print " pos of pacman " + str(currentPacmanPos)
            # print " state in buffer " + str(self.ringBuffer[index][0])
            # print " state pacman " + str(self.ringBuffer[0][0])
            # """ If Pacman position now is not the same as the current one in buffer """
            # if not (self.ringBuffer[index][3] == currentPacmanPos):
            #     # print "different state " + str(self.ringBuffer[index][3]) + " AMD " + str(currentPacmanPos)
            #     self.ringBuffer[index][1] = delta * self.alpha * pow(self.ourLambda, index)
            #     # print self.ringBuffer[index][1]
            #     """ Pacman position now is same as the current one in buffer and actions are not the same """
            # elif (self.ringBuffer[index][3] == currentPacmanPos) and not (self.ringBuffer[index][0] == self.ringBuffer[0][0]):
            #     # print "different action " + str(self.ringBuffer[index][0]) + " AMD " + str(self.ringBuffer[0][0])
            #     self.ringBuffer[index][1] = 0
            # elif (self.ringBuffer[index][3] == currentPacmanPos) and (self.ringBuffer[index][0] == self.ringBuffer[0][0]):
            #     # print "same state action " + str(self.ringBuffer[index][3]) + " AMD " + str(currentPacmanPos) + " action: " + str(self.ringBuffer[index][0]) + " AMD " + str(self.ringBuffer[0][0])
            #     self.ringBuffer[index][1] = delta * self.alpha * pow(self.ourLambda, index) + 1
            self.ratingStorage.setRatingForState(self.ringBuffer[index][0], self.ringBuffer[index][2], self.ringBuffer[index][1])


    def calcReward(self, state):
        # pos reward fuer Grosse Punkt
        # pos reward fuer Geister fressen wenn grosser Punkt
        # pos reward win game
        # neg reward loss game
        reward = 0
        rewardSmallPoints = (len(self.prevState.getFood().asList()) - len(state.getFood().asList())) * 20
        rewardEatablePoint = (len(self.prevState.getCapsules()) - len(state.getCapsules())) * 20
        rewardEatGhost = 0
        rewardLose = 0
        rewardWin = 0
        PacmanPos = state.getPacmanPosition()
        for ghostPos in state.getGhostPositions():
            if (not state.isLose()) and ((int(ghostPos[0]) == PacmanPos[0]) and (int(ghostPos[1]) == PacmanPos[1])):
                rewardEatGhost = 100

        if state.isLose():
            rewardLose = -300
        elif state.isWin():
            rewardWin = 300
        reward += rewardSmallPoints + rewardEatablePoint + rewardEatGhost + rewardWin + rewardLose
        # print reward
        return reward

    """ Is called after each step """
    def observationFunction(self, state):
        if self.lastAction:
            reward = self.calcReward(state)
            # reward = state.getScore() - self.prevState.getScore()
            # print "--- reward --- " + str(reward)
            self.sarsaAlgo(self.lastAction, reward)
        return state

    """ Is calles at the end of game """
    def final(self, state):
        reward = self.calcReward(state)
        # reward = state.getScore() - self.prevState.getScore()
        # print [method for method in dir(object) if callable(getattr(object, method))]
        self.sarsaAlgo(self.lastAction, reward)
        self.lastAction = None
        self.ringBuffer = []
        self.prevState = None
        self.lastStateActionRating = None
        print state.isLose()
