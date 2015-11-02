import ConfigParser
import tkMessageBox
import subprocess
from datatypeUtils import DatatypeUtils
from pacman import startByLauncher
from graphicsDisplay import *

CONFIGURATION_FILE = "settings.ini"

class LauncherController:
    def __init__(self, view, numTrainingVar, numGamesVar, numGhostsVar, layoutVar, pacmanVar, fixRandomSeedVar, zoomVar, frameTimeVar, textGraphicsVar, quietTextGraphicsVar):
        self.view = view
        self.numTrainingVar = numTrainingVar
        self.numGamesVar = numGamesVar
        self.numGhostsVar = numGhostsVar
        self.layoutVar = layoutVar
        self.pacmanVar = pacmanVar
        self.fixRandomSeedVar = fixRandomSeedVar
        
        self.zoomVar = zoomVar
        self.frameTimeVar = frameTimeVar
        self.textGraphicsVar = textGraphicsVar
        self.quietTextGraphicsVar = quietTextGraphicsVar
    
    # Used for executing with direct Pacman call
    def getArgumentArray(self):
        argumentValues = []
        
        argumentValues.append("-x " + self.numTrainingVar.get())
        argumentValues.append("--numGames=" + self.numGamesVar.get())
        argumentValues.append("--numghosts=" + self.numGhostsVar.get())
        argumentValues.append("--layout=" + self.layoutVar.get())
        argumentValues.append("--pacman=" + self.pacmanVar.get())
        if (DatatypeUtils.stringToBoolean(self.fixRandomSeedVar.get())):
            argumentValues.append("--fixRandomSeed")
        
        argumentValues.append("--zoom=" + self.zoomVar.get())
        argumentValues.append("--frameTime=" + self.frameTimeVar.get())
        if (DatatypeUtils.stringToBoolean(self.textGraphicsVar.get())):
            argumentValues.append("--textGraphics")
        if (DatatypeUtils.stringToBoolean(self.quietTextGraphicsVar.get())):
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
        if (not DatatypeUtils.isIntegerString(self.numTrainingVar.get())):
            invalidFields.append("'Anzahl der Trainings' muss eine Ganzzahl sein (zum Beispiel: 1)!")
        if (not DatatypeUtils.isIntegerString(self.numGamesVar.get())):
            invalidFields.append("'Anzahl der Spiele' muss eine Ganzzahl sein (zum Beispiel: 1)!")
        if (not DatatypeUtils.isIntegerString(self.numGhostsVar.get())):
            invalidFields.append("'Anzahl der Geister' muss eine Ganzzahl sein (zum Beispiel: 4)!")
        if (not DatatypeUtils.isString(self.layoutVar.get())):
            invalidFields.append("'Spielfeld' muss eine Zeichenkette sein (zum Beispiel: mediumClassic)!")
        if (not DatatypeUtils.isString(self.pacmanVar.get())):
            invalidFields.append("'Pacman-Agent' muss eine Zeichenkette sein (zum Beispiel: KeyboardAgent)!")
        if (not DatatypeUtils.isBooleanString(self.fixRandomSeedVar.get())):
            invalidFields.append("'Feste Random-Seed' muss ein Wahrheitswert sein (True oder False)!")
        
        if (not DatatypeUtils.isFloatString(self.zoomVar.get())):
            invalidFields.append("'Zoomfaktor' muss eine Kommazahl sein (zum Beispiel: 1.0)!")
        if (not DatatypeUtils.isFloatString(self.frameTimeVar.get())):
            invalidFields.append("'Spielgeschwindigkeit' muss eine Kommazahl sein (zum Beispiel: 0.1)!")
        if (not DatatypeUtils.isBooleanString(self.textGraphicsVar.get())):
            invalidFields.append("'Ausgabe als Text' muss ein Wahrheitswert sein (True oder False)!")
        if (not DatatypeUtils.isBooleanString(self.quietTextGraphicsVar.get())):
            invalidFields.append("'Minimale Ausgabe' muss ein Wahrheitswert sein (True oder False)!")
        
        # Value checking (numTraining)
        if (DatatypeUtils.isIntegerString(self.numTrainingVar.get())):
            numTrainingValue = DatatypeUtils.stringToInteger(self.numTrainingVar.get())
            if (numTrainingValue < 0):
                invalidFields.append("'Anzahl der Trainings' muss groesser oder gleich " + str(0) + " sein!")
        
        # Value checking (numGames)
        if (DatatypeUtils.isIntegerString(self.numGamesVar.get())):
            numGamesValue = DatatypeUtils.stringToInteger(self.numGamesVar.get())
            if (numGamesValue < 1):
                invalidFields.append("'Anzahl der Spiele' muss groesser oder gleich " + str(1) + " sein!")
        
        # Value checking (numGhosts)
        if (DatatypeUtils.isIntegerString(self.numGhostsVar.get())):
            numGhostsValue = DatatypeUtils.stringToInteger(self.numGhostsVar.get())
            if (numGhostsValue < 0):
                invalidFields.append("'Anzahl der Geister' muss groesser oder gleich " + str(0) + " sein!")
            
            layout = self.layoutVar.get()
            mapNumGhosts = self.getMapNumGhosts(layout)
            if (mapNumGhosts > 5):
                mapNumGhosts = 5
            
            if (numGhostsValue > mapNumGhosts):
                invalidFields.append("'Anzahl der Geister' muss fuer Spielfeld '" + layout + "' kleiner oder gleich " + str(mapNumGhosts) + " sein!")

        # Value checking (zoom)
        if (DatatypeUtils.isFloatString(self.zoomVar.get())):
            zoomValue = DatatypeUtils.stringToFloat(self.zoomVar.get())
            if (zoomValue > MAX_ZOOM):
                invalidFields.append("'Zoomfaktor' muss kleiner oder gleich " + str(MAX_ZOOM) + " sein!")
            if (zoomValue < MIN_ZOOM):
                invalidFields.append("'Zoomfaktor' muss groesser oder gleich " + str(MIN_ZOOM) + " sein!")
        
        # Value checking (frameTime)
        if (DatatypeUtils.isFloatString(self.frameTimeVar.get())):
            frameTimeValue = DatatypeUtils.stringToFloat(self.frameTimeVar.get())
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
        self.numTrainingVar.set("0")
        self.numGamesVar.set("1")
        self.numGhostsVar.set("2")
        self.layoutVar.set("mediumClassic")
        self.pacmanVar.set("KeyboardAgent")
        self.fixRandomSeedVar.set("False")
        
        self.zoomVar.set("1.0")
        self.frameTimeVar.set("0.1")
        self.textGraphicsVar.set("False")
        self.quietTextGraphicsVar.set("False")
        
        self.validateData('Fehlerhafte Einstellungen!', 'Einige Standard-Einstellungswerte sind ungueltig: ')
        
    def loadSettingsFromConfigFile(self):
        try:
            Config = ConfigParser.ConfigParser()
            Config.read(CONFIGURATION_FILE)
            
            self.numTrainingVar.set(Config.get('GameSettings', 'numTraining'))
            self.numGamesVar.set(Config.get('GameSettings', 'numGames'))
            self.numGhostsVar.set(Config.get('GameSettings', 'numGhosts'))
            self.layoutVar.set(Config.get('GameSettings', 'layout'))
            self.pacmanVar.set(Config.get('GameSettings', 'pacman'))
            self.fixRandomSeedVar.set(Config.get('GameSettings', 'fixRandomSeed'))
            
            self.zoomVar.set(Config.get('DisplaySettings', 'zoom'))
            self.frameTimeVar.set(Config.get('DisplaySettings', 'frameTime'))
            self.textGraphicsVar.set(Config.get('DisplaySettings', 'textGraphics'))
            self.quietTextGraphicsVar.set(Config.get('DisplaySettings', 'quietTextGraphics'))
            
            self.validateData('Fehlerhafte Einstellungen!', 'Einige Einstellungswerte sind ungueltig: ')
        except:
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
        Config.set('GameSettings', 'numTraining', self.numTrainingVar.get())
        Config.set('GameSettings', 'numGames', self.numGamesVar.get())
        Config.set('GameSettings', 'numGhosts', self.numGhostsVar.get())
        Config.set('GameSettings', 'layout', self.layoutVar.get())
        Config.set('GameSettings', 'pacman', self.pacmanVar.get())
        Config.set('GameSettings', 'fixRandomSeed', self.fixRandomSeedVar.get())
        
        Config.add_section('DisplaySettings')
        Config.set('DisplaySettings', 'zoom', self.zoomVar.get())
        Config.set('DisplaySettings', 'frameTime', self.frameTimeVar.get())
        Config.set('DisplaySettings', 'textGraphics', self.textGraphicsVar.get())
        Config.set('DisplaySettings', 'quietTextGraphics', self.quietTextGraphicsVar.get())
        Config.write(cfgfile)
        
        cfgfile.close()
