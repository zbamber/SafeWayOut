import tkinter as tk
from tkinter import ttk, filedialog
import customtkinter as ctk
from customtkinter import CTkImage
from PIL import Image
import time
import json
from queue import PriorityQueue
import copy
import math

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
        self.matrix = [[{'base': 1} for _ in range(120)] for _ in range(80)]
        self.nodePositions = {2:(-1,-1), 3:(-1,-1), 4:(-1,-1), 5:(-1,-1), 6:(-1,-1), 7:(-1,-1)}
        self.capacityValues={2:-1,3:-1,4:-1,5:-1,6:-1,7:-1}
        self.dataAdded = ctk.BooleanVar(value=False)
        self.simulationRan = False
    
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
        self.master.homePage.update()

    def openInputDataPage(self):
        self.master.showPage(self.master.inputDataPage)
        self.after(100, lambda: self.inputDataButton.configure(text_color='black', fg_color='white'))

    def openOptimisePlanPage(self):
        self.master.showPage(self.master.optimisePlanPage)
        self.master.optimisePlanPage.canvas.display()
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
        self.noData = False

    def update(self):
        self.mapCanvas.delete('all')
        if self.master.dataAdded.get() == True:
            self.noData = False
            self.mapCanvas.display()
            self.sitePlanCheckBox.select()
        else:
            self.noData = True
            self.sitePlanCheckBox.deselect()
        if not self.noData:
            self.mapCanvas.delete(self.noDataText)
        else:
            self.noDataText = self.mapCanvas.create_text(300,200, text='No Data', font=('Excalifont',20))
        self.placeNodesCheckBox.deselect()
        for coord in app.nodePositions.values():
            if coord != (-1,-1):
                self.placeNodesCheckBox.select()
                break
        if app.simulationRan == True:
            self.optimiseCheckBox.select()
        else:
            self.optimiseCheckBox.deselect()
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
        self.nodes = {2:True,3:True,4:True,5:True,6:True,7:True}
        self.drawingLine = False
        self.lineEnd = (-1,-1)
        self.currentTool = 0
        self.tempPixels = []
        self.previousActions = []
        self.redoActions = []
        self.dragIndex = -1
        self.planInserted = False
        self.capacityInputOpen = False
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
        self.blackDiskette = CTkImage(light_image=Image.open('assets/blackDiskette.png'), size=(32,32))
        self.blackImport = CTkImage(light_image=Image.open('assets/blackImport.png'), size=(32,32))
        self.whitePencil = CTkImage(light_image=Image.open('assets/whitePencil.png'), size=(16,16))
        self.whiteEraser = CTkImage(light_image=Image.open('assets/whiteEraser.png'), size=(16,16))
        self.whiteLine = CTkImage(light_image=Image.open('assets/whiteLine.png'), size=(16,16))
        self.whiteBullseye = CTkImage(light_image=Image.open('assets/whiteBullseye.png'), size=(16,16))
        self.whiteUndo = CTkImage(light_image=Image.open('assets/whiteUndo.png'), size=(16,16))
        self.whiteRedo = CTkImage(light_image=Image.open('assets/whiteRedo.png'), size=(16,16))
        self.whiteDiskette = CTkImage(light_image=Image.open('assets/whiteDiskette.png'), size=(32,32))
        self.whiteImport = CTkImage(light_image=Image.open('assets/whiteImport.png'), size=(32,32))
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
        self.toolContainer.rowconfigure((0,1,2,3,4,5,6), weight=1)
        self.toolContainer.rowconfigure(7, weight=3)
        self.toolContainer.rowconfigure((8,9), weight=1)
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
        self.openFileButton = ctk.CTkButton(self.toolContainer, image=self.blackImport, text='', **ButtonStyling, command=lambda: self.after(100, self.handleOpenFileButtonClick))
        self.saveButton = ctk.CTkButton(self.toolContainer, image=self.blackDiskette, text='', **ButtonStyling, command=lambda: self.after(100, self.handleSaveButtonClick))
        self.padder = ctk.CTkFrame(self.toolContainer, bg_color='white', fg_color='white')
        self.mapContainer = ctk.CTkFrame(self.upperFrame, corner_radius=15, border_color='black', border_width=5, bg_color='white', fg_color='white')
        self.mapCanvas = Canvas(parent=self.mapContainer, width=960, height=640)
        self.capacityButton = ctk.CTkButton(self, text='Input Capacity Data', border_width=2, border_color='black', text_color='black', fg_color='white', corner_radius=10, font=('Excalifont',20), width=300, command=lambda: self.after(100, self.handleCapacityButtonClick))
        self.mapCanvas.bind('<Button>', lambda event: self.handleDrawing(event=event, drag=False))
        self.mapCanvas.bind('<B1-Motion>', lambda event: self.handleDrawing(event=event, drag=True))
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
        self.saveButton.bind('<Enter>', lambda event: self.saveButton.configure(text_color='white', fg_color='black', image=self.whiteDiskette))
        self.saveButton.bind('<Leave>', lambda event: self.saveButton.configure(text_color='black', fg_color='white', image=self.blackDiskette))
        self.openFileButton.bind('<Enter>', lambda event: self.openFileButton.configure(text_color='white', fg_color='black', image=self.whiteImport))
        self.openFileButton.bind('<Leave>', lambda event: self.openFileButton.configure(text_color='black', fg_color='white', image=self.blackImport))
        self.configureTextButtons(self.clearCanvasButton)
        self.configureTextButtons(self.doneButton)
        self.configureTextButtons(self.capacityButton)
        self.overwriteWarning = overwriteWarning(self)
        self.capacityDataPage = capacityDataInput(self)

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
        self.doneButton.grid(row=6, column=0, sticky='nsew', columnspan=2, padx=2, pady=4)
        self.padder.grid(row=7, column=0, columnspan=2)
        self.openFileButton.grid(row=8, column=0, sticky='nsew', columnspan=2, padx=2, pady=4)
        self.saveButton.grid(row=9, column=0, sticky='nsew', columnspan=2, padx=2, pady=4)
        self.mapCanvas.pack(pady=10, padx=10)
        self.upperFrame.pack(fill='both', expand=True)
        self.capacityButton.pack(pady=10)

    def handleCapacityButtonClick(self):
        self.deselectCurrentButton()
        self.capacityButton.configure(text_color='white', fg_color='black')
        if self.capacityInputOpen:
            self.capacityDataPage.place_forget()
            self.capacityButton.configure(text='Input Capacity Data')
            app.capacityValues = self.capacityDataPage.getValues()
            print(f'capacity values: {app.capacityValues}')
            self.capacityInputOpen = False
        else:
            self.capacityDataPage.refresh()
            self.capacityDataPage.place(x = 200, y = 350)
            self.capacityButton.configure(text='Done')
            self.capacityInputOpen = True

    def handleDrawing(self, event, drag):
        x = event.x // self.mapCanvas.pixelSize
        y = event.y // self.mapCanvas.pixelSize
        if x != self.previousActions[-1].x or y != self.previousActions[-1].y or self.currentTool != self.previousActions[-1].colour:
            if drag != True:
                self.dragIndex += 1
            if self.mapCanvas.matrix[y][x]['base'] > 1:
                self.nodes[self.mapCanvas.matrix[y][x]['base']] = True
                app.nodePositions[self.mapCanvas.matrix[y][x]['base']] = (-1, -1)
                self.bullseyeButton.configure(state='normal')
            if self.currentTool < 2 or self.nodes[self.currentTool] == True:
                self.previousActions.append(dataPoint(x, y, self.mapCanvas.matrix[y][x]['base'], self.currentTool, self.dragIndex))
                self.mapCanvas.creation(x,y,self.currentTool,False)
            if self.currentTool > 1:
                self.nodes[self.currentTool] = False
                app.nodePositions[self.currentTool] = (x,y)
                for node, available in self.nodes.items():
                    if available == True:
                        self.currentTool = node
                        break
                    elif node == 7:
                        self.noNodesLeft()
        if self.master.dataAdded.get() == True:
            self.planInserted = True

    def configureTextButtons(self, button):
        button.bind('<Enter>', lambda event: button.configure(text_color='white', fg_color='black'))
        button.bind('<Leave>', lambda event: button.configure(text_color='black', fg_color='white'))

    def noNodesLeft(self):
        self.currentTool = 0
        self.bullseyeButton.configure(state='disabled')
        self.deselectCurrentButton()

    def deselectCurrentButton(self):
        self.pencilButton.configure(border_width=2)
        self.eraserButton.configure(border_width=2)
        self.lineButton.configure(border_width=2)
        self.bullseyeButton.configure(border_width=2)
        self.pencilButton.grid_configure(pady=4)
        self.eraserButton.grid_configure(pady=4)
        self.lineButton.grid_configure(pady=4)
        self.bullseyeButton.grid_configure(pady=4)
        self.mapCanvas.bind('<Button>', lambda event: self.handleDrawing(event=event, drag=False))
        self.mapCanvas.bind('<B1-Motion>', lambda event: self.handleDrawing(event=event, drag=True))
        self.mapCanvas.unbind('<Motion>')

    def handlePencilButtonClick(self):
        self.deselectCurrentButton()
        self.pencilButton.configure(text_color='black', fg_color='white', image=self.blackPencil, border_width=4)
        self.pencilButton.grid_configure(pady=2)
        self.currentTool = 0
        self.mapCanvas.bind('<Button>', lambda event: self.handleDrawing(event=event, drag=False))
        self.mapCanvas.bind('<B1-Motion>', lambda event: self.handleDrawing(event=event, drag=True))
        self.mapCanvas.unbind('<Motion>')

    def handleEraserButtonClick(self):
        self.deselectCurrentButton()
        self.eraserButton.configure(text_color='white', fg_color='black', image=self.blackEraser, border_width=4)
        self.eraserButton.grid_configure(pady=2)
        self.currentTool = 1
        self.mapCanvas.bind('<Button>', lambda event: self.handleDrawing(event=event, drag=False))
        self.mapCanvas.bind('<B1-Motion>', lambda event: self.handleDrawing(event=event, drag=True))
        self.mapCanvas.unbind('<Motion>')

    def handleLineButtonClick(self):
        self.deselectCurrentButton()
        self.lineButton.configure(text_color='white', fg_color='black', image=self.blackLine, border_width=4)
        self.lineButton.grid_configure(pady=2)
        self.mapCanvas.unbind('<B1-Motion>')
        self.mapCanvas.bind('<Motion>', lambda event: self.handleLineDrawing(event))
        self.mapCanvas.bind('<Button>', lambda event: self.handleLineClick(event))

    def handleLineClick(self, event):
        x = event.x // self.mapCanvas.pixelSize
        y = event.y // self.mapCanvas.pixelSize
        if self.drawingLine:
            self.lineEnd = (x,y)
            self.drawingLine = False
            self.dragIndex += 1
            lineData = self.drawLine(self.lineStart, (x,y), False)
            self.previousActions += lineData
        else:
            self.lineStart = (x,y)
            self.drawingLine = True

    def handleLineDrawing(self, event):
        x = event.x // self.mapCanvas.pixelSize
        y = event.y // self.mapCanvas.pixelSize
        if self.drawingLine:
            for pixel in self.tempPixels:
                self.mapCanvas.delete(pixel)
            self.tempPixels = self.drawLine(self.lineStart, (x,y), self.drawingLine)

    def deleteTemporarySquares(self, squareIDs):
        for squareID in squareIDs:
            self.mapCanvas.delete(squareID)

    def handleBullseyeButtonClick(self):
        self.deselectCurrentButton()
        self.bullseyeButton.configure(text_color='white', fg_color='black', image=self.blackBullseye, border_width=4)
        self.bullseyeButton.grid_configure(pady=2)
        for node, available in self.nodes.items():
            if available == True:
                self.currentTool = node
                break
        self.mapCanvas.bind('<Button>', lambda event: self.handleDrawing(event=event, drag=False))
        self.mapCanvas.bind('<B1-Motion>', lambda event: self.handleDrawing(event=event, drag=True))
        self.mapCanvas.unbind('<Motion>')

    def handleUndoButtonClick(self):
        self.deselectCurrentButton()
        self.undoButton.configure(text_color='white', fg_color='black', image=self.blackUndo)
        while self.previousActions:
            previousAction = self.previousActions.pop()
            x = previousAction.x
            y = previousAction.y
            colourValue = previousAction.prevColour
            dragIndex = previousAction.dragIndex + 1
            if colourValue > 1 and self.nodes[colourValue] == True:
                self.nodes[colourValue] = False
                app.nodePositions[colourValue] = (x,y)
            elif colourValue > 1 and self.nodes[colourValue] == False:
                break
            if self.mapCanvas.matrix[y][x]['base'] > 1:
                self.nodes[self.mapCanvas.matrix[y][x]['base']] = True
                app.nodePositions[self.mapCanvas.matrix[y][x]['base']] = (-1, -1)
                self.bullseyeButton.configure(state='normal')
            self.redoActions.append(dataPoint(x, y, self.mapCanvas.matrix[y][x]['base'], colourValue, dragIndex))
            self.mapCanvas.creation(x,y,colourValue,False)
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
            dragIndex = redoAction.dragIndex + 1
            if colourValue > 1 and self.nodes[colourValue] == True:
                self.nodes[colourValue] = False
                app.nodePositions[colourValue] = (x,y)
            elif colourValue > 1 and self.nodes[colourValue] == False:
                break
            if self.mapCanvas.matrix[y][x]['base'] > 1:
                self.nodes[self.mapCanvas.matrix[y][x]['base']] = True
                app.nodePositions[self.mapCanvas.matrix[y][x]['base']] = (-1, -1)
            self.previousActions.append(dataPoint(x, y, self.mapCanvas.matrix[y][x]['base'], colourValue, dragIndex))
            self.mapCanvas.creation(x,y,colourValue, False)
            if not self.redoActions or self.redoActions[-1].dragIndex != redoAction.dragIndex:
                break

    def handleClearButtonClick(self):
        self.deselectCurrentButton()
        self.clearCanvasButton.configure(text_color='white', fg_color='black')
        self.mapCanvas.delete('all')
        for y in range(len(self.mapCanvas.matrix)):
            for x in range(len(self.mapCanvas.matrix[y])):
                self.mapCanvas.matrix[y][x]['base'] = 1
        for node in self.nodes.keys():
            self.nodes[node] = True
            app.nodePositions[node] = (-1, -1)
        self.bullseyeButton.configure(state='normal')
        self.planInserted = False

    def handleDoneButtonClick(self):
        self.deselectCurrentButton()
        self.doneButton.configure(text_color='white', fg_color='black')
        if self.planInserted == True:
            self.master.dataAdded.set(True)
        else:
            self.master.dataAdded.set(False)
            app.simulationRan = False
        self.master.matrix = copy.deepcopy(self.mapCanvas.matrix)
        self.master.optimisePlanPage.packAvailableNodes()

    def handleSaveButtonClick(self):
        self.deselectCurrentButton()
        self.saveButton.configure(text_color='white', fg_color='black')
        filePath = filedialog.asksaveasfilename()
        filePath += '.json'
        self.master.matrix = copy.deepcopy(self.mapCanvas.matrix)
        with open(filePath, 'w') as file:
            json.dump(self.mapCanvas.matrix, file, indent=None)

    def handleOpenFileButtonClick(self):
        self.deselectCurrentButton()
        self.openFileButton.configure(text_color='white', fg_color='black')
        self.filePath = filedialog.askopenfilename(initialdir='/temp', title='Choose File', filetypes=[('json Files', '*.json')])
        if self.master.dataAdded.get() == True:
            self.overwriteWarning.place(x = 300, y = 250)
        else:
            self.readFile()

    def readFile(self):
        with open(self.filePath, 'r') as file:
            self.mapCanvas.matrix = json.load(file)
            self.master.dataAdded.set(True)
            self.master.matrix = copy.deepcopy(self.mapCanvas.matrix)
            self.mapCanvas.display()

    def drawLine(self, start, end, lineSubmitted):
        lineData = []
        if abs(end[0] - start[0]) > abs(end[1] - start[1]):
            lineData = self.drawHorizontalLine(start[0], start[1], end[0], end[1], lineSubmitted)
        else:
            lineData = self.drawVerticalLine(start[0], start[1], end[0], end[1], lineSubmitted)
        return lineData
    
    def drawHorizontalLine(self, x0, y0, x1, y1, lineSubmitted):
        lineData = []
        if x0 > x1:
            x0 , x1 = x1 , x0
            y0 , y1 = y1 , y0
        
        dx = x1 - x0
        dy = y1 - y0

        direction = -1 if dy < 0 else 1
        dy *= direction

        if dx != 0:
            y = y0
            p = 2 * dy - dx
            for i in range(dx + 1):
                if not lineSubmitted:
                    lineData.append(dataPoint(x0 + i, y, self.mapCanvas.matrix[y][x0 + i]['base'], 0, self.dragIndex))
                pixelID = self.mapCanvas.creation(x0 + i, y, 0, lineSubmitted)
                if lineSubmitted:
                    lineData.append(pixelID)
                if p >= 0:
                    y += direction
                    p = p - 2 * dx
                p = p + 2 * dy
        return lineData

    def drawVerticalLine(self, x0, y0, x1, y1, lineSubmitted):
        lineData = []
        if y0 > y1:
            x0 , x1 = x1 , x0
            y0 , y1 = y1 , y0
        
        dx = x1 - x0
        dy = y1 - y0

        direction = -1 if dx < 0 else 1
        dx *= direction

        if dy != 0:
            x = x0
            p = 2 * dx - dy
            for i in range(dy + 1):
                if not lineSubmitted:
                    lineData.append(dataPoint(x, y0 + i, self.mapCanvas.matrix[y0 + i][x]['base'], 0, self.dragIndex))
                pixelID = self.mapCanvas.creation(x, y0 + i, 0, lineSubmitted)
                if lineSubmitted:
                    lineData.append(pixelID)
                    
                if p >= 0:
                    x += direction
                    p = p - 2 * dy
                p = p + 2 * dx
        
        return lineData
    
class optimisePlanPage(ctk.CTkFrame):
    def __init__(self,parent):
        super().__init__(parent)
        self.startOrEndNode = ""
        self.evacPoint = -1
        self.startNode = -1
        self.nodeChooserOpen = False
        self.paths = {
            12:[],
            13:[],
            14:[],
            15:[],
            16:[],
            17:[]
        }

        self.WALKING_PACE = 1.4
        self.DISTANCE_BETWEEN_PEOPLE = 0.6
        self.PEOPLE_PER_METRE = 2
        self.PEOPLE_PER_SECOND_PER_METRE = self.WALKING_PACE * self.PEOPLE_PER_METRE / self.DISTANCE_BETWEEN_PEOPLE
        
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
        self.timeLabel = ctk.CTkLabel(self, text='Time: ---', text_color='black')
        self.timeSlider = ctk.CTkSlider(self, from_=0, to=100, command=self.updateTimeLabel, state='disabled')
        self.evacPointButton = ctk.CTkButton(self.rightFrame, text='', **ButtonStyling, command=lambda:self.after(100, self.handleEvacPointClick), image=self.fire)
        self.chooseNodeLabel = ctk.CTkLabel(self.rightFrame, text='Choose\nNode', font=('Excalifont',20), text_color='black')
        self.chooseNodeButton = ctk.CTkButton(self.rightFrame, text='', **ButtonStyling, command=lambda:self.after(100, self.handleChooseNodeClick), image=self.fire)
        self.runButton = ctk.CTkButton(self.rightFrame, text='Run', **ButtonStyling, command=lambda: self.after(100, self.handleRunButtonClick))
        self.scrollFrame = ctk.CTkScrollableFrame(self.rightFrame, bg_color='white', fg_color='white')
        self.canvasContainer = ctk.CTkFrame(self.upperFrame, corner_radius=15, border_color='black', border_width=5, bg_color='white', fg_color='white')
        self.canvas = Canvas(parent=self.canvasContainer, width=960, height=640)
        self.showAllPaths = ctk.CTkButton(self, text='Show all Paths', **ButtonStyling, command=lambda: self.after(100, self.handleShowAllPathsClick))
        self.simulateEvent = ctk.CTkButton(self, text='Simulate Event', **ButtonStyling, command=lambda: self.after(100, self.handleSimulateEventClick), state='disabled')
        self.handleHovering(self.evacPointButton)
        self.handleHovering(self.chooseNodeButton)
        self.handleHovering(self.runButton)
        self.handleHovering(self.showAllPaths)
        self.handleHovering(self.simulateEvent)

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
        
        for button in self.Buttons.keys():
            button.bind('<Enter>', lambda event, b=button: self.buttonEnter(b))
            button.bind('<Leave>', lambda event, b=button: self.buttonLeave(b))
    
    def placeWidgets(self):
        self.canvasContainer.pack(pady=(10,0), side='left')
        self.rightFrame.pack(side='left', fill='both', expand=True, pady=(10,0))
        self.canvas.pack(pady=10, padx=10)
        self.upperFrame.pack(fill='both', expand=True)
        self.simulateEvent.pack(side='left', fill='y', expand=True, pady=2, ipadx=75, ipady=5, padx=(0,10))
        self.timeLabel.pack(side='left', fill='y', expand=True, pady=2, padx=5)
        self.timeSlider.pack(side='left', padx=(0,131))
        self.showAllPaths.pack(side='right', fill='y', expand=True, pady=2, ipadx=75, ipady=5)
        self.padder.grid(column=0, row=2, sticky='nsew')
        self.evacPointLabel.grid(column=0, row=0, sticky='nsew', padx=5)
        self.evacPointButton.grid(column=0, row=1, sticky='nsew', padx=5)
        self.chooseNodeLabel.grid(column=0, row=3, sticky='nsew', padx=5)
        self.chooseNodeButton.grid(column=0, row=4, sticky='nsew', padx=5)
        self.runButton.grid(column=0, row=5, sticky='nsew', padx=5, pady=(5,0))

    def updateTimeLabel(self, value):
        formattedValue = f'{int(value):03}'
        self.timeLabel.configure(text=f'Time: {formattedValue}')


    def handleHovering(self,button):
        button.bind('<Enter>', lambda event: button.configure(text_color='white', fg_color='black'))
        button.bind('<Leave>', lambda event: button.configure(text_color='black', fg_color='white'))

    def setMinimumTime(self):
        minTime = 0
        for key, path in self.paths.items():
            print(f'{key}: length: {len(path)}')
            if len(path) / self.WALKING_PACE > minTime:
                minTime = math.ceil(len(path) / self.WALKING_PACE)
                print(f'min time {minTime}')
        self.timeSlider.configure(from_=minTime, to=300)
        

    def handleRunButtonClick(self):
        self.runButton.configure(text_color='black', fg_color='white')
        self.disableAllButtons()
        if self.evacPoint != -1 and self.startNode != -1:
            self.astar(self.startNode, self.evacPoint)
            self.timeSlider.configure(state='normal')
            self.simulateEvent.configure(state='normal')
            print(f'red {len(self.paths[12])}')
        self.enableAllButtons()
        self.setMinimumTime()
        app.simulationRan = True
    
    def handleShowAllPathsClick(self):
        self.showAllPaths.configure(text_color='white', fg_color='black')
        self.disableAllButtons()
        if self.evacPoint != -1:
            for node in app.nodePositions.keys():
                if app.nodePositions[node] != (-1,-1) and node != self.evacPoint:
                    self.astar(node, self.evacPoint)
            self.timeSlider.configure(state='normal')
            self.simulateEvent.configure(state='normal')
            self.setMinimumTime()
        self.enableAllButtons()
        app.simulationRan = True
    
    def astar(self, startNode, endNode):
        self.master.optimisePlanPage.canvas.matrix = copy.deepcopy(self.master.matrix)
        tempSquareIDs = []
        start = app.nodePositions[startNode]
        end = app.nodePositions[endNode]
        count = 0
        openSet = PriorityQueue()
        openSet.put((0,count,start))
        previousNodes = {}
        gScore = [[float("inf")] * 120 for _ in range(80)]
        gScore[start[1]][start[0]] = 0
        fScore = [[float("inf")] * 120 for _ in range(80)]
        fScore[start[1]][start[0]] = self.heuristic(start,end)
        queue = {start}

        def run_algorithm_step():
            nonlocal count
            if openSet.empty():
                self.after(250, self.deleteTemporarySquares(tempSquareIDs))
                return False

            neighbors = []
            current = openSet.get()[2]
            queue.remove(current)

            if current == end:
                self.reconstructPath(previousNodes, start, current, startNode)
                self.timeSlider.configure(state='normal')
                self.simulateEvent.configure(state='normal')
                self.enableAllButtons()
                self.setMinimumTime()
                self.after(250, self.deleteTemporarySquares(tempSquareIDs))
                app.matrix = copy.deepcopy(self.canvas.matrix)
                return True

            if current[1] < 79 and self.canvas.matrix[current[1] + 1][current[0]]['base'] != 0:
                neighbors.append((current[0], current[1] + 1))
            if current[1] > 0 and self.canvas.matrix[current[1] - 1][current[0]]['base'] != 0:
                neighbors.append((current[0], current[1] - 1))
            if current[0] < 119 and self.canvas.matrix[current[1]][current[0] + 1]['base'] != 0:
                neighbors.append((current[0] + 1, current[1]))
            if current[0] > 0 and self.canvas.matrix[current[1]][current[0] - 1]['base'] != 0:
                neighbors.append((current[0] - 1, current[1]))

            for neighbor in neighbors:
                tempGScore = gScore[current[1]][current[0]] + 1
                if tempGScore < gScore[neighbor[1]][neighbor[0]]:
                    previousNodes[neighbor] = current
                    gScore[neighbor[1]][neighbor[0]] = tempGScore
                    fScore[neighbor[1]][neighbor[0]] = tempGScore + self.heuristic(neighbor, end)
                    if neighbor not in queue:
                        count += 1
                        openSet.put((fScore[neighbor[1]][neighbor[0]], count, neighbor))
                        queue.add(neighbor)
                        squareID = self.canvas.creation(neighbor[0], neighbor[1], 9, True)
                        tempSquareIDs.append(squareID)

            if current != start:
                squareID = self.canvas.creation(current[0], current[1], 8, True)
                tempSquareIDs.append(squareID)

            self.after(1, run_algorithm_step)
        run_algorithm_step()
        
        return True

    def deleteTemporarySquares(self, squareIDs):
        for squareID in squareIDs:
            self.canvas.delete(squareID)

    def reconstructPath(self, previousNodes, start, current, startNode):
        while current in previousNodes:
            current = previousNodes[current]
            if current != start:
                self.canvas.creation(current[0], current[1], startNode+10, False)
                self.paths[startNode+10].append(current)
    
    def heuristic(self, point1, point2):
        x1, y1 = point1
        x2, y2 = point2
        return abs(x1 - x2) + abs(y1 - y2)

    def handleSimulateEventClick(self):
        self.disableAllButtons()
        self.simulateEvent.configure(text_color='white', fg_color='black')
        tempSquareIDs = self.runFlowSimulation()
        # self.deleteTemporarySquares(tempSquareIDs)
        self.enableAllButtons()

    def runFlowSimulation(self):
        problems = []
        tempSquareIDs = []
        pathWidths = []
        for path in self.paths.keys():
            if self.paths[path]:
                for position in self.paths[path]:
                    pathWidth = 1
                    if position[1] < 79 and path not in self.canvas.matrix[position[1] + 1][position[0]].get('paths', []) and position[1] > 0 and path not in self.canvas.matrix[position[1] - 1][position[0]].get('paths', []): # path is horizontal
                        tempCount  = 0
                        while tempCount < app.capacityValues[path - 10] / self.PEOPLE_PER_SECOND_PER_METRE:
                            if position[1] + tempCount < 79 and self.canvas.matrix[position[1] + tempCount + 1][position[0]]['base'] != 0:
                                tempCount += 1
                                squareID = self.canvas.creation(position[0], position[1] + tempCount, 9, True)
                                tempSquareIDs.append(squareID)
                                print(tempCount)
                            else:
                                print(f'tempCount to pathwidth {tempCount}')
                                pathWidth += tempCount
                                break
                        else:
                            pathWidth += tempCount
                        tempCount  = 0
                        while tempCount < app.capacityValues[path - 10] / self.PEOPLE_PER_SECOND_PER_METRE:
                            if position[1] - tempCount > 0 and self.canvas.matrix[position[1] - tempCount - 1][position[0]]['base'] != 0:
                                tempCount += 1
                                squareID = self.canvas.creation(position[0], position[1] - tempCount, 9, True)
                                tempSquareIDs.append(squareID)
                                print(tempCount)
                            else:
                                print(f'tempCount to pathwidth {tempCount}')
                                pathWidth += tempCount
                                break
                        else:
                            pathWidth += tempCount
                    elif position[0] < 119 and path not in self.canvas.matrix[position[1]][position[0] + 1].get('paths', []) and position[0] > 0 and path not in self.canvas.matrix[position[1]][position[0] - 1].get('paths', []): # path vertical
                        tempCount  = 0
                        while tempCount < app.capacityValues[path - 10] / self.PEOPLE_PER_SECOND_PER_METRE:
                            if position[0] + tempCount < 119 and self.canvas.matrix[position[1]][position[0] + tempCount + 1]['base'] != 0:
                                tempCount += 1
                                squareID = self.canvas.creation(position[0] + tempCount, position[1], 9, True)
                                tempSquareIDs.append(squareID)
                            else:
                                pathWidth += tempCount
                                break
                        else:
                            pathWidth += tempCount
                        tempCount  = 0
                        while tempCount < app.capacityValues[path - 10] / self.PEOPLE_PER_SECOND_PER_METRE:
                            if position[0] - tempCount > 0 and self.canvas.matrix[position[1]][position[0] - tempCount - 1]['base'] != 0:
                                tempCount += 1
                                squareID = self.canvas.creation(position[0] - tempCount, position[1], 9, True)
                                tempSquareIDs.append(squareID)
                            else:
                                pathWidth += tempCount
                                break
                        else:
                            pathWidth += tempCount
                    elif position[1] < 79 and path not in self.canvas.matrix[position[1] + 1][position[0]].get('paths', []) and position[0] < 119 and path not in self.canvas.matrix[position[1]][position[0] + 1].get('paths', []):
                        outsideWall = self.findNearestWall(position, (1, 1))
                        if 0 <= position[0] - 1 <= 119 and 0 <= position[1] - 1 <= 79:
                            if self.canvas.matrix[position[1] - 1][position[0] - 1]['base'] == 0:
                                insideWall = (position[0] - 1, position[1] - 1)
                            else:
                                insideWall = self.findNearestWall((position[0] - 1, position[1] - 1), (-1, -1))
                        else:
                            insideWall = (position[0] - 1, position[1] - 1)
                        pathWidth  = self.calculateDistance(outsideWall, insideWall)
                        print(f'Bottom Right corner, drawing line between: {insideWall} and {outsideWall} pathwidth = {pathWidth}')
                        tempSquareIDs += self.drawLine(insideWall, outsideWall)

                    elif position[1] < 79 and path not in self.canvas.matrix[position[1] + 1][position[0]].get('paths', []) and position[0] > 0 and path not in self.canvas.matrix[position[1]][position[0] - 1].get('paths', []):
                        outsideWall = self.findNearestWall(position, (-1, 1))
                        if 0 <= position[0] + 1 <= 119 and 0 <= position[1] - 1 <= 79:
                            if self.canvas.matrix[position[1] - 1][position[0] + 1]['base'] == 0:
                                insideWall = (position[0] + 1, position[1] - 1)
                            else:
                                insideWall = self.findNearestWall((position[0] + 1, position[1] - 1), (1, -1))
                        else:
                            insideWall = (position[0] + 1, position[1] - 1)
                        pathWidth  = self.calculateDistance(outsideWall, insideWall)
                        print(f'Bottom Left corner, drawing line between: {insideWall} and {outsideWall} pathwidth = {pathWidth}')
                        tempSquareIDs += self.drawLine(insideWall, outsideWall)

                    elif position[1] > 0 and path not in self.canvas.matrix[position[1] - 1][position[0]].get('paths', []) and position[0] < 119 and path not in self.canvas.matrix[position[1]][position[0] + 1].get('paths', []):
                        outsideWall = self.findNearestWall(position, (1, -1))
                        if 0 <= position[0] - 1 <= 119 and 0 <= position[1] + 1 <= 79:
                            if self.canvas.matrix[position[1] + 1][position[0] - 1]['base'] == 0:
                                insideWall = (position[0] - 1, position[1] + 1)
                            else:
                                insideWall = self.findNearestWall((position[0] - 1, position[1] + 1), (-1, 1))
                        else:
                            insideWall = (position[0] - 1, position[1] + 1)
                        pathWidth  = self.calculateDistance(outsideWall, insideWall)
                        print(f'Top Right corner, drawing line between: {insideWall} and {outsideWall} pathwidth = {pathWidth}')
                        tempSquareIDs += self.drawLine(insideWall, outsideWall)

                    elif position[1] > 0 and path not in self.canvas.matrix[position[1] - 1][position[0]].get('paths', []) and position[0] > 0 and path not in self.canvas.matrix[position[1]][position[0] - 1].get('paths', []):
                        outsideWall = self.findNearestWall(position, (-1, -1))
                        if 0 <= position[0] + 1 <= 119 and 0 <= position[1] + 1 <= 79:
                            if self.canvas.matrix[position[1] + 1][position[0] + 1]['base'] == 0:
                                insideWall = (position[0] + 1, position[1] + 1)
                            else:
                                insideWall = self.findNearestWall((position[0] + 1, position[1] + 1), (1, 1))
                        else:
                            insideWall = (position[0] + 1, position[1] + 1)
                        pathWidth  = self.calculateDistance(outsideWall, insideWall)
                        print(f'Top Left corner, drawing line between: {insideWall} and {outsideWall} pathwidth = {pathWidth}')
                        tempSquareIDs += self.drawLine(insideWall, outsideWall)

                    people = 0

                    for group in self.canvas.matrix[position[1]][position[0]].get('paths', []):
                        people += app.capacityValues[group - 10]
                        
                    pathWidths.append((position, pathWidth))

                # print(f'people {people} evacTime: {self.timeSlider.get()}')
                desiredFlow = people / self.timeSlider.get()
                minWidth = desiredFlow / self.PEOPLE_PER_SECOND_PER_METRE

                print(f'pathwidths: {pathWidths}')
                pathWidths.sort(key=lambda element: element[1] / minWidth)
                print(f'orderd pathwidths: {pathWidths}')

                counter = 0
                previous = -1

                for position in pathWidths:
                    if counter > 20 and position[1] != previous:
                        break
                    if position[1] < minWidth:
                        problems.append(position)
                        self.canvas.creation(position[0][0], position[0][1], 2, False)
                    else:
                        problems.append(position)
                        self.canvas.creation(position[0][0], position[0][1], 5, False)
                    counter += 1
                    previous = position[1]
                    


        # print(f'problems: {problems}')
        # for problem in problems:
        #     self.canvas.creation(problem[0], problem[1], 2, False)
        # return tempSquareIDs

    def findNearestWall(self, corner, direction):
        nearestWall = (-1,-1)
        layer = 1
        while nearestWall == (-1,-1):
            position = 0
            while position <= layer:
                if 0 <= corner[1] + direction[1] * position <= 79 and 0 <= corner[0] + direction[0] * layer <= 119 and self.canvas.matrix[corner[1] + direction[1] * position][corner[0] + direction[0] * layer]['base'] == 0:
                    nearestWall = (corner[0] + direction[0] * layer, corner[1] + direction[1] * position)
                    break
                elif 0 <= corner[1] + direction[1] * layer <= 79 and 0 <= corner[0] + direction[0] * position <= 119 and self.canvas.matrix[corner[1] + direction[1] * layer][corner[0] + direction[0] * position]['base'] == 0:
                    nearestWall = (corner[0] + direction[0] * position, corner[1] + direction[1] * layer)
                    break
                position += 1
            if not (0 <= corner[1] + direction[1] * layer <= 79) and not (0 <= corner[0] + direction[0] * layer <= 119):
                break
            layer += 1
        return nearestWall

    def calculateDistance(self, corner, wall):
        return math.sqrt(abs(corner[0]-wall[0]) ** 2 + abs(corner[1]-wall[1]) ** 2)
    
    def drawLine(self, start, end):
        tempPixels = []
        if abs(end[0] - start[0]) > abs(end[1] - start[1]):
            tempPixels = self.drawHorizontalLine(start[0], start[1], end[0], end[1])
        else:
            tempPixles = self.drawVerticalLine(start[0], start[1], end[0], end[1])
        return tempPixels
    
    def drawHorizontalLine(self, x0, y0, x1, y1):
        tempPixels = []
        if x0 > x1:
            x0 , x1 = x1 , x0
            y0 , y1 = y1 , y0
        
        dx = x1 - x0
        dy = y1 - y0

        direction = -1 if dy < 0 else 1
        dy *= direction

        if dx != 0:
            y = y0
            p = 2 * dy - dx
            for i in range(dx + 1):
                if i != 0 and y != y0 and x0 + i != x1 and y != y1:
                    pixelID = self.canvas.creation(x0 + i, y, 6, True)
                    tempPixels.append(pixelID)
                if p >= 0:
                    y += direction
                    p = p - 2 * dx
                p = p + 2 * dy
        
        return tempPixels


    def drawVerticalLine(self, x0, y0, x1, y1):
        tempPixels = []
        if y0 > y1:
            x0 , x1 = x1 , x0
            y0 , y1 = y1 , y0
        
        dx = x1 - x0
        dy = y1 - y0

        direction = -1 if dx < 0 else 1
        dx *= direction

        if dy != 0:
            x = x0
            p = 2 * dx - dy
            for i in range(dy + 1):
                if x != x0 and i != 0 and x != x1 and y0 + i != y1:
                    pixelID = self.canvas.creation(x, y0 + i, 6, True)
                    tempPixels.append(pixelID)
                if p >= 0:
                    x += direction
                    p = p - 2 * dy
                p = p + 2 * dx
        
        return tempPixels

    def disableAllButtons(self):
        self.master.menu.homeButton.configure(state='disabled')
        self.master.menu.inputDataButton.configure(state='disabled')
        self.master.menu.optimisePlanButton.configure(state='disabled')
        self.evacPointButton.configure(state='disabled')
        self.chooseNodeButton.configure(state='disabled')
        self.runButton.configure(state='disabled')
        self.showAllPaths.configure(state='disabled')

    def enableAllButtons(self):
        self.master.menu.homeButton.configure(state='normal')
        self.master.menu.inputDataButton.configure(state='normal')
        self.master.menu.optimisePlanButton.configure(state='normal')
        self.evacPointButton.configure(state='normal')
        self.chooseNodeButton.configure(state='normal')
        self.runButton.configure(state='normal')
        self.showAllPaths.configure(state='normal')

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
        for button in self.Buttons.keys():
            button.configure(state='enabled', fg_color='white')
            button.pack_forget()
        self.evacPoint = -1
        self.startNode = -1
        self.setButtonImages()

    def handleNodeChoiceButtonClick(self,button):
        grey = "#AAAFB4"
        if self.startOrEndNode == "start":
            self.startNode = self.Buttons[button]
        else:
            self.evacPoint = self.Buttons[button]
        print(button.__class__.__name__)
        button.configure(state='disabled', fg_color=grey)
        for button, value in self.Buttons.items():
            if value != self.evacPoint and value != self.startNode:
                button.configure(state='normal', fg_color='white')
        self.setButtonImages()
        self.scrollFrame.grid_forget()
        self.nodeChooserOpen = False

    def buttonEnter(self,button):
        button.configure(border_width=4)
        button.pack_configure(pady=0)

    def buttonLeave(self,button):
        button.configure(border_width=2)
        button.pack_configure(pady=2)
    
    def handleEvacPointClick(self):
        self.evacPointButton.configure(text_color='black', fg_color='white')
        self.startOrEndNode = "end"
        if not self.nodeChooserOpen:
            self.nodeChooser()
        else:
            self.scrollFrame.grid_forget()
            self.nodeChooserOpen = False

    def handleChooseNodeClick(self):
        self.chooseNodeButton.configure(text_color='black', fg_color='white')
        self.startOrEndNode = "start"
        if not self.nodeChooserOpen:
            self.nodeChooser()
        else:
            self.scrollFrame.grid_forget()
            self.nodeChooserOpen = False

    def packAvailableNodes(self):
        self.resetButtons()
        for button, node in self.Buttons.items():
            if app.nodePositions[node] != (-1,-1):
                button.pack(pady=2)

    def nodeChooser(self):
        self.scrollFrame.grid(column=0, row=2, sticky='nsew')
        self.nodeChooserOpen = True


class Canvas(ctk.CTkCanvas):
    def __init__(self, parent, height, width):
        super().__init__(parent)
        self.configure(height=height, width=width, bd=0, background='white', highlightthickness=0)
        self.pixelSize = height // 80
        self.matrix = [[{'base': 1} for _ in range(120)] for _ in range(80)]
        
    def creation(self, x, y, colourValue, temporary):
        red = '#ff0000'
        blue = '#0010ff'
        green = '#00ff7c'
        orange = '#ffa300'
        pink = '#ff00cf'
        yellow = '#fffc00'
        purple = '#800080'
        darkPurple = '#320032'

        match colourValue:
            case 0:
                colour = 'black'
            case 1:
                colour = 'white'
            case 2:
                colour = red
            case 3:
                colour = blue
            case 4:
                colour = green
            case 5:
                colour = orange
            case 6:
                colour = pink
            case 7:
                colour = yellow
            case 8:
                colour = purple
            case 9:
                colour = darkPurple
            case _:
                colour = purple

        self.master.master.master.master.dataAdded.set(True)
        # print(f'drawing at x:{x}, y:{y}, colour={colour}, colourValue={colourValue}')
        if not temporary:
            self.create_rectangle((self.pixelSize * (x+1) - self.pixelSize, self.pixelSize * (y+1) - self.pixelSize, self.pixelSize * (x+1) - 1, self.pixelSize * (y+1) - 1), fill=colour, outline=colour)
            if colourValue < 12:
                self.matrix[y][x]['base'] = colourValue
            else:
                self.matrix[y][x].setdefault('paths', []).append(colourValue)
        else:
            squareID = self.create_rectangle((self.pixelSize * (x+1) - self.pixelSize, self.pixelSize * (y+1) - self.pixelSize, self.pixelSize * (x+1) - 1, self.pixelSize * (y+1) - 1), fill=colour, outline=colour)
            return squareID

    def display(self):
        red = '#ff0000'
        blue = '#0010ff'
        green = '#00ff7c'
        orange = '#ffa300'
        pink = '#ff00cf'
        yellow = '#fffc00'
        purple = '#800080'
        darkPurple = '#320032'
        self.delete('all')
        for y in range(80):
            for x in range(120):
                match app.matrix[y][x]['base']:
                    case 0:
                        colour = 'black'
                    case 2:
                        colour = red
                    case 3:
                        colour = blue
                    case 4:
                        colour = green
                    case 5:
                        colour = orange
                    case 6:
                        colour = pink
                    case 7:
                        colour = yellow
                    case 8:
                        colour = purple
                    case 9:
                        colour = darkPurple
                if app.matrix[y][x]['base'] == 0 or app.matrix[y][x]['base'] > 1:
                    self.create_rectangle((self.pixelSize * (x+1) - self.pixelSize, self.pixelSize * (y+1) - self.pixelSize, self.pixelSize * (x+1) - 1, self.pixelSize * (y+1) - 1), fill=colour, outline=colour)

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

class capacityDataInput(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(height=200, width=400, corner_radius=15, border_color='black', border_width=5, bg_color='white', fg_color='white')
        self.values={2:-1,3:-1,4:-1,5:-1,6:-1,7:-1}
        self.createWidgets()
        self.placeWidgets()

    def createWidgets(self):
        self.red = CTkImage(light_image=Image.open('assets/red.png'))
        self.blue = CTkImage(light_image=Image.open('assets/blue.png'))
        self.green = CTkImage(light_image=Image.open('assets/green.png'))
        self.orange = CTkImage(light_image=Image.open('assets/orange.png'))
        self.pink = CTkImage(light_image=Image.open('assets/pink.png'))
        self.yellow = CTkImage(light_image=Image.open('assets/yellow.png'))

        self.titleLabel = ctk.CTkLabel(self, text='Input Capacity Data', text_color='black', font=('Excalifont',25))
        self.scrollFrame = ctk.CTkScrollableFrame(self, bg_color='white', fg_color='white')

        self.redEntry = nodeWidget(self.scrollFrame, image=self.red)
        self.blueEntry = nodeWidget(self.scrollFrame, image=self.blue)
        self.greenEntry = nodeWidget(self.scrollFrame, image=self.green)
        self.orangeEntry = nodeWidget(self.scrollFrame, image=self.orange)
        self.pinkEntry = nodeWidget(self.scrollFrame, image=self.pink)
        self.yellowEntry = nodeWidget(self.scrollFrame, image=self.yellow)

        self.entries={self.redEntry:2, self.blueEntry:3, self.greenEntry:4, self.orangeEntry:5, self.pinkEntry:6, self.yellowEntry:7}
        
    def placeWidgets(self):
        self.titleLabel.pack(padx=200, pady=10)
        self.scrollFrame.pack(padx=10, pady=(0,10), expand=True, fill='both')

    def refresh(self):
        for entry, node in self.entries.items():
            entry.pack_forget()
        for entry, node in self.entries.items():
            if app.nodePositions[node] != (-1,-1):
                entry.pack(pady=2)
    
    def getValues(self):
        for entry, node in self.entries.items():
            self.values[node] = int(entry.getEntry() or -1)
        return self.values

class nodeWidget(ctk.CTkFrame):
    def __init__(self, parent, image):
        super().__init__(parent)
        self.configure(corner_radius=15, border_color='black', border_width=5, bg_color='white', fg_color='white')
        self.createWidgets(image)
        self.placeWidgets()

    def createWidgets(self, image):
        self.image = ctk.CTkLabel(self, image=image, text='')
        self.label = ctk.CTkLabel(self, text='Input Capacity', text_color='black', font=('Excalifont',20))
        self.entryField = ctk.CTkEntry(self, fg_color='white', text_color='black', font=('Excalifont',15), justify='center')
    
    def placeWidgets(self):
        self.image.pack(padx=(10,0), pady=10, side='left')
        self.label.pack(padx=10, pady=(10,0))
        self.entryField.pack(pady=10, padx=(10,20))

    def getEntry(self):
        return self.entryField.get()
 
if __name__ == '__main__':
    app = App()
    app.mainloop()