import tkinter as tk
from tkinter import ttk, font
import customtkinter as ctk
from PIL import Image, ImageTk

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
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=20)
        self.rowconfigure(0, weight=1)
        self.configure(bg='white')
        self.iconbitmap('fire.ico')
        self.menu = Menu(self)
        self.currentPage = homePage(self)
    
class Menu(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)
        self.configure(corner_radius=15, border_color='black', border_width=5, bg_color='white', fg_color='white')
        self.homeDark = ImageTk.PhotoImage(Image.open('homeDark.png'))
        self.homeLight = ImageTk.PhotoImage(Image.open('homeLight.png'))
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
        self.optimisePlanButton = ctk.CTkButton(self, text='Optimise Plan', **menuButtonStyling, command=self.openOptimisePlanPage)
        self.inputDataButton = ctk.CTkButton(self, text='Input Data', **menuButtonStyling)
    
    def placeMenuWidgets(self):
        self.title.pack(pady=20, padx=20)
        self.homeButton.pack(fill='x', padx=10, pady=5)
        self.homeButton.bind('<Enter>', lambda event: self.homeButton.configure(text_color='white', fg_color='black', image=self.homeLight))
        self.homeButton.bind('<Leave>', lambda event: self.homeButton.configure(text_color='black', fg_color='white', image=self.homeDark))
        self.placeMenuButton(self.optimisePlanButton)
        self.placeMenuButton(self.inputDataButton)

    def placeMenuButton(self, button):
        button.pack(fill='x', padx=10, pady=5)
        button.bind('<Enter>', lambda event: button.configure(text_color='white', fg_color='black'))
        button.bind('<Leave>', lambda event: button.configure(text_color='black', fg_color='white'))
    
    def openHomePage(self):
        app.currentPage = homePage(app)

    def openOptimisePlanPage(self):
        app.currentPage = optimisePlanPage(app)

class homePage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(bg_color='white', fg_color='white')
        self.rowconfigure(0, weight=4)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.mapImage = Image.open('siteplan.png')
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
        self.mapCanvas = ctk.CTkCanvas(self.mapContainer, background='white', bd=0, highlightthickness=0, relief='ridge')
        self.mapCanvas.bind('<Configure>', self.stretchImage)
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


    def stretchImage(self, event):
        global resizedMap
        width = event.width
        height = event.height

        resizedMap = ImageTk.PhotoImage(self.mapImage.resize((width,height)))
        self.mapCanvas.create_image(0,0, image = resizedMap, anchor='nw')

class optimisePlanPage(ctk.CTkFrame):
    def __init__(self,parent):
        super().__init__(parent)
        self.configure()

if __name__ == '__main__':
    app = App()
    app.mainloop()