# Application name
WINDOW_TITLE = "Pacman Launcher"

# Window layout
WINDOW_ALIGN_TO_LEFT_FACTOR = 2
WINDOW_ALIGN_TO_TOP_FACTOR = 2
WINDOW_BORDER = 20
WINDOW_SPACING = 5
WINDOW_TEXTBOX_WIDTH = 30
WINDOW_LABEL_WIDTH = 20

import Tkinter
import tkFont
from statisticsController import LauncherController
import glob
import re

class LauncherView(Tkinter.Tk):
    def __init__(self,parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()

    # Align the window
    def align(self):
        self.update_idletasks()
        w = self.winfo_screenwidth()
        h = self.winfo_screenheight()
        size = tuple(int(_) for _ in self.geometry().split('+')[0].split('x'))
        x = w/2 - size[0]/2
        y = h/2 - size[1]/2
        x = x * (1.0/WINDOW_ALIGN_TO_LEFT_FACTOR)
        y = y * (1.0/WINDOW_ALIGN_TO_TOP_FACTOR)
        self.geometry("%dx%d+%d+%d" % (size + (x, y)))
        
    # Create label
    def createLabel(self, text, row):
        paddingLeft = WINDOW_BORDER
        paddingTop = WINDOW_BORDER if (row == 0) else 0
        
        labelFont = tkFont.nametofont("TkDefaultFont")
        
        text = text + ":"
        label = Tkinter.Label(self,
            anchor="e", fg="black", text=text, width=WINDOW_LABEL_WIDTH, font=labelFont)
        label.grid(column=0, row=row, sticky='NE',
            padx=(paddingLeft, WINDOW_SPACING), pady=(paddingTop, WINDOW_SPACING))
            
    def createHeader(self, text, row):
        paddingLeft = WINDOW_BORDER
        paddingTop = WINDOW_BORDER if (row == 0) else 0
        
        labelFont = tkFont.nametofont("TkDefaultFont")
        labelFont = labelFont.copy()
        labelFont.config(weight='bold')
        
        text = text + ":"
        label = Tkinter.Label(self,
            anchor="e", fg="black", text=text, width=WINDOW_LABEL_WIDTH, font=labelFont)
        label.grid(column=0, row=row, sticky='NE',
            padx=(paddingLeft, WINDOW_SPACING), pady=(paddingTop, WINDOW_SPACING))
    
    def createSpace(self, row):
        paddingLeft = WINDOW_BORDER
        paddingTop = WINDOW_BORDER if (row == 0) else 0
        
        labelFont = tkFont.nametofont("TkDefaultFont")
        labelFont = labelFont.copy()
        labelFont.config(weight='bold')
        
        text = ""
        label = Tkinter.Label(self,
            anchor="e", fg="black", text=text, width=WINDOW_LABEL_WIDTH, font=labelFont)
        label.grid(column=0, row=row, sticky='NE',
            padx=(paddingLeft, WINDOW_SPACING), pady=(paddingTop, WINDOW_SPACING))
            
    # Create textbox
    # Returns a StringVar to access the input
    def createTextbox(self, row):
        paddingRight = WINDOW_BORDER
        paddingTop = WINDOW_BORDER if (row == 0) else 0
    
        textboxVariable = Tkinter.StringVar()
        textbox = Tkinter.Entry(self,
            textvariable=textboxVariable, width=WINDOW_TEXTBOX_WIDTH)
        textbox.grid(column=1, row=row, sticky='NW',
            padx=(WINDOW_SPACING, paddingRight), pady=(paddingTop, WINDOW_SPACING))
        textboxVariable.set("")
        return textboxVariable
        
    def createDropDown(self, row, values):
        paddingRight = WINDOW_BORDER
        paddingTop = WINDOW_BORDER if (row == 0) else 0
    
        textboxVariable = Tkinter.StringVar()
        textbox = Tkinter.OptionMenu(self,
            textboxVariable, *values)
        textbox.grid(column=1, row=row, sticky="ew",
            padx=(WINDOW_SPACING, paddingRight), pady=(paddingTop, WINDOW_SPACING))
        textboxVariable.set(values[0])
        return textboxVariable
        
    def createCheckBox(self, row):
        paddingRight = WINDOW_BORDER
        paddingTop = WINDOW_BORDER if (row == 0) else 0
    
        textboxVariable = Tkinter.StringVar()
        textbox = Tkinter.Checkbutton(
            self, variable=textboxVariable,
            onvalue="True", offvalue="False"
            )
        textbox.grid(column=1, row=row, sticky='NW',
            padx=(WINDOW_TEXTBOX_WIDTH*3, paddingRight), pady=(paddingTop, WINDOW_SPACING))
        textboxVariable.set("False")
        return textboxVariable
    
    def finishRow(self):
        self.nextRow = self.nextRow + 1
        
    def getLayoutValues(self):
        values = []
        for layout in glob.glob("layouts/*.lay"):
            values.append(layout.replace("layouts", "")[1:].replace(".lay", ""))
        
        return values
        
    def getPacmanValues(self):
        values = []
        files = glob.glob("*Agents.py")
        for filename in files:
            if ("ghost" in filename.lower()):
                continue
            
            with open(filename) as file:
                content = file.readlines()
                for line in content:
                    if (("class" in line) and ("agent" in line.lower())):
                        match = re.search('class (.*?)\(', line)
                        values.append(match.group(1).strip())
                    
        return values
    
    # Initialize the window
    def initialize(self):
        self.nextRow = 0
        self.grid()

        # Labels and textboxes for different attributes
        self.createHeader("Statistikeinstellungen", self.nextRow)
        self.finishRow()
        
        self.createLabel("Max. Anzahl der Trainings", self.nextRow)
        self.numTrainingVar = self.createTextbox(self.nextRow)
        self.finishRow()
        
        self.createLabel("Abstufungen der Trainings", self.nextRow)
        self.incrementVar = self.createTextbox(self.nextRow)
        self.finishRow()
        
        self.createLabel("Anzahl der Wertungsspiele", self.nextRow)
        self.numGamesVar = self.createTextbox(self.nextRow)
        self.finishRow()
        
        self.createLabel("Ausgabedatei", self.nextRow)
        self.outputFilenameVar = self.createTextbox(self.nextRow)
        self.finishRow()
        
        self.createSpace(self.nextRow)
        self.finishRow()
        
        self.createHeader("Spieleinstellungen", self.nextRow)
        self.finishRow()
        
        self.createLabel("Anzahl der Geister", self.nextRow)
        self.numGhostsVar = self.createTextbox(self.nextRow)
        self.finishRow()
        
        self.createLabel("Spielfeld", self.nextRow)
        self.layoutVar = self.createDropDown(self.nextRow, self.getLayoutValues())
        self.finishRow()
        
        self.createLabel("Pacman-Agent", self.nextRow)
        self.pacmanVar = self.createDropDown(self.nextRow, self.getPacmanValues())
        self.finishRow()
        
        self.createLabel("Feste Random-Seed", self.nextRow)
        self.fixRandomSeedVar = self.createCheckBox(self.nextRow)
        self.finishRow()
        
        self.createSpace(self.nextRow)
        self.finishRow()
        
        # Button to apply default settings
        defaultSettingsButton = Tkinter.Button(self,
            text=u"Standard-Einstellungen laden",
            command=self.OnDefaultSettingsButtonClick)
        defaultSettingsButton.grid(column=0, row=self.nextRow, sticky='NE',
            padx=(WINDOW_BORDER, WINDOW_SPACING), pady=(WINDOW_SPACING, WINDOW_SPACING))
        
        saveSettingsButton = Tkinter.Button(self,
            text=u"   Einstellungen speichern   ",
            command=self.OnSaveSettingsButtonClick)
        saveSettingsButton.grid(column=1, row=self.nextRow, sticky='NW',
            padx=(WINDOW_TEXTBOX_WIDTH*0.7, WINDOW_BORDER), pady=(WINDOW_SPACING, WINDOW_SPACING))
        self.finishRow()
        
        loadSettingsButton = Tkinter.Button(self,
            text=u"         Einstellungen laden        ",
            command=self.OnLoadSettingsButtonClick)
        loadSettingsButton.grid(column=0, row=self.nextRow, sticky='NE',
            padx=(WINDOW_BORDER, WINDOW_SPACING), pady=(WINDOW_SPACING, WINDOW_SPACING))
            
        boldFont = tkFont.nametofont("TkDefaultFont")
        boldFont = boldFont.copy()
        boldFont.config(weight='bold')
        
        # Exit button
        exitButton = Tkinter.Button(self,
            text=u" Beenden ",
            command=self.OnExitButtonClick)
        exitButton['font'] = boldFont
        exitButton.grid(column=1, row=self.nextRow, sticky='NW',
            padx=(WINDOW_TEXTBOX_WIDTH*0.7, WINDOW_SPACING), pady=(WINDOW_SPACING, WINDOW_BORDER))
        
        # Start button
        startButton = Tkinter.Button(self,
            text=u" Starten ",
            command=self.OnStartButtonClick)
        startButton['font'] = boldFont
        startButton.grid(column=1, row=self.nextRow, sticky='NE',
            padx=(WINDOW_SPACING, WINDOW_TEXTBOX_WIDTH*1.1), pady=(WINDOW_SPACING, WINDOW_BORDER))
        
        # Disable resizing
        self.resizable(False,False)
        
        # Align the window
        self.align()
        
        # Create controller
        self.launcherController = LauncherController(self)
            
        # Load settings
        self.launcherController.loadSettingsFromConfigFile()

    # Button events
    def OnExitButtonClick(self):
        self.quit()
        
    def OnStartButtonClick(self):
        if (self.launcherController is not None):
            self.launcherController.startApplication()
        
    def OnDefaultSettingsButtonClick(self):
        if (self.launcherController is not None):
            self.launcherController.loadDefaultSettings()
        
    def OnLoadSettingsButtonClick(self):
        if (self.launcherController is not None):
            self.launcherController.loadSettingsFromConfigFile()
        
    def OnSaveSettingsButtonClick(self):
        if (self.launcherController is not None):
            self.launcherController.saveSettingsToConfigFile()

if __name__ == "__main__":
    app = LauncherView(None)
    app.title(WINDOW_TITLE)
    app.mainloop()
