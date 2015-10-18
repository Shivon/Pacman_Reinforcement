class LauncherController:
    numGamesVar = None
    numGhostsVar = None
    pacmanVar = None
    frameTimeVar = None
    textGraphicsVar = None
    quietTextGraphicsVar = None
    
    def __init__(self, numGamesVar, numGhostsVar, pacmanVar, frameTimeVar, textGraphicsVar, quietTextGraphicsVar):
        self.numGamesVar = numGamesVar
        self.numGhostsVar = numGhostsVar
        self.pacmanVar = pacmanVar
        self.frameTimeVar = frameTimeVar
        self.textGraphicsVar = textGraphicsVar
        self.quietTextGraphicsVar = quietTextGraphicsVar
        
    def startApplication(self):
        print "NotImplementedError: LauncherController.OnStartButtonClick!"
        
    def loadDefaultSettings(self):
        print "NotImplementedError: LauncherController.OnDefaultSettingsButtonClick!"
        
    def loadSettingsFromConfigFile(self):
        print "NotImplementedError: LauncherController.OnLoadSettingsButtonClick!"
        
    def saveSettingsToConfigFile(self):
        print "NotImplementedError: LauncherController.OnSaveSettingsButtonClick!"
