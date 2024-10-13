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
    


app = tk.Tk()
app.title('Safe Way Out')
app.geometry('1280x720')
app.columnconfigure(0, weight=1)
app.columnconfigure(1, weight=20)
app.rowconfigure(0, weight=1)
app.configure(bg='white')
app.iconbitmap('fire.ico')

style = ttk.Style()
style.configure('menu.TButton', foreground = 'black', background='white', font = ('Excalifont', 20))
style.map('menu.TButton', foreground=[('pressed', 'red'),('disabled', 'yellow')])
mapImage = Image.open('siteplan.png')

menuFrame = ctk.CTkFrame(app, corner_radius=15, border_color='black', border_width=5, bg_color='white', fg_color='white')
title = ttk.Label(menuFrame, text='Safe Way Out', background='white', foreground='black', font=('Excalifont', 20))
title.pack(pady=20, padx=20)
homeButton = ttk.Button(menuFrame, text='Home', style='menu.TButton')
optimisePlanButton = ttk.Button(menuFrame, text='Optimise Plan', style='menu.TButton')
inputDataButton = ttk.Button(menuFrame, text='Input Data', style='menu.TButton')
homeButton.pack()
optimisePlanButton.pack()
inputDataButton.pack()

contentFrame = ctk.CTkFrame(app, bg_color='white', fg_color='white')
contentFrame.rowconfigure(0, weight=4)
contentFrame.rowconfigure(1, weight=1)
contentFrame.columnconfigure(0, weight=1)

upperContentFrame = ctk.CTkFrame(contentFrame, bg_color='white', fg_color='white')
upperContentFrame.columnconfigure(0, weight=5)
upperContentFrame.columnconfigure(1, weight=2)
upperContentFrame.rowconfigure(0, weight=1)
lowerContentFrame = ctk.CTkFrame(contentFrame, corner_radius=15, border_color='black', border_width=5, bg_color='white', fg_color='white')

mapContainer = ctk.CTkFrame(upperContentFrame, corner_radius=15, border_color='black', border_width=5, bg_color='white', fg_color='white')
mapCanvas = tk.Canvas(mapContainer, background='white', bd=0, highlightthickness=0, relief='ridge')
mapCanvas.pack(fill='both', expand=True, padx=10, pady=10)
toDoContainer = ctk.CTkFrame(upperContentFrame, corner_radius=15, border_color='black', border_width=5, bg_color='white', fg_color='white')

mapContainer.grid(row=0, column=0, sticky='nsew', padx=(10, 5), pady=10)
toDoContainer.grid(row=0, column=1, sticky='nsew', padx=(5, 10), pady=10)
upperContentFrame.grid(row=0, column=0, sticky='nsew')
lowerContentFrame.grid(row=1, column=0, sticky='nsew', padx=10, pady=(5, 10))

menuFrame.grid(row=0, column=0, sticky='nsew', padx=(10,5), pady=10)
contentFrame.grid(row=0, column=1, sticky='nsew')

mapCanvas.bind('<Configure>', stretchImage)



app.mainloop()