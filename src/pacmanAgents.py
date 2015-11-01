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

from bfsSearch import NearestObjectSearch
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
        assert True
    
    def evade(self, direction, state):
        legal = state.getLegalPacmanActions()
        if Directions.STOP in legal: legal.remove(Directions.STOP)
        if direction in legal: legal.remove(direction)
        if (not legal):
            return Directions.STOP
        else:
            return random.choice(legal)
        
    def goTo(self, direction, state):
        legal = state.getLegalPacmanActions()
        if direction in legal: return direction
        if (not legal):
            return Directions.STOP
        else:
            return random.choice(legal)
    
    def getNearestEnermy(self, state, bfsResult):
        nearestEnermy = None
        lastDistance = 99999
        
        index = 1
        while index < state.getNumAgents():
            for loc in bfsResult.ghosts:
                if (not loc.isEatable):
                    if (lastDistance > loc.threat):
                        lastDistance = loc.threat
                        nearestEnermy = loc
            index += 1
            
        return nearestEnermy
        
    def getNearestEatable(self, state, bfsResult):
        nearestEnermy = None
        lastDistance = 99999
        
        index = 1
        while index < state.getNumAgents():
            for loc in bfsResult.ghosts:
                if (loc.isEatable):
                    if (lastDistance > loc.threat):
                        lastDistance = loc.threat
                        nearestEnermy = loc
            index += 1
            
        return nearestEnermy
    
    def getAction(self, state):
        evadeDistance = 2
        
        bfsResult = NearestObjectSearch(state).getReinforcmentResult()
        # SarsaAgent.sarsaAlgo(bfsResult)
        # EVADE UNEATABLE GHOST
        nearestEnermy = self.getNearestEnermy(state, bfsResult)
        if (nearestEnermy != None):
            if (nearestEnermy.threat < evadeDistance):
                return self.evade(ReinforcementDirection.toGameDirection(nearestEnermy.direction), state)

        # GET NEAREST FOOD
        return ReinforcementDirection.toGameDirection(bfsResult.bestDirection)

def scoreEvaluation(state):
    return state.getScore()

# class SarsaAgenet(game.Agent):
#
#     def __init__(self, evalFn="scoreEvaluation"):
#         assert True
#
#     def getAction(self, state):
#         return SarsaAgent.sarsaAlgo(self, state)
#
#
#     def sarsaAlgo(state):
#         # qState = 0
#         steps = 4
#         # gammar = 0.2
#         # delta = 0
#         # randomNum = random.randint(0, 3)
#         for num in range(steps):
#             direction = Directions.NORTH
#             legal = state.getLegalPacmanActions()
#             if direction in legal:
#                 print direction
#                 return direction

