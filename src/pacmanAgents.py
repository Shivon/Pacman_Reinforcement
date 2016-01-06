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
import random
import game
from game import Directions
import util
from ReinforcementState import ReinforcementDirection
# from ReinforcementSave import *

CONFIGURATIONSARSA_FILE = "sarsasettings.ini"

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


