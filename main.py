import tkinter
import tkinter.messagebox
import customtkinter

customtkinter.set_appearance_mode("System")
# I will modify this theme later
customtkinter.set_default_color_theme("dark-blue")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Safe Way Out")
        self.geometry(f"{1000}x{600}")

if __name__ == "__main__":
    app = App()
    app.mainloop()