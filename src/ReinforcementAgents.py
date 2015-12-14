from game import Directions
import game
import random
from ReinforcementState import ReinforcementDirection, ReinforcementState
from ReinforcementSave import *
from bfsSearch import ReinforcementSearch

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
        return hash(hash(self.ghostThreat) + hash(self.foodDistance) + hash(self.powerPelletDist) + hash(self.eatableGhosts))

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
         self.epsilon = 0.1
         self.numTraining = int(numTraining)
         self.episodesSoFar = 0

    def getAction(self, state):
        #print str(state)
        self.lastAction = self.chooseAction(state)

        return self.lastAction

    def chooseAction(self, state):
        directions = self.legaldirections(state)
        rnd = self.random.random()
        if self.epsilon > rnd:
            #print "random " + str(rnd) + " gamma " + str(self.epsilon)
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
            print "Training " + str(self.episodesSoFar) + " of " + str (self.numTraining)
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
        self.chosenAction = None;

    def getAction(self, state):
        if not self.chosenAction:
            self.chosenAction = self.chooseAction(state)
        self.lastAction = self.chosenAction
        return self.lastAction

    def updater(self, state):
        reward = self.calcReward(state)
        currentValue = self.saving.getRatingForNextState(self.lastAction, self.lastState)
        if state.isLose() or state.isWin():
            #print "end" + str(self.epsilon)
            maxPossibleFutureValue = 0;
        else:
            self.chosenAction = self.chooseAction(state)
            maxPossibleFutureValue = self.saving.getRatingForNextState(self.chosenAction, state)
        calcVal =  currentValue + self.alpha * (reward + self.gamma * maxPossibleFutureValue - currentValue)
        #print "Calc " + str(calcVal)
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

    def getStateSearch(self, state, direction):
        vecX, vecY = self.directionToCoordinate(direction)
        posX, posY = state.getPacmanPosition()
        food = state.getFood()
        walls = state.getWalls()
        # eatableGhosts = self.getEatableGhosts(state)
        nonEatableGhosts = self.getNonEatableGhosts(state)
        powerPellets = state.getCapsules()
        openList = [(posX + vecX, posY + vecY, 0)]
        closedList = set()
        searchResult = myDict(None)
        maxDistance = -1
        searchResult['nearestFoodDist'] = None
        searchResult['nearestPowerPelletDist'] = None
        print "powerPellets = " + str(powerPellets)
        while openList:
            curX, curY, dist = openList.pop(0)
            if not (curX, curY) in closedList:
                closedList.add((curX, curY))
                if (searchResult['nearestFoodDist'] is None) and food[curX][curY] and not (curX, curY) in nonEatableGhosts:
                    searchResult['nearestFoodDist'] = dist
                    searchResult['nearestFoodPos'] = (curX, curY)
                if (curX, curY) in nonEatableGhosts:
                    # print "###################################### nonEatableGhosts= " + str(nonEatableGhosts)
                    # print "###################################### state.getGhostStates = " + str(not state.getGhostStates()[0].isScared())
                    if not searchResult.has_key('nearestGhostDistances'):
                        searchResult['nearestGhostDistances'] = dist
                if (searchResult['nearestPowerPelletDist'] is None) and (curX, curY) in powerPellets and not (curX, curY) in nonEatableGhosts:
                    searchResult['nearestPowerPelletDist'] = dist
                    searchResult['nearestPowerPelletPos'] = (curX, curY)
                # if (curX, curY) in eatableGhosts:
                #     # print "###################################### eatableGhosts= " + str(eatableGhosts)
                #     # print "###################################### state.getGhostStates = " + str(state.getGhostStates()[0].isScared())
                #     if not searchResult.has_key('nearestEatableGhostDistances'):
                #         searchResult['nearestEatableGhostDistances'] = dist
                for (sucX, sucY) in self.getMovableDirections(curX, curY,walls):
                    openList.append((sucX, sucY, dist + 1))
                maxDistance = max(maxDistance, dist)
        searchResult['maxDistance'] = maxDistance
        return searchResult

    def getEatableGhosts(self, state):
        eatableGhosts = []
        ghostStates = state.getGhostStates()
        for ghostState in ghostStates:
            if ghostState.isScared():
                eatableGhosts.append(ghostState.getPosition())
        # print "############################################# eatableGhosts = " + str(eatableGhosts)
        return eatableGhosts

    def getNonEatableGhosts(self, state):
        nonEatableGhosts = []
        ghostStates = state.getGhostStates()
        for ghostState in ghostStates:
            if not ghostState.isScared():
                nonEatableGhosts.append(ghostState.getPosition())
        # print "############################################# nonEatableGhosts = " + str(nonEatableGhosts)
        return nonEatableGhosts

    # TODO: insert features here
    def getfeatures(self, state, direction):
        features = myDict(0.0)
        #features['base'] = 1.0
        #print "str " + str(state)
        #print "dir " + str(direction)
        stateSearch = self.getStateSearch(state, direction)
        maxDistance = stateSearch['maxDistance'] #state.getWalls().width + state.getWalls().height#
        print "MaxDistance " + str(direction) + " " + str(maxDistance)
        if stateSearch['nearestFoodDist'] is not None:
            #print "FoodDist " +  str(stateSearch['nearestFoodDist'])
            features['foodValuability'] = (float(stateSearch['nearestFoodDist'])) #/ maxDistance
        if stateSearch['nearestGhostDistances'] is not None:
            features['ghostThreat'] = (float(stateSearch['nearestGhostDistances'])) #/ maxDistance
        if stateSearch['nearestPowerPelletDist'] is not None:
            # print "PowerPelletDist " +  str(stateSearch['nearestPowerPelletDist'])
            features['powerPelletValuability'] = (float(stateSearch['nearestPowerPelletDist'])) #/ maxDistance
        # if stateSearch['nearestEatableGhostDistances'] is not None:
        #     features['eatableGhosts'] = (float(stateSearch['nearestEatableGhostDistances'])) #/ maxDistance
        #features['maxDistance'] = maxDistance
        features.normalize()

        #print str(features)
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

    def safeListRemove(self,lst,item):
        try:
            lst.remove(item)
        except ValueError:
            pass

    def getCombinedValue(self,state, direction):
        combinedValue = 0.0
        features = self.ruleGenerator.getfeatures(state, direction)
        print "Features " + str(direction) + " " + str(features)
        for featureKey in features.keys():
            combinedValue += features[featureKey] * self.actionPower[featureKey]
        return combinedValue

    def updater(self,nextState):
        print "Start Updating"
        reward = self.calcReward(nextState)
        features = self.ruleGenerator.getfeatures(self.lastState, self.lastAction)
        combinatedValue = self.getCombinedValue(self.lastState, self.lastAction)
        maxPossibleFutureValue = self.getBestValue(nextState, self.legaldirections(nextState))
        for ruleKey in features.keys():
            difference = reward + self.gamma * maxPossibleFutureValue - combinatedValue
            print "Difference: " + str(difference)
            self.actionPower[ruleKey] = self.actionPower[ruleKey] + self.alpha * difference * features[ruleKey]
            #zur demo orginal QLearning
            #different = (reward + self.gamma * maxPossibleFutureValue - currentValue)
            #calcVal =  currentValue + self.alpha * different
        print "ActionPower: " + str(self.actionPower)
        #self.saving.setRatingForState(self.lastAction, self.lastState, calcVal)
        print "Stop Updating"

    def calcReward(self, state):
        return state.getScore() - self.lastState.getScore()

    def getAction(self, state):
        print "Start GetAction"
        self.lastAction = self.chooseAction(state)
        print "Action Power: " + str(self.actionPower)
        if self.isInTesting():
#            raw_input("Press Any Key ")
            pass
        print "Chosen Acction: " + str(self.lastAction)
        print "Stop GetAction"
        #print str(self.lastAction)
        return self.lastAction

    def chooseAction(self, state):
        directions = self.legaldirections(state)
        #print str(directions)
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
        # self.safeListRemove(directions, Directions.STOP)
        return directions

    def getBestDirection(self, state, directions):
        bestVal = float('-inf')
        bestDirection = None
        print "Possible Directions" + str(directions)
        for direction in directions:
            tmpValue = self.getCombinedValue(state, direction)
            print "Combinated Value " + str(direction) + " " + str(tmpValue)
            #print str(tmpValue)
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
