import tkinter as tk
from tkinter import ttk, filedialog
import customtkinter as ctk
from customtkinter import CTkImage
from PIL import Image
import time
import json

class App(tk.Tk):

    checkboxStyling = {
    'width':5,
    'height':10,
    'fg_color':'white',
    'text_color':'black',
    'font':('Excalifont',20),
    'border_color':'black',
    'hover_color':'black'
    }

    def __init__(self):
        super().__init__()
        self.title('Safe Way Out')
        self.geometry('1280x720')
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.configure(bg='white')
        self.iconbitmap('assets/fire.ico')
        self.menu = Menu(self)
        self.homePage = homePage(self)
        self.inputDataPage = inputDataPage(self)
        self.optimisePlanPage = optimisePlanPage(self)
        self.resizable(False,False)
        self.matrix = [[1] * 120 for _ in range(80)]

        self.dataAdded = ctk.BooleanVar(value=False)
    
    def showPage(self, page):
        print(f"Attempting to show: {page.__class__.__name__}")
        self.homePage.grid_forget()
        self.inputDataPage.grid_forget()
        self.optimisePlanPage.grid_forget()
        page.grid(row=0, column=1, sticky='nsew')

class Menu(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)
        self.configure(corner_radius=15, border_color='black', border_width=5, bg_color='white', fg_color='white')
        self.homeDark = CTkImage(light_image=Image.open('assets/homeDark.png'))
        self.homeLight = CTkImage(light_image=Image.open('assets/homeLight.png'))
        self.createMenuWidgets()
        self.placeMenuWidgets()
        self.grid(row=0, column=0, sticky='nsew', padx=(10,5), pady=10)
    
    def createMenuWidgets(self):

        menuButtonStyling = {
        'border_width':2,
        'border_color':'black',
        'text_color':'black',
        'font':('Excalifont',20),
        'fg_color':'white',
        'corner_radius':10
        }

        self.title = ctk.CTkLabel(self, text='Safe Way Out', fg_color='white', text_color='black', font=('Excalifont', 20))
        self.homeButton = ctk.CTkButton(self, text='   Home', image=self.homeDark, anchor='w', **menuButtonStyling, command=self.openHomePage)
        self.inputDataButton = ctk.CTkButton(self, text='Input Data', **menuButtonStyling, command=self.openInputDataPage)
        self.optimisePlanButton = ctk.CTkButton(self, text='Optimise Plan', **menuButtonStyling, command=self.openOptimisePlanPage)
    
    def placeMenuWidgets(self):
        self.title.pack(pady=20, padx=30)
        self.homeButton.pack(fill='x', padx=10, pady=5)
        self.homeButton.bind('<Enter>', lambda event: self.homeButton.configure(text_color='white', fg_color='black', image=self.homeLight))
        self.homeButton.bind('<Leave>', lambda event: self.homeButton.configure(text_color='black', fg_color='white', image=self.homeDark))
        self.placeMenuButton(self.inputDataButton)
        self.placeMenuButton(self.optimisePlanButton)

    def placeMenuButton(self, button):
        button.pack(fill='x', padx=10, pady=5)
        button.bind('<Enter>', lambda event: button.configure(text_color='white', fg_color='black'))
        button.bind('<Leave>', lambda event: button.configure(text_color='black', fg_color='white'))
    
    def openHomePage(self):
        self.master.showPage(self.master.homePage)
        self.after(100, lambda: self.homeButton.configure(text_color='black', fg_color='white', image=self.homeDark))
        if self.master.dataAdded.get() == True:
            self.master.homePage.mapCanvas.delete(self.master.homePage.noDataText)
            self.master.homePage.mapCanvas.display()

    def openInputDataPage(self):
        self.master.showPage(self.master.inputDataPage)
        self.after(100, lambda: self.inputDataButton.configure(text_color='black', fg_color='white'))

    def openOptimisePlanPage(self):
        self.master.showPage(self.master.optimisePlanPage)
        self.after(100, lambda: self.optimisePlanButton.configure(text_color='black', fg_color='white'))

class homePage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(bg_color='white', fg_color='white')
        self.rowconfigure(0, weight=4)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.createWidgets()
        self.placeHomePageWidgets()

    def createWidgets(self):

        checkboxStyling = {
            'width':5,
            'height':10,
            'fg_color':'white',
            'text_color':'black',
            'font':('Excalifont',20),
            'border_color':'black',
            'hover_color':'black'
        }

        self.upperContentFrame = ctk.CTkFrame(self, bg_color='white', fg_color='white')
        self.upperContentFrame.columnconfigure(0, weight=5)
        self.upperContentFrame.columnconfigure(1, weight=2)
        self.upperContentFrame.rowconfigure(0, weight=1)
        self.lowerContentFrame = ctk.CTkFrame(self, corner_radius=15, border_color='black', border_width=5, bg_color='white', fg_color='white')
        self.warningLabel = ctk.CTkLabel(self.lowerContentFrame, text='Warning!', fg_color='white', text_color='black', font=('Excalifont', 25) )
        self.warningTable = ttk.Treeview(self.lowerContentFrame, columns=('Index','Type', 'Extra Information'), show='headings')
        self.warningTable.heading('Index', text='Index')
        self.warningTable.heading('Type', text='Type')
        self.warningTable.heading('Extra Information', text='Extra Information')
        self.mapContainer = ctk.CTkFrame(self.upperContentFrame, corner_radius=15, border_color='black', border_width=5, bg_color='white', fg_color='white')
        self.mapCanvas = Canvas(parent=self.mapContainer, width=600, height=400)
        self.noDataText = self.mapCanvas.create_text(300,200, text='No Data', font=('Excalifont',20))
        self.toDoContainer = ctk.CTkFrame(self.upperContentFrame, corner_radius=15, border_color='black', border_width=5, bg_color='white', fg_color='white')
        self.toDoLabel = ctk.CTkLabel(self.toDoContainer, text='To Do:', fg_color='white', text_color='black', font=('Excalifont', 25) )
        self.sitePlanCheckBox = ctk.CTkCheckBox(self.toDoContainer, text=' Insert Site Plan', **checkboxStyling)
        self.placeNodesCheckBox = ctk.CTkCheckBox(self.toDoContainer, text=' Place Nodes', **checkboxStyling)
        self.optimiseCheckBox = ctk.CTkCheckBox(self.toDoContainer, text=' Optimise', **checkboxStyling)
        self.analyseCheckBox = ctk.CTkCheckBox(self.toDoContainer, text=' Analyse Bottlenecks', **checkboxStyling)
        self.capacityDataCheckBox = ctk.CTkCheckBox(self.toDoContainer, text=' Import Capacity Data', **checkboxStyling)
        self.simulateCheckBox = ctk.CTkCheckBox(self.toDoContainer, text=' Simulate Event', **checkboxStyling)

    def placeHomePageWidgets(self):
        self.warningLabel.pack(pady=10)
        self.warningTable.pack(fill='both', expand=True, padx=10, pady=(0,10))
        self.mapCanvas.pack(fill='both', expand=True, padx=10, pady=10)
        self.toDoLabel.pack(pady=20)
        self.sitePlanCheckBox.pack(fill='x', padx=30, pady=10)
        self.placeNodesCheckBox.pack(fill='x', padx=30, pady=10)
        self.optimiseCheckBox.pack(fill='x', padx=30, pady=10)
        self.analyseCheckBox.pack(fill='x', padx=30, pady=10)
        self.capacityDataCheckBox.pack(fill='x', padx=30, pady=10)
        self.simulateCheckBox.pack(fill='x', padx=30, pady=10)
        self.mapContainer.grid(row=0, column=0, sticky='nsew', padx=(10, 5), pady=10)
        self.toDoContainer.grid(row=0, column=1, sticky='nsew', padx=(5, 10), pady=10)
        self.upperContentFrame.grid(row=0, column=0, sticky='nsew')
        self.lowerContentFrame.grid(row=1, column=0, sticky='nsew', padx=10, pady=(5, 10))
        self.grid(row=0, column=1, sticky='nsew')

class dataPoint():
    def __init__(self, x, y, prevColour, colour, dragIndex):
       self.x = x
       self.y = y
       self.prevColour = prevColour
       self.colour = colour
       self.dragIndex = dragIndex

class inputDataPage(ctk.CTkFrame):
    def __init__(self,parent):
        super().__init__(parent)
        self.nextColorValue = 2
        self.currentTool = 0
        self.previousActions = []
        self.redoActions = []
        self.dragIndex = -1
        self.previousActions.append(dataPoint(-1,-1,-1,-1,-1))
        self.redoActions.append(dataPoint(-1,-1,-1,-1,-1))
        self.upload = CTkImage(light_image=Image.open('assets/upload.png'))
        self.brush = CTkImage(light_image=Image.open('assets/brush(64).png'), size=(64,64))
        self.blackPencil = CTkImage(light_image=Image.open('assets/blackPencil.png'), size=(16,16))
        self.blackEraser = CTkImage(light_image=Image.open('assets/blackEraser.png'), size=(16,16))
        self.blackLine = CTkImage(light_image=Image.open('assets/blackLine.png'), size=(16,16))
        self.blackBullseye = CTkImage(light_image=Image.open('assets/blackBullseye.png'), size=(16,16))
        self.blackUndo = CTkImage(light_image=Image.open('assets/blackUndo.png'), size=(16,16))
        self.blackRedo = CTkImage(light_image=Image.open('assets/blackRedo.png'), size=(16,16))
        self.whitePencil = CTkImage(light_image=Image.open('assets/whitePencil.png'), size=(16,16))
        self.whiteEraser = CTkImage(light_image=Image.open('assets/whiteEraser.png'), size=(16,16))
        self.whiteLine = CTkImage(light_image=Image.open('assets/whiteLine.png'), size=(16,16))
        self.whiteBullseye = CTkImage(light_image=Image.open('assets/whiteBullseye.png'), size=(16,16))
        self.whiteUndo = CTkImage(light_image=Image.open('assets/whiteUndo.png'), size=(16,16))
        self.whiteRedo = CTkImage(light_image=Image.open('assets/whiteRedo.png'), size=(16,16))
        self.configure(bg_color='white', fg_color='white')
        self.createWidgets()
        self.placeWidgets()
        self.handlePencilButtonClick()
    
    def createWidgets(self):
        ButtonStyling = {
        'border_width':2,
        'border_color':'black',
        'text_color':'black',
        'font':('Excalifont',20),
        'fg_color':'white',
        'corner_radius':10
        }

        self.upperFrame = ctk.CTkFrame(self, bg_color='white', fg_color='white')
        self.toolContainer = ctk.CTkFrame(self.upperFrame, bg_color='white', fg_color='white')
        self.toolContainer.rowconfigure((0,1,2,3,4,5), weight=1)
        self.toolContainer.rowconfigure(6, weight=3)
        self.toolContainer.rowconfigure((7,8), weight=1)
        self.toolContainer.columnconfigure((0,1), weight=1)
        self.brushLabel = ctk.CTkLabel(self.toolContainer, image=self.brush, text='')
        self.pencilButton = ctk.CTkButton(self.toolContainer, image=self.blackPencil, text='', **ButtonStyling, command=lambda: self.after(100, self.handlePencilButtonClick))
        self.eraserButton = ctk.CTkButton(self.toolContainer, image=self.blackEraser, text='', **ButtonStyling, command=lambda: self.after(100, self.handleEraserButtonClick))
        self.lineButton = ctk.CTkButton(self.toolContainer, image=self.blackLine, text='', **ButtonStyling, command=lambda: self.after(100, self.handleLineButtonClick))
        self.bullseyeButton = ctk.CTkButton(self.toolContainer, image=self.blackBullseye, text='', **ButtonStyling, command=lambda: self.after(100, self.handleBullseyeButtonClick))
        self.undoButton = ctk.CTkButton(self.toolContainer, image=self.blackUndo, text='', **ButtonStyling, command=lambda: self.after(100, self.handleUndoButtonClick))
        self.redoButton = ctk.CTkButton(self.toolContainer, image=self.blackRedo, text='', **ButtonStyling, command=lambda: self.after(100, self.handleRedoButtonClick))
        self.clearCanvasButton = ctk.CTkButton(self.toolContainer, text='Clear', **ButtonStyling, command=lambda: self.after(100, self.handleClearButtonClick))
        self.doneButton = ctk.CTkButton(self.toolContainer, text='Done', **ButtonStyling, command=lambda: self.after(100, self.handleDoneButtonClick))
        self.saveButton = ctk.CTkButton(self.toolContainer,text='Save', **ButtonStyling, command=lambda: self.after(100, self.handleSaveButtonClick))
        self.padder = ctk.CTkFrame(self.toolContainer, bg_color='white', fg_color='white')
        self.mapContainer = ctk.CTkFrame(self.upperFrame, corner_radius=15, border_color='black', border_width=5, bg_color='white', fg_color='white')
        self.mapCanvas = Canvas(parent=self.mapContainer, width=960, height=640)
        self.mapCanvas.bind('<Button>', lambda event: self.handleDrawing(event=event, drag=False))
        self.mapCanvas.bind('<B1-Motion>', lambda event: self.handleDrawing(event=event, drag=True))
        self.openFile = ctk.CTkButton(self, text='Open a file', font=('Excalifont',20), text_color='black', fg_color='white', hover_color='white', command=self.handleOpenFileButtonClick, image=self.upload)
        self.pencilButton.bind('<Enter>', lambda event: self.pencilButton.configure(text_color='white', fg_color='black', image=self.whitePencil))
        self.pencilButton.bind('<Leave>', lambda event: self.pencilButton.configure(text_color='black', fg_color='white', image=self.blackPencil))
        self.eraserButton.bind('<Enter>', lambda event: self.eraserButton.configure(text_color='white', fg_color='black', image=self.whiteEraser))
        self.eraserButton.bind('<Leave>', lambda event: self.eraserButton.configure(text_color='black', fg_color='white', image=self.blackEraser))
        self.lineButton.bind('<Enter>', lambda event: self.lineButton.configure(text_color='white', fg_color='black', image=self.whiteLine))
        self.lineButton.bind('<Leave>', lambda event: self.lineButton.configure(text_color='black', fg_color='white', image=self.blackLine))
        self.bullseyeButton.bind('<Enter>', lambda event: self.bullseyeButton.configure(text_color='white', fg_color='black', image=self.whiteBullseye))
        self.bullseyeButton.bind('<Leave>', lambda event: self.bullseyeButton.configure(text_color='black', fg_color='white', image=self.blackBullseye))
        self.undoButton.bind('<Enter>', lambda event: self.undoButton.configure(text_color='white', fg_color='black', image=self.whiteUndo))
        self.undoButton.bind('<Leave>', lambda event: self.undoButton.configure(text_color='black', fg_color='white', image=self.blackUndo))
        self.redoButton.bind('<Enter>', lambda event: self.redoButton.configure(text_color='white', fg_color='black', image=self.whiteRedo))
        self.redoButton.bind('<Leave>', lambda event: self.redoButton.configure(text_color='black', fg_color='white', image=self.blackRedo))
        self.configureTextButtons(self.clearCanvasButton)
        self.configureTextButtons(self.doneButton)
        self.configureTextButtons(self.saveButton)
        self.overwriteWarning = overwriteWarning(self)

    def handleDrawing(self, event, drag):
        x = event.x // self.mapCanvas.pixelSize
        y = event.y // self.mapCanvas.pixelSize
        if x != self.previousActions[-1].x or y != self.previousActions[-1].y or self.currentTool != self.previousActions[-1].colour:
            if drag != True:
                self.dragIndex += 1
            print(f'dragIndex:{self.dragIndex}')
            self.previousActions.append(dataPoint(x, y, self.mapCanvas.matrix[y][x], self.currentTool, self.dragIndex))
            if self.mapCanvas.matrix[y][x] > 2:
                self.nextColorValue -= 1
            self.mapCanvas.creation(x=x, y=y, colourValue=self.currentTool)

    def configureTextButtons(self, button):
        button.bind('<Enter>', lambda event: button.configure(text_color='white', fg_color='black'))
        button.bind('<Leave>', lambda event: button.configure(text_color='black', fg_color='white'))
    
    def deselectCurrentButton(self):
        self.pencilButton.configure(border_width=2)
        self.eraserButton.configure(border_width=2)
        self.lineButton.configure(border_width=2)
        self.bullseyeButton.configure(border_width=2)
        self.pencilButton.grid_configure(pady=4)
        self.eraserButton.grid_configure(pady=4)
        self.lineButton.grid_configure(pady=4)
        self.bullseyeButton.grid_configure(pady=4)

    def handlePencilButtonClick(self):
        self.deselectCurrentButton()
        self.pencilButton.configure(text_color='black', fg_color='white', image=self.blackPencil, border_width=4)
        self.pencilButton.grid_configure(pady=2)
        self.currentTool = 0

    def handleEraserButtonClick(self):
        self.deselectCurrentButton()
        self.eraserButton.configure(text_color='white', fg_color='black', image=self.blackEraser, border_width=4)
        self.eraserButton.grid_configure(pady=2)
        self.currentTool = 1

    def handleLineButtonClick(self):
        self.deselectCurrentButton()
        self.lineButton.configure(text_color='white', fg_color='black', image=self.blackLine, border_width=4)
        self.lineButton.grid_configure(pady=2)
        for action in self.redoActions:
            print(f'x: {action.x}, y: {action.y}, prevColour: {action.prevColour}, dragIndex:{action.dragIndex}')

    def handleBullseyeButtonClick(self):
        self.deselectCurrentButton()
        self.bullseyeButton.configure(text_color='white', fg_color='black', image=self.blackBullseye, border_width=4)
        self.bullseyeButton.grid_configure(pady=2)
        self.currentTool = self.nextColorValue
        if self.nextColorValue < 7:
            self.nextColorValue += 1


    def handleUndoButtonClick(self):
        self.deselectCurrentButton()
        self.undoButton.configure(text_color='white', fg_color='black', image=self.blackUndo)
        while self.previousActions:
            previousAction = self.previousActions.pop()
            x = previousAction.x
            y = previousAction.y
            colourValue = previousAction.prevColour
            dragIndex = previousAction.dragIndex + 1
            self.redoActions.append(dataPoint(x, y, self.mapCanvas.matrix[y][x], colourValue, dragIndex))
            self.mapCanvas.creation(x=x, y=y,colourValue=colourValue)
            if not self.previousActions or self.previousActions[-1].dragIndex != previousAction.dragIndex:
                break

    def handleRedoButtonClick(self):
        self.deselectCurrentButton()
        self.redoButton.configure(text_color='white', fg_color='black', image=self.blackRedo)
        while self.redoActions:
            redoAction = self.redoActions.pop()
            x = redoAction.x
            y = redoAction.y
            colourValue = redoAction.prevColour
            if colourValue > 1:
                self.nextColorValue += 1
            dragIndex = redoAction.dragIndex + 1
            self.previousActions.append(dataPoint(x, y, self.mapCanvas.matrix[y][x], colourValue, dragIndex))
            self.mapCanvas.creation(x=x, y=y,colourValue=colourValue)
            if not self.redoActions or self.redoActions[-1].dragIndex != redoAction.dragIndex:
                break

    def handleClearButtonClick(self):
        self.deselectCurrentButton()
        self.clearCanvasButton.configure(text_color='white', fg_color='black')
        self.mapCanvas.delete('all')
        for i in range(len(self.mapCanvas.matrix)):
            for j in range(len(self.mapCanvas.matrix[i])):
                self.mapCanvas.matrix[i][j] = 1

    def handleDoneButtonClick(self):
        self.deselectCurrentButton()
        self.doneButton.configure(text_color='white', fg_color='black')
        self.master.dataAdded.set(True)
        self.master.matrix = [row[:] for row in self.mapCanvas.matrix]

    def handleSaveButtonClick(self):
        self.deselectCurrentButton()
        self.saveButton.configure(text_color='white', fg_color='black')
        filePath = filedialog.asksaveasfilename()
        filePath += '.json'
        self.master.matrix = [row[:] for row in self.mapCanvas.matrix]
        with open(filePath, 'w') as file:
            json.dump(self.mapCanvas.matrix, file, indent=None)

    def handleOpenFileButtonClick(self):
        self.filePath = filedialog.askopenfilename(initialdir='/temp', title='Choose File', filetypes=[('json Files', '*.json')])
        if self.master.dataAdded.get() == True:
            self.overwriteWarning.place(x = 300, y = 250)
        else:
            self.readFile()

    def readFile(self):
        with open(self.filePath, 'r') as file:
            self.mapCanvas.matrix = json.load(file)
            self.master.dataAdded.set(True)
            self.master.matrix = [row[:] for row in self.mapCanvas.matrix]
            self.mapCanvas.display()

    def placeWidgets(self):
        self.mapContainer.pack(pady=(10,0), side='left')
        self.toolContainer.pack(side='left', fill='both', expand=True, pady=(10,0))
        self.brushLabel.grid(row=0, column=0, rowspan=2, columnspan=2, sticky='new', pady=(5,0))
        self.pencilButton.grid(row=2, column=0, sticky='nsew', padx=2, pady=4)
        self.eraserButton.grid(row=2, column=1, sticky='nsew', padx=2, pady=4)
        self.lineButton.grid(row=3, column=0, sticky='nsew', padx=2, pady=4)
        self.bullseyeButton.grid(row=3, column=1, sticky='nsew', padx=2, pady=4)
        self.undoButton.grid(row=4, column=0, sticky='nsew', padx=2, pady=4)
        self.redoButton.grid(row=4, column=1, sticky='nsew', padx=2, pady=4)
        self.clearCanvasButton.grid(row=5, column=0, sticky='nsew', columnspan=2, padx=2, pady=4)
        self.padder.grid(row=6, column=0, columnspan=2, sticky='nsew')
        self.doneButton.grid(row=7, column=0, sticky='nsew', columnspan=2, padx=2, pady=4)
        self.saveButton.grid(row=8, column=0, sticky='nsew', columnspan=2, padx=2, pady=4)
        self.mapCanvas.pack(pady=10, padx=10)
        self.upperFrame.pack(fill='both', expand=True)
        self.openFile.pack(fill='y', expand=True, pady=(0,10))

class optimisePlanPage(ctk.CTkFrame):
    def __init__(self,parent):
        super().__init__(parent)
        self.configure(bg_color='white', fg_color='white')
        self.createWidgets()
        self.setButtonImages()
        self.placeWidgets()
    
    def createWidgets(self):
        ButtonStyling = {
        'border_width':2,
        'border_color':'black',
        'text_color':'black',
        'font':('Excalifont',20),
        'fg_color':'white',
        'corner_radius':10
        }
        self.startOrEndNode = ""
        self.evacPoint = -1
        self.startNode = -1
        self.fire = CTkImage(light_image=Image.open('assets/fire.png'))
        self.red = CTkImage(light_image=Image.open('assets/red.png'))
        self.blue = CTkImage(light_image=Image.open('assets/blue.png'))
        self.green = CTkImage(light_image=Image.open('assets/green.png'))
        self.orange = CTkImage(light_image=Image.open('assets/orange.png'))
        self.pink = CTkImage(light_image=Image.open('assets/pink.png'))
        self.yellow = CTkImage(light_image=Image.open('assets/yellow.png'))
        self.upperFrame = ctk.CTkFrame(self, bg_color='white', fg_color='white')
        self.rightFrame = ctk.CTkFrame(self.upperFrame, bg_color='white', fg_color='white')
        self.rightFrame.columnconfigure(0, weight=1)
        self.rightFrame.rowconfigure((0,1), weight=1)
        self.rightFrame.rowconfigure(2, weight=3)
        self.rightFrame.rowconfigure((3,4,5), weight=1)
        self.padder = ctk.CTkFrame(self.rightFrame, bg_color='white', fg_color='white')
        self.evacPointLabel = ctk.CTkLabel(self.rightFrame, text='Evac\nPoint', font=('Excalifont',20), text_color='black')
        self.evacPointButton = ctk.CTkButton(self.rightFrame, text='', **ButtonStyling, command=lambda:self.after(100, self.handleEvacPointClick))
        self.chooseNodeLabel = ctk.CTkLabel(self.rightFrame, text='Choose\nNode', font=('Excalifont',20), text_color='black')
        self.chooseNodeButton = ctk.CTkButton(self.rightFrame, text='', **ButtonStyling, command=lambda:self.after(100, self.handleChooseNodeClick))
        self.runButton = ctk.CTkButton(self.rightFrame, text='Run', **ButtonStyling)
        self.scrollFrame = ctk.CTkScrollableFrame(self.rightFrame, bg_color='white', fg_color='white')
        self.canvasContainer = ctk.CTkFrame(self.upperFrame, corner_radius=15, border_color='black', border_width=5, bg_color='white', fg_color='white')
        self.canvas = Canvas(parent=self.canvasContainer, width=960, height=640)
        self.showAllPaths = ctk.CTkButton(self, text='Show all Paths', **ButtonStyling, command=lambda: self.after(100, self.handleShowAllPathsClick))
        self.showAllPaths.bind('<Enter>', lambda event: self.showAllPaths.configure(text_color='white', fg_color='black'))
        self.showAllPaths.bind('<Leave>', lambda event: self.showAllPaths.configure(text_color='black', fg_color='white'))

        ButtonConfig = {
        'master':self.scrollFrame,
        'border_width':2,
        'border_color':'black',
        'text_color':'black',
        'font':('Excalifont',20),
        'fg_color':'white',
        'corner_radius':10,
        'text':''
        }

        
        self.redButton = ctk.CTkButton(**ButtonConfig, image=self.red, command=lambda: self.after(100, self.handleNodeChoiceButtonClick(self.redButton)))
        self.blueButton = ctk.CTkButton(**ButtonConfig, image=self.blue, command=lambda: self.after(100, self.handleNodeChoiceButtonClick(self.blueButton)))
        self.greenButton = ctk.CTkButton(**ButtonConfig, image=self.green, command=lambda: self.after(100, self.handleNodeChoiceButtonClick(self.greenButton)))
        self.orangeButton = ctk.CTkButton(**ButtonConfig, image=self.orange, command=lambda: self.after(100, self.handleNodeChoiceButtonClick(self.orangeButton)))
        self.pinkButton = ctk.CTkButton(**ButtonConfig, image=self.pink, command=lambda: self.after(100, self.handleNodeChoiceButtonClick(self.pinkButton)))
        self.yellowButton = ctk.CTkButton(**ButtonConfig, image=self.yellow, command=lambda: self.after(100, self.handleNodeChoiceButtonClick(self.yellowButton)))
    
        self.Buttons={self.redButton:2, self.blueButton:3, self.greenButton:4, self.orangeButton:5, self.pinkButton:6, self.yellowButton:7}
        
        for button, value in self.Buttons.items():
            button.bind('<Enter>', lambda event, b=button: self.buttonEnter(b))
            button.bind('<Leave>', lambda event, b=button: self.buttonLeave(b))

    def setButtonImages(self):
        match self.evacPoint:
            case -1:
                self.evacPointButton.configure(image=self.fire)
            case 2:
                self.evacPointButton.configure(image=self.red)
            case 3:
                self.evacPointButton.configure(image=self.blue)
            case 4:
                self.evacPointButton.configure(image=self.green)
            case 5:
                self.evacPointButton.configure(image=self.orange)
            case 6:
                self.evacPointButton.configure(image=self.pink)
            case 7:
                self.evacPointButton.configure(image=self.yellow)


        match self.startNode:
            case -1:
                self.chooseNodeButton.configure(image=self.fire)
            case 2:
                self.chooseNodeButton.configure(image=self.red)
            case 3:
                self.chooseNodeButton.configure(image=self.blue)
            case 4:
                self.chooseNodeButton.configure(image=self.green)
            case 5:
                self.chooseNodeButton.configure(image=self.orange)
            case 6:
                self.chooseNodeButton.configure(image=self.pink)
            case 7:
                self.chooseNodeButton.configure(image=self.yellow)
    
    def resetButtons(self):
        for button, value in self.Buttons.items():
            button.configure(state='enabled', fg_color='white')

    def handleNodeChoiceButtonClick(self,button):
        self.resetButtons()
        grey = "#AAAFB4"
        button.configure(state='disabled', fg_color=grey)
        if self.startOrEndNode == "start":
            self.startNode = self.Buttons[button]
        else:
            self.evacPoint = self.Buttons[button]
        self.setButtonImages()
        self.scrollFrame.grid_forget()

    def buttonEnter(self,button):
        button.configure(border_width=4)
        button.pack_configure(pady=0)

    def buttonLeave(self,button):
        button.configure(border_width=2)
        button.pack_configure(pady=2)
    
    def placeWidgets(self):
        self.canvasContainer.pack(pady=(10,0), side='left')
        self.rightFrame.pack(side='left', fill='both', expand=True, pady=(10,0))
        self.canvas.pack(pady=10, padx=10)
        self.upperFrame.pack(fill='both', expand=True)
        self.showAllPaths.pack(fill='y', expand=True, pady=5, ipadx=75)
        self.padder.grid(column=0, row=2, sticky='nsew')
        self.evacPointLabel.grid(column=0, row=0, sticky='nsew', padx=5)
        self.evacPointButton.grid(column=0, row=1, sticky='nsew', padx=5)
        self.chooseNodeLabel.grid(column=0, row=3, sticky='nsew', padx=5)
        self.chooseNodeButton.grid(column=0, row=4, sticky='nsew', padx=5)
        self.runButton.grid(column=0, row=5, sticky='nsew', padx=5, pady=(5,0))

    def handleEvacPointClick(self):
        self.startOrEndNode = "end"
        self.nodeChooser()

    def handleChooseNodeClick(self):
        self.startOrEndNode = "start"
        self.nodeChooser()

    def nodeChooser(self):
        self.scrollFrame.grid(column=0, row=2, sticky='nsew')

        self.redButton.pack(pady=2)
        self.blueButton.pack(pady=2)
        self.greenButton.pack(pady=2)
        self.orangeButton.pack(pady=2)
        self.pinkButton.pack(pady=2)
        self.yellowButton.pack(pady=2)

    def handleShowAllPathsClick(self):
        self.showAllPaths.configure(text_color='white', fg_color='black')

class Canvas(ctk.CTkCanvas):
    def __init__(self, parent, height, width):
        super().__init__(parent)
        self.configure(height=height, width=width, bd=0, background='white', highlightthickness=0)
        self.pixelSize = height // 80
        self.matrix = [[1] * 120 for _ in range(80)]
        
        
    def creation(self, x, y, colourValue):
        
        match colourValue:
            case 0:
                colour = 'black'
            case 1:
                colour = 'white'
            case 2:
                colour = 'red'

        self.master.master.master.master.dataAdded.set(True)
        print(f'drawing at x:{x}, y:{y}, colour={colour}, colourValue={colourValue}')
        self.create_rectangle((self.pixelSize * (x+1) - self.pixelSize, self.pixelSize * (y+1) - self.pixelSize, self.pixelSize * (x+1), self.pixelSize * (y+1)), fill=colour, outline=colour)
        self.matrix[y][x] = colourValue

    def display(self):
        self.delete('all')
        for y in range(80):
            for x in range(120):
                if app.matrix[y][x] == 0:
                    self.create_rectangle((self.pixelSize * (x+1) - self.pixelSize, self.pixelSize * (y+1) - self.pixelSize, self.pixelSize * (x+1), self.pixelSize * (y+1)), fill='black')

class overwriteWarning(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(height=200, width=400, corner_radius=15, border_color='black', border_width=5, bg_color='white', fg_color='white')
        self.createWidgets()
        self.placeWidgets()

    def createWidgets(self):
        warnButtonStyling = {
        'border_width':2,
        'border_color':'black',
        'text_color':'black',
        'font':('Excalifont',20),
        'fg_color':'white',
        'corner_radius':10
        }
        self.warningLabel = ctk.CTkLabel(self, text='Are you sure you want to overwrite the data', text_color='black', font=('Excalifont',20))
        self.confirmButton = ctk.CTkButton(self, text='Confirm', **warnButtonStyling, command=lambda: self.after(100, self.handleconfirmButtonClick))
        self.cancelButton = ctk.CTkButton(self, text='Cancel', **warnButtonStyling, command=lambda: self.after(100, self.handlecancelButtonClick))
        self.confirmButton.bind('<Enter>', lambda event: self.confirmButton.configure(text_color='white', fg_color='black'))
        self.confirmButton.bind('<Leave>', lambda event: self.confirmButton.configure(text_color='black', fg_color='white'))
        self.cancelButton.bind('<Enter>', lambda event: self.cancelButton.configure(text_color='white', fg_color='black'))
        self.cancelButton.bind('<Leave>', lambda event: self.cancelButton.configure(text_color='black', fg_color='white'))
        

    def placeWidgets(self):
        self.warningLabel.pack(padx=10, pady=(10,0))
        self.confirmButton.pack(side='left', padx=(90,10), pady=10)
        self.cancelButton.pack(side='left', padx=10, pady=10)

    def handleconfirmButtonClick(self):
        self.confirmButton.configure(text_color='black', fg_color='white')
        self.master.readFile()
        self.place_forget()

    def handlecancelButtonClick(self):
        self.cancelButton.configure(text_color='black', fg_color='white')
        self.place_forget()

 
if __name__ == '__main__':
    app = App()
    app.mainloop()