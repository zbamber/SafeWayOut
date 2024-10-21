import tkinter as tk
from tkinter import ttk, font
import customtkinter as ctk
from PIL import Image, ImageTk

class App(tk.Tk):
    
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
    
class Menu(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(corner_radius=15, border_color='black', border_width=5, bg_color='white', fg_color='white')
        self.grid(row=0, column=0, sticky='nsew', padx=(10,5), pady=10)
    
    def placeMenuWidgets():
        title = ctk.CTkLabel(menuFrame, text='Safe Way Out', fg_color='white', text_color='black', font=('Excalifont', 20))
        homeButton = ctk.CTkButton(menuFrame, text='   Home', image=homeDark, anchor='w', **menuButtonStyling)
        optimisePlanButton = ctk.CTkButton(menuFrame, text='Optimise Plan', **menuButtonStyling)
        inputDataButton = ctk.CTkButton(menuFrame, text='Input Data', **menuButtonStyling)
app = App()
app.mainloop()