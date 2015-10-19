import ConfigParser
import tkMessageBox
import subprocess
from datatypeUtils import DatatypeUtils

CONFIGURATION_FILE = "settings.ini"

class LauncherController:
    view = None
    numGamesVar = None
    numGhostsVar = None
    pacmanVar = None
    frameTimeVar = None
    textGraphicsVar = None
    quietTextGraphicsVar = None
    
    def __init__(self, view, numGamesVar, numGhostsVar, pacmanVar, frameTimeVar, textGraphicsVar, quietTextGraphicsVar):
        print DatatypeUtils.isBooleanString("False")
        
        self.view = view
        self.numGamesVar = numGamesVar
        self.numGhostsVar = numGhostsVar
        self.pacmanVar = pacmanVar
        
        self.frameTimeVar = frameTimeVar
        self.textGraphicsVar = textGraphicsVar
        self.quietTextGraphicsVar = quietTextGraphicsVar
    
    def getArgumentString(self):
        argumentValues = []
        
        argumentValues.append("--numGames=" + self.numGamesVar.get())
        argumentValues.append("--numghosts=" + self.numGhostsVar.get())
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
        if (not self.validateData('Error! Invalid settings!', 'Some values are not valid: ')):
            return
        
        arguments = self.getArgumentString()
        
        self.view.destroy()
        subprocess.call("pacman.py " + arguments, shell=True)
    
    def getInvalidFields(self):
        print "NotImplementedError: LauncherController.getInvalidFields()!"
        
        invalidFields = []
        if (not DatatypeUtils.isIntegerString(self.numGamesVar.get())):
            invalidFields.append("numGames is not a Integer!")
        if (not DatatypeUtils.isIntegerString(self.numGhostsVar.get())):
            invalidFields.append("numGhosts is not a Integer!")
        if (not DatatypeUtils.isString(self.pacmanVar.get())):
            invalidFields.append("pacman is not a String!")
            
        if (not DatatypeUtils.isFloatString(self.frameTimeVar.get())):
            invalidFields.append("frameTime is not a Float!")
        if (not DatatypeUtils.isBooleanString(self.textGraphicsVar.get())):
            invalidFields.append("textGraphics is not a Boolean!")
        if (not DatatypeUtils.isBooleanString(self.quietTextGraphicsVar.get())):
            invalidFields.append("quietTextGraphics is not a Boolean!")
        
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
        self.pacmanVar.set("KeyboardAgent")
        
        self.frameTimeVar.set("0.1")
        self.textGraphicsVar.set("False")
        self.quietTextGraphicsVar.set("False")
        
        self.validateData('Error! Invalid settings!', 'Some values are not valid: ')
        
    def loadSettingsFromConfigFile(self):
        try:
            Config = ConfigParser.ConfigParser()
            Config.read(CONFIGURATION_FILE)
            
            self.numGamesVar.set(Config.get('GameSettings', 'numGames'))
            self.numGhostsVar.set(Config.get('GameSettings', 'numGhosts'))
            self.pacmanVar.set(Config.get('GameSettings', 'pacman'))
            
            self.frameTimeVar.set(Config.get('DisplaySettings', 'frameTime'))
            self.textGraphicsVar.set(Config.get('DisplaySettings', 'textGraphics'))
            self.quietTextGraphicsVar.set(Config.get('DisplaySettings', 'quietTextGraphics'))
            
            self.validateData('Error! Invalid settings!', 'Some values are not valid: ')
        except:
            self.handleMissingConfigFile();
        
    def handleMissingConfigFile(self):
        self.loadDefaultSettings()
        self.saveSettingsToConfigFile()
        
    def saveSettingsToConfigFile(self):
        if (not self.validateData('Error! Invalid settings!', 'Some values are not valid: ')):
            return
            
        Config = ConfigParser.ConfigParser()
        cfgfile = open(CONFIGURATION_FILE, 'w')
        
        Config.add_section('GameSettings')
        Config.set('GameSettings', 'numGames', self.numGamesVar.get())
        Config.set('GameSettings', 'numGhosts', self.numGhostsVar.get())
        Config.set('GameSettings', 'pacman', self.pacmanVar.get())
        
        Config.add_section('DisplaySettings')
        Config.set('DisplaySettings', 'frameTime', self.frameTimeVar.get())
        Config.set('DisplaySettings', 'textGraphics', self.textGraphicsVar.get())
        Config.set('DisplaySettings', 'quietTextGraphics', self.quietTextGraphicsVar.get())
        Config.write(cfgfile)
        
        cfgfile.close()
