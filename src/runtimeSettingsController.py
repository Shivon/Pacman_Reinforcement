import ConfigParser
import tkMessageBox
import subprocess
from datatypeUtils import DatatypeUtils
from pacman import startByLauncher
from graphicsDisplay import *

CONFIGURATION_FILE = "settingsRuntime.ini"

class RuntimeSettingsController:
    view = None
    #TODO: ADD ATTRIBUTES
    
    def __init__(self, view): #TODO: ADD ATTRIBUTES
        self.view = view
        #TODO: ADD ATTRIBUTES
    
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
        # TODO: ADD ATTRIBUTES
        
        # Value checking
        # TODO: ADD ATTRIBUTES
        
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
        #TODO: ADD ATTRIBUTES
        
        self.validateData('Fehlerhafte Einstellungen!', 'Einige Standard-Einstellungswerte sind ungueltig: ')
        
    def loadSettingsFromConfigFile(self):
        try:
            Config = ConfigParser.ConfigParser()
            Config.read(CONFIGURATION_FILE)
            
            #TODO: ADD ATTRIBUTES
            
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
        
        Config.add_section('RuntimeSettings')
        #TODO: ADD ATTRIBUTES
        Config.write(cfgfile)
        
        cfgfile.close()
