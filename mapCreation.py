import tkinter as tk
from tkinter import ttk, font
import customtkinter as ctk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('figuring this out')
        self.geometry('1280x720')
        self.configure(bg='white')
        self.createWidgets()
        self.placeWidgets()
    
    def createWidgets(self):
        self.prettyFrame = ctk.CTkFrame(self, corner_radius=15, border_color='black', border_width=5, bg_color='white', fg_color='white')
        self.canvas = ctk.CTkCanvas(self.prettyFrame)

    def placeWidgets(self):
        self.prettyFrame.pack(fill='both', expand=True, padx=10, pady=10)
        self.canvas.pack(fill='both', expand=True)
if __name__ == '__main__':
    app = App()
    app.mainloop()