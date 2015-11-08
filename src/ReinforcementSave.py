from ReinforcementState import *
from game import Directions
import os.path
import os
import struct

class ReinforcementSave(object):
    """docstring for ClassName"""
    def __init__(self, fileName, numGhosts, maxMemoryInMB=1):
        self.fileName = fileName
        self.numGhosts = numGhosts
        self.maxMemoryInMB = maxMemoryInMB
        self.initFile()

    def maxNumberOfStates(self):
        return 2 ** ((self.numGhosts * 5) + 2)

    def fileSizeInBit(self):
        return self.maxNumberOfStates() * self.numGhosts * 16

    def createInitialFile(self, filePath):
        wf = open(str(filePath), "wb")
        for x in range(0, self.maxNumberOfStates()):
            for y in xrange(0,self.numGhosts):
                wf.write(struct.pack("h", 0))
        wf.close()

    def initFile(self):
        if not(os.path.isdir(os.getcwd() + os.sep + 'savedLearned')):
            os.makedirs(os.getcwd() + os.sep + 'savedLearned')
        if not(os.path.isfile(os.getcwd() + os.sep + 'savedLearned' + os.sep + self.fileName)):
            self.createInitialFile(os.getcwd() + os.sep + 'savedLearned' + os.sep + self.fileName)
        if not((self.fileSizeInBit() / 8) == os.path.getsize(os.getcwd() + os.sep + 'savedLearned' + os.sep + self.fileName)):
            raise ValueError('The fileSize does not match with the Options')
        self.filePath = os.getcwd() + os.sep + 'savedLearned' + os.sep + self.fileName

    def savePage(self, pageNr):
        virtualAdress = self.pageNrToVirtualNr[pageNr]
        if (virtualAdress < 0 or virtualAdress > self.maxPages):
            raise ValueError('Virtual Adress out of range: ' + str(virtualAdress) + ' Maximum: ' + str(self.maxPages))
        if(self.virtMem[virtualAdress] != pageNr):
            raise ValueError('The Relation PageNr and virtual Adresse are corrupted = ' + str(pageNr) + ' ' + str(self.virtMem[virtualAdress]))
        if((self.flagTable[pageNr] & self.DIRTY) == self.DIRTY):
            startingAdress = (virtualAdress << self.offsetBits) * 2
            wf = open(str(self.filePath), "r+b")
            wf.seek(startingAdress)
            for value in self.ramMem[pageNr]:
                wf.write(struct.pack("h", value))
            wf.close()
            self.flagTable[pageNr] = (self.flagTable[pageNr] ^ self.DIRTY)

    def loadPage(self, virtualPageNr):
        startAdress = (virtualPageNr << self.offsetBits) * 2
        freePageNr = self.getFreePageNr()
        if(virtualPageNr > self.maxPages or virtualPageNr < 0 or self.virtMem[virtualPageNr] > -1 or self.pageNrToVirtualNr[freePageNr] > -1):
            raise ValueError('Something is wrong with the Adress')
        wf = open(str(self.filePath), "rb")
        wf.seek(startAdress)
        print self.maxNumberOfStates()
        print startAdress
        for offset in range(0, self.offsetSize):
            self.ramMem[freePageNr][offset] = struct.unpack("h", wf.read(2))[0]
        wf.close
        self.virtMem[virtualPageNr] = freePageNr
        self.pageNrToVirtualNr[freePageNr] = virtualPageNr
        self.flagTable[freePageNr] = self.USED
        return freePageNr

    def getFreePageNr(self):
        freePage = -1
        if (self.usedPages < self.maxPages):
            freePage = self.usedPages
            self.usedPages += 1
        else:
            self.savePage(self.nextPageToReplace)
            freePage = self.nextPageToReplace
        self.virtMem[self.pageNrToVirtualNr[freePage]] = -1
        self.pageNrToVirtualNr[freePage] = -1
        self.nextPageToReplace = (self.nextPageToReplace + 1) % self.maxPages
        return freePage

    def getPageNr(self, virtualPageNr):
        pageNr = self.virtMem[virtualPageNr]
        if (pageNr >= 0):
            return pageNr
        else:
            return self.loadPage(virtualPageNr)

    def getRatingForNextState(self, wentDirection, state):
        wf = open(str(self.filePath), "rb")
        binVal = state.toBin()
        adress = (binVal << 2) + ReinforcementDirection.fromGameDirection(wentDirection)
        virtualPageNr = adress >> self.offsetBits
        offset = adress & (self.offsetSize - 1)
        pageNr = self.getPageNr(virtualPageNr)
        self.flagTable[pageNr] = self.flagTable[pageNr] | self.USED
        return self.ramMem[pageNr][offset]

    def setRatingForState(self, wentDirection, state, rating):
        if rating > (2**15 - 1):
            raise ValueError('Rating to high')
        if rating < -(2**15):
            raise ValueError('Rating to low')
        binVal = state.toBin()
        wf.seek((binVal * 2) + ReinforcementDirection.fromGameDirection(wentDirection))
        wf.write(struct.pack("H", rating))
        wf.close()


        #a = ReinforcementSave('1ghost', 1, 128)
        #print str(a.maxNumberOfStates()) + ' ' + str(float(a.fileSizeInBit()) / (8 * 1024 * 1024))
        #state = ReinforcementState(Directions.WEST, [GhostState(Directions.NORTH, Threat.DANGER, True)])
        #print 'getRatingForNextState' + str(a.getRatingForNextState(Directions.WEST, state))
        #a.setRatingForState(Directions.WEST,state,7)
        #print 'setRatingForNextState' + str(a.getRatingForNextState(Directions.WEST, state))
        #a = ReinforcementSave('2ghost', 2, 128)
        #print str(a.maxNumberOfStates()) + ' ' + str(float(a.fileSizeInBit()) / (8 * 1024 * 1024))
        #a = ReinforcementSave('3ghost', 3, 128)
        #print str(a.maxNumberOfStates()) + ' ' + str(float(a.fileSizeInBit()) / (8 * 1024 * 1024))
        #a = ReinforcementSave('4ghost', 4, 128)
        #print str(a.maxNumberOfStates()) + ' ' + str(float(a.fileSizeInBit()) / (8 * 1024 * 1024))
