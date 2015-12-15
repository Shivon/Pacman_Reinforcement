import ConfigParser
import tkMessageBox
import subprocess
from datatypeUtils import DatatypeUtils
from pacman import startByLauncher
from graphicsDisplay import *
from pacmanGlobals import PacmanGlobals

CONFIGURATION_FILE = "settings.ini"

class LauncherController:
    def __init__(self, view):
        self.view = view
    
    # Used for executing with direct Pacman call
    def getArgumentArray(self):
        argumentValues = []
        
        argumentValues.append("-x " + self.view.numTrainingVar.get())
        numGamesValue = DatatypeUtils.stringToInteger(self.view.numGamesVar.get()) + DatatypeUtils.stringToInteger(self.view.numTrainingVar.get())
        argumentValues.append("--numGames=" + str(numGamesValue))
        argumentValues.append("--numghosts=" + self.view.numGhostsVar.get())
        argumentValues.append("--layout=" + self.view.layoutVar.get())
        argumentValues.append("--pacman=" + self.view.pacmanVar.get())
        if (DatatypeUtils.stringToBoolean(self.view.fixRandomSeedVar.get())):
            argumentValues.append("--fixRandomSeed")
        
        argumentValues.append("--zoom=" + self.view.zoomVar.get())
        argumentValues.append("--frameTime=" + self.view.frameTimeVar.get())
        if (DatatypeUtils.stringToBoolean(self.view.textGraphicsVar.get())):
            argumentValues.append("--textGraphics")
        if (DatatypeUtils.stringToBoolean(self.view.quietTextGraphicsVar.get())):
            argumentValues.append("--quietTextGraphics")
            
        return argumentValues
    
    # Used for executing with subprocess.call
    def getArgumentString(self):
        argumentValues = self.getArgumentArray()
        if (len(argumentValues) > 0):
            return " ".join(argumentValues)
        else:
            return ""
    
    def startApplication(self):
        if (not self.validateData('Fehlerhafte Einstellungen!', 'Einige Einstellungswerte sind ungueltig: ')):
            return
        
        numGhostsValue = DatatypeUtils.stringToInteger(self.view.numGhostsVar.get())
        PacmanGlobals.numGhostAgents = numGhostsValue

        debugModeSet = DatatypeUtils.stringToBoolean((self.view.displayDebugVar.get()))
        PacmanGlobals.debugModeBool = debugModeSet

        self.saveSettingsToConfigFile()
        
        self.view.destroy()
        
        #arguments = self.getArgumentString()
        #subprocess.call("python pacman.py " + arguments, shell=True)
        
        argumentArray = self.getArgumentArray()
        startByLauncher(argumentArray)
    
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
    
    def getInvalidFields(self):        
        invalidFields = []
        
        # Datatype checking
        if (not DatatypeUtils.isIntegerString(self.view.numTrainingVar.get())):
            invalidFields.append("'Anzahl der Trainings' muss eine Ganzzahl sein (zum Beispiel: 1)!")
        if (not DatatypeUtils.isIntegerString(self.view.numGamesVar.get())):
            invalidFields.append("'Anzahl der Spiele' muss eine Ganzzahl sein (zum Beispiel: 1)!")
        if (not DatatypeUtils.isIntegerString(self.view.numGhostsVar.get())):
            invalidFields.append("'Anzahl der Geister' muss eine Ganzzahl sein (zum Beispiel: 4)!")
        if (not DatatypeUtils.isString(self.view.layoutVar.get())):
            invalidFields.append("'Spielfeld' muss eine Zeichenkette sein (zum Beispiel: mediumClassic)!")
        if (not DatatypeUtils.isString(self.view.pacmanVar.get())):
            invalidFields.append("'Pacman-Agent' muss eine Zeichenkette sein (zum Beispiel: KeyboardAgent)!")
        if (not DatatypeUtils.isBooleanString(self.view.fixRandomSeedVar.get())):
            invalidFields.append("'Feste Random-Seed' muss ein Wahrheitswert sein (True oder False)!")
        
        if (not DatatypeUtils.isFloatString(self.view.zoomVar.get())):
            invalidFields.append("'Zoomfaktor' muss eine Kommazahl sein (zum Beispiel: 1.0)!")
        if (not DatatypeUtils.isFloatString(self.view.frameTimeVar.get())):
            invalidFields.append("'Spielgeschwindigkeit' muss eine Kommazahl sein (zum Beispiel: 0.1)!")
        if (not DatatypeUtils.isBooleanString(self.view.textGraphicsVar.get())):
            invalidFields.append("'Ausgabe als Text' muss ein Wahrheitswert sein (True oder False)!")
        if (not DatatypeUtils.isBooleanString(self.view.quietTextGraphicsVar.get())):
            invalidFields.append("'Minimale Ausgabe' muss ein Wahrheitswert sein (True oder False)!")
        
        # Value checking (numTraining)
        if (DatatypeUtils.isIntegerString(self.view.numTrainingVar.get())):
            numTrainingValue = DatatypeUtils.stringToInteger(self.view.numTrainingVar.get())
            if (numTrainingValue < 0):
                invalidFields.append("'Anzahl der Trainings' muss groesser oder gleich " + str(0) + " sein!")
        
        # Value checking (numGames)
        if (DatatypeUtils.isIntegerString(self.view.numGamesVar.get())):
            numGamesValue = DatatypeUtils.stringToInteger(self.view.numGamesVar.get())
            if (numGamesValue < 1):
                invalidFields.append("'Anzahl der Spiele' muss groesser oder gleich " + str(1) + " sein!")
        
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

        # Value checking (zoom)
        if (DatatypeUtils.isFloatString(self.view.zoomVar.get())):
            zoomValue = DatatypeUtils.stringToFloat(self.view.zoomVar.get())
            if (zoomValue > MAX_ZOOM):
                invalidFields.append("'Zoomfaktor' muss kleiner oder gleich " + str(MAX_ZOOM) + " sein!")
            if (zoomValue < MIN_ZOOM):
                invalidFields.append("'Zoomfaktor' muss groesser oder gleich " + str(MIN_ZOOM) + " sein!")
        
        # Value checking (frameTime)
        if (DatatypeUtils.isFloatString(self.view.frameTimeVar.get())):
            frameTimeValue = DatatypeUtils.stringToFloat(self.view.frameTimeVar.get())
            if (frameTimeValue > MAX_SPEED):
                invalidFields.append("'Spielgeschwindigkeit' muss kleiner oder gleich " + str(MAX_SPEED) + " sein!")
            if (frameTimeValue < MIN_SPEED):
                invalidFields.append("'Spielgeschwindigkeit' muss groesser oder gleich " + str(MIN_SPEED) + " sein!")
        
        return invalidFields
        
    def validateData(self, errorTitle, errorMessage):
        invalidFields = self.getInvalidFields()
        if (len(invalidFields) > 0):
            tkMessageBox.showerror(
                title = errorTitle,
                message = errorMessage + '\n- ' + '\n- '.join(invalidFields))
            return False
        else:
            return True
    
    def loadDefaultSettings(self):
        self.view.numTrainingVar.set("0")
        self.view.numGamesVar.set("1")
        self.view.numGhostsVar.set("2")
        self.view.layoutVar.set("mediumClassic")
        self.view.pacmanVar.set("KeyboardAgent")
        self.view.fixRandomSeedVar.set("False")
        
        self.view.zoomVar.set("1.0")
        self.view.frameTimeVar.set("0.1")
        self.view.textGraphicsVar.set("False")
        self.view.quietTextGraphicsVar.set("False")
        self.view.displayDebugVar.set("False")

        self.validateData('Fehlerhafte Einstellungen!', 'Einige Standard-Einstellungswerte sind ungueltig: ')
        
    def loadSettingsFromConfigFile(self):
        try:
            Config = ConfigParser.ConfigParser()
            Config.read(CONFIGURATION_FILE)
            
            self.view.numTrainingVar.set(Config.get('GameSettings', 'numTraining'))
            self.view.numGamesVar.set(Config.get('GameSettings', 'numGames'))
            self.view.numGhostsVar.set(Config.get('GameSettings', 'numGhosts'))
            self.view.layoutVar.set(Config.get('GameSettings', 'layout'))
            self.view.pacmanVar.set(Config.get('GameSettings', 'pacman'))
            self.view.fixRandomSeedVar.set(Config.get('GameSettings', 'fixRandomSeed'))
            
            self.view.zoomVar.set(Config.get('DisplaySettings', 'zoom'))
            self.view.frameTimeVar.set(Config.get('DisplaySettings', 'frameTime'))
            self.view.textGraphicsVar.set(Config.get('DisplaySettings', 'textGraphics'))
            self.view.quietTextGraphicsVar.set(Config.get('DisplaySettings', 'quietTextGraphics'))
            self.view.displayDebugVar.set(Config.get('DisplaySettings', 'displayDebugMode'))

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
        
        Config.add_section('GameSettings')
        Config.set('GameSettings', 'numTraining', self.view.numTrainingVar.get())
        Config.set('GameSettings', 'numGames', self.view.numGamesVar.get())
        Config.set('GameSettings', 'numGhosts', self.view.numGhostsVar.get())
        Config.set('GameSettings', 'layout', self.view.layoutVar.get())
        Config.set('GameSettings', 'pacman', self.view.pacmanVar.get())
        Config.set('GameSettings', 'fixRandomSeed', self.view.fixRandomSeedVar.get())
        
        Config.add_section('DisplaySettings')
        Config.set('DisplaySettings', 'zoom', self.view.zoomVar.get())
        Config.set('DisplaySettings', 'frameTime', self.view.frameTimeVar.get())
        Config.set('DisplaySettings', 'textGraphics', self.view.textGraphicsVar.get())
        Config.set('DisplaySettings', 'quietTextGraphics', self.view.quietTextGraphicsVar.get())
        Config.set('DisplaySettings', 'displayDebugMode', self.view.displayDebugVar.get())
        Config.write(cfgfile)
        
        cfgfile.close()
