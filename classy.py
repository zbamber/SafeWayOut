import tkinter as tk
from tkinter import ttk, filedialog
import customtkinter as ctk
from customtkinter import CTkImage
from PIL import Image
import json
from queue import PriorityQueue
import copy
import math

class App(tk.Tk):

    def __init__(self):
        super().__init__()

        # configuring the window
        self.title('Safe Way Out')
        self.geometry('1280x720')
        # defining the grid
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.configure(bg='white')
        self.iconbitmap('assets/fire.ico')
        self.resizable(False,False)

        # creating the pages
        self.menu = Menu(self)
        self.homePage = homePage(self)
        self.inputDataPage = inputDataPage(self)
        self.optimisePlanPage = optimisePlanPage(self)

        # initialising the global data structures
        self.matrix = [[{'base': 1} for _ in range(120)] for _ in range(80)]
        self.nodePositions = {2:(-1,-1), 3:(-1,-1), 4:(-1,-1), 5:(-1,-1), 6:(-1,-1), 7:(-1,-1)}
        self.capacityValues={2:-1,3:-1,4:-1,5:-1,6:-1,7:-1}
        self.dataAdded = ctk.BooleanVar(value=False)
        self.simulationRan = False
    
    def showPage(self, page): # function to switch between pages

        # ensures no pages is currently being shown
        self.homePage.grid_forget()
        self.inputDataPage.grid_forget()
        self.optimisePlanPage.grid_forget()

        # shows the page passed as an argument
        page.grid(row=0, column=1, sticky='nsew')

class Menu(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)
        # configuring and placing the menu
        self.configure(corner_radius=15, border_color='black', border_width=5, bg_color='white', fg_color='white')
        self.grid(row=0, column=0, sticky='nsew', padx=(10,5), pady=10)

        # importing the images
        self.homeDark = CTkImage(light_image=Image.open('assets/homeDark.png'))
        self.homeLight = CTkImage(light_image=Image.open('assets/homeLight.png'))

        # creating and placing the widgets in the menu
        self.createMenuWidgets()
        self.placeMenuWidgets()
    
    def createMenuWidgets(self):

        # repeated styling between menu buttons
        menuButtonStyling = {
        'border_width':2,
        'border_color':'black',
        'text_color':'black',
        'font':('Excalifont',20),
        'fg_color':'white',
        'corner_radius':10
        }

        # creating the widgets by giving the menuButtonStyling dictionary as an argument to avoid repeated code
        self.title = ctk.CTkLabel(self, text='Safe Way Out', fg_color='white', text_color='black', font=('Excalifont', 20))
        self.homeButton = ctk.CTkButton(self, text='   Home', image=self.homeDark, anchor='w', **menuButtonStyling, command=self.openHomePage)
        self.inputDataButton = ctk.CTkButton(self, text='Input Data', **menuButtonStyling, command=self.openInputDataPage)
        self.optimisePlanButton = ctk.CTkButton(self, text='Optimise Plan', **menuButtonStyling, command=self.openOptimisePlanPage)
    
    def placeMenuWidgets(self):
        # placing the widgets based on their verticle order
        self.title.pack(pady=20, padx=30)
        self.homeButton.pack(fill='x', padx=10, pady=5)
        
        # binding the enter and leave events to the homeButton to achieve the desired hover effect
        self.homeButton.bind('<Enter>', lambda event: self.homeButton.configure(text_color='white', fg_color='black', image=self.homeLight))
        self.homeButton.bind('<Leave>', lambda event: self.homeButton.configure(text_color='black', fg_color='white', image=self.homeDark))

        # these buttons do not have images so we use a helper function to avoid repeated code
        self.placeMenuButton(self.inputDataButton)
        self.placeMenuButton(self.optimisePlanButton)

    def placeMenuButton(self, button): # helper function to set the colours when the button is hovered over
        button.pack(fill='x', padx=10, pady=5)
        button.bind('<Enter>', lambda event: button.configure(text_color='white', fg_color='black'))
        button.bind('<Leave>', lambda event: button.configure(text_color='black', fg_color='white'))
    
    def openHomePage(self):
        self.master.showPage(self.master.homePage) # calls the method in the app class to show the home page
        # returns the button to its original state after 100ms to avoid default tkinter behaviour in which the button will stay blue
        self.after(100, lambda: self.homeButton.configure(text_color='black', fg_color='white', image=self.homeDark))
        self.master.homePage.update() # calls a method in the homePage class to refresh any changes to the page

    def openInputDataPage(self):
        self.master.showPage(self.master.inputDataPage) # calls the method in the app class to show the input data page
        self.after(100, lambda: self.inputDataButton.configure(text_color='black', fg_color='white')) # returns the button to its original state after 100ms

    def openOptimisePlanPage(self):
        self.master.showPage(self.master.optimisePlanPage) # calls the method in the app class to show the optimise plan page
        self.master.optimisePlanPage.canvas.display() # refreshes the canvas to show any changes made to the plan
        self.after(100, lambda: self.optimisePlanButton.configure(text_color='black', fg_color='white'))

class homePage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        # configuring the frame the homePage sits in
        self.configure(bg_color='white', fg_color='white')
        self.rowconfigure(0, weight=4) 
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        self.createWidgets()
        self.placeWidgets()

        self.noData = True # boolean that tracks if any data has been added on the input data page

    def createWidgets(self):
        # all checkboxes have the same styling so we can use a dictionary to pass these arguments, avoiding repeated code
        checkboxStyling = {
            'width':5,
            'height':10,
            'fg_color':'white',
            'text_color':'black',
            'font':('Excalifont',20),
            'border_color':'black',
            'hover_color':'black'
        }

        # creating and configuring the frames that organise where the content sits
        self.upperContentFrame = ctk.CTkFrame(self, bg_color='white', fg_color='white')
        self.upperContentFrame.columnconfigure(0, weight=5)
        self.upperContentFrame.columnconfigure(1, weight=2)
        self.upperContentFrame.rowconfigure(0, weight=1)
        # the lower content frame does not need a grid defining as the simple pack methods are sufficient for its internal layout
        self.lowerContentFrame = ctk.CTkFrame(self, corner_radius=15, border_color='black', border_width=5, bg_color='white', fg_color='white')
        
        #creating the widgets that will be placed in the lower content frame
        self.warningLabel = ctk.CTkLabel(self.lowerContentFrame, text='Warning!', fg_color='white', text_color='black', font=('Excalifont', 25) )
        self.warningTable = ttk.Treeview(self.lowerContentFrame, columns=('Index','Type', 'Extra Information'), show='headings')
        # initialising the headings of the table
        self.warningTable.heading('Index', text='Index')
        self.warningTable.heading('Type', text='Type')
        self.warningTable.heading('Extra Information', text='Extra Information')

        # creating the widgets that will be placed in the upper content frame
        self.mapContainer = ctk.CTkFrame(self.upperContentFrame, corner_radius=15, border_color='black', border_width=5, bg_color='white', fg_color='white')
        self.canvas = Canvas(parent=self.mapContainer, width=600, height=400)
        self.noDataText = self.canvas.create_text(300,200, text='No Data', font=('Excalifont',20))
        self.toDoContainer = ctk.CTkFrame(self.upperContentFrame, corner_radius=15, border_color='black', border_width=5, bg_color='white', fg_color='white')
        self.toDoLabel = ctk.CTkLabel(self.toDoContainer, text='To Do:', fg_color='white', text_color='black', font=('Excalifont', 25) )

        #creating the checkboxes that show the state of the application to the user
        self.sitePlanCheckBox = ctk.CTkCheckBox(self.toDoContainer, text=' Insert Site Plan', **checkboxStyling)
        self.placeNodesCheckBox = ctk.CTkCheckBox(self.toDoContainer, text=' Place Nodes', **checkboxStyling)
        self.optimiseCheckBox = ctk.CTkCheckBox(self.toDoContainer, text=' Optimise', **checkboxStyling)
        self.analyseCheckBox = ctk.CTkCheckBox(self.toDoContainer, text=' Analyse Bottlenecks', **checkboxStyling)
        self.capacityDataCheckBox = ctk.CTkCheckBox(self.toDoContainer, text=' Import Capacity Data', **checkboxStyling)
        self.simulateCheckBox = ctk.CTkCheckBox(self.toDoContainer, text=' Simulate Event', **checkboxStyling)

    def placeWidgets(self):
        # lower frame
        self.warningLabel.pack(pady=10)
        self.warningTable.pack(fill='both', expand=True, padx=10, pady=(0,10))

        # upper frame
        self.canvas.pack(fill='both', expand=True, padx=10, pady=10)

        # in the to do container the widgets are packed vertically one on top of the other
        self.toDoLabel.pack(pady=20)
        self.sitePlanCheckBox.pack(fill='x', padx=30, pady=10)
        self.placeNodesCheckBox.pack(fill='x', padx=30, pady=10)
        self.optimiseCheckBox.pack(fill='x', padx=30, pady=10)
        self.analyseCheckBox.pack(fill='x', padx=30, pady=10)
        self.capacityDataCheckBox.pack(fill='x', padx=30, pady=10)
        self.simulateCheckBox.pack(fill='x', padx=30, pady=10)

        # the map container and to do container are placed side by side in the upper content frame
        self.mapContainer.grid(row=0, column=0, sticky='nsew', padx=(10, 5), pady=10)
        self.toDoContainer.grid(row=0, column=1, sticky='nsew', padx=(5, 10), pady=10)
        # the upper and lower content frames are placed vertically in the home page
        self.upperContentFrame.grid(row=0, column=0, sticky='nsew')
        self.lowerContentFrame.grid(row=1, column=0, sticky='nsew', padx=10, pady=(5, 10))

        # the home page is placed on the application, this is done as the home page is the default page when the user opens the app
        self.grid(row=0, column=1, sticky='nsew')

    def update(self):
        # resets the canvas
        self.canvas.delete('all')
        
        # logic to indicate to the user if they have added data by placing or removing a peice of text from the canvas that says 'no data'
        # also sets the checkbox to the correct state
        if self.master.dataAdded.get() == True:
            self.noData = False
            self.canvas.display()
            self.sitePlanCheckBox.select()
        else:
            self.noData = True
            self.sitePlanCheckBox.deselect()

        if not self.noData:
            self.canvas.delete(self.noDataText)
        else:
            self.noDataText = self.canvas.create_text(300,200, text='No Data', font=('Excalifont',20))

        # resets the checkbox that indicates whether the user has placed nodes
        self.placeNodesCheckBox.deselect()
        # if the user has placed a node one of the values in the dictionary will not be (-1,-1) and hence the checkbox will be selected
        for coord in app.nodePositions.values():
            if coord != (-1,-1):
                self.placeNodesCheckBox.select()
                break

        # sets the checkbox to indicate to the user if they have ran the simulation
        if app.simulationRan == True:
            self.optimiseCheckBox.select()
        else:
            self.optimiseCheckBox.deselect()

class dataPoint(): # this class provides a blueprint for the pixels that are to be stored in the previousActions and redoActions lists
    def __init__(self, x, y, prevColour, colour, dragIndex):
       self.x = x
       self.y = y
       self.prevColour = prevColour
       self.colour = colour
       self.dragIndex = dragIndex

class inputDataPage(ctk.CTkFrame):
    def __init__(self,parent):
        super().__init__(parent)
        self.configure(bg_color='white', fg_color='white')

        # initialising the variables that will be used in the class
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

        # importing the images
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

        self.createWidgets()
        self.placeWidgets()

        # sets the pencil as the default tool when the page is opened
        self.handlePencilButtonClick()
    
    def createWidgets(self):
        # styling dictionary to avoid repeated code
        ButtonStyling = {
        'border_width':2,
        'border_color':'black',
        'text_color':'black',
        'font':('Excalifont',20),
        'fg_color':'white',
        'corner_radius':10
        }

        # setting up and defining the frames that will organise the content
        self.upperFrame = ctk.CTkFrame(self, bg_color='white', fg_color='white') # does not need a grid to be defined as using pack internally
        self.toolContainer = ctk.CTkFrame(self.upperFrame, bg_color='white', fg_color='white')
        self.toolContainer.rowconfigure((0,1,2,3,4,5,6), weight=1)
        self.toolContainer.rowconfigure(7, weight=3)
        self.toolContainer.rowconfigure((8,9), weight=1)
        self.toolContainer.columnconfigure((0,1), weight=1)

        # creating the widgets that will be placed in the tool container
        # *the self.after() method is used in each of the commands to get around the default behaviour of the buttons
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
        # this padder is used to ensure the buttons are not stretched to fill the space
        self.padder = ctk.CTkFrame(self.toolContainer, bg_color='white', fg_color='white')

        # creating the canvas for the user to draw on as well as the frame that it sits in for aesthetic purposes
        self.mapContainer = ctk.CTkFrame(self.upperFrame, corner_radius=15, border_color='black', border_width=5, bg_color='white', fg_color='white')
        self.canvas = Canvas(parent=self.mapContainer, width=960, height=640)

        # this button is styled differently than the others so cannot shared the button stlying dictionary
        self.capacityButton = ctk.CTkButton(self, text='Input Capacity Data', border_width=2, border_color='black', text_color='black', fg_color='white', corner_radius=10, font=('Excalifont',20), width=300, command=lambda: self.after(100, self.handleCapacityButtonClick))
        
        # will call the handleDrawing function when either the user clicks or clicks and drags the mouse
        self.canvas.bind('<Button>', lambda event: self.handleDrawing(event=event, drag=False))
        self.canvas.bind('<B1-Motion>', lambda event: self.handleDrawing(event=event, drag=True))

        # setting up the hover effects for the buttons
        # could use a helper function here but it would end up being less programatically efficient with the amount of changing variables
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

        # using a helper function to define the hover behaviour for these buttons
        self.configureTextButtons(self.clearCanvasButton)
        self.configureTextButtons(self.doneButton)
        self.configureTextButtons(self.capacityButton)

        # these two widgets use custom classes to allow for more complex designs
        self.overwriteWarning = overwriteWarning(self)
        self.capacityDataPage = capacityDataInput(self)

    def placeWidgets(self):
        # placing the mapcontainer and tool container frames side by side
        self.mapContainer.pack(pady=(10,0), side='left')
        self.toolContainer.pack(side='left', fill='both', expand=True, pady=(10,0))

        # the widgets in the toolcontainer are placed using the grid method to allow them to be 2 by 2
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

        self.canvas.pack(pady=10, padx=10)
        self.upperFrame.pack(fill='both', expand=True)

        # the capacity button is placed directly on the page with the upperFrame above it
        self.capacityButton.pack(pady=10)

    def configureTextButtons(self, button): # helper function to set the colours when the button is hovered over
        button.bind('<Enter>', lambda event: button.configure(text_color='white', fg_color='black'))
        button.bind('<Leave>', lambda event: button.configure(text_color='black', fg_color='white'))

    def handleDrawing(self, event, drag): # this function is called when the user clicks or clicks and drags the mouse
        # converts the x and y coordinates of the mouse to the corresponding pixel on the canvas
        x = event.x // self.canvas.pixelSize
        y = event.y // self.canvas.pixelSize

        # the selection is used to avoid unnecesarilly drawing the same pixel multiple times
        if x != self.previousActions[-1].x or y != self.previousActions[-1].y or self.currentTool != self.previousActions[-1].colour:
            if drag != True: # drag is used so that undo and redo can be handled correctly for a single dragged line
                self.dragIndex += 1
            if self.canvas.matrix[y][x]['base'] > 1: # if the pixel is a node it will be removed and the node will be available again
                self.nodes[self.canvas.matrix[y][x]['base']] = True
                app.nodePositions[self.canvas.matrix[y][x]['base']] = (-1, -1) # sets the node position to (-1,-1) to indicate it is not placed
                self.bullseyeButton.configure(state='normal') # if the bullseye was disabled in the case of no nodes left it will be re-enabled
            if self.currentTool < 2 or self.nodes[self.currentTool] == True: # if the current tool is a pencil or eraser or the node is available
                # the pixel is drawn on the canvas and the previous action is stored in the previousActions list to allow for undo and redo
                self.previousActions.append(dataPoint(x, y, self.canvas.matrix[y][x]['base'], self.currentTool, self.dragIndex))
                self.canvas.creation(x,y,self.currentTool,False)
            if self.currentTool > 1: # if the current tool is a node
                self.nodes[self.currentTool] = False # the node is set to unavailable
                app.nodePositions[self.currentTool] = (x,y) # the position of the node is stored in the app wide variable
                for node, available in self.nodes.items(): # if there are no nodes left the bullseye button will be disabled
                    if available == True:
                        self.currentTool = node
                        break
                    elif node == 7:
                        self.noNodesLeft()
        if self.master.dataAdded.get() == True: # if the user has added data the checkbox will be selected
            self.planInserted = True

    def handleLineClick(self, event):
        # converting the x and y coordinates of the mouse to the corresponding pixel on the canvas
        x = event.x // self.canvas.pixelSize
        y = event.y // self.canvas.pixelSize

        if self.drawingLine: # if a line has been started when the button is clicked the line will be ended
            self.lineEnd = (x,y)
            self.drawingLine = False # the line is no longer being drawn
            self.dragIndex += 1 # the drag index is increased to allow for undo and redo to undo and redo the whole line
            lineData = self.drawLine(self.lineStart, (x,y), False) # the line is drawn on the canvas
            self.previousActions += lineData # the line data returned from the drawLine function is added to the previousActions list
        else: # if the line has not been started then we start it
            self.lineStart = (x,y) # the start of the line is stored
            self.drawingLine = True # the line is being drawn

    def handleLineDrawing(self, event):
        # converting the x and y coordinates of the mouse to the corresponding pixel on the canvas
        x = event.x // self.canvas.pixelSize
        y = event.y // self.canvas.pixelSize

        # if a line is being drawn the old lines pixels are removed and the line is redrawn with the new end point
        if self.drawingLine:
            for pixel in self.tempPixels:
                self.canvas.delete(pixel)
            # the draw line function returns the pixels drawn so that if the line needs to be deleted it can be done so easily
            self.tempPixels = self.drawLine(self.lineStart, (x,y), self.drawingLine)

    def drawLine(self, start, end, lineSubmitted):
        lineData = []
        if abs(end[0] - start[0]) > abs(end[1] - start[1]): # if the line is more horizontal than vertical
            lineData = self.drawHorizontalLine(start[0], start[1], end[0], end[1], lineSubmitted)
        else: # if the line is more vertical than horizontal
            lineData = self.drawVerticalLine(start[0], start[1], end[0], end[1], lineSubmitted)
        return lineData
    
    def drawHorizontalLine(self, x0, y0, x1, y1, lineSubmitted): # Bresenhams line algorithm *explained in the report*
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
                    lineData.append(dataPoint(x0 + i, y, self.canvas.matrix[y][x0 + i]['base'], 0, self.dragIndex))
                pixelID = self.canvas.creation(x0 + i, y, 0, lineSubmitted)
                if lineSubmitted:
                    lineData.append(pixelID)
                if p >= 0:
                    y += direction
                    p = p - 2 * dx
                p = p + 2 * dy
        return lineData

    def drawVerticalLine(self, x0, y0, x1, y1, lineSubmitted): # Bresenhams line algorithm *explained in the report*
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
                    lineData.append(dataPoint(x, y0 + i, self.canvas.matrix[y0 + i][x]['base'], 0, self.dragIndex))
                pixelID = self.canvas.creation(x, y0 + i, 0, lineSubmitted)
                if lineSubmitted:
                    lineData.append(pixelID)
                    
                if p >= 0:
                    x += direction
                    p = p - 2 * dy
                p = p + 2 * dx
        
        return lineData

    def handleCapacityButtonClick(self):
        # handles the hover behaviour as well as deselecting the current tool to avoid user accidentally drawing/erasing
        self.deselectCurrentButton()
        self.capacityButton.configure(text_color='white', fg_color='black')

        # if the pages is not open it will be opened and vice versa
        if self.capacityInputOpen:
            self.capacityDataPage.place_forget() # hides the capacity data page
            self.capacityButton.configure(text='Input Capacity Data') # restores the default text of the capacity button
            # calls a method from the capacityDataPage class to get the values and stores them in the app wide variable
            app.capacityValues = self.capacityDataPage.getValues()
            self.capacityInputOpen = False # sets the boolean to false to indicate the page is closed
        else:
            # calls a method from the capacityDataPage class to refresh the page so that it will update as the user draws/removes nodes
            self.capacityDataPage.refresh()
            self.capacityDataPage.place(x = 200, y = 350) # places the capacity data page in the correct position
            self.capacityButton.configure(text='Done') # changes the text of the capacity button so that the user clicks this when finished to close the page
            self.capacityInputOpen = True # sets the boolean to true to indicate the page is open

    def handlePencilButtonClick(self):
        self.deselectCurrentButton()
        # the border of a button thickens when selected to indicate the button selected
        self.pencilButton.configure(text_color='black', fg_color='white', image=self.blackPencil, border_width=4)
        self.pencilButton.grid_configure(pady=2) # the external padding is reduced to avoid the buttons shifting when the border width is increased

        self.currentTool = 0 # the current tool is set to 0 to indicate the pencil is selected

        # the event bindings are set so that the canvas will draw when the user clicks or clicks and drags the mouse
        self.canvas.bind('<Button>', lambda event: self.handleDrawing(event=event, drag=False))
        self.canvas.bind('<B1-Motion>', lambda event: self.handleDrawing(event=event, drag=True))
        self.canvas.unbind('<Motion>')

    def handleEraserButtonClick(self):
        self.deselectCurrentButton()
        # indicating the button has been selected
        self.eraserButton.configure(text_color='white', fg_color='black', image=self.blackEraser, border_width=4)
        self.eraserButton.grid_configure(pady=2)

        self.currentTool = 1 # setting the current tool to 1 to indicate the eraser is selected

        # setting the event bindings so that the canvas will erase when the user clicks or clicks and drags the mouse
        self.canvas.bind('<Button>', lambda event: self.handleDrawing(event=event, drag=False))
        self.canvas.bind('<B1-Motion>', lambda event: self.handleDrawing(event=event, drag=True))
        self.canvas.unbind('<Motion>')

    def handleLineButtonClick(self): 
        self.deselectCurrentButton()
        # indicating the button has been selected
        self.lineButton.configure(text_color='white', fg_color='black', image=self.blackLine, border_width=4)
        self.lineButton.grid_configure(pady=2)

        # changing the event bindings so that that user does not have to drag to draw a line and will call a different function
        self.canvas.unbind('<B1-Motion>')
        self.canvas.bind('<Motion>', lambda event: self.handleLineDrawing(event))
        self.canvas.bind('<Button>', lambda event: self.handleLineClick(event))

    def handleBullseyeButtonClick(self):
        self.deselectCurrentButton()
        # indicating the button has been selected
        self.bullseyeButton.configure(text_color='white', fg_color='black', image=self.blackBullseye, border_width=4)
        self.bullseyeButton.grid_configure(pady=2)

        for node, available in self.nodes.items(): # sets the current tool to the next available node
            if available == True:
                self.currentTool = node
                break
        
        # restores the default canvas bindings so that the user can draw nodes
        self.canvas.bind('<Button>', lambda event: self.handleDrawing(event=event, drag=False))
        self.canvas.bind('<B1-Motion>', lambda event: self.handleDrawing(event=event, drag=True))
        self.canvas.unbind('<Motion>')

    def handleUndoButtonClick(self):
        self.deselectCurrentButton()
        self.undoButton.configure(text_color='white', fg_color='black', image=self.blackUndo)
        
        while self.previousActions: # while there are previous actions to undo
            previousAction = self.previousActions.pop() # the last action is removed from the previousActions list

            # storing the data of the previous action in local variables
            x = previousAction.x
            y = previousAction.y
            colourValue = previousAction.prevColour
            dragIndex = previousAction.dragIndex + 1

            if colourValue > 1 and self.nodes[colourValue] == True: # if the pixel was a node and the node is still available
                self.nodes[colourValue] = False # the node is set to unavailable
                app.nodePositions[colourValue] = (x,y) # the position of the node is stored in the app wide variable
            elif colourValue > 1 and self.nodes[colourValue] == False: # if the pixel was a node and the node is not available we avoid running any more code
                break

            if self.canvas.matrix[y][x]['base'] > 1: # if there was a node at the position that will be replaced by a previous action
                self.nodes[self.canvas.matrix[y][x]['base']] = True # the node is set to available
                app.nodePositions[self.canvas.matrix[y][x]['base']] = (-1, -1) # the position of the node is set to (-1,-1) to indicate it is not placed
                self.bullseyeButton.configure(state='normal') # if the bullseye button was disabled it will be re-enabled

            # we store the previous state of the pixel in the redoActions list so that the action can be redone
            self.redoActions.append(dataPoint(x, y, self.canvas.matrix[y][x]['base'], colourValue, dragIndex))
            self.canvas.creation(x,y,colourValue,False) # the pixel is drawn on the canvas

            # if the list is empty or the next action is not part of the same drag we break the loop
            if not self.previousActions or self.previousActions[-1].dragIndex != previousAction.dragIndex:
                break

    def handleRedoButtonClick(self):
        self.deselectCurrentButton()
        self.redoButton.configure(text_color='white', fg_color='black', image=self.blackRedo)

        while self.redoActions: # while there are actions to redo
            redoAction = self.redoActions.pop() # the last action is removed from the redoActions list

            # storing the data of the redo action in local variables
            x = redoAction.x
            y = redoAction.y
            colourValue = redoAction.prevColour
            dragIndex = redoAction.dragIndex + 1

            if colourValue > 1 and self.nodes[colourValue] == True: # if the pixel was a node and the node is available
                self.nodes[colourValue] = False # the node is set to unavailable
                app.nodePositions[colourValue] = (x,y) # the position of the node is stored in the app wide variable
            elif colourValue > 1 and self.nodes[colourValue] == False: # if the pixel was a node and the node is not available we avoid running any more code
                break

            if self.canvas.matrix[y][x]['base'] > 1: # if there was a node at the position that will be replaced by a redo action
                self.nodes[self.canvas.matrix[y][x]['base']] = True # the node is set to available
                app.nodePositions[self.canvas.matrix[y][x]['base']] = (-1, -1)  # the position of the node is set to (-1,-1) to indicate it is not placed

            # we store the previous state of the pixel in the previousActions list so that the action can be undone
            self.previousActions.append(dataPoint(x, y, self.canvas.matrix[y][x]['base'], colourValue, dragIndex))
            self.canvas.creation(x,y,colourValue, False) # the pixel is drawn on the canvas

            # if the list is empty or the next action is not part of the same drag we break the loop
            if not self.redoActions or self.redoActions[-1].dragIndex != redoAction.dragIndex: 
                break

    def handleClearButtonClick(self):
        self.deselectCurrentButton()
        self.clearCanvasButton.configure(text_color='white', fg_color='black')
        # items on the canvas are deleted
        self.canvas.delete('all')

        # the matrix storing the pixel data is reset to the default state
        for y in range(len(self.canvas.matrix)):
            for x in range(len(self.canvas.matrix[y])):
                self.canvas.matrix[y][x]['base'] = 1

        # the nodes are reset to available and their positions are reset
        for node in self.nodes.keys():
            self.nodes[node] = True
            app.nodePositions[node] = (-1, -1)

        # if the bullseye button was disabled it will be re-enabled
        self.bullseyeButton.configure(state='normal')
        self.planInserted = False # the planInserted boolean is set to false to indicate no data has been added

    def handleDoneButtonClick(self): 
        self.deselectCurrentButton()
        self.doneButton.configure(text_color='white', fg_color='black')

        # the planInserted boolean has to be used seperate to the dataAdded boolean so that if a user clears
        # the canvas without pressing the done button it does not clear across the application
        if self.planInserted == True:
            self.master.dataAdded.set(True) # the dataAdded boolean is set to true to indicate data has been added
        else:
            self.master.dataAdded.set(False) # if the canvas has been cleared and done button pressed dataAdded is set to false
            app.simulationRan = False # also resets whether the simulation has been ran

        # copies the matrix from the input data page to the app wide matrix, deepcopy is used to avoid the two variables being linked
        self.master.matrix = copy.deepcopy(self.canvas.matrix)
        # calls a method from the optimisePlanPage class to display the available nodes when the user is choosing a node
        self.master.optimisePlanPage.packAvailableNodes()

    def handleSaveButtonClick(self): # this function saves the canvas data to a json file
        self.deselectCurrentButton()
        self.saveButton.configure(text_color='white', fg_color='black')

        filePath = filedialog.asksaveasfilename() # opens a file dialog to allow the user to choose a file to save to
        filePath += '.json' # adds the file extension to the file name
        self.master.matrix = copy.deepcopy(self.canvas.matrix) # copies the matrix from the input data page to the app wide matrix
        with open(filePath, 'w') as file: # opens the file in write mode
            json.dump(self.canvas.matrix, file, indent=None) # writes the matrix to the file

    def handleOpenFileButtonClick(self):
        self.deselectCurrentButton()
        self.openFileButton.configure(text_color='white', fg_color='black')

        # opens a file dialog to allow the user to choose a file to open
        self.filePath = filedialog.askopenfilename(initialdir='/temp', title='Choose File', filetypes=[('json Files', '*.json')])
        if self.master.dataAdded.get() == True: # if there is already data there it will warn the user and give the option to cancel
            self.overwriteWarning.place(x = 300, y = 250) # places the custom class warning on the page
        else:
            self.readFile() # if there is no data it will read the file

    def readFile(self):
        with open(self.filePath, 'r') as file: # opens the file in read mode
            self.canvas.matrix = json.load(file) # loads the matrix from the file into the input data page matrix
            self.master.dataAdded.set(True) # sets the dataAdded boolean to true to indicate data has been added
            self.master.matrix = copy.deepcopy(self.canvas.matrix) # copies the matrix from the input data page to the app wide matrix
            self.canvas.display() # displays the data from the file on the canvas

    def noNodesLeft(self): # function to disable the bullseye button when there are no nodes left
        self.currentTool = 0
        self.bullseyeButton.configure(state='disabled')
        self.deselectCurrentButton()

    def deleteTemporarySquares(self, squareIDs): # function to delete the temporary squares drawn when drawing a line
        for squareID in squareIDs:
            self.canvas.delete(squareID)

    def deselectCurrentButton(self): # function to restore the default look of the buttons
        self.pencilButton.configure(border_width=2)
        self.eraserButton.configure(border_width=2)
        self.lineButton.configure(border_width=2)
        self.bullseyeButton.configure(border_width=2)
        self.pencilButton.grid_configure(pady=4)
        self.eraserButton.grid_configure(pady=4)
        self.lineButton.grid_configure(pady=4)
        self.bullseyeButton.grid_configure(pady=4)

        # restores the default event bindings of the canvas as the line drawing button uses different bindings
        self.canvas.bind('<Button>', lambda event: self.handleDrawing(event=event, drag=False))
        self.canvas.bind('<B1-Motion>', lambda event: self.handleDrawing(event=event, drag=True))
        self.canvas.unbind('<Motion>')
    
class optimisePlanPage(ctk.CTkFrame):
    def __init__(self,parent):
        super().__init__(parent)
        self.configure(bg_color='white', fg_color='white')

        # the following variables are used for the function of this page
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

        # the following constants are used in the flow simulation algorithm
        self.WALKING_PACE = 1.4
        self.DISTANCE_BETWEEN_PEOPLE = 0.6
        self.PEOPLE_PER_METRE = 2
        self.PEOPLE_PER_SECOND_PER_METRE = self.WALKING_PACE * self.PEOPLE_PER_METRE / self.DISTANCE_BETWEEN_PEOPLE
        
        # creating and placing the widgets on the page
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

        # importing the images for the buttons that allow the user to choose which node they want
        self.fire = CTkImage(light_image=Image.open('assets/fire.png'))
        self.red = CTkImage(light_image=Image.open('assets/red.png'))
        self.blue = CTkImage(light_image=Image.open('assets/blue.png'))
        self.green = CTkImage(light_image=Image.open('assets/green.png'))
        self.orange = CTkImage(light_image=Image.open('assets/orange.png'))
        self.pink = CTkImage(light_image=Image.open('assets/pink.png'))
        self.yellow = CTkImage(light_image=Image.open('assets/yellow.png'))

        # creating and defining the organistational components of the page
        self.upperFrame = ctk.CTkFrame(self, bg_color='white', fg_color='white')
        self.rightFrame = ctk.CTkFrame(self.upperFrame, bg_color='white', fg_color='white')
        self.rightFrame.columnconfigure(0, weight=1)
        self.rightFrame.rowconfigure((0,1), weight=1)
        self.rightFrame.rowconfigure(2, weight=3)
        self.rightFrame.rowconfigure((3,4,5), weight=1)
        self.padder = ctk.CTkFrame(self.rightFrame, bg_color='white', fg_color='white')

        # creating the widgets that will be placed on the page
        self.evacPointLabel = ctk.CTkLabel(self.rightFrame, text='Evac\nPoint', font=('Excalifont',20), text_color='black')
        self.evacPointButton = ctk.CTkButton(self.rightFrame, text='', **ButtonStyling, command=lambda:self.after(100, self.handleEvacPointClick), image=self.fire)
        self.chooseNodeLabel = ctk.CTkLabel(self.rightFrame, text='Choose\nNode', font=('Excalifont',20), text_color='black')
        self.chooseNodeButton = ctk.CTkButton(self.rightFrame, text='', **ButtonStyling, command=lambda:self.after(100, self.handleChooseNodeClick), image=self.fire)
        self.runButton = ctk.CTkButton(self.rightFrame, text='Run', **ButtonStyling, command=lambda: self.after(100, self.handleRunButtonClick))
        self.scrollFrame = ctk.CTkScrollableFrame(self.rightFrame, bg_color='white', fg_color='white')
        self.canvasContainer = ctk.CTkFrame(self.upperFrame, corner_radius=15, border_color='black', border_width=5, bg_color='white', fg_color='white')
        self.canvas = Canvas(parent=self.canvasContainer, width=960, height=640)
        self.showAllPaths = ctk.CTkButton(self, text='Show all Paths', **ButtonStyling, command=lambda: self.after(100, self.handleShowAllPathsClick))
        self.simulateEvent = ctk.CTkButton(self, text='Simulate Event', **ButtonStyling, command=lambda: self.after(100, self.handleSimulateEventClick), state='disabled')
        self.timeLabel = ctk.CTkLabel(self, text='Time: ---', text_color='black')
        self.timeSlider = ctk.CTkSlider(self, from_=0, to=100, command=self.updateTimeLabel, state='disabled')

        # helper function to define the hovering behaviour for these buttons
        self.handleHovering(self.evacPointButton)
        self.handleHovering(self.chooseNodeButton)
        self.handleHovering(self.runButton)
        self.handleHovering(self.showAllPaths)
        self.handleHovering(self.simulateEvent)

        # could have reused the ButtonStyling dictionary but this means we dont have to set the master and text on each button
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

        # creating the buttons that will be placed in the scrollable frame
        self.redButton = ctk.CTkButton(**ButtonConfig, image=self.red, command=lambda: self.after(100, self.handleNodeChoiceButtonClick(self.redButton)))
        self.blueButton = ctk.CTkButton(**ButtonConfig, image=self.blue, command=lambda: self.after(100, self.handleNodeChoiceButtonClick(self.blueButton)))
        self.greenButton = ctk.CTkButton(**ButtonConfig, image=self.green, command=lambda: self.after(100, self.handleNodeChoiceButtonClick(self.greenButton)))
        self.orangeButton = ctk.CTkButton(**ButtonConfig, image=self.orange, command=lambda: self.after(100, self.handleNodeChoiceButtonClick(self.orangeButton)))
        self.pinkButton = ctk.CTkButton(**ButtonConfig, image=self.pink, command=lambda: self.after(100, self.handleNodeChoiceButtonClick(self.pinkButton)))
        self.yellowButton = ctk.CTkButton(**ButtonConfig, image=self.yellow, command=lambda: self.after(100, self.handleNodeChoiceButtonClick(self.yellowButton)))
    
        # creating a dictionary to store the buttons and their corresponding node values for easy access
        self.Buttons={self.redButton:2, self.blueButton:3, self.greenButton:4, self.orangeButton:5, self.pinkButton:6, self.yellowButton:7}
        
        for button in self.Buttons.keys(): # binding the hover behaviour to the buttons
            button.bind('<Enter>', lambda event, b=button: self.buttonEnter(b))
            button.bind('<Leave>', lambda event, b=button: self.buttonLeave(b))
    
    def placeWidgets(self): # placing the widgets on the page
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

    def handleHovering(self,button): # helper function to set the colours when the button is hovered over
        button.bind('<Enter>', lambda event: button.configure(text_color='white', fg_color='black'))
        button.bind('<Leave>', lambda event: button.configure(text_color='black', fg_color='white'))

    def buttonEnter(self,button): # sets the hover behaviour to thicken the border of the button when hovered over
        button.configure(border_width=4)
        button.pack_configure(pady=0)

    def buttonLeave(self,button): # sets the behaviour when the user stops hovering over the button so the button returns to normal thickness
        button.configure(border_width=2)
        button.pack_configure(pady=2)

    def astar(self, startNode, endNode): # A* algorithm *will be explained in the report*
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

    def reconstructPath(self, previousNodes, start, current, startNode): # function to reconstruct the path from the A* algorithm *explained in the report*
        while current in previousNodes:
            current = previousNodes[current]
            if current != start:
                self.canvas.creation(current[0], current[1], startNode+10, False)
                self.paths[startNode+10].append(current)
    
    def heuristic(self, point1, point2): # function to calculate the heuristic for the A* algorithm *explained in the report*
        x1, y1 = point1
        x2, y2 = point2
        return abs(x1 - x2) + abs(y1 - y2)

    def runFlowSimulation(self): # function to run the flow simulation algorithm *explained in the report*
        problems = []
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
                            else:
                                pathWidth += tempCount
                                break
                        else:
                            pathWidth += tempCount
                        tempCount  = 0
                        while tempCount < app.capacityValues[path - 10] / self.PEOPLE_PER_SECOND_PER_METRE:
                            if position[1] - tempCount > 0 and self.canvas.matrix[position[1] - tempCount - 1][position[0]]['base'] != 0:
                                tempCount += 1
                            else:
                                pathWidth += tempCount
                                break
                        else:
                            pathWidth += tempCount
                    elif position[0] < 119 and path not in self.canvas.matrix[position[1]][position[0] + 1].get('paths', []) and position[0] > 0 and path not in self.canvas.matrix[position[1]][position[0] - 1].get('paths', []): # path vertical
                        tempCount  = 0
                        while tempCount < app.capacityValues[path - 10] / self.PEOPLE_PER_SECOND_PER_METRE:
                            if position[0] + tempCount < 119 and self.canvas.matrix[position[1]][position[0] + tempCount + 1]['base'] != 0:
                                tempCount += 1
                            else:
                                pathWidth += tempCount
                                break
                        else:
                            pathWidth += tempCount
                        tempCount  = 0
                        while tempCount < app.capacityValues[path - 10] / self.PEOPLE_PER_SECOND_PER_METRE:
                            if position[0] - tempCount > 0 and self.canvas.matrix[position[1]][position[0] - tempCount - 1]['base'] != 0:
                                tempCount += 1
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

                    people = 0

                    for group in self.canvas.matrix[position[1]][position[0]].get('paths', []):
                        people += app.capacityValues[group - 10]
                        
                    pathWidths.append((position, pathWidth))

                desiredFlow = people / self.timeSlider.get()
                minWidth = desiredFlow / self.PEOPLE_PER_SECOND_PER_METRE

                pathWidths.sort(key=lambda element: element[1] / minWidth)

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

    def findNearestWall(self, corner, direction): # function to find the nearest wall to a given position *explained in the report*
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

    def calculateDistance(self, corner, wall): # calculates the distance between the passed in coordinates for corner and wall
        return math.sqrt(abs(corner[0]-wall[0]) ** 2 + abs(corner[1]-wall[1]) ** 2)
    
    def drawLine(self, start, end): # function to draw a line between two points *explained in the report*
        tempPixels = []
        if abs(end[0] - start[0]) > abs(end[1] - start[1]):
            tempPixels = self.drawHorizontalLine(start[0], start[1], end[0], end[1])
        else:
            tempPixles = self.drawVerticalLine(start[0], start[1], end[0], end[1])
        return tempPixels
    
    def drawHorizontalLine(self, x0, y0, x1, y1): # Bresenhams line algorithm *explained in the report*
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

    def drawVerticalLine(self, x0, y0, x1, y1): # Bresenhams line algorithm *explained in the report*
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

    def handleRunButtonClick(self): # called when the search is run for one path
        self.runButton.configure(text_color='black', fg_color='white')
        self.disableAllButtons()

        if self.evacPoint != -1 and self.startNode != -1: # if the user has selected a start and end node
            self.astar(self.startNode, self.evacPoint) # run the A* algorithm to find the path
            self.timeSlider.configure(state='normal') # the slider is enabled as the user can now run a simulation
            self.simulateEvent.configure(state='normal') # the simulate event button is enabled

        self.enableAllButtons()
        self.setMinimumTime() # sets the minimum time on the slider
        app.simulationRan = True # sets the simulationRan boolean to true to indicate the simulation has been run on the home page
    
    def handleShowAllPathsClick(self): # this is called when the user wants to run all the paths at once
        self.showAllPaths.configure(text_color='white', fg_color='black')
        self.disableAllButtons()

        if self.evacPoint != -1: # if the user has selected an evac point
            for node in app.nodePositions.keys(): # for each node that is not the evac point
                if app.nodePositions[node] != (-1,-1) and node != self.evacPoint:
                    self.astar(node, self.evacPoint) # run the A* algorithm to find the path
            # enable to button and set the minimum time on the slider
            self.timeSlider.configure(state='normal')
            self.simulateEvent.configure(state='normal')
            self.setMinimumTime()
        self.enableAllButtons()
        app.simulationRan = True

    def handleSimulateEventClick(self):
        self.disableAllButtons()
        self.simulateEvent.configure(text_color='white', fg_color='black')
        self.runFlowSimulation() # runs the flow simulation algorithm
        self.enableAllButtons()

    def handleEvacPointClick(self):
        self.evacPointButton.configure(text_color='black', fg_color='white') # resets the button to the default appearance when clicked
        self.startOrEndNode = "end" # sets the start or end node to end so that we can reuse the code for the buttons on the scrollable frame
        
        # if the node chooser is not open then we pop up a scrollable frame containing the buttons for the nodes
        if not self.nodeChooserOpen:
            self.nodeChooser()
        else: # if the node chooser is open then we hide the scrollable frame
            self.scrollFrame.grid_forget()
            self.nodeChooserOpen = False

    def handleChooseNodeClick(self):
        self.chooseNodeButton.configure(text_color='black', fg_color='white') # resets the button to the default appearance when clicked
        self.startOrEndNode = "start" # sets the start or end node to start so that we can reuse the code for the buttons on the scrollable frame
        
        # if the node chooser is not open then we pop up a scrollable frame containing the buttons for the nodes
        if not self.nodeChooserOpen:
            self.nodeChooser() 
        else: # if the node chooser is open then we hide the scrollable frame
            self.scrollFrame.grid_forget()
            self.nodeChooserOpen = False

    def handleNodeChoiceButtonClick(self,button):
        grey = "#AAAFB4"

        if self.startOrEndNode == "start": # depends on which button was clicked evac point or start node
            self.startNode = self.Buttons[button] # sets the start node to the value assigned to the button
        else:
            self.evacPoint = self.Buttons[button]
        button.configure(state='disabled', fg_color=grey) # disables the button so the user cannot set the start and the end node as the same
        
        # resets the buttons that are not the evac point or the start node so the user can change their selection if they need to
        for button, value in self.Buttons.items():
            if value != self.evacPoint and value != self.startNode:
                button.configure(state='normal', fg_color='white')
        
        self.setButtonImages()
        self.scrollFrame.grid_forget() # hides the scrollable frame once the user has selected a node
        self.nodeChooserOpen = False
    
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

    def setButtonImages(self): # sets the images of the evac and start buttons based on the user selection
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
    
    def resetButtons(self): # resets and removes all the buttons from the scrollable frame as well as resetting the evac and start node values
        for button in self.Buttons.keys():
            button.configure(state='enabled', fg_color='white')
            button.pack_forget()
        self.evacPoint = -1
        self.startNode = -1
        self.setButtonImages() # sets the images of the evac and start buttons back to the fire icon
    
    def deleteTemporarySquares(self, squareIDs):
        for squareID in squareIDs:
            self.canvas.delete(squareID)

    def packAvailableNodes(self): # this function chooses which nodes will be available in the scrollable frame so we only show nodes the user can select
        self.resetButtons()
        # for each button in the dictionary of buttons we check if the node is available and if it is we pack the button
        for button, node in self.Buttons.items():
            if app.nodePositions[node] != (-1,-1):
                button.pack(pady=2)

    def nodeChooser(self):
        self.scrollFrame.grid(column=0, row=2, sticky='nsew') # places the node chooser on the page
        self.nodeChooserOpen = True

    def updateTimeLabel(self, value): # function to update the time label when the slider is moved
        formattedValue = f'{int(value):03}' # formatting the value to be 3 digits long so that the interface doesnt shift
        self.timeLabel.configure(text=f'Time: {formattedValue}') # updating the text of the label

    def setMinimumTime(self):
        minTime = 0
        for path in self.paths.values():
            if len(path) / self.WALKING_PACE > minTime: # if the time to evacuate is greater than the current minimum time it will be set as the minimum time
                minTime = math.ceil(len(path) / self.WALKING_PACE)
        self.timeSlider.configure(from_=minTime, to=300) # the slider is updated to have the minimum time as the minimum value

class Canvas(ctk.CTkCanvas):
    def __init__(self, parent, height, width):
        super().__init__(parent)
        # the canvas is configurable to different sizes depending on which page its on
        self.configure(height=height, width=width, bd=0, background='white', highlightthickness=0)
        self.pixelSize = height // 80 # calculates the size of each canvas pixel in pixels
        self.matrix = [[{'base': 1} for _ in range(120)] for _ in range(80)] # list comprehension to initialize the matrix with the base value of 1
        
    def creation(self, x, y, colourValue, temporary):
        # defining custom colours
        red = '#ff0000'
        blue = '#0010ff'
        green = '#00ff7c'
        orange = '#ffa300'
        pink = '#ff00cf'
        yellow = '#fffc00'
        purple = '#800080'
        darkPurple = '#320032'

        match colourValue: # setting the colour based on the colour value passed in so we can reuse the function for different colours
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

        if not temporary: # temporary is a parameter that effects whether the pixel will have its id recorded for deletion later if it is temporary
            # the create_rectangle function takes in coordinates of the top left of the rectangle and the bottom right as well as the fill and outline colours
            # pixelsize is in pixels so to get a pixel at a specific coordinate we multiply the coordinate by the pixel size
            self.create_rectangle((self.pixelSize * (x+1) - self.pixelSize, self.pixelSize * (y+1) - self.pixelSize, self.pixelSize * (x+1) - 1, self.pixelSize * (y+1) - 1), fill=colour, outline=colour)
            if colourValue < 12: # if the colour value is less than 12 then we set the base value of the pixel to the colour value
                self.matrix[y][x]['base'] = colourValue
            else: # if the colour value is greater than 12 then we are drawing a path so set the path value instead of the base
                self.matrix[y][x].setdefault('paths', []).append(colourValue)
        else: # if the pixel is temporary then we return the id of the pixel so we can delete it later
            # also do not need to worry about the colour value being greater than 12 here as we dont draw temporary paths
            squareID = self.create_rectangle((self.pixelSize * (x+1) - self.pixelSize, self.pixelSize * (y+1) - self.pixelSize, self.pixelSize * (x+1) - 1, self.pixelSize * (y+1) - 1), fill=colour, outline=colour)
            return squareID

    def display(self):
        # defining custom colours
        red = '#ff0000'
        blue = '#0010ff'
        green = '#00ff7c'
        orange = '#ffa300'
        pink = '#ff00cf'
        yellow = '#fffc00'
        purple = '#800080'
        darkPurple = '#320032'

        # resets the canvas so we can redraw the matrix
        self.delete('all')

        # for each pixel in the matrix we draw a square with the colour based on the base value of the pixel
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

        # creating the widgets for the warning frame
        self.warningLabel = ctk.CTkLabel(self, text='Are you sure you want to overwrite the data', text_color='black', font=('Excalifont',20))
        self.confirmButton = ctk.CTkButton(self, text='Confirm', **warnButtonStyling, command=lambda: self.after(100, self.handleconfirmButtonClick))
        self.cancelButton = ctk.CTkButton(self, text='Cancel', **warnButtonStyling, command=lambda: self.after(100, self.handlecancelButtonClick))

        # setting the hover behaviour for the buttons
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
        self.master.readFile() # calls the read file function on the parent frame if the user confirms they want to overwrite the data
        self.place_forget() # hides the warning frame

    def handlecancelButtonClick(self):
        self.cancelButton.configure(text_color='black', fg_color='white')
        self.place_forget() # hides the warning frame without overwriting the data

class capacityDataInput(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(height=200, width=400, corner_radius=15, border_color='black', border_width=5, bg_color='white', fg_color='white')
        self.values={2:-1,3:-1,4:-1,5:-1,6:-1,7:-1} # dictionary to store the values of the input capacity data
        self.createWidgets()
        self.placeWidgets()

    def createWidgets(self):
        # importing the images for the nodes
        self.red = CTkImage(light_image=Image.open('assets/red.png'))
        self.blue = CTkImage(light_image=Image.open('assets/blue.png'))
        self.green = CTkImage(light_image=Image.open('assets/green.png'))
        self.orange = CTkImage(light_image=Image.open('assets/orange.png'))
        self.pink = CTkImage(light_image=Image.open('assets/pink.png'))
        self.yellow = CTkImage(light_image=Image.open('assets/yellow.png'))

        self.titleLabel = ctk.CTkLabel(self, text='Input Capacity Data', text_color='black', font=('Excalifont',25))
        self.scrollFrame = ctk.CTkScrollableFrame(self, bg_color='white', fg_color='white')

        # creating the widgets for the input capacity data of each node based on the custom nodeWidget class
        self.redEntry = nodeWidget(self.scrollFrame, image=self.red)
        self.blueEntry = nodeWidget(self.scrollFrame, image=self.blue)
        self.greenEntry = nodeWidget(self.scrollFrame, image=self.green)
        self.orangeEntry = nodeWidget(self.scrollFrame, image=self.orange)
        self.pinkEntry = nodeWidget(self.scrollFrame, image=self.pink)
        self.yellowEntry = nodeWidget(self.scrollFrame, image=self.yellow)

        # dictionary to associate the entry widgets with the node values
        self.entries={self.redEntry:2, self.blueEntry:3, self.greenEntry:4, self.orangeEntry:5, self.pinkEntry:6, self.yellowEntry:7}
        
    def placeWidgets(self):
        self.titleLabel.pack(padx=200, pady=10)
        self.scrollFrame.pack(padx=10, pady=(0,10), expand=True, fill='both')

    def refresh(self):
        
        # removes all the entry widgets from the scrollable frame
        for entry in self.entries.keys():
            entry.pack_forget()

        # packs the entry widgets for the nodes that have been placed by the user
        for entry, node in self.entries.items():
            if app.nodePositions[node] != (-1,-1):
                entry.pack(pady=2)
    
    def getValues(self): # a method to get return the values of the input capacity data
        for entry, node in self.entries.items():
            self.values[node] = int(entry.getEntry() or -1)
        return self.values

class nodeWidget(ctk.CTkFrame):
    def __init__(self, parent, image):
        super().__init__(parent)
        self.configure(corner_radius=15, border_color='black', border_width=5, bg_color='white', fg_color='white')
        self.createWidgets(image) # we pass the image from the parent so we dont have to store all the images in each entry widget
        self.placeWidgets()

    def createWidgets(self, image):
        self.image = ctk.CTkLabel(self, image=image, text='')
        self.label = ctk.CTkLabel(self, text='Input Capacity', text_color='black', font=('Excalifont',20))
        self.entryField = ctk.CTkEntry(self, fg_color='white', text_color='black', font=('Excalifont',15), justify='center')
    
    def placeWidgets(self):
        self.image.pack(padx=(10,0), pady=10, side='left')
        self.label.pack(padx=10, pady=(10,0))
        self.entryField.pack(pady=10, padx=(10,20))

    def getEntry(self): # a method to get the value of the entry field
        return self.entryField.get()
 
if __name__ == '__main__': # runs the app if the file is run as the main file
    app = App()
    app.mainloop()