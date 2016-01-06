from game import Directions


class ReinforcementDirection(object):
    """
    ReinforcementDirection dient zur Umwandlung von Strings, die in der game.Directions verwendet werden, in Integer.
    """

    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    @classmethod
    def fromGameDirection(self, direction):
        """
        Wandelt eine die Repraesentation einer game.Directions in die entsprechende ReinforcementDirection um.
        :param direction: Eine game.Directions oder die entsprechende Stringrepraesentation {'North', 'South', 'East', 'West'}.
                          'Stop' ist eine illegale Eingabe, da das Anhalten nicht vorgesehen ist.
        :return: Gibt die Intergerrepraesentation der eingegebenen direction wieder.
        """
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
        """
        Wandelt eine die Repraesentation einer ReinforcementDirection in die entsprechende game.Directions um.
        :param direction: Eine ReinforcementDirection oder die entsprechende Integerrepraesentation {0, 1, 2, 3}.
        :return: Gibt die Stringrepraesentation der eingegebenen direction wieder.
        """
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
        """
        :return: Ein Liste bestehend aus allen ReinforcementDirection's
        """
        resultList = []
        resultList.append(self.NORTH)
        resultList.append(self.EAST)
        resultList.append(self.SOUTH)
        resultList.append(self.WEST)
        return resultList


class Threat(object):
    """Thread dient zur Umwandlung von echten Entfernungen in approximierte Werte."""

    DANGER = 0
    NEXT = 1
    NEAR = 2
    FAR_AWAY = 3

    @classmethod
    def fromDistance(self, distance):
        """
        Wandelt eine Entfernung in den approximierten Wert um. Eine Rueckumwandlung ist nicht moeglich.
        :param distance: Integer reale Entfernung
        :return: Integer approximierter Wert
        """
        if distance <=1:
            return self.DANGER
        elif distance <= 3:
            return self.NEXT
        elif distance <= 5:
            return self.NEAR
        else:
            return self.FAR_AWAY


class GhostState(object):
    """Der GhostState repraesentiert den Status eines Geistes im Spiel."""

    def __init__(self, direction, threat, isEatable):
        """
        :param direction: ReinforcementDirection die die Richtung wiederspiegelt, in die Pacman laufen muesste, um auf den Geist zuzulaufen
        :param threat: Threat des Geistes, also die approximierte Entfernung zwischen Pacman und dem Geist
        :param isEatable: Boolean, ob der Geist fressbar ist.
        """
        self.direction = direction
        self.threat = threat
        self.isEatable = 1 if isEatable else 0

    def __repr__(self):
        """
        Stringrepraesentation des Zustandes.
        """
        return ('GhostState[direction=' + str(self.direction) + ',threat=' + str(self.threat) + ',isEatable=' + str(self.isEatable) + ']')

    def toBin(self):
        """
        Binaerrepreasentation des Zustandes.
        """
        return self.direction << 3 | self.threat << 1 | self.isEatable

class ReinforcementState(object):
    """Der ReinforcementState repraesentiert den gesamten fuer die Reinforcementberechnung noetigen Spielstatus."""
    def __init__(self, nextFoodDirection, nextFoodDistance, ghosts):
        """
        :param nextFoodDirection: ReinforcementDirection Richtung, in der der naechste Fresspunkt liegt.
        :param nextFoodDistance: Distanz zum naechsten Fresspunkt, maximal 32
        :param ghosts: Liste von GhostState.
        """
        self.ghosts = ghosts
        self.nextFoodDirection = nextFoodDirection
        self.nextFoodDistance = nextFoodDistance
        if self.nextFoodDistance > 32:
            self.nextFoodDistance = 32

    def __repr__(self):
        """
        Stringrepraesentation des Zustandes.
        """
        ghostStrings = '['
        for ghost in self.ghosts:
            ghostStrings += str(ghost) + ','
        ghostStrings = ghostStrings[:-1] + ']'
        return ('GhostState[direction=' + str(self.nextFoodDirection) + ',nextFoodDistance=' + str(self.nextFoodDistance)+ ',ghosts=' + ghostStrings + ']')

    def toBin(self):
        """
        Binaerrepreasentation des Zustandes.
        """
        binVal = 0
        for ghost in self.ghosts:
            binVal = binVal << 5 | ghost.toBin()
        binVal = binVal << 5 | self.nextFoodDistance
        return binVal << 2 | self.nextFoodDirection

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.toBin() == other.toBin()
        else:
            return False

#print bin(GhostState(Directions.WEST, Threat.DANGER, True).toBin())

#print bin(ReinforcementState(Directions.WEST, [GhostState(Directions.NORTH, Threat.DANGER, True),GhostState(Directions.NORTH, Threat.DANGER, True),GhostState(Directions.SOUTH, Threat.FAR_AWAY, True),GhostState(Directions.NORTH, Threat.DANGER, True)]).toBin())
