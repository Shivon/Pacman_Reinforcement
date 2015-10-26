import ConfigParser
import tkMessageBox
import subprocess
from datatypeUtils import DatatypeUtils
from graphicsDisplay import *

CONFIGURATION_FILE = "settings.ini"

class LauncherController:
    view = None
    numGamesVar = None
    numGhostsVar = None
    pacmanVar = None
    frameTimeVar = None
    textGraphicsVar = None
    quietTextGraphicsVar = None
    
    def __init__(self, view, numGamesVar, numGhostsVar, layoutVar, pacmanVar, frameTimeVar, textGraphicsVar, quietTextGraphicsVar):
        self.view = view
        self.numGamesVar = numGamesVar
        self.numGhostsVar = numGhostsVar
        self.layoutVar = layoutVar
        self.pacmanVar = pacmanVar
        
        self.frameTimeVar = frameTimeVar
        self.textGraphicsVar = textGraphicsVar
        self.quietTextGraphicsVar = quietTextGraphicsVar
    
    def getArgumentString(self):
        argumentValues = []
        
        argumentValues.append("--numGames=" + self.numGamesVar.get())
        argumentValues.append("--numghosts=" + self.numGhostsVar.get())
        argumentValues.append("--layout=" + self.layoutVar.get())
        argumentValues.append("--pacman=" + self.pacmanVar.get())
        
        argumentValues.append("--frameTime=" + self.frameTimeVar.get())
        if (DatatypeUtils.stringToBoolean(self.textGraphicsVar.get())):
            argumentValues.append("--textGraphics")
        if (DatatypeUtils.stringToBoolean(self.quietTextGraphicsVar.get())):
            argumentValues.append("--quietTextGraphics")
        
        if (len(argumentValues) > 0):
            return " ".join(argumentValues)
        else:
            return ""
    
    def startApplication(self):
        if (not self.validateData('Fehlerhafte Einstellungen!', 'Einige Einstellungswerte sind ungueltig: ')):
            return
        
        self.saveSettingsToConfigFile()
        arguments = self.getArgumentString()
        
        self.view.destroy()
        subprocess.call("python pacman.py " + arguments, shell=True)
    
    def getInvalidFields(self):        
        invalidFields = []
        
        # Datatype checking
        if (not DatatypeUtils.isIntegerString(self.numGamesVar.get())):
            invalidFields.append("'Anzahl der Spiele' muss eine Ganzzahl sein (zum Beispiel: 1)!")
        if (not DatatypeUtils.isIntegerString(self.numGhostsVar.get())):
            invalidFields.append("'Anzahl der Geister' muss eine Ganzzahl sein (zum Beispiel: 4)!")
        if (not DatatypeUtils.isString(self.layoutVar.get())):
            invalidFields.append("'Spielfeld' muss eine Zeichenkette sein (zum Beispiel: mediumClassic)!")
        if (not DatatypeUtils.isString(self.pacmanVar.get())):
            invalidFields.append("'Pacman-Agent' muss eine Zeichenkette sein (zum Beispiel: KeyboardAgent)!")
            
        if (not DatatypeUtils.isFloatString(self.frameTimeVar.get())):
            invalidFields.append("'Spielgeschwindigkeit' muss eine Kommazahl sein (zum Beispiel: 0.1)!")
        if (not DatatypeUtils.isBooleanString(self.textGraphicsVar.get())):
            invalidFields.append("'Ausgabe als Text' muss ein Wahrheitswert sein (True oder False)!")
        if (not DatatypeUtils.isBooleanString(self.quietTextGraphicsVar.get())):
            invalidFields.append("'Minimale Ausgabe' muss ein Wahrheitswert sein (True oder False)!")
            
        # Value checking
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
        self.numGamesVar.set("1")
        self.numGhostsVar.set("4")
        self.layoutVar.set("mediumClassic")
        self.pacmanVar.set("KeyboardAgent")
        
        self.frameTimeVar.set("0.1")
        self.textGraphicsVar.set("False")
        self.quietTextGraphicsVar.set("False")
        
        self.validateData('Fehlerhafte Einstellungen!', 'Einige Standard-Einstellungswerte sind ungueltig: ')
        
    def loadSettingsFromConfigFile(self):
        try:
            Config = ConfigParser.ConfigParser()
            Config.read(CONFIGURATION_FILE)
            
            self.numGamesVar.set(Config.get('GameSettings', 'numGames'))
            self.numGhostsVar.set(Config.get('GameSettings', 'numGhosts'))
            self.layoutVar.set(Config.get('GameSettings', 'layout'))
            self.pacmanVar.set(Config.get('GameSettings', 'pacman'))
            
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
        Config.set('GameSettings', 'numGames', self.numGamesVar.get())
        Config.set('GameSettings', 'numGhosts', self.numGhostsVar.get())
        Config.set('GameSettings', 'layout', self.layoutVar.get())
        Config.set('GameSettings', 'pacman', self.pacmanVar.get())
        
        Config.add_section('DisplaySettings')
        Config.set('DisplaySettings', 'frameTime', self.frameTimeVar.get())
        Config.set('DisplaySettings', 'textGraphics', self.textGraphicsVar.get())
        Config.set('DisplaySettings', 'quietTextGraphics', self.quietTextGraphicsVar.get())
        Config.write(cfgfile)
        
        cfgfile.close()
