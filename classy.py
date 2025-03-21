import tkinter as tk
from tkinter import ttk, filedialog
import customtkinter as ctk
from customtkinter import CTkImage
from PIL import Image
import json
from queue import PriorityQueue
import copy
import math
import cv2
import numpy as np

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
        self.paths = {
            12:[],
            13:[],
            14:[],
            15:[],
            16:[],
            17:[]
        }
        self.bottlenecks = []
        self.dataAdded = ctk.BooleanVar(value=False)
        self.pathsFound = False
        self.bottlenecksFound = False
    
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
        self.master.inputDataPage.canvas.display(self.master.matrix, self.master.bottlenecks, False)
        self.after(100, lambda: self.inputDataButton.configure(text_color='black', fg_color='white')) # returns the button to its original state after 100ms

    def openOptimisePlanPage(self):
        self.master.showPage(self.master.optimisePlanPage) # calls the method in the app class to show the optimise plan page
        self.master.optimisePlanPage.canvas.display(self.master.matrix, self.master.bottlenecks, True) # refreshes the canvas to show any changes made to the plan
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
        self.warningTable.column('Index', width=100, anchor='center')
        self.warningTable.column('Type', width=250, anchor='center')
        self.warningTable.column('Extra Information', width=400, anchor='center')
        # initialising the headings of the table
        self.warningTable.heading('Index', text='Index', anchor='center')
        self.warningTable.heading('Type', text='Type', anchor='center')
        self.warningTable.heading('Extra Information', text='Extra Information', anchor='center')
        self.warningTable.bind('<<TreeviewSelect>>', self.warningSelected)

        style = ttk.Style()
        style.configure("Treeview", font=('Excalifont',10))
        style.configure("Treeview.Heading", font=('Excalifont',15))

        # creating the widgets that will be placed in the upper content frame
        self.mapContainer = ctk.CTkFrame(self.upperContentFrame, corner_radius=15, border_color='black', border_width=5, bg_color='white', fg_color='white')
        self.canvas = Canvas(parent=self.mapContainer, width=600, height=400)
        self.noDataText = self.canvas.create_text(300,200, text='No Data', font=('Excalifont',20))
        self.toDoContainer = ctk.CTkFrame(self.upperContentFrame, corner_radius=15, border_color='black', border_width=5, bg_color='white', fg_color='white')
        self.toDoLabel = ctk.CTkLabel(self.toDoContainer, text='To Do:', fg_color='white', text_color='black', font=('Excalifont', 25) )

        #creating the checkboxes that show the state of the application to the user
        self.sitePlanCheckBox = ctk.CTkCheckBox(self.toDoContainer, text=' Insert Site Plan', **checkboxStyling)
        self.placeNodesCheckBox = ctk.CTkCheckBox(self.toDoContainer, text=' Place Nodes', **checkboxStyling)
        self.capacityDataCheckBox = ctk.CTkCheckBox(self.toDoContainer, text=' Import Capacity Data', **checkboxStyling)
        self.optimiseCheckBox = ctk.CTkCheckBox(self.toDoContainer, text=' Optimise', **checkboxStyling)
        self.analyseCheckBox = ctk.CTkCheckBox(self.toDoContainer, text=' Analyse Bottlenecks', **checkboxStyling)
        # self.simulateCheckBox = ctk.CTkCheckBox(self.toDoContainer, text=' Simulate Event', **checkboxStyling)

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
        self.capacityDataCheckBox.pack(fill='x', padx=30, pady=10)
        self.optimiseCheckBox.pack(fill='x', padx=30, pady=10)
        self.analyseCheckBox.pack(fill='x', padx=30, pady=10)
        # self.simulateCheckBox.pack(fill='x', padx=30, pady=10)

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
            self.canvas.display(self.master.matrix, self.master.bottlenecks, True)
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
        for coord in self.master.nodePositions.values():
            if coord != (-1,-1):
                self.placeNodesCheckBox.select()
                break

        # sets the checkbox to indicate to the user if they have found the optimal paths
        if self.master.pathsFound == True:
            self.optimiseCheckBox.select()
        else:
            self.optimiseCheckBox.deselect()

        if self.master.bottlenecksFound == True:
            self.analyseCheckBox.select()
        else:
            self.analyseCheckBox.deselect()

        for capacity in self.master.capacityValues.values():
            if capacity > 0:
                self.capacityDataCheckBox.select()
                break
            self.capacityDataCheckBox.deselect()
        
        for index, bottleneck in enumerate(self.master.bottlenecks):
            position, width, severity = bottleneck
            if severity == 1:
                self.warningTable.insert(parent='', index=tk.END, values=(index, 'Bottleneck', 'Urgent Bottleneck'))
            else:
                self.warningTable.insert(parent='', index=tk.END, values=(index, 'Bottleneck', 'Potential Bottleneck'))

    def warningSelected(self,_):
        for i in self.warningTable.selection():
            index = self.warningTable.item(i)['values'][0]
            position = self.master.bottlenecks[index][0]
            x, y = position
            self.highlightPoint(x, y)

    def highlightPoint(self, x, y):
        temporaryPixels = []
        for dx, dy in [(-2, -2), (0, -2), (2, -2), (-2, 0), (2, 0), (-2, 2), (0, 2), (2, 2),
    (-1, -2), (1, -2), (-2, -1), (2, -1), (-2, 1), (2, 1), (-1, 2), (1, 2)]:
            tempPixel = self.canvas.creation(x + dx, y + dy, 2, True)
            temporaryPixels.append(tempPixel)
        
        self.after(1000, lambda: self.deleteTempPixels(temporaryPixels))

    def deleteTempPixels(self, tempPixels): # function to delete the temporary squares drawn when drawing a line
        for pixel in tempPixels:
            self.canvas.delete(pixel)
        
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
        self.JSONOverwriteWarning = warningWidget(self, 'Are you sure you want to overwrite the data', confirmCommand=self.JSONOverwrite)
        self.PNGOverwriteWarning = warningWidget(self, 'Are you sure you want to overwrite the data', confirmCommand=lambda: self.imageImportWarning.place(x=300, y=250))
        self.imageImportWarning = warningWidget(self, 'This is a tool to speed up data input, will require significant cleanup', confirmCommand=self.PNGOverwrite)
        self.capacityDataPage = capacityDataInput(self)

    def JSONOverwrite(self):
        self.readJSONFile()
    
    def PNGOverwrite(self):
        self.importImage()

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
                self.master.nodePositions[self.canvas.matrix[y][x]['base']] = (-1, -1) # sets the node position to (-1,-1) to indicate it is not placed
                self.bullseyeButton.configure(state='normal') # if the bullseye was disabled in the case of no nodes left it will be re-enabled
            if self.currentTool < 2 or self.nodes[self.currentTool] == True: # if the current tool is a pencil or eraser or the node is available
                # the pixel is drawn on the canvas and the previous action is stored in the previousActions list to allow for undo and redo
                self.previousActions.append(dataPoint(x, y, self.canvas.matrix[y][x]['base'], self.currentTool, self.dragIndex))
                self.canvas.creation(x,y,self.currentTool,False)
                self.planInserted = True
            if self.currentTool > 1: # if the current tool is a node
                self.nodes[self.currentTool] = False # the node is set to unavailable
                self.master.nodePositions[self.currentTool] = (x,y) # the position of the node is stored in the app wide variable
                for node, available in self.nodes.items(): # if there are no nodes left the bullseye button will be disabled
                    if available == True:
                        self.currentTool = node
                        break
                    elif node == 7:
                        self.noNodesLeft()

    def handleLineClick(self, event):
        # converting the x and y coordinates of the mouse to the corresponding pixel on the canvas
        x = event.x // self.canvas.pixelSize
        y = event.y // self.canvas.pixelSize

        if self.drawingLine: # if a line has been started when the button is clicked the line will be ended
            self.lineEnd = (x,y)
            self.drawingLine = False # the line is no longer being drawn
            self.dragIndex += 1 # the drag index is increased to allow for undo and redo to undo and redo the whole line
            lineData = self.drawStraightLine(self.lineStart, (x,y), False) # the line is drawn on the canvas
            self.previousActions += lineData # the line data returned from the drawStraightLine function is added to the previousActions list
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
            self.tempPixels = self.drawStraightLine(self.lineStart, (x,y), self.drawingLine)

    def drawStraightLine(self, start, end, lineSubmitted):
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
            self.master.capacityValues = self.capacityDataPage.getValues()
            self.capacityInputOpen = False # sets the boolean to false to indicate the page is closed
        else:
            # calls a method from the capacityDataPage class to refresh the page so that it will update as the user draws/removes nodes
            self.capacityDataPage.refresh(self.master.nodePositions)
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
                self.master.nodePositions[colourValue] = (x,y) # the position of the node is stored in the app wide variable
            elif colourValue > 1 and self.nodes[colourValue] == False: # if the pixel was a node and the node is not available we avoid running any more code
                break

            if self.canvas.matrix[y][x]['base'] > 1: # if there was a node at the position that will be replaced by a previous action
                self.nodes[self.canvas.matrix[y][x]['base']] = True # the node is set to available
                self.master.nodePositions[self.canvas.matrix[y][x]['base']] = (-1, -1) # the position of the node is set to (-1,-1) to indicate it is not placed
                self.bullseyeButton.configure(state='normal') # if the bullseye button was disabled it will be re-enabled

            # we store the previous state of the pixel in the redoActions list so that the action can be redone
            self.redoActions.append(dataPoint(x, y, self.canvas.matrix[y][x]['base'], colourValue, dragIndex))
            self.canvas.creation(x,y,colourValue,False) # the pixel is drawn on the canvas

            # if the list is empty or the next action is not part of the same drag we break the loop
            if not self.previousActions or self.previousActions[-1].dragIndex != previousAction.dragIndex:
                break

    def handleRedoButtonClick(self):
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
                self.master.nodePositions[colourValue] = (x,y) # the position of the node is stored in the app wide variable
            elif colourValue > 1 and self.nodes[colourValue] == False: # if the pixel was a node and the node is not available we avoid running any more code
                break

            if self.canvas.matrix[y][x]['base'] > 1: # if there was a node at the position that will be replaced by a redo action
                self.nodes[self.canvas.matrix[y][x]['base']] = True # the node is set to available
                self.master.nodePositions[self.canvas.matrix[y][x]['base']] = (-1, -1)  # the position of the node is set to (-1,-1) to indicate it is not placed

            # we store the previous state of the pixel in the previousActions list so that the action can be undone
            self.previousActions.append(dataPoint(x, y, self.canvas.matrix[y][x]['base'], colourValue, dragIndex))
            self.canvas.creation(x,y,colourValue, False) # the pixel is drawn on the canvas

            # if the list is empty or the next action is not part of the same drag we break the loop
            if not self.redoActions or self.redoActions[-1].dragIndex != redoAction.dragIndex: 
                break

    def resetCanvas(self):
        # items on the canvas are deleted
        self.canvas.delete('all')

        # the matrix storing the pixel data is reset to the default state
        for y in range(len(self.canvas.matrix)):
            for x in range(len(self.canvas.matrix[y])):
                self.canvas.matrix[y][x]['base'] = 1

    def handleClearButtonClick(self):
        self.deselectCurrentButton()
        self.clearCanvasButton.configure(text_color='white', fg_color='black')
        self.resetCanvas()

        # the nodes are reset to available and their positions are reset
        for node in self.nodes.keys():
            self.nodes[node] = True
            self.master.nodePositions[node] = (-1, -1)

        # the capacity values are reset to -1
        for node in self.master.capacityValues.keys():
            self.master.capacityValues[node] = -1

        for path in self.master.paths.keys():
            self.master.paths[path] = []

        self.master.bottlenecks = []
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
            self.master.pathsFound = False
            self.master.bottlenecksFound = False

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
        self.filePath = filedialog.askopenfilename(initialdir='/temp', title='Choose File', filetypes=[('json Files', '*.json'), ('images', '*.png')])
        print(self.filePath)
        if self.filePath.__contains__('.json'):
            if self.master.dataAdded.get() == True: # if there is already data there it will warn the user and give the option to cancel
                self.JSONOverwriteWarning.place(x = 300, y = 250) # places the custom class warning on the page
            else:
                self.readJSONFile() # if there is no data it will read the file
        elif self.filePath.__contains__('.png'):
            if self.master.dataAdded.get() == True:
                self.PNGOverwriteWarning.place(x=300, y=250)
            else:
                self.imageImportWarning.place(x=300, y=250)

    def importImage(self):
        self.resetCanvas()
        image = cv2.imread(self.filePath)
        grayscaleImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, thresholdedImage = cv2.threshold(grayscaleImage, 4, 255, cv2.THRESH_BINARY)
        imageHeight, imageWidth = thresholdedImage.shape
        gridHeight = 80
        gridWidth = 120
        cellHeight = imageHeight / gridHeight
        cellWidth = imageWidth / gridWidth

        for y in range(gridHeight):
            for x in range(gridWidth):
                xStart = int(x * cellWidth)
                xEnd = int((x+1) * cellWidth)
                yStart = int(y * cellHeight)
                yEnd = int((y+1) * cellHeight)

                cell = thresholdedImage[yStart:yEnd, xStart:xEnd]

                if np.any(cell == 0):
                    self.canvas.creation(x, y, 0, False)

    def readJSONFile(self):
        with open(self.filePath, 'r') as file: # opens the file in read mode
            self.canvas.matrix = json.load(file) # loads the matrix from the file into the input data page matrix
            self.master.dataAdded.set(True) # sets the dataAdded boolean to true to indicate data has been added
            self.master.matrix = copy.deepcopy(self.canvas.matrix) # copies the matrix from the input data page to the app wide matrix
            self.canvas.display(self.master.matrix, self.master.bottlenecks, False) # displays the data from the file on the canvas
            self.planInserted = True

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
        self.astarRunning = False

        # the following constants are used in the flow simulation algorithm
        self.WALKING_PACE = 1.4
        self.DISTANCE_BETWEEN_PEOPLE = 0.6
        self.PEOPLE_PER_METRE = 2
        self.PEOPLE_PER_SECOND_PER_METRE = self.WALKING_PACE * self.PEOPLE_PER_METRE / self.DISTANCE_BETWEEN_PEOPLE
        self.MAX_HEIGHT = 79
        self.MAX_WIDTH = 119
        self.SEVERE_THRESHOLD = 0.9
        self.MODERATE_THRESHOLD = 0.7
        self.MILD_THRESHOLD = 0.5


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
        self.capacityWarning = warningWidget(self, message='Capacity Data for all paths needed')
        self.evacPointWarning = warningWidget(self, message='Must select an Evac Point')
        self.startNodeWarning = warningWidget(self, message='Must select a Start Node')
        self.noSelectionWarning = warningWidget(self, message='Must Select Start Node and Evac Point')
        self.pathAlreadyFoundWarning = warningWidget(self, message='You have already found this path')

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

    def astar(self, startNode, endNode, callback=None): # A* algorithm *will be explained in the report*
        self.astarRunning = True
        self.canvas.matrix = copy.deepcopy(self.master.matrix)
        tempSquareIDs = []
        start = self.master.nodePositions[startNode]
        end = self.master.nodePositions[endNode]
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
                self.astarRunning = False
                if callback:
                    callback()
                return

            neighbours = []
            current = openSet.get()[2]
            queue.remove(current)

            if current == end:
                self.reconstructPath(previousNodes, start, current, startNode)
                self.timeSlider.configure(state='normal')
                self.simulateEvent.configure(state='normal')
                self.enableAllButtons()
                self.setMinimumTime()
                self.after(250, self.deleteTemporarySquares(tempSquareIDs))
                self.master.matrix = copy.deepcopy(self.canvas.matrix)
                self.astarRunning = False
                if callback:
                    callback()
                return

            if current[1] < self.MAX_HEIGHT and self.canvas.matrix[current[1] + 1][current[0]]['base'] != 0:
                neighbours.append((current[0], current[1] + 1))
            if current[1] > 0 and self.canvas.matrix[current[1] - 1][current[0]]['base'] != 0:
                neighbours.append((current[0], current[1] - 1))
            if current[0] < self.MAX_WIDTH and self.canvas.matrix[current[1]][current[0] + 1]['base'] != 0:
                neighbours.append((current[0] + 1, current[1]))
            if current[0] > 0 and self.canvas.matrix[current[1]][current[0] - 1]['base'] != 0:
                neighbours.append((current[0] - 1, current[1]))

            for neighbour in neighbours:
                tempGScore = gScore[current[1]][current[0]] + 1
                if tempGScore < gScore[neighbour[1]][neighbour[0]]:
                    previousNodes[neighbour] = current
                    gScore[neighbour[1]][neighbour[0]] = tempGScore
                    fScore[neighbour[1]][neighbour[0]] = tempGScore + self.heuristic(neighbour, end)
                    if neighbour not in queue:
                        count += 1
                        openSet.put((fScore[neighbour[1]][neighbour[0]], count, neighbour))
                        queue.add(neighbour)
                        squareID = self.canvas.creation(neighbour[0], neighbour[1], 9, True)
                        tempSquareIDs.append(squareID)

            if current != start:
                squareID = self.canvas.creation(current[0], current[1], 8, True)
                tempSquareIDs.append(squareID)

            self.after(1, run_algorithm_step)
        run_algorithm_step()

    def reconstructPath(self, previousNodes, start, current, startNode): # function to reconstruct the path from the A* algorithm *explained in the report*
        while current in previousNodes:
            current = previousNodes[current]
            if current != start:
                self.canvas.creation(current[0], current[1], startNode+10, False)
                self.master.paths[startNode+10].append(current)
    
    def heuristic(self, point1, point2): # function to calculate the heuristic for the A* algorithm *explained in the report*
        x1, y1 = point1
        x2, y2 = point2
        return abs(x1 - x2) + abs(y1 - y2)

    def flowSimulation(self): # function to run the flow simulation algorithm *explained in the report*
        problems = []
        for pathID, pathPositions in self.master.paths.items():
            if pathPositions:
                pathAnalysis = self.analysePath(pathID, pathPositions)
                problems.extend(pathAnalysis)
        return self.markProblems(problems)

    def analysePath(self, pathID, pathPositions):
        pathProblems = []

        for position in pathPositions:
            totalPeople = self.calculatePositionCapacity(position)
            minWidth = self.calculateRequiredWidth(totalPeople)
            width = self.measurePathWidth(position, pathID)
            severity = self.assessSeverity(width, minWidth)
            pathProblems.append((position, width, severity))

        return pathProblems

    def markProblems(self, problems):
        bottlenecks = []
        for pos, width, severity in problems:
            if severity > 0:
                colour = self.getSeverityColour(severity)
                self.canvas.creation(pos[0], pos[1], colour, False)
                if severity >= 0.7:
                    bottlenecks.append((pos, width, severity))
        return bottlenecks

    def measurePathWidth(self, position, pathID):
        corner = self.determineCornerType(position, pathID)

        if corner:
            return self.measureCornerWidth(position, pathID, corner)
        elif not self.checkVertical(position, pathID):
            return self.measureVerticalWidth(position)
        else:
            return self.measureHorizontalWidth(position)

    def measureVerticalWidth(self, position):
        x, y = position
        width = 1

        for direction in [-1, 1]:
            offset = 0
            while True:
                newY = y + (offset + 1) * direction
                if not self.isValidPosition(x, newY) or self.canvas.matrix[newY][x]['base'] == 0:
                    break
                width += 1
                offset += 1

        return width
    
    def measureHorizontalWidth(self, position):
        x, y = position
        width = 1

        for direction in [-1, 1]:
            offset = 0
            while True:
                newX = x + (offset + 1) * direction
                if not self.isValidPosition(newX, y) or self.canvas.matrix[y][newX]['base'] == 0:
                    break
                width += 1
                offset += 1
        
        return width
    
    def measureCornerWidth(self, position, pathID, cornerType):
        x, y = position
        
        outerWall = self.findNearestWall(position, cornerType)
        innerDX, innerDY = -cornerType[0], -cornerType[1]
        innerStart = (x + innerDX, y + innerDY)

        if self.isValidPosition(innerStart[0], innerStart[1]):
            if self.canvas.matrix[innerStart[1]][innerStart[0]]['base'] == 0:
                innerWall = innerStart
            else:
                innerWall = self.findNearestWall(innerStart, (innerDX, innerDY))
        else:
            innerWall = innerStart

        return round(math.sqrt(abs(innerWall[0] - outerWall[0]) ** 2 + abs(innerWall[1] - outerWall[1]) ** 2))

    def findNearestWall(self, position, direction):
        x, y = position
        dx, dy = direction
        
        layer = 1
        while True:
            searchPosition = 0
            while searchPosition <= layer:
                if self.isValidPosition(x + dx * layer, y + dy * searchPosition):
                    if self.canvas.matrix[y + dy * searchPosition][x + dx * layer]['base'] == 0:
                        return (x + dx * layer, y + dy * searchPosition)
                elif self.isValidPosition(x + dx * searchPosition, y + dy * layer):
                    if self.canvas.matrix[y + dy * layer][x + dx + searchPosition]['base'] == 0:
                        return (x + dx * searchPosition, y + dy * layer)
                searchPosition += 1
            layer += 1
            if not self.isValidPosition(x + dx * layer, y + dy * layer):
                return (x + dx * (layer - 1), y + dy * (layer - 1))

    def determineCornerType(self, position, pathID):
        x, y = position

        connections = self.checkConnections(position, pathID)

        if connections['up'] and connections['right']:
            return (-1,-1)
        elif connections['up'] and connections['left']:
            return (1,-1)
        elif connections['down'] and connections['right']:
            return (-1,1)
        elif connections['down'] and connections['left']:
            return (1,1)

        return None

    def assessSeverity(self, width, minWidth):
        widthRatio = minWidth / width
        if widthRatio >= self.SEVERE_THRESHOLD:
            return 1
        elif widthRatio >= self.MODERATE_THRESHOLD:
            severity = 0.7 + (0.29 * (widthRatio - self.MODERATE_THRESHOLD) / (self.SEVERE_THRESHOLD - self.MODERATE_THRESHOLD))
            return severity
        elif widthRatio >= self.MILD_THRESHOLD:
            severity = 0.3 + (0.4 * (widthRatio - self.MILD_THRESHOLD) / (self.MODERATE_THRESHOLD - self.MILD_THRESHOLD))
            return severity
        else:
            severity = 0.3 * (widthRatio / self.MILD_THRESHOLD)
            return severity

    def getSeverityColour(self, severity):
        if severity == 1:
            return 20
        elif severity >= 0.7:
            return 21
        elif severity >= 0.3:
            return 22
        else:
            return 23
        

    def isValidPosition(self, x, y):
        return 0 <= x <= self.MAX_WIDTH and 0 <= y <= self.MAX_HEIGHT

    def checkVertical(self, position, pathID):
        x, y = position
        connections = self.checkConnections(position, pathID)

        if connections['up'] and connections['down']:
            return True

        return False

    def checkConnections(self, position, pathID):
        x, y = position
        connections = {
            'up': y < self.MAX_HEIGHT and pathID in self.canvas.matrix[y+1][x].get('paths', []),
            'down': y > 0 and pathID in self.canvas.matrix[y-1][x].get('paths', []),
            'right': x < self.MAX_WIDTH and pathID in self.canvas.matrix[y][x+1].get('paths', []),
            'left': x > 0 and pathID in self.canvas.matrix[y][x-1].get('paths', [])
        }
        return connections

    def calculateRequiredWidth(self, totalPeople):
        desiredFlow = totalPeople / self.timeSlider.get()
        return desiredFlow / self.PEOPLE_PER_SECOND_PER_METRE

    def calculatePositionCapacity(self, position):
        totalPeople = 0
        x, y = position

        for pathID in self.canvas.matrix[y][x].get('paths', []):
            totalPeople += self.master.capacityValues[pathID - 10]

        return totalPeople

    def handleRunButtonClick(self): # called when the search is run for one path
        self.runButton.configure(text_color='black', fg_color='white')
        self.disableAllButtons()

        if self.evacPoint != -1 and self.startNode != -1 and not self.master.paths[self.startNode + 10]: # if the user has selected a start and end node
            self.astar(self.startNode, self.evacPoint) # run the A* algorithm to find the path
            self.timeSlider.configure(state='normal') # the slider is enabled as the user can now run a simulation
            self.simulateEvent.configure(state='normal') # the simulate event button is enabled
            self.master.pathsFound = True # sets the pathsFound boolean to true to indicate the optimal paths have been found on the homepage
        elif self.startNode != -1 and self.master.paths[self.startNode + 10]:
            self.pathAlreadyFoundWarning.place(x=300, y=250)
        elif self.evacPoint != -1:
            self.startNodeWarning.place(x=300, y=250)
        elif self.startNode != -1:
            self.evacPointWarning.place(x=300, y=250)
        else:
            self.noSelectionWarning.place(x=300, y=250)
        self.enableAllButtons()
        self.setMinimumTime() # sets the minimum time on the slider
    
    def handleShowAllPathsClick(self): # this is called when the user wants to run all the paths at once
        self.showAllPaths.configure(text_color='white', fg_color='black')
        self.disableAllButtons()

        self.nodesToProcess = []

        if self.evacPoint == -1: # If the user does not have an evac point selected
            self.evacPointWarning.place(x=300, y=250)
            self.enableAllButtons()
            return None

        # loops through all nodes creating a list of available nodes
        for node in self.master.nodePositions.keys():
            if self.master.nodePositions[node] != (-1,-1) and node != self.evacPoint and not self.master.paths[node + 10]:
                self.nodesToProcess.append(node)

        # callback function to run the next path
        def processNext():
            # once we have finished running all paths
            if not self.nodesToProcess:
                self.timeSlider.configure(state='normal')
                self.simulateEvent.configure(state='normal')
                self.setMinimumTime()
                self.master.pathsFound = True
                self.enableAllButtons()
                return
            
            # astarRunning flag decides whether we run the next step
            if not self.astarRunning:
                self.astar(self.nodesToProcess.pop(0), self.evacPoint, callback=processNext)
            else:
                self.after(10, processNext) # recursion call
        processNext()

    def handleSimulateEventClick(self):
        self.disableAllButtons()
        self.simulateEvent.configure(text_color='white', fg_color='black')
        for path in self.master.paths.keys():
            if self.master.paths[path] and self.master.capacityValues[path - 10] == -1:
                self.enableAllButtons()
                self.capacityWarning.place(x=300, y=250)
                return None
        bottlenecks = self.flowSimulation() # runs the flow simulation algorithm
        if bottlenecks:
            self.master.bottlenecks = bottlenecks
        self.master.bottlenecksFound = True
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
            if self.master.nodePositions[node] != (-1,-1):
                button.pack(pady=2)

    def nodeChooser(self):
        self.scrollFrame.grid(column=0, row=2, sticky='nsew') # places the node chooser on the page
        self.nodeChooserOpen = True

    def updateTimeLabel(self, value): # function to update the time label when the slider is moved
        formattedValue = f'{int(value):03}' # formatting the value to be 3 digits long so that the interface doesnt shift
        self.timeLabel.configure(text=f'Time: {formattedValue}') # updating the text of the label

    def setMinimumTime(self):
        minTime = 0
        for path in self.master.paths.values():
            if len(path) / self.WALKING_PACE > minTime: # if the time to evacuate is greater than the current minimum time it will be set as the minimum time
                minTime = math.ceil(len(path) / self.WALKING_PACE)
        self.timeSlider.configure(from_=minTime, to=500) # the slider is updated to have the minimum time as the minimum value

class Canvas(ctk.CTkCanvas):
    def __init__(self, parent, height, width):
        super().__init__(parent)
        # defining custom colours
        self.red = '#ff0000'
        self.blue = '#0010ff'
        self.green = '#00ff7c'
        self.orange = '#ffa300'
        self.pink = '#ff00cf'
        self.yellow = '#fffc00'
        self.purple = '#800080'
        self.darkPurple = '#320032'

        # warning colours
        self.warningRed = '#ff0000'
        self.warningOrange = '#ff6b00'
        self.warningYellow = '#ffd700'
        self.warningGreen = '#90ee90'

        # the canvas is configurable to different sizes depending on which page its on
        self.configure(height=height, width=width, bd=0, background='white', highlightthickness=0)
        self.pixelSize = height // 80 # calculates the size of each canvas pixel in pixels
        self.matrix = [[{'base': 1} for _ in range(120)] for _ in range(80)] # list comprehension to initialize the matrix with the base value of 1
        
    def creation(self, x, y, colourValue, temporary):

        match colourValue: # setting the colour based on the colour value passed in so we can reuse the function for different colours
            case 0:
                colour = 'black'
            case 1:
                colour = 'white'
            case 2:
                colour = self.red
            case 3:
                colour = self.blue
            case 4:
                colour = self.green
            case 5:
                colour = self.orange
            case 6:
                colour = self.pink
            case 7:
                colour = self.yellow
            case 8:
                colour = self.purple
            case 9:
                colour = self.darkPurple
            case 20:
                colour = self.warningRed
            case 21:
                colour = self.warningOrange
            case 22:
                colour = self.warningYellow
            case 23:
                colour = self.warningGreen
            case _:
                colour = self.purple

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

    def display(self, matrix, bottlenecks, drawBottlenecks):
        # resets the canvas so we can redraw the matrix
        self.delete('all')

        # for each pixel in the matrix we draw a square with the colour based on the base value of the pixel
        for y in range(80):
            for x in range(120):
                if matrix[y][x].get('paths', []):
                    colour = self.purple
                    self.create_rectangle((self.pixelSize * (x+1) - self.pixelSize, self.pixelSize * (y+1) - self.pixelSize, self.pixelSize * (x+1) - 1, self.pixelSize * (y+1) - 1), fill=colour, outline=colour)

                match matrix[y][x]['base']:
                    case 0:
                        colour = 'black'
                    case 2:
                        colour = self.red
                    case 3:
                        colour = self.blue
                    case 4:
                        colour = self.green
                    case 5:
                        colour = self.orange
                    case 6:
                        colour = self.pink
                    case 7:
                        colour = self.yellow

                if matrix[y][x]['base'] == 0 or matrix[y][x]['base'] > 1:
                    self.create_rectangle((self.pixelSize * (x+1) - self.pixelSize, self.pixelSize * (y+1) - self.pixelSize, self.pixelSize * (x+1) - 1, self.pixelSize * (y+1) - 1), fill=colour, outline=colour)

        if drawBottlenecks:
            for bottleneck in bottlenecks:
                position, width, severity = bottleneck
                x, y = position
                if severity == 1:
                    colour = self.warningRed
                else:
                    colour = self.warningOrange
                self.create_rectangle((self.pixelSize * (x+1) - self.pixelSize, self.pixelSize * (y+1) - self.pixelSize, self.pixelSize * (x+1) - 1, self.pixelSize * (y+1) - 1), fill=colour, outline=colour)

class warningWidget(ctk.CTkFrame):
    def __init__(self, parent, message, confirmCommand=None, cancelCommand=None):
        super().__init__(parent)
        self.configure(height=200, width=400, corner_radius=15, border_color='black', border_width=5, bg_color='white', fg_color='white')
        self.message = message
        self.confirmCommand = confirmCommand
        self.cancelCommand = cancelCommand
        
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
        self.warningLabel = ctk.CTkLabel(self, text=self.message, text_color='black', font=('Excalifont',20))
        self.buttonFrame = ctk.CTkFrame(self, fg_color='transparent')
        self.confirmButton = ctk.CTkButton(self.buttonFrame, text='Confirm', **warnButtonStyling, command=lambda: self.after(100, self.handleconfirmButtonClick))
        self.cancelButton = ctk.CTkButton(self.buttonFrame, text='Cancel', **warnButtonStyling, command=lambda: self.after(100, self.handlecancelButtonClick))

        # setting the hover behaviour for the buttons
        self.confirmButton.bind('<Enter>', lambda event: self.confirmButton.configure(text_color='white', fg_color='black'))
        self.confirmButton.bind('<Leave>', lambda event: self.confirmButton.configure(text_color='black', fg_color='white'))
        self.cancelButton.bind('<Enter>', lambda event: self.cancelButton.configure(text_color='white', fg_color='black'))
        self.cancelButton.bind('<Leave>', lambda event: self.cancelButton.configure(text_color='black', fg_color='white'))

    def placeWidgets(self):
        self.warningLabel.pack(padx=10, pady=(10,0))
        self.buttonFrame.pack(pady=(0,10), padx=10, anchor='center')
        self.confirmButton.pack(side='left', padx=10, pady=10)
        self.cancelButton.pack(side='left', padx=10, pady=10)

    def handleconfirmButtonClick(self):
        self.confirmButton.configure(text_color='black', fg_color='white')
        if self.confirmCommand:
            self.confirmCommand()
        self.place_forget() # hides the warning frame

    def handlecancelButtonClick(self):
        self.cancelButton.configure(text_color='black', fg_color='white')
        if self.cancelCommand:
            self.cancelCommand()
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

    def refresh(self, nodePositions):
        
        # removes all the entry widgets from the scrollable frame
        for entry in self.entries.keys():
            entry.pack_forget()

        # packs the entry widgets for the nodes that have been placed by the user
        for entry, node in self.entries.items():
            if nodePositions[node] != (-1,-1):
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
        self.entryValue = ctk.StringVar()
        self.entryValue.trace_add("write", self.validateEntry)
        self.image = ctk.CTkLabel(self, image=image, text='')
        self.label = ctk.CTkLabel(self, text='Input Capacity', text_color='black', font=('Excalifont', 20))
        self.entryField = ctk.CTkEntry(self, fg_color='white', text_color='black', font=('Excalifont', 15), justify='center', textvariable=self.entryValue)
    
    def placeWidgets(self):
        self.image.pack(padx=(10,0), pady=10, side='left')
        self.label.pack(padx=10, pady=(10,0))
        self.entryField.pack(pady=10, padx=(10,20))

    def getEntry(self): # a method to get the value of the entry field
        return self.entryField.get()

    def validateEntry(self, *args): # a method to validate the entry field so that only integers can be entered
        newValue = self.entryValue.get()
        if not newValue.isdigit():
            self.entryValue.set("".join(filter(str.isdigit, newValue)))
    
if __name__ == '__main__': # runs the app if the file is run as the main file
    app = App()
    app.mainloop()