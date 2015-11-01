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

from bfsSearch import ReinforcementSearch
from ReinforcementState import ReinforcementDirection
from pacman import Directions
from game import Agent
import random
import game
import util
import Queue

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
        assert True

    def getAction(self, state):
        return SarsaAgent.sarsaAlgo(self, state)


    def sarsaAlgo(self, state):
        qState = 0
        steps = 4

        alpha = 0.2
        gammar = 0.2
        epsilon = 0
        ourLambda = 0

        # delta = 0
        # randomNum = random.randint(0, 3)
        reward = 0
        pacmanPosState = self.state.getPacmanPosition()
        for num in range(steps):
            newQState = 0
            delta = reward + gammar * newQState - qState

