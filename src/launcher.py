# Application name
WINDOW_TITLE = "Pacman Launcher"

# Window layout
WINDOW_ALIGN_TO_LEFT_FACTOR = 2
WINDOW_ALIGN_TO_TOP_FACTOR = 2
WINDOW_BORDER = 20
WINDOW_SPACING = 5
WINDOW_TEXTBOX_WIDTH = 20
WINDOW_LABEL_WIDTH = 20
WINDOW_BUTTON_PADDING_LEFT = 15

import Tkinter
import tkFont

class Launcher(Tkinter.Tk):
    def __init__(self,parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.nextRow = 0
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
            
    # Create textbox
    # Returns a StringVar to access the input
    def createTextbox(self, text, row):
        paddingRight = WINDOW_BORDER
        paddingTop = WINDOW_BORDER if (row == 0) else 0
    
        textboxVariable = Tkinter.StringVar()
        textbox = Tkinter.Entry(self,
            textvariable=textboxVariable, width=WINDOW_TEXTBOX_WIDTH)
        textbox.grid(column=1, row=row, sticky='NW',
            padx=(WINDOW_SPACING, paddingRight), pady=(paddingTop, WINDOW_SPACING))
        textboxVariable.set(text)
        return textboxVariable
    
    def finishRow(self):
        self.nextRow = self.nextRow + 1
    
    # Initialize the window
    def initialize(self):
        self.grid()

        # Labels and textboxes for different attributes
        self.createHeader("Spieleinstellungen", self.nextRow)
        self.finishRow()
        
        self.createLabel("Anzahl der Spiele", self.nextRow)
        self.numGamesVar = self.createTextbox("1", self.nextRow)
        self.finishRow()
        
        self.createLabel("Anzahl der Geister", self.nextRow)
        self.numGhostsVar = self.createTextbox("4", self.nextRow)
        self.finishRow()
        
        self.createLabel("Pacman-Agent", self.nextRow)
        self.pacmanVar = self.createTextbox("KeyboardAgent", self.nextRow)
        self.finishRow()
        
        self.createHeader("Anzeigeeinstellungen", self.nextRow)
        self.finishRow()
        
        self.createLabel("Spielgeschwindigkeit", self.nextRow)
        self.frameTimeVar = self.createTextbox("0.1", self.nextRow)
        self.finishRow()
        
        self.createLabel("Ausgabe als Text", self.nextRow)
        self.textGraphicsVar = self.createTextbox("False", self.nextRow)
        self.finishRow()
        
        self.createLabel("Minimale Ausgabe", self.nextRow)
        self.quietTextGraphicsVar = self.createTextbox("False", self.nextRow)
        self.finishRow()
        
        # Exit button
        exitButton = Tkinter.Button(self,
            text=u"Beenden",
            command=self.OnExitButtonClick)
        exitButton.grid(column=1, row=self.nextRow, sticky='NW',
            padx=(WINDOW_BUTTON_PADDING_LEFT, 0), pady=(WINDOW_SPACING, WINDOW_BORDER))
        
        # Start button
        startButton = Tkinter.Button(self,
            text=u"Starten",
            command=self.OnStartButtonClick)
        startButton.grid(column=1, row=self.nextRow, sticky='NE',
            padx=(0, WINDOW_BORDER), pady=(WINDOW_SPACING, WINDOW_BORDER))

        # Disable resizing
        self.resizable(False,False)
        
        # Align the window
        self.align()

    # Button events
    def OnExitButtonClick(self):
        self.quit()
        
    def OnStartButtonClick(self):
        print "NotImplementedError!"

if __name__ == "__main__":
    app = Launcher(None)
    app.title(WINDOW_TITLE)
    app.mainloop()
