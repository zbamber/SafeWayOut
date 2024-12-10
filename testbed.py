import customtkinter as ctk


class MyFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # add widgets onto the frame...
        self.label = ctk.CTkLabel(self)
        self.label.grid(row=0, column=0, padx=20)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry('1200x720')
        self.choiceButton = Choice(self)
        self.choiceButton.pack()

class Choice(ctk.CTkButton):
    def __init__(self, parent):
        menuButtonStyling = {
        'border_width':2,
        'border_color':'black',
        'text_color':'black',
        'font':('Excalifont',20),
        'fg_color':'white',
        'corner_radius':10
        }
        super().__init__(parent, **menuButtonStyling)


app = App()
app.mainloop()