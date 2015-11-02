from game import Directions


class ReinforcementDirection(object):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    @classmethod
    def fromGameDirection(self, direction):
        if direction == Directions.NORTH:
            return self.NORTH
        elif direction == Directions.EAST:
            return self.EAST
        elif direction == Directions.SOUTH:
            return self.SOUTH
        elif direction == Directions.WEST:
            return self.WEST
        else:
            raise ValueError('Direction Unknown: ' + str(direction))

    @classmethod
    def toGameDirection(self, direction):
        if direction == self.NORTH:
            return Directions.NORTH
        elif direction == self.EAST:
            return Directions.EAST
        elif direction == self.SOUTH:
            return Directions.SOUTH
        elif direction == self.WEST:
            return Directions.WEST
        else:
            raise ValueError('Direction Unknown')
        
    @classmethod
    def getDirections(self): 
        resultList = []
        resultList.append(self.NORTH)
        resultList.append(self.EAST)
        resultList.append(self.SOUTH)
        resultList.append(self.WEST)
        return resultList


class Threat(object):
    """docstring for ClassName"""
    DANGER = 0
    NEXT = 1
    NEAR = 2
    FAR_AWAY = 3

    @classmethod
    def fromDistance(self, distance):
        if distance <=1:
            return self.DANGER
        elif distance <= 3:
            return self.NEXT
        elif distance <= 5:
            return self.NEAR
        else:
            return self.FAR_AWAY


class GhostState(object):
    """docstring for ClassName"""
    def __init__(self, direction, threat, isEatable):
        self.direction = direction
        self.threat = threat
        self.isEatable = 1 if isEatable else 0

    def __repr__(self):
        return ('GhostState[direction=' + str(self.direction) + ',threat=' + str(self.threat) + ',isEatable=' + str(self.isEatable) + ']')

    def toBin(self):
        return self.direction << 3 | self.threat << 1 | self.isEatable

class ReinforcementState(object):
    """docstring for ClassName"""
    def __init__(self, bestDirection, ghosts):
        self.ghosts = ghosts
        self.bestDirection = bestDirection

    def __repr__(self):
        ghostStrings = '['
        for ghost in self.ghosts:
            ghostStrings += str(ghost) + ','
        ghostStrings = ghostStrings[:-1] + ']'
        return ('GhostState[direction=' + str(self.bestDirection) + ',ghosts=' + ghostStrings + ']')

    def toBin(self):
        binVal = 0
        for ghost in self.ghosts:
            binVal = binVal << 5 | ghost.toBin()
        return binVal << 2 | self.bestDirection



#print bin(GhostState(Directions.WEST, Threat.DANGER, True).toBin())

#print bin(ReinforcementState(Directions.WEST, [GhostState(Directions.NORTH, Threat.DANGER, True),GhostState(Directions.NORTH, Threat.DANGER, True),GhostState(Directions.SOUTH, Threat.FAR_AWAY, True),GhostState(Directions.NORTH, Threat.DANGER, True)]).toBin())
