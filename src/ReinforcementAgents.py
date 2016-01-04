from game import Directions
import game
import random
from ReinforcementState import ReinforcementDirection, ReinforcementState
from ReinforcementSave import *
from bfsSearch import ReinforcementSearch
import logging
import copy

class AbstractQState():
    def __init__(self, state, direction):
        #self.state = state
        # TODO: check this => these keys are not in featue but in stateSearch/ searchResult
        features = RuleGenerator().getStateSearch(state,direction)
        self.ghostThreat = features['nearestGhostDistances']
        self.foodDistance = features['nearestFoodDist']
        self.powerPelletDist = features['nearestPowerPelletDist']
        # self.eatableGhosts = features['nearestEatableGhostDistances']
        #self.direction = direction

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            # return self.ghostThreat == other.ghostThreat and self.foodDistance == other.foodDistance and self.powerPelletDist == other.powerPelletDist and self.eatableGhosts == other.eatableGhosts
            return self.ghostThreat == other.ghostThreat and self.foodDistance == other.foodDistance and self.powerPelletDist == other.powerPelletDist
        else:
            return False
    def __hash__(self):
        # return hash(hash(self.ghostThreat) + hash(self.foodDistance) + hash(self.powerPelletDist) + hash(self.eatableGhosts))
        return hash(hash(self.ghostThreat) + hash(self.foodDistance) + hash(self.powerPelletDist))

class Saving():
    def __init__(self, evalFn="scoreEvaluation"):
        self.savedStates = {}

    def getRatingForNextState(self, direction, state):
        abstractState = AbstractQState(state, direction)
        value = self.savedStates.get(abstractState)
        if value == None:
            return 0
        else:
            return value

    def setRatingForState(self, direction, state, value):
        abstractState = AbstractQState(state, direction)
        self.savedStates[abstractState] = value

    def getBestDirection(self, state, directions):
        bestVal = float('-inf')
        bestDirection = None
        for direction in directions:
            tmpValue = self.getRatingForNextState(direction, state)
            if bestVal < tmpValue:
                bestVal = tmpValue
                bestDirection = direction
        return bestDirection

    def getBestValue(self, state, directions):
        bestDirection = self.getBestDirection(state,directions)
        if bestDirection:
            return self.getRatingForNextState(bestDirection, state)
        else:
            return 0.0

    def __repr__(self):
        return str(self.savedStates)

class ReinforcementQAgent(game.Agent):
    def __init__(self, numTraining = 0):
         self.saving = Saving()
         self.random = random.Random()
         self.lastState = None
         self.lastAction = None
         self.alpha = 0.1
         self.gamma = 0.5
         self.epsilon = 0.2
         self.numTraining = int(numTraining)
         self.episodesSoFar = 0

    def getAction(self, state):
        logging.debug(str(state))
        self.lastAction = self.chooseAction(state)

        return self.lastAction

    def chooseAction(self, state):
        directions = self.legaldirections(state)
        rnd = self.random.random()
        if self.epsilon > rnd:
            logging.debug("random " + str(rnd) + " gamma " + str(self.epsilon))
            return self.random.choice(directions)
        else:
            return self.saving.getBestDirection(self.lastState, directions)

    def calcReward(self, state):
        return state.getScore() - self.lastState.getScore()

    def legaldirections(self, state):
        directions = state.getLegalPacmanActions()
        self.safeListRemove(directions, Directions.LEFT)
        self.safeListRemove(directions, Directions.REVERSE)
        self.safeListRemove(directions, Directions.RIGHT)
        #self.safeListRemove(directions, Directions.STOP)
        return directions

    def safeListRemove(self,lst,item):
        try:
            lst.remove(item)
        except ValueError:
            pass

    def updater(self, state):
        reward = self.calcReward(state)
        currentValue = self.saving.getRatingForNextState(self.lastAction, self.lastState)
        maxPossibleFutureValue = self.saving.getBestValue(state, self.legaldirections(state))
        calcVal =  currentValue + self.alpha * (reward + self.gamma * maxPossibleFutureValue - currentValue)
        self.saving.setRatingForState(self.lastAction, self.lastState, calcVal)

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
            logging.info("Training " + str(self.episodesSoFar) + " of " + str(self.numTraining))
        else:
            self.epsilon = 0.0
            self.alpha = 0.0

    def isInTraining(self):
        return self.episodesSoFar < self.numTraining

    def isInTesting(self):
        return not self.isInTraining()


class ReinforcementSAgent(ReinforcementQAgent):
    def __init__(self, numTraining = 0):
        ReinforcementQAgent.__init__(self, numTraining)
        self.chosenAction = None

    def getAction(self, state):
        if not self.chosenAction:
            self.chosenAction = self.chooseAction(state)
        self.lastAction = self.chosenAction
        return self.lastAction

    def updater(self, state):
        reward = self.calcReward(state)
        currentValue = self.saving.getRatingForNextState(self.lastAction, self.lastState)
        if state.isLose() or state.isWin():
            logging.debug("end" + str(self.epsilon))
            maxPossibleFutureValue = 0
        else:
            self.chosenAction = self.chooseAction(state)
            maxPossibleFutureValue = self.saving.getRatingForNextState(self.chosenAction, state)
        calcVal =  currentValue + self.alpha * (reward + self.gamma * maxPossibleFutureValue - currentValue)
        logging.debug("Calc " + str(calcVal))
        self.saving.setRatingForState(self.lastAction, self.lastState, calcVal)

    def final(self, state):
        ReinforcementQAgent.final(self, state)
        self.chosenAction = None

class myDict(dict):
    def __init__(self, default):
        self.default = default

    def __getitem__(self, key):
        self.setdefault(key, self.default)
        return dict.__getitem__(self, key)

    def sumAll(self):
        sumAllret = 0.0
        for key in self.keys():
            sumAllret += self[key]
        return sumAllret

    def normalize(self):
        sumAlla = self.sumAll()
        if sumAlla == 0.0:
            newValue = float(1)/len(self)
            for key in self.keys():
                self[key] = newValue
        else:
            for key in self.keys():
                self[key] = self[key] / sumAlla

    def divideAll(self, value):
        for key in self.keys():
            self[key] = float(self[key]) / value
    
    def mulAll(self, value):
        for key in self.keys():
            self[key] = float(self[key]) * value

class RuleGenerator():
    def directionToCoordinate(self, direction):
        if direction == Directions.NORTH:
            return (0,1)
        elif direction == Directions.SOUTH:
            return (0,-1)
        elif direction == Directions.EAST:
            return (1,0)
        elif direction == Directions.WEST:
            return (-1,0)
        else:
            return (0,0)
    def getMovableDirections(self,posX,posY, walls):
        lst = [(0,0)]
        try:
            if not walls[posX][posY+1]:
                lst.append((posX, posY+1))
        except IndexError:
            pass

        try:
            if not walls[posX][posY-1]:
                lst.append((posX, posY-1))
        except IndexError:
            pass

        try:
            if not walls[posX-1][posY]:
                lst.append((posX-1, posY))
        except IndexError:
            pass

        try:
            if not walls[posX+1][posY]:
                lst.append((posX+1, posY))
        except IndexError:
            pass

        return lst
        
    def abstractBroadSearch(self,field, startingPosition, stopCondition):
        startX, startY = startingPosition
        openList = [(startX, startY, 0)]
        closedList = set()
        while openList:
            curX, curY, dist = openList.pop(0)
            if not (curX, curY) in closedList:
                closedList.add((curX, curY))
                if stopCondition(curX, curY):
                    return [dist,(curX, curY)]
                for (sucX, sucY) in self.getMovableDirections(curX, curY,field):
                    openList.append((sucX, sucY, dist + 1))
        return [None,None]
        
#    def getNearestFoodPosition(self,state, pacmanSpositionAfterMoving):
#        food = state.getFood()
#        nonEatableGhosts = self.getNonEatableGhosts(state)
#        def stopCondition(curX,curY):
#            return food[curX][curY] and not (curX, curY) in nonEatableGhosts        
#        return self.abstractBroadSearch(state.getWalls(), pacmanSpositionAfterMoving, stopCondition)[0]
#    
    def getNextNonEatableGhost(self,state,pacmanSpositionAfterMoving):
        nonEatableGhosts = self.getNonEatableGhosts(state)
        def stopCondition(curX,curY):
            return (curX, curY) in nonEatableGhosts        
        return self.abstractBroadSearch(state.getWalls(), pacmanSpositionAfterMoving, stopCondition)[0]    
#    
#    def getNextCapsul(self, state, pacmanSpositionAfterMoving):
#        capsules = state.getCapsules()
#        nonEatableGhosts = self.getNonEatableGhosts(state)
#        if len(capsules) > 0:
#            def stopConditionEatableGhost(curX,curY):
#                return (curX, curY) in capsules and not (curX, curY) in nonEatableGhosts
#            return self.abstractBroadSearch(state.getWalls(), pacmanSpositionAfterMoving, stopConditionEatableGhost)[0]
#            pass 
#        return None
#
#    def getNextEatableGhost(self, state, pacmanSpositionAfterMoving):
#        nonEatableGhosts = self.getNonEatableGhosts(state)
#        eatableGhosts = self.getEatableGhosts(state)
#        if len(eatableGhosts) > 0:
#            def stopConditionEatableGhost(curX,curY):
#                return (curX, curY) in eatableGhosts and not (curX, curY) in nonEatableGhosts
#            return self.abstractBroadSearch(state.getWalls(), pacmanSpositionAfterMoving, stopConditionEatableGhost)[0]        
#            pass
#        return None  
    
    def isInSpawnArea(self,state, pacmanSpositionAfterMoving):
        agentPos = state.data.layout.agentPositions
        spawnPoints = set()
        for isPacman, pos in agentPos:
            if not isPacman and len(spawnPoints) < len(state.getGhostStates()):
                spawnPoints.add(pos)
        #print spawnPoints
        if pacmanSpositionAfterMoving in spawnPoints:
            return 1.0
        else: 
            return 0.0
        
    def combinatedBroadSearch(self,state, startingPosition):
        startX, startY = startingPosition
        searchResult = myDict(None)
        nonEatableGhosts = self.getNonEatableGhosts(state)
        eatableGhosts = self.getEatableGhosts(state)
        food = state.getFood()
        capsules = state.getCapsules()
        openList = [(startX, startY, 0)]
        field = copy.deepcopy(state.getWalls())
        for (x,y) in nonEatableGhosts:
            field[x][y] = True
        closedList = set()
        while openList:
            curX, curY, dist = openList.pop(0)
            if not (curX, curY) in closedList:
                closedList.add((curX, curY))
                if searchResult['nearestFoodDist'] is None and food[curX][curY] and not (curX, curY) in nonEatableGhosts:
                    searchResult['nearestFoodDist'] = dist
#                if searchResult['nearestGhostDistances'] is None and (curX, curY) in nonEatableGhosts:
#                    searchResult['nearestGhostDistances'] = dist
                if searchResult['nearestEatableGhostDist'] is None and (curX, curY) in eatableGhosts and not (curX, curY) in nonEatableGhosts:
                    searchResult['nearestEatableGhostDist'] = dist
                if searchResult['nearestCapsul'] is None and (curX, curY) in capsules and not (curX, curY) in nonEatableGhosts:
                    searchResult['nearestCapsul'] = dist 
#                if searchResult['nearestCapsul'] is None:
#                    if len(eatableGhosts) > 0:
#                        if (curX, curY) in eatableGhosts and not (curX, curY) in nonEatableGhosts:
#                            searchResult['nearestCapsul'] = dist
#                    elif len(capsules) > 0:
#                        if (curX, curY) in capsules and not (curX, curY) in nonEatableGhosts:
#                            searchResult['nearestCapsul'] = dist + self.getNextNonEatableGhost(state,(curX, curY))
                for (sucX, sucY) in self.getMovableDirections(curX, curY,field):
                    openList.append((sucX, sucY, dist + 1))
        return searchResult
        
    def getStateSearch(self, state, direction):
        vecX, vecY = self.directionToCoordinate(direction)
        posX, posY = state.getPacmanPosition()
        pacmanSpositionAfterMoving = (posX + vecX, posY + vecY)
        searchResult = self.combinatedBroadSearch(state, pacmanSpositionAfterMoving)
        searchResult['nearestGhostDistances'] = self.getNextNonEatableGhost(state, pacmanSpositionAfterMoving)
        searchResult['inSpawnArea'] = self.isInSpawnArea(state, pacmanSpositionAfterMoving)
        #searchResult['maxDistance'] = maxDistance
        return searchResult

    def getEatableGhosts(self, state):
        eatableGhosts = []
        ghostStates = state.getGhostStates()
        for ghostState in ghostStates:
            if ghostState.isScared():
                x,y = ghostState.getPosition()
                eatableGhosts.append((int(x),int(y)))
        logging.debug("############################################# eatableGhosts = " + str(eatableGhosts))
        return eatableGhosts

    def getNonEatableGhosts(self, state):
        nonEatableGhosts = []
        ghostStates = state.getGhostStates()
        for ghostState in ghostStates:
            if not ghostState.isScared():
                x,y = ghostState.getPosition()
                nonEatableGhosts.append((int(x),int(y)))
        logging.debug("############################################# nonEatableGhosts = " + str(nonEatableGhosts))
        return nonEatableGhosts

    # TODO: insert features here
    def getfeatures(self, state, direction):
        features = myDict(0.0)
        #features['base'] = 1.0
        logging.debug("str " + str(state))
        logging.debug("dir " + str(direction))
        stateSearch = self.getStateSearch(state, direction)
        maxDistance = state.getWalls().width + state.getWalls().height #stateSearch['maxDistance'] #
        logging.info("MaxDistance " + str(direction) + " " + str(maxDistance))
        if stateSearch['nearestFoodDist'] is not None:
            logging.debug("FoodDist " +  str(stateSearch['nearestFoodDist']))
            features['foodValuability'] = -(float(stateSearch['nearestFoodDist']))
        if stateSearch['nearestGhostDistances'] is not None:
            logging.debug("nearestGhostDistances " +  str(stateSearch['nearestGhostDistances']))
            features['ghostThreat'] = -(float(stateSearch['nearestGhostDistances'])) #/ maxDistance
#        else:
#            features['ghostThreat'] = float(maxDistance)
#        if stateSearch['nearestEatableGhostDist'] is not None:
#            logging.debug("nearestEatableGhostDist " +  str(stateSearch['nearestEatableGhostDist']))
#            features['eatableGhostValuability'] = -(float(stateSearch['nearestEatableGhostDist'])) #/ maxDistance
        if stateSearch['nearestCapsul'] is not None:
            logging.debug("nearestCapsul " +  str(stateSearch['nearestCapsul']))
            features['nearestCapsulValuability'] = -(float(stateSearch['nearestCapsul'])) 
#        else:
#            features['nearestCapsulValuability'] = 0.0
#        if stateSearch['inSpawnArea'] is not None:
#            logging.debug("inSpawnArea " +  str(stateSearch['inSpawnArea']))
#            features['inSpawnArea'] = (float(stateSearch['inSpawnArea'])) 
#        else: 
#            features['powerPelletValuability'] = 0.0    
        # if stateSearch['nearestEatableGhostDistances'] is not None:
        #     features['eatableGhosts'] = (float(stateSearch['nearestEatableGhostDistances'])) #/ maxDistance
        features['BIAS'] = -1.0 
        features['BIAS2'] = 1.0
        #features.divideAll(100)
        features.normalize()
        logging.debug(str(features))
        return features

class ReinforcementRAgent(game.Agent):
    def __init__(self, numTraining = 0):
        self.actionPower = myDict(0.0)
        self.ruleGenerator = RuleGenerator();
        self.random = random.Random()
        self.lastState = None
        self.lastAction = None
        self.alpha = 0.5
        self.gamma = 0.5
        self.epsilon = 0.1
        self.numTraining = int(numTraining)
        self.episodesSoFar = 0
        self.actionPowerDict = myDict(None)

    def getActionPower(self, keys):
        actionPower = self.actionPowerDict[frozenset(keys)]
        if actionPower: 
            return actionPower
        else:
            self.actionPowerDict[frozenset(keys)] = myDict(0.0)
            return self.actionPowerDict[frozenset(keys)]
#        return self.actionPower
            
    def safeListRemove(self,lst,item):
        try:
            lst.remove(item)
        except ValueError:
            pass

    def getCombinedValue(self,state, direction):
        combinedValue = 0.0
        features = self.ruleGenerator.getfeatures(state, direction)
        logging.info("Features " + str(direction) + " " + str(features))
        actionPower = self.getActionPower(features.keys())
        #if self.isInTesting() and len(features.keys()) == 1:
            #raw_input("Only One Feature ")
        for featureKey in features.keys():
            combinedValue += features[featureKey] * actionPower[featureKey]
        return combinedValue

    def updater(self,nextState):
        logging.info("Start Updating")
        reward = self.calcReward(nextState)
        features = self.ruleGenerator.getfeatures(self.lastState, self.lastAction)
        combinatedValue = self.getCombinedValue(self.lastState, self.lastAction)
        maxPossibleFutureValue = self.getBestValue(nextState, self.legaldirections(nextState))
        actionPower = self.getActionPower(features.keys())
        for ruleKey in features.keys():
            difference = reward + self.gamma * maxPossibleFutureValue - combinatedValue
            logging.info("Difference: " + str(difference))
            actionPower[ruleKey] = actionPower[ruleKey] + self.alpha * difference * features[ruleKey]
            #zur demo orginal QLearning
            #different = (reward + self.gamma * maxPossibleFutureValue - currentValue)
            #calcVal =  currentValue + self.alpha * different
        logging.info("ActionPower: " + str(actionPower))
        #self.saving.setRatingForState(self.lastAction, self.lastState, calcVal)
        logging.info("Stop Updating")

    def calcReward(self, state):
        score = state.getScore() - self.lastState.getScore()
        if (len(state.getCapsules()) != len(self.lastState.getCapsules())):
            score += 15
#        if state.isLose():
#            score -=1000
        return score

    def getAction(self, state):
        logging.info("Start GetAction")
        self.lastAction = self.chooseAction(state)
        logging.info("Action Power: " + str(self.actionPowerDict))
        if self.isInTesting():
#            raw_input("Press Any Key ")
            pass
        logging.info("Chosen Acction: " + str(self.lastAction))
        logging.info("Stop GetAction")
        logging.debug(str(self.lastAction))
        return self.lastAction

    def chooseAction(self, state):
        directions = self.legaldirections(state)
        logging.debug(str(directions))
        rnd = self.random.random()
        if self.epsilon > rnd:
            return self.random.choice(directions)
        else:
            return self.getBestDirection(self.lastState, directions)

    def legaldirections(self, state):
        directions = state.getLegalPacmanActions()
        self.safeListRemove(directions, Directions.LEFT)
        self.safeListRemove(directions, Directions.REVERSE)
        self.safeListRemove(directions, Directions.RIGHT)
        #self.safeListRemove(directions, Directions.STOP)
        return directions

    def getBestDirection(self, state, directions):
        bestVal = float('-inf')
        bestDirection = None
        logging.info("Possible Directions" + str(directions))
        for direction in directions:
            tmpValue = self.getCombinedValue(state, direction)
            logging.info("Combinated Value " + str(direction) + " " + str(tmpValue))
            logging.debug(str(tmpValue))
            if bestVal < tmpValue:
                bestVal = tmpValue
                bestDirection = direction
        return bestDirection

    def getBestValue(self, state, directions):
        bestDirection = self.getBestDirection(state,directions)
        if bestDirection:
            return self.getCombinedValue(state, bestDirection)
        else:
            return 0.0

    def observationFunction(self, state):
        if self.lastState:
            self.updater(state)
        else:
            if not self.isInTraining():
               self.epsilon = 0.0
               self.alpha = 0.0
               pass
        self.lastState = state
        #raw_input("Press Any Key ")
        return state

    def final(self, state):
        self.updater(state)
        self.lastState = None
        self.lastAction = None
        #raw_input("Press Any Key ")
        if self.isInTraining():
            self.episodesSoFar += 1
            print "Training " + str(self.episodesSoFar) + " of " + str (self.numTraining)
        else:
            self.epsilon = 0.0
            self.alpha = 0.0
            if state.isLose():
                #raw_input("Press Any Key ")
                pass

    def isInTraining(self):
        return self.episodesSoFar < self.numTraining

    def isInTesting(self):
        return not self.isInTraining()
