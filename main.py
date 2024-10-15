import tkinter as tk
from tkinter import ttk, font
import customtkinter as ctk
from PIL import Image, ImageTk

def stretchImage(event):
    global resizedMap
    width = event.width
    height = event.height

    # print(f'width: {width}, height: {height}')
    resizedMap = ImageTk.PhotoImage(mapImage.resize((width,height)))
    mapCanvas.create_image(0,0, image = resizedMap, anchor='nw')

def placeMenuButton(button):
    button.pack(fill='x', padx=10, pady=5)
    button.bind('<Enter>', lambda event: button.configure(text_color='white', fg_color='black'))
    button.bind('<Leave>', lambda event: button.configure(text_color='black', fg_color='white'))

menuButtonStyling = {
    'border_width':2,
    'border_color':'black',
    'text_color':'black',
    'font':('Excalifont',20),
    'fg_color':'white',
    'corner_radius':10
}

checkboxStyling = {
    'width':5,
    'height':10,
    'fg_color':'white',
    'text_color':'black',
    'font':('Excalifont',20),
    'border_color':'black',
    'hover_color':'black'
}


app = tk.Tk()
app.title('Safe Way Out')
app.geometry('1280x720')
app.columnconfigure(0, weight=1)
app.columnconfigure(1, weight=20)
app.rowconfigure(0, weight=1)
app.configure(bg='white')
app.iconbitmap('fire.ico')


mapImage = Image.open('siteplan.png')
homeDark = ImageTk.PhotoImage(Image.open('homeDark.png'))
homeLight = ImageTk.PhotoImage(Image.open('homeLight.png'))

menuFrame = ctk.CTkFrame(app, corner_radius=15, border_color='black', border_width=5, bg_color='white', fg_color='white')
title = ctk.CTkLabel(menuFrame, text='Safe Way Out', fg_color='white', text_color='black', font=('Excalifont', 20))
title.pack(pady=20, padx=20)

homeButton = ctk.CTkButton(menuFrame, text='   Home', image=homeDark, anchor='w', **menuButtonStyling)
optimisePlanButton = ctk.CTkButton(menuFrame, text='Optimise Plan', **menuButtonStyling)
inputDataButton = ctk.CTkButton(menuFrame, text='Input Data', **menuButtonStyling)


homeButton.pack(fill='x', padx=10, pady=5)
homeButton.bind('<Enter>', lambda event: homeButton.configure(text_color='white', fg_color='black', image=homeLight))
homeButton.bind('<Leave>', lambda event: homeButton.configure(text_color='black', fg_color='white', image=homeDark))
placeMenuButton(optimisePlanButton)
placeMenuButton(inputDataButton)

contentFrame = ctk.CTkFrame(app, bg_color='white', fg_color='white')
contentFrame.rowconfigure(0, weight=4)
contentFrame.rowconfigure(1, weight=1)
contentFrame.columnconfigure(0, weight=1)

upperContentFrame = ctk.CTkFrame(contentFrame, bg_color='white', fg_color='white')
upperContentFrame.columnconfigure(0, weight=5)
upperContentFrame.columnconfigure(1, weight=2)
upperContentFrame.rowconfigure(0, weight=1)
lowerContentFrame = ctk.CTkFrame(contentFrame, corner_radius=15, border_color='black', border_width=5, bg_color='white', fg_color='white')
WarningLabel = ctk.CTkLabel(lowerContentFrame, text='Warning!', fg_color='white', text_color='black', font=('Excalifont', 25) )
warningTable = ttk.Treeview(lowerContentFrame, columns=('Index','Type', 'Extra Information'), show='headings')
warningTable.heading('Index', text='Index')
warningTable.heading('Type', text='Type')
warningTable.heading('Extra Information', text='Extra Information')
WarningLabel.pack(pady=10)
warningTable.pack(fill='both', expand=True, padx=10, pady=(0,10))

mapContainer = ctk.CTkFrame(upperContentFrame, corner_radius=15, border_color='black', border_width=5, bg_color='white', fg_color='white')
mapCanvas = ctk.CTkCanvas(mapContainer, background='white', bd=0, highlightthickness=0, relief='ridge')
mapCanvas.pack(fill='both', expand=True, padx=10, pady=10)

toDoContainer = ctk.CTkFrame(upperContentFrame, corner_radius=15, border_color='black', border_width=5, bg_color='white', fg_color='white')
toDoLabel = ctk.CTkLabel(toDoContainer, text='To Do:', fg_color='white', text_color='black', font=('Excalifont', 25) )
sitePlanCheckBox = ctk.CTkCheckBox(toDoContainer, text=' Insert Site Plan', **checkboxStyling)
placeNodesCheckBox = ctk.CTkCheckBox(toDoContainer, text=' Place Nodes', **checkboxStyling)
optimiseCheckBox = ctk.CTkCheckBox(toDoContainer, text=' Optimise', **checkboxStyling)
analyseCheckBox = ctk.CTkCheckBox(toDoContainer, text=' Analyse Bottlenecks', **checkboxStyling)
capacityDataCheckBox = ctk.CTkCheckBox(toDoContainer, text=' Import Capacity Data', **checkboxStyling)
simulateCheckBox = ctk.CTkCheckBox(toDoContainer, text=' Simulate Event', **checkboxStyling)

toDoLabel.pack(pady=20)
sitePlanCheckBox.pack(fill='x', padx=30, pady=10)
placeNodesCheckBox.pack(fill='x', padx=30, pady=10)
optimiseCheckBox.pack(fill='x', padx=30, pady=10)
analyseCheckBox.pack(fill='x', padx=30, pady=10)
capacityDataCheckBox.pack(fill='x', padx=30, pady=10)
simulateCheckBox.pack(fill='x', padx=30, pady=10)

mapContainer.grid(row=0, column=0, sticky='nsew', padx=(10, 5), pady=10)
toDoContainer.grid(row=0, column=1, sticky='nsew', padx=(5, 10), pady=10)
upperContentFrame.grid(row=0, column=0, sticky='nsew')
lowerContentFrame.grid(row=1, column=0, sticky='nsew', padx=10, pady=(5, 10))

menuFrame.grid(row=0, column=0, sticky='nsew', padx=(10,5), pady=10)
contentFrame.grid(row=0, column=1, sticky='nsew')

mapCanvas.bind('<Configure>', stretchImage)

app.mainloop()