from ReinforcementState import *
import os.path
import os
import struct
import numpy as np

class ReinforcementSave(object):
    PRESENT = 2 ** 0
    USED = 2 ** 1
    DIRTY = 2 ** 3

    """
    Speicherverwaltung fuer das Reinforcementlearning.
    Es sollte pro Spiel maximal eine Instanz existieren.
    Auf garkeinen Fall duerfen 2 oder mehr Instanzen auf die gleiche Datei zugreifen.
    TODO: Check ob zwei Instanzen die gleiche Datei verwenden.
    Auch sollte darauf geachte werden, das die Instanz so selten wie moeglich geloescht und neuinstanziert wird,
    am besten nur einmal pro Spiel.
    Bei der Instanzierung wird im Unterordner savedLearned die entsprechende Datei erstellt, wenn nicht vorhanden,
    sonst wir gecheckt, ob die vorhandene Datei Konsistent ist.
    """

    def __init__(self, fileName, numGhosts, maxMemoryInMB = 16, offsetBits = 7):
        """
        :param fileName: String Dateiname
        :param numGhosts: Integer Anzahl der Geister im Spiel
        :param maxMemoryInMB: Integer Groesse des im Arbeitsspeicher vorgehaltenem Bereichs in MB
        :param offsetBits: Integer Bestimmt die Seitengroesse 2 ** offsetBits ist die Anzahl der Ratings pro Seite.
        """
        self.fileName = fileName
        self.numGhosts = numGhosts
        self.maxNeededBitsForSaving = ((self.numGhosts * 5) + 2) + 2
        self.maxMemoryInMB = maxMemoryInMB
        if (offsetBits > self.maxNeededBitsForSaving):
            self.offsetBits = self.maxNeededBitsForSaving
        else:
            self.offsetBits = offsetBits
        self.offsetSize = (2 ** self.offsetBits)
        self.usedPages = 0
        self.nextPageToReplace = 0
        self.maxPages = (self.maxMemoryInMB * (1024 ** 2)) / (4 * self.offsetSize)
        self.__initVirtualAdressSpace()
        self.__initRamMem()
        self.__initFile()

    def __enter__(self):
        return self

    def __del__(self):
        """
        Destruktor, Speichert beim loeschen des Objektes die Aenderungen auf die HDD
        """
        for x in range(0, self.usedPages):
            if(self.pageNrToVirtualNr[x] >= 0):
                self.__savePage(x)

    def maxNumberOfStates(self):
        """
        :return: Integer Anzahl der States, die im Spiel maximal existieren koennen
        """
        return 2 ** self.maxNeededBitsForSaving

    def fileSizeInBit(self):
        """
        :return: Integer Dateigroesse in Bit
        """
        return self.maxNumberOfStates() * self.numGhosts * 32

    def __createInitialFile(self, filePath):
        wf = open(str(filePath), "wb")
        for x in range(0, self.maxNumberOfStates()):
            for y in xrange(0,self.numGhosts):
                wf.write(struct.pack("f", 0))
        wf.close()

    def __initVirtualAdressSpace(self):
        """
        Initiert die Seitenzuordnungstabelle
        """
        self.virtMem = np.array([-1] * self.maxPages, np.int32)

    def __initRamMem(self):
        """
        Initiert den RAM
        """
        self.ramMem = np.array(([([0] * self.offsetSize)] * self.maxPages), np.float32)
        self.flagTable = np.array([0] * self.maxPages, np.uint8)
        self.pageNrToVirtualNr = np.array([-1] * self.maxPages, np.int32)

    def __initFile(self):
        """
        Initiert und ueberprueft die Auslagerungsdatei
        """
        if not(os.path.isdir(os.getcwd() + os.sep + 'savedLearned')):
            os.makedirs(os.getcwd() + os.sep + 'savedLearned')
        if not(os.path.isfile(os.getcwd() + os.sep + 'savedLearned' + os.sep + self.fileName)):
            self.__createInitialFile(os.getcwd() + os.sep + 'savedLearned' + os.sep + self.fileName)
        if not((self.fileSizeInBit() / 8) == os.path.getsize(os.getcwd() + os.sep + 'savedLearned' + os.sep + self.fileName)):
            raise ValueError('The fileSize does not match with the Options')
        self.filePath = os.getcwd() + os.sep + 'savedLearned' + os.sep + self.fileName

    def __savePage(self, pageNr):
        """
        Speichert eine Seite aus dem ramMem in die Auslagerungsdatei
        """
        virtualAdress = self.pageNrToVirtualNr[pageNr]
        if (virtualAdress < 0 or virtualAdress > self.maxPages):
            raise ValueError('Virtual Adress out of range: ' + str(virtualAdress) + ' Maximum: ' + str(self.maxPages))
        if(self.virtMem[virtualAdress] != pageNr):
            raise ValueError('The Relation PageNr and virtual Adresse are corrupted = ' + str(pageNr) + ' ' + str(self.virtMem[virtualAdress]))
        if((self.flagTable[pageNr] & self.DIRTY) == self.DIRTY):
            startingAdress = (virtualAdress << self.offsetBits) * 4
            wf = open(str(self.filePath), "r+b")
            wf.seek(startingAdress)
            for value in self.ramMem[pageNr]:
                wf.write(struct.pack("f", value))
            wf.close()
            self.flagTable[pageNr] = (self.flagTable[pageNr] ^ self.DIRTY)

    def __loadPage(self, virtualPageNr):
        """
        Laed eine Seite aus der Auslagerungsdatei in den Arbeitsspeicher
        """
        startAdress = (virtualPageNr << self.offsetBits) * 4
        freePageNr = self.__getFreePageNr()
        if(virtualPageNr > self.maxPages or virtualPageNr < 0 or self.virtMem[virtualPageNr] > -1 or self.pageNrToVirtualNr[freePageNr] > -1):
            raise ValueError('Something is wrong with the Adress')
        wf = open(str(self.filePath), "rb")
        wf.seek(startAdress)
        for offset in range(0, self.offsetSize):
            self.ramMem[freePageNr][offset] = struct.unpack("f", wf.read(4))[0]
        wf.close
        self.virtMem[virtualPageNr] = freePageNr
        self.pageNrToVirtualNr[freePageNr] = virtualPageNr
        self.flagTable[freePageNr] = self.USED
        return freePageNr

    def __getFreePageNr(self):
        """
        Sucht die naechste freie Seite exisitiert keine, wird mittels FIFO eine gespeichert und freigegeben.
        """
        freePage = -1
        if (self.usedPages < self.maxPages):
            freePage = self.usedPages
            self.usedPages += 1
        else:
            self.__savePage(self.nextPageToReplace)
            freePage = self.nextPageToReplace
        self.virtMem[self.pageNrToVirtualNr[freePage]] = -1
        self.pageNrToVirtualNr[freePage] = -1
        self.nextPageToReplace = (self.nextPageToReplace + 1) % self.maxPages
        return freePage

    def __getPageNr(self, virtualPageNr):
        """

        """
        pageNr = self.virtMem[virtualPageNr]
        if (pageNr >= 0):
            return pageNr
        else:
            return self.__loadPage(virtualPageNr)

    def getRatingForNextState(self, wentDirection, state):
        binVal = state.toBin()
        adress = (binVal << 2) + ReinforcementDirection.fromGameDirection(wentDirection)
        virtualPageNr = adress >> self.offsetBits
        offset = adress & (self.offsetSize - 1)
        pageNr = self.__getPageNr(virtualPageNr)
        self.flagTable[pageNr] = self.flagTable[pageNr] | self.USED
        return self.ramMem[pageNr][offset]

    def setRatingForState(self, wentDirection, state, rating):
        if rating > (np.finfo('f').max):
            raise ValueError('Rating to high')
        if rating < (np.finfo('f').min):
            raise ValueError('Rating to low')
        binVal = state.toBin()
        adress = (binVal << 2) + ReinforcementDirection.fromGameDirection(wentDirection)
        virtualPageNr = adress >> self.offsetBits
        offset = adress & (self.offsetSize - 1)
        pageNr = self.__getPageNr(virtualPageNr)
        self.flagTable[pageNr] = self.flagTable[pageNr] | self.USED | self.DIRTY
        self.ramMem[pageNr][offset] = rating

a = ReinforcementSave('1ghost', 1)
print str(a.maxNumberOfStates()) + ' ' + str(float(a.fileSizeInBit()) / (8 * 1024 * 1024))
state = ReinforcementState(ReinforcementDirection.WEST, [GhostState(ReinforcementDirection.WEST, Threat.FAR_AWAY, True)])
print 'getRatingForNextState ' + str(a.getRatingForNextState(Directions.WEST, state))
a.setRatingForState(Directions.WEST,state,8.2356283723627367)
print 'setRatingForNextState ' + str(a.getRatingForNextState(Directions.WEST, state))
#a = ReinforcementSave('2ghost', 2)
#print str(a.maxNumberOfStates()) + ' ' + str(float(a.fileSizeInBit()) / (8 * 1024 * 1024))
#a = ReinforcementSave('3ghost', 3, 128)
#print str(a.maxNumberOfStates()) + ' ' + str(float(a.fileSizeInBit()) / (8 * 1024 * 1024))
#a = ReinforcementSave('4ghost', 4, 128)
#print str(a.maxNumberOfStates()) + ' ' + str(float(a.fileSizeInBit()) / (8 * 1024 * 1024))
