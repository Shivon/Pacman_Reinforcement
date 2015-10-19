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
        self.view = view
        self.numGamesVar = numGamesVar
        self.numGhostsVar = numGhostsVar
        self.pacmanVar = pacmanVar
        
        self.frameTimeVar = frameTimeVar
        self.textGraphicsVar = textGraphicsVar
        self.quietTextGraphicsVar = quietTextGraphicsVar
    
    def getArgumentString(self):
        print "NotImplementedError: LauncherController.getArgumentString()!"
        return ""
    
    def startApplication(self):
        if (not self.validateData('Error! Invalid settings!', 'Some values are not valid: ')):
            return
        
        arguments = self.getArgumentString()
        
        self.view.destroy()
        subprocess.call("pacman.py" + arguments, shell=True)
    
    def getInvalidFields(self):
        print "NotImplementedError: LauncherController.getInvalidFields()!"
        return []
        
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
        Config = ConfigParser.ConfigParser()
        Config.read(CONFIGURATION_FILE)
        
        self.numGamesVar.set(Config.get('GameSettings', 'numGames'))
        self.numGhostsVar.set(Config.get('GameSettings', 'numGhosts'))
        self.pacmanVar.set(Config.get('GameSettings', 'pacman'))
        
        self.frameTimeVar.set(Config.get('DisplaySettings', 'frameTime'))
        self.textGraphicsVar.set(Config.get('DisplaySettings', 'textGraphics'))
        self.quietTextGraphicsVar.set(Config.get('DisplaySettings', 'quietTextGraphics'))
        
        self.validateData('Error! Invalid settings!', 'Some values are not valid: ')
        
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
