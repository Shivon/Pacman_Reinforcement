import ConfigParser
import tkMessageBox
import subprocess
from datatypeUtils import DatatypeUtils
from pacman import startByLauncher
from graphicsDisplay import *

CONFIGURATION_FILE = "settingsRuntime.ini"

class RuntimeSettingsController:
    view = None
    
    def __init__(self, view):
        self.view = view
    
    def apply(self):
        if (not self.validateData('Fehlerhafte Einstellungen!', 'Einige Einstellungswerte sind ungueltig: ')):
            return
        
        self.saveSettingsToConfigFile()
        
        self.view.quit()
        self.view.destroy()
        
        print "TODO: IMPLEMENT APPLYING SETTINGS!"
    
    
    def getInvalidFields(self):        
        invalidFields = []
        
        # Datatype checking
        if (not DatatypeUtils.isIntegerString(self.view.stepsVar.get())):
            invalidFields.append("'Groesse des Ringpuffers' muss eine Ganzzahl sein (zum Beispiel: 1)!")
        if (not DatatypeUtils.isFloatString(self.view.alphaVar.get())):
            invalidFields.append("'Alpha' muss eine Kommazahl sein (zum Beispiel: 1.0)!")
        if (not DatatypeUtils.isFloatString(self.view.gammaVar.get())):
            invalidFields.append("'Gamma' muss eine Kommazahl sein (zum Beispiel: 1.0)!")
        if (not DatatypeUtils.isFloatString(self.view.epsilonVar.get())):
            invalidFields.append("'Epsilon' muss eine Kommazahl sein (zum Beispiel: 1.0)!")
        if (not DatatypeUtils.isFloatString(self.view.lambdaVar.get())):
            invalidFields.append("'Lambda' muss eine Kommazahl sein (zum Beispiel: 1.0)!")
        
        # Value checking
        # TODO!
        
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
        self.view.stepsVar.set("10")
        self.view.alphaVar.set("0.1")
        self.view.gammaVar.set("0.2")
        self.view.epsilonVar.set("0.1")
        self.view.lambdaVar.set("1.0")
        
        self.validateData('Fehlerhafte Einstellungen!', 'Einige Standard-Einstellungswerte sind ungueltig: ')
        
    def loadSettingsFromConfigFile(self):
        try:
            Config = ConfigParser.ConfigParser()
            Config.read(CONFIGURATION_FILE)
            
            self.view.stepsVar.set(Config.get('SarsaLambdaSettings', 'steps'))
            self.view.alphaVar.set(Config.get('SarsaLambdaSettings', 'alpha'))
            self.view.gammaVar.set(Config.get('SarsaLambdaSettings', 'gamma'))
            self.view.epsilonVar.set(Config.get('SarsaLambdaSettings', 'epsilon'))
            self.view.lambdaVar.set(Config.get('SarsaLambdaSettings', 'lambda'))
            
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
        
        Config.add_section('SarsaLambdaSettings')
        Config.set('SarsaLambdaSettings', 'steps', self.view.stepsVar.get())
        Config.set('SarsaLambdaSettings', 'alpha', self.view.alphaVar.get())
        Config.set('SarsaLambdaSettings', 'gamma', self.view.gammaVar.get())
        Config.set('SarsaLambdaSettings', 'epsilon', self.view.epsilonVar.get())
        Config.set('SarsaLambdaSettings', 'lambda', self.view.lambdaVar.get())
        Config.write(cfgfile)
        
        cfgfile.close()
