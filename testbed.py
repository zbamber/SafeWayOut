import tkinter as tk
import customtkinter as ctk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Testbed')
        self.geometry('1280x720')
        self.toolcontainer = toolContainer(self).pack(padx=10, pady=10)
        

class toolContainer(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(fg_color='white', bg_color='white', corner_radius=15, border_color='black', border_width=5, width=500, height=500)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)
        self.rowconfigure(6, weight=1)
        self.rowconfigure(7, weight=1)
        self.rowconfigure(8, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.tester = ctk.CTkLabel(self, text='', bg_color='red', fg_color='red', corner_radius=15).grid(row=7, column=1, sticky='nsew', padx=10, pady=10)

app = App()
app.mainloop()