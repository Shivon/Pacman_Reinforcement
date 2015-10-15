from ReinforcementState import *
from game import Directions
import os.path
import os
import struct

class ReinforcementSave(object):
	"""docstring for ClassName"""
	def __init__(self, fileName, numGhosts, maxMemoryInMB, maxBitForRating):
		self.fileName = fileName
		self.numGhosts = numGhosts
		self.maxMemoryInMB = maxMemoryInMB
		self.maxBitForRating = maxBitForRating
		self.checkMaxBits()
		self.initFile()

	def checkMaxBits(self):
		if ((self.numGhosts * 5) + 2) + self.maxBitForRating > 32:
			raise ValueError('You are using more than 32 Bit')

	def maxNumberOfStates(self):
		return 2 ** ((self.numGhosts * 5) + 2)

	def fileSizeInBit(self):
		return self.maxNumberOfStates() * 32
	def createInitialFile(self, filePath):
		wf = open(str(filePath), "wb")
		for x in range(0, self.maxNumberOfStates()):
			wf.write(struct.pack("I", x << self.maxBitForRating))
		wf.close()

	def initFile(self):
		if not(os.path.isdir(os.getcwd() + os.sep + 'savedLearned')):
			os.makedirs(os.getcwd() + os.sep + 'savedLearned')
		if not(os.path.isfile(os.getcwd() + os.sep + 'savedLearned' + os.sep + self.fileName)):
			self.createInitialFile(os.getcwd() + os.sep + 'savedLearned' + os.sep + self.fileName)
		if not((self.fileSizeInBit() / 8) == os.path.getsize(os.getcwd() + os.sep + 'savedLearned' + os.sep + self.fileName)):
			raise ValueError('The fileSize does not match with the Options')
		self.filePath = os.getcwd() + os.sep + 'savedLearned' + os.sep + self.fileName
	
	def getRatingForNextState(self, wentDirection, state):
		wf = open(str(self.filePath), "rb")
		binVal = state.toBin()
		print 'BinVal' + str(bin(binVal))
		wf.seek(binVal*4)
		tmp = struct.unpack("I", wf.read(4))[0]
		print 'tmp' + str(bin(tmp))
		wf.close()
		return (binVal << self.maxBitForRating)^tmp

	def setRatingForState(self, wentDirection, state, rating):
		if rating > 2**self.maxBitForRating:
			raise ValueError('Rating to high')
		wf = open(str(self.filePath), "r+b")
		binVal = state.toBin()
		wf.seek(binVal*4)
		wf.write(struct.pack("I", (binVal << self.maxBitForRating) + rating))
		wf.close()


a = ReinforcementSave('1ghost', 1, 128, 5)
print str(a.maxNumberOfStates()) + ' ' + str(float(a.fileSizeInBit()) / (8 * 1024 * 1024))
state = ReinforcementState(Directions.WEST, [GhostState(Directions.NORTH, Threat.DANGER, True)])
print 'getRatingForNextState' + str(a.getRatingForNextState(Directions.WEST, state))
a.setRatingForState(Directions.WEST,state,7)
print 'setRatingForNextState' + str(a.getRatingForNextState(Directions.WEST, state))
a = ReinforcementSave('2ghost', 2, 128, 5)
print str(a.maxNumberOfStates()) + ' ' + str(float(a.fileSizeInBit()) / (8 * 1024 * 1024))
a = ReinforcementSave('3ghost', 3, 128, 5)
print str(a.maxNumberOfStates()) + ' ' + str(float(a.fileSizeInBit()) / (8 * 1024 * 1024))
a = ReinforcementSave('4ghost', 4, 128, 5)
print str(a.maxNumberOfStates()) + ' ' + str(float(a.fileSizeInBit()) / (8 * 1024 * 1024))

print bin(2**16 - 1)