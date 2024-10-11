import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from PIL import Image, ImageTk

def stretchImage(event):
    global resizedMap
    width = event.width
    height = event.height
    resizedMap = ImageTk.PhotoImage(mapImage.resize((width,height)))
    mapCanvas.create_image(0,0, image = resizedMap, anchor='nw')


app = tk.Tk()
app.title('Safe Way Out')
app.geometry('1280x720')
app.columnconfigure(0, weight=1)
app.columnconfigure(1, weight=3)
app.rowconfigure(0, weight=1)
 
mapImage = Image.open('exampleSitePlan.png')

menuFrame = tk.Frame(app, bg='red')
contentFrame = tk.Frame(app, bg='blue')
contentFrame.rowconfigure(0, weight=2)
contentFrame.rowconfigure(1, weight=1)
contentFrame.columnconfigure(0, weight=1)
upperContentFrame = tk.Frame(contentFrame, bg='yellow')
upperContentFrame.columnconfigure(0, weight=5)
upperContentFrame.columnconfigure(1, weight=2)
upperContentFrame.rowconfigure(0, weight=1)
lowerContentFrame = tk.Frame(contentFrame, bg='green')
mapContainer = tk.Frame(upperContentFrame, bg='orange')
mapCanvas = tk.Canvas(mapContainer, background='grey', bd=0, highlightthickness=0, relief='ridge')
mapCanvas.pack(fill='both', expand=True)

toDoContainer = tk.Frame(upperContentFrame, bg='lightblue')

mapContainer.grid(row=0, column=0, sticky='nsew', padx=(10, 5), pady=10)
toDoContainer.grid(row=0, column=1, sticky='nsew', padx=(5, 10), pady=10)

upperContentFrame.grid(row=0, column=0, sticky='nsew', padx=10, pady=(10, 5))
lowerContentFrame.grid(row=1, column=0, sticky='nsew', padx=10, pady=(5, 10))

menuFrame.grid(row=0, column=0, sticky='nsew')
contentFrame.grid(row=0, column=1, sticky='nsew')

mapCanvas.bind('<Configure>', stretchImage)


app.mainloop()