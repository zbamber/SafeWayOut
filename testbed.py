import customtkinter as ctk
from customtkinter import CTkImage
from PIL import Image


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        # menuButtonStyling = {
        # 'border_width':2,
        # 'border_color':'black',
        # 'text_color':'black',
        # 'font':('Excalifont',20),
        # 'fg_color':'white',
        # 'corner_radius':10
        # }
        # self.red = CTkImage(light_image=Image.open('assets/red.png'))
        self.geometry('1200x720')
        # self.aSimpleContainer = ctk.CTkFrame(self, fg_color='white', bg_color='white')
        # self.aSimpleContainer.columnconfigure(0,weight=1)
        # self.aSimpleContainer.rowconfigure((0,1,2,3), weight=1)
        # self.choiceButton = Choice(self.aSimpleContainer)
        # fillerButton1 = ctk.CTkButton(self.aSimpleContainer, **menuButtonStyling, text='', image=self.red)
        # fillerButton2 = ctk.CTkButton(self.aSimpleContainer, **menuButtonStyling, text='', image=self.red)
        # fillerButton3 = ctk.CTkButton(self.aSimpleContainer, **menuButtonStyling, text='', image=self.red)
        # self.choiceButton.grid(row=0, column=0, sticky='nsew')
        # fillerButton1.grid(row=1, column=0, sticky='nsew')
        # fillerButton2.grid(row=2, column=0, sticky='nsew')
        # fillerButton3.grid(row=3, column=0, sticky='nsew')
        # self.aSimpleContainer.pack()

        self.scrollFrame = ctk.CTkScrollableFrame(self, width=100)
        self.scrollFrame.pack(pady=10)


# class Choice(ctk.CTkButton):
#     def __init__(self, parent):
#         menuButtonStyling = {
#         'border_width':2,
#         'border_color':'black',
#         'text_color':'black',
#         'font':('Excalifont',20),
#         'fg_color':'white',
#         'corner_radius':10
#         }
#         self.red = CTkImage(light_image=Image.open('assets/red.png'))
#         super().__init__(parent, **menuButtonStyling, command=self.handleButtonClick, image=self.red, text='')
        
        
    
#     def handleButtonClick(self):
#         self.scrollFrame = ctk.CTkScrollableFrame(self.master)
#         self.scrollFrame.grid(column=0, row=1, rowspan=2)

app = App()
app.mainloop()