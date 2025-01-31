import tkinter as tk
from tkinter import ttk, font
import customtkinter as ctk
import math

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Speedrun')
        self.geometry('1200x1200')
        self.configure(bg='white')
        self.createWidgets()
        self.placeWidgets()
        # self.colourIn()

    def createWidgets(self):
        self.prettyFrame = ctk.CTkFrame(self, corner_radius=15, border_color='black', border_width=5, bg_color='white', fg_color='white')
        self.canvas = Canvas(parent=self.prettyFrame, height=901, width=901)
        # self.canvas.bind('<Button>', lambda event: self.handleDrawing(event=event))
        self.canvas.bind('<Motion>', lambda event: print('hello'))

    def placeWidgets(self):
        self.prettyFrame.pack(fill='both', expand=True, padx=10, pady=10)
        self.canvas.pack(side='left', padx=20)

    # def colourIn(self):
    #     centrepoint  = (self.canvas.width // 2, self.canvas.height // 2)
    #     maxdistance = math.sqrt(centrepoint[0]**2+centrepoint[1]**2)
    #     print(maxdistance)
    #     for y in range(901):
    #         for x in range(901):
    #             coordinate = (x,y)
    #             distance  = math.sqrt((x-centrepoint[0])**2+(y-centrepoint[1])**2)
    #             fractionOfSpectrum = distance/maxdistance
    #             subtractor = 510 * fractionOfSpectrum
    #             if subtractor < 255:
    #                 r = 0 + subtractor
    #                 g = 255
    #                 b = 0
    #             else:
    #                 newsubtractor = subtractor - 255
    #                 g = 255 - newsubtractor
    #                 r = 255
    #                 b = 0
                
    #             r, g, b = int(r), int(g), int(b)
    #             hexcolour = f"#{r:02x}{g:02x}{b:02x}"

    #             self.canvas.creation(coordinate, colour=hexcolour)

class Canvas(ctk.CTkCanvas):
    def __init__(self, parent, height, width):
        super().__init__(parent)
        self.width=width
        self.height=height
        self.configure(height=height, width=width)
        
    def creation(self, coordinate, colour):
        gridXIndex = coordinate[0]
        gridYIndex = coordinate[1]
        self.create_rectangle((gridXIndex+1,gridYIndex+1,gridXIndex+1,gridYIndex+1), fill=colour, outline='')

class Coordinate():
    def __init__(self, x, y):
        self.x = x
        self.y = y

if __name__ == '__main__':
    app = App()
    app.mainloop()