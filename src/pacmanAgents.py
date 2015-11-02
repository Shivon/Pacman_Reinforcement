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

    def __init__(self, state, evalFn="scoreEvaluation"):
        # Config = ConfigParser.ConfigParser()
        # Config.read(CONFIGURATIONSARSA_FILE)
        steps = 4
        alpha = 0.2
        gammar = 0.2
        # wird noch nicht gebraucht
        epsilon = 0
        ourLambda = 1
        queue = Queue.Queue(steps)
        lastStateAction = 0

    def getAction(self, state):
        reward = -0.4
        return SarsaAgent.sarsaAlgo(self, state, reward)

    def sarsaAlgo(self, state, reward):
        if self.lastStateAction == 0:
            self.firstInit()
        """momentan ohne explorationsrate"""
        currentStateAction = ReinforcementState.ReinforcementState.toBin()
        # currentStateAction = pacman.GameState.getLegalPacmanActions()
        posInQueue = len(self.queue) - 1
        for elem in self.queue:
            delta = reward + (self.gammar * currentStateAction) - self.lastStateAction
            elem1 = elem + delta * self.alpha * pow(self.ourLambda, posInQueue)
            print elem1
            self.queue.pop(elem)
            self.queue.push(elem1)
            posInQueue -= 1
        self.lastStateAction  = currentStateAction

        if len(self.queue) > self.steps:
            self.queue.remove()

        self.queue.push(currentStateAction)

    def firstInit(self):
        currentStateAction = ReinforcementState.ReinforcementState.toBin()
        # currentStateAction = pacman.GameState.getLegalPacmanActions()
        lastStateAction = currentStateAction
        self.queue.push(currentStateAction)