import ConfigParser
import tkMessageBox
import subprocess
from datatypeUtils import DatatypeUtils
from pacman import startByLauncher
from graphicsDisplay import *
from pacmanGlobals import PacmanGlobals
from pacman import GameState

CONFIGURATION_FILE = "statistic_settings.ini"
OUTPUT_DIR = "statistics"

class LauncherController:
    def __init__(self, view):
        self.view = view
    
    # Used for executing with direct Pacman call
    def getArgumentArray(self, numTrainings):
        argumentValues = []
        
        argumentValues.append("-x " + str(numTrainings))
        numGamesValue = DatatypeUtils.stringToInteger(self.view.numGamesVar.get()) + numTrainings
        argumentValues.append("--numGames=" + str(numGamesValue))
        argumentValues.append("--numghosts=" + self.view.numGhostsVar.get())
        argumentValues.append("--layout=" + self.view.layoutVar.get())
        argumentValues.append("--pacman=" + self.view.pacmanVar.get())
        if (DatatypeUtils.stringToBoolean(self.view.fixRandomSeedVar.get())):
            argumentValues.append("--fixRandomSeed")
        
        argumentValues.append("--textGraphics")
        argumentValues.append("--quietTextGraphics")
            
        return argumentValues
    
    # Used for executing with subprocess.call
    def getArgumentString(self):
        argumentValues = self.getArgumentArray()
        if (len(argumentValues) > 0):
            return " ".join(argumentValues)
        else:
            return ""
    
    def outputFilePath(self):
        return OUTPUT_DIR + os.sep + self.view.outputFilenameVar.get()
    
    def writeConfiguration(self):
        Config = ConfigParser.ConfigParser()
        cfgfile = open(self.outputFilePath(), 'w')
        
        Config.add_section('StatisticSettings')
        Config.set('StatisticSettings', 'numTraining', self.view.numTrainingVar.get())
        Config.set('StatisticSettings', 'increment', self.view.incrementVar.get())
        Config.set('StatisticSettings', 'numGames', self.view.numGamesVar.get())
        Config.set('StatisticSettings', 'outputFilename', self.view.outputFilenameVar.get())
        
        Config.add_section('GameSettings')
        Config.set('GameSettings', 'numGhosts', self.view.numGhostsVar.get())
        Config.set('GameSettings', 'layout', self.view.layoutVar.get())
        Config.set('GameSettings', 'pacman', self.view.pacmanVar.get())
        Config.set('GameSettings', 'fixRandomSeed', self.view.fixRandomSeedVar.get())
        Config.write(cfgfile)
        
        cfgfile.close()
        
        with open(self.outputFilePath(), "a") as file:
            file.write("[Results]\n")
            file.close()
    
    def writeGameResult(self, numTrainings, games):
        scores = [game.state.getScore() for game in games]
        wins = [game.state.isWin() for game in games]

        winRate = wins.count(True)/ float(len(wins))
        averageScore = sum(scores) / float(len(scores))
        
        with open(self.outputFilePath(), "a") as file:
            file.write(str(numTrainings) + ";" + str(winRate) + ";" + str(averageScore) + "\n")
            file.close()
    
    def processGame(self, numTrainings):
        #arguments = self.getArgumentString()
        #subprocess.call("python pacman.py " + arguments, shell=True)
        
        argumentArray = self.getArgumentArray(numTrainings)
        games = startByLauncher(argumentArray)
        self.writeGameResult(numTrainings, games)
    
    def processGames(self):
        maxNumTraining = DatatypeUtils.stringToInteger(self.view.numTrainingVar.get())
        increment = DatatypeUtils.stringToInteger(self.view.incrementVar.get())
        
        #from pympler import tracker
        #memory_tracker = tracker.SummaryTracker()
        
        for numTraining in range(0, maxNumTraining, increment):
            self.processGame(numTraining)
            GameState.getAndResetExplored()
            #memory_tracker.print_diff()
    
    def startApplication(self):
        if (not self.validateData('Fehlerhafte Einstellungen!', 'Einige Einstellungswerte sind ungueltig: ', False)):
            return
        
        numGhostsValue = DatatypeUtils.stringToInteger(self.view.numGhostsVar.get())
        PacmanGlobals.numGhostAgents = numGhostsValue
        
        self.saveSettingsToConfigFile()
        
        self.view.destroy()
        
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)
        self.writeConfiguration()
        self.processGames()
    
    def getMapNumGhosts(self, layout):
        filename = "layouts/" + layout + ".lay"
        count = 0
        
        with open(filename) as f:
            while True:
                ch = f.read(1)
                if (not ch):
                    break
                
                if (ch == 'G'):
                    count = count + 1
        
        return count
    
    def outputFileAlreadyExists(self):
        return os.path.isfile(self.outputFilePath())
    
    def getInvalidFields(self, justLaunched):        
        invalidFields = []
        
        # Datatype checking
        if (not DatatypeUtils.isIntegerString(self.view.numTrainingVar.get())):
            invalidFields.append("'Maximale Anzahl der Trainings' muss eine Ganzzahl sein (zum Beispiel: 100)!")
        if (not DatatypeUtils.isIntegerString(self.view.incrementVar.get())):
            invalidFields.append("'Abstufungen der Trainings' muss eine Ganzzahl sein (zum Beispiel: 10)!")
        if (not DatatypeUtils.isIntegerString(self.view.numGamesVar.get())):
            invalidFields.append("'Anzahl der Wertungsspiele' muss eine Ganzzahl sein (zum Beispiel: 20)!")
        if (not DatatypeUtils.isString(self.view.outputFilenameVar.get())):
            invalidFields.append("'Ausgabedatei' muss eine Zeichenkette sein (zum Beispiel: output_001.csv)!")
        
        if (not DatatypeUtils.isIntegerString(self.view.numGhostsVar.get())):
            invalidFields.append("'Anzahl der Geister' muss eine Ganzzahl sein (zum Beispiel: 4)!")
        if (not DatatypeUtils.isString(self.view.layoutVar.get())):
            invalidFields.append("'Spielfeld' muss eine Zeichenkette sein (zum Beispiel: mediumClassic)!")
        if (not DatatypeUtils.isString(self.view.pacmanVar.get())):
            invalidFields.append("'Pacman-Agent' muss eine Zeichenkette sein (zum Beispiel: KeyboardAgent)!")
        if (not DatatypeUtils.isBooleanString(self.view.fixRandomSeedVar.get())):
            invalidFields.append("'Feste Random-Seed' muss ein Wahrheitswert sein (True oder False)!")
        
        # Value checking (numTraining)
        if (DatatypeUtils.isIntegerString(self.view.numTrainingVar.get())):
            numTrainingValue = DatatypeUtils.stringToInteger(self.view.numTrainingVar.get())
            if (numTrainingValue < 0):
                invalidFields.append("'Maximale Anzahl der Trainings' muss groesser oder gleich " + str(0) + " sein!")
        
        # Value checking (increment)
        if (DatatypeUtils.isIntegerString(self.view.incrementVar.get())):
            incrementValue = DatatypeUtils.stringToInteger(self.view.incrementVar.get())
            if (incrementValue < 0):
                invalidFields.append("'Abstufungen der Trainings' muss groesser oder gleich " + str(0) + " sein!")
        
        # Value checking (numGames)
        if (DatatypeUtils.isIntegerString(self.view.numGamesVar.get())):
            numGamesValue = DatatypeUtils.stringToInteger(self.view.numGamesVar.get())
            if (numGamesValue < 1):
                invalidFields.append("'Anzahl der Spiele' muss groesser oder gleich " + str(1) + " sein!")
        
        # Value checking (outputFilename)
        if (DatatypeUtils.isString(self.view.outputFilenameVar.get()) and (not justLaunched)):
            if self.outputFileAlreadyExists():
                invalidFields.append("Ausgabedatei '" + self.view.outputFilenameVar.get() + "' ist bereits vorhanden!")
        
        # Value checking (numGhosts)
        if (DatatypeUtils.isIntegerString(self.view.numGhostsVar.get())):
            numGhostsValue = DatatypeUtils.stringToInteger(self.view.numGhostsVar.get())
            if (numGhostsValue < 0):
                invalidFields.append("'Anzahl der Geister' muss groesser oder gleich " + str(0) + " sein!")
            
            layout = self.view.layoutVar.get()
            mapNumGhosts = self.getMapNumGhosts(layout)
            if (mapNumGhosts > 5):
                mapNumGhosts = 5
            
            if (numGhostsValue > mapNumGhosts):
                invalidFields.append("'Anzahl der Geister' muss fuer Spielfeld '" + layout + "' kleiner oder gleich " + str(mapNumGhosts) + " sein!")
        
        return invalidFields
        
    def validateData(self, errorTitle, errorMessage, justLaunched = True):
        invalidFields = self.getInvalidFields(justLaunched)
        if (len(invalidFields) > 0):
            tkMessageBox.showerror(
                title = errorTitle,
                message = errorMessage + '\n- ' + '\n- '.join(invalidFields))
            return False
        else:
            return True
    
    def loadDefaultSettings(self):
        self.view.numTrainingVar.set("100")
        self.view.incrementVar.set("10")
        self.view.numGamesVar.set("20")
        self.view.outputFilenameVar.set("output_001.csv")
        
        self.view.numGhostsVar.set("2")
        self.view.layoutVar.set("mediumClassic")
        self.view.pacmanVar.set("KeyboardAgent")
        self.view.fixRandomSeedVar.set("False")
        
        self.validateData('Fehlerhafte Einstellungen!', 'Einige Standard-Einstellungswerte sind ungueltig: ')
        
    def loadSettingsFromConfigFile(self):
        try:
            Config = ConfigParser.ConfigParser()
            Config.read(CONFIGURATION_FILE)
            
            self.view.numTrainingVar.set(Config.get('StatisticSettings', 'numTraining'))
            self.view.incrementVar.set(Config.get('StatisticSettings', 'increment'))
            self.view.numGamesVar.set(Config.get('StatisticSettings', 'numGames'))
            self.view.outputFilenameVar.set(Config.get('StatisticSettings', 'outputFilename'))
            
            self.view.numGhostsVar.set(Config.get('GameSettings', 'numGhosts'))
            self.view.layoutVar.set(Config.get('GameSettings', 'layout'))
            self.view.pacmanVar.set(Config.get('GameSettings', 'pacman'))
            self.view.fixRandomSeedVar.set(Config.get('GameSettings', 'fixRandomSeed'))
            
            self.validateData('Fehlerhafte Einstellungen!', 'Einige Einstellungswerte sind ungueltig: ')
        except Exception, e:
            print str(e)
            print "Because an error occured, the default configuration will be loaded and will also be written to the configuration file!"
            self.handleMissingConfigFile();
        
    def handleMissingConfigFile(self):
        self.loadDefaultSettings()
        self.saveSettingsToConfigFile()
        
    def saveSettingsToConfigFile(self):
        if (not self.validateData('Fehlerhafte Einstellungen!', 'Einige Einstellungswerte sind ungueltig: ')):
            return
            
        Config = ConfigParser.ConfigParser()
        cfgfile = open(CONFIGURATION_FILE, 'w')
        
        Config.add_section('StatisticSettings')
        Config.set('StatisticSettings', 'numTraining', self.view.numTrainingVar.get())
        Config.set('StatisticSettings', 'increment', self.view.incrementVar.get())
        Config.set('StatisticSettings', 'numGames', self.view.numGamesVar.get())
        Config.set('StatisticSettings', 'outputFilename', self.view.outputFilenameVar.get())
        
        Config.add_section('GameSettings')
        Config.set('GameSettings', 'numGhosts', self.view.numGhostsVar.get())
        Config.set('GameSettings', 'layout', self.view.layoutVar.get())
        Config.set('GameSettings', 'pacman', self.view.pacmanVar.get())
        Config.set('GameSettings', 'fixRandomSeed', self.view.fixRandomSeedVar.get())
        Config.write(cfgfile)
        
        cfgfile.close()
