import tkinter as tk
from tkinter import ttk, font
import customtkinter as ctk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('figuring this out')
        self.geometry('1200x720')
        self.configure(bg='white')
        self.createWidgets()
        self.placeWidgets()
        self.matrix = [[1] * 120 for _ in range(80)]
        # self.acanvas.placeacheckerpattern()
    def showcoords(self, event):
        print(f'x: {event.x}, y: {event.y}')
    
    def deletion(self):
        print('deleting')
        self.input.destroy()
        self.output.pack()
        self.output.display()

    def createWidgets(self):
        self.prettyFrame = ctk.CTkFrame(self, corner_radius=15, border_color='black', border_width=5, bg_color='white', fg_color='white')
        # self.acanvas = testCanvas(parent=self.prettyFrame, height=291, width=291)
        # self.anothercanvas = Canvas(parent=self.prettyFrame, height=291, width=291)
        self.input = Canvas(parent=self.prettyFrame, height=640, width=960)
        self.input.bind('<Button>', lambda event: self.input.creation(event=event))
        self.input.bind('<B1-Motion>', lambda event: self.input.creation(event=event))
        self.output = Canvas(parent=self.prettyFrame, height=400, width=600)
        self.bind('<Escape>', lambda event: self.deletion())
        self.bind('<a>', lambda event: self.input.display())
        # self.acanvas.bind('<Motion>', lambda event: self.showcoords(event=event))
        # self.anothercanvas.bind('<Button>', lambda event: self.anothercanvas.placeasquare(event=event))

    def placeWidgets(self):
        self.prettyFrame.pack(fill='both', expand=True, padx=10, pady=10)
        # self.acanvas.pack(padx=10, side='left')
        # self.anothercanvas.pack(side='left', padx=(0,10))
        self.input.pack(side='left')

class testCanvas(ctk.CTkCanvas):
    def __init__(self, parent, height, width):
        super().__init__(parent)
        self.configure(height=height, width=width)
        self.testmatrix = [[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                       [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                       [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                       [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                       [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                       [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                       [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                       [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                       [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                       [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                       [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                       [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                       [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                       [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                       [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                       [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                       [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                       [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                       [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                       [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                       [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                       [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                       [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                       [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                       [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                       [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                       [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                       [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                       [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                       [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]

    def placeacheckerpattern(self):
        self.create_rectangle(2,2,292,292)
        flipflop = True
        for y in range(29):
            for x in range(29):
                if flipflop == True:
                    self.create_rectangle((10 * (x+1) - 8, 10 * (y+1) - 8, 10 * (x+1) + 2, 10 * (y+1) + 2 ), fill='black')
                    flipflop = False
                else:
                    flipflop= True
    
    def placeasquare(self, event):
        gridXIndex = event.x // 10
        gridYIndex = event.y // 10
        print(f'xclick: {gridXIndex}, yclick: {gridYIndex}')
        self.create_rectangle((10 * (gridXIndex+1) - 8, 10 * (gridYIndex+1) - 8, 10 * (gridXIndex+1) + 2, 10 * (gridYIndex+1) + 2), fill='black')
        self.testmatrix[gridYIndex][gridXIndex] = 0
        for i in range(29):    
            print(self.testmatrix[i])

class Canvas(ctk.CTkCanvas):
    def __init__(self, parent, height, width):
        super().__init__(parent)
        self.configure(height=height, width=width)
        
    def creation(self, event):
        gridXIndex = event.x // 8
        gridYIndex = event.y // 8
        print(f'xclick: {gridXIndex}, yclick: {gridYIndex}')
        self.create_rectangle((8 * (gridXIndex+1) - 5, 8 * (gridYIndex+1) - 5, 8 * (gridXIndex+1) + 2, 8 * (gridYIndex+1) + 2), fill='black')
        self.master.master.matrix[gridYIndex][gridXIndex] = 0

    def display(self):
        for y in range(80):
            for x in range(120):
                if self.master.master.matrix[y][x] == 0:
                    print('here i am')
                    self.create_rectangle((5 * (x+1) - 3, 5 * (y+1) - 3, 5 * (x+1) + 2, 5 * (y+1) + 2), fill='black')

if __name__ == '__main__':
    app = App()
    app.mainloop()