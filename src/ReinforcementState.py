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
			raise ValueError('Direction Unknown')

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


class Threat(object):
	"""docstring for ClassName"""
	DANGER = 0
	NEXT = 1
	NEAR = 2
	FAR_AWAY = 3

class GhostState(object):
	"""docstring for ClassName"""
	def __init__(self, direction, threat):
		self.direction = ReinforcementDirection.fromGameDirection(direction)
		self.threat = threat

	def __repr__(self):
		return ('GhostState[direction=' + str(self.direction) + ',threat=' + str(self.threat) + ']')

class ReinforcementState(object):
	"""docstring for ClassName"""
	def __init__(self, direction, ghosts):
		self.ghosts = ghosts
		self.direction = ReinforcementDirection.fromGameDirection(direction)
	def __repr__(self):
		ghostStrings = '['
		for ghost in self.ghosts:
			ghostStrings += str(ghost) + ','
		ghostStrings = ghostStrings[:-1] + ']'
		return ('GhostState[direction=' + str(self.direction) + ',ghosts=' + ghostStrings + ']')

print GhostState(Directions.NORTH, Threat.DANGER)

print ReinforcementState(Directions.WEST, [GhostState(Directions.NORTH, Threat.DANGER),GhostState(Directions.NORTH, Threat.DANGER),GhostState(Directions.SOUTH, Threat.FAR_AWAY),GhostState(Directions.NORTH, Threat.DANGER)])


		