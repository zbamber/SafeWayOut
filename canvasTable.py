import tkinter as tk
from tkinter import Canvas
import customtkinter as ctk

class CustomTable(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master)
        self.canvas = Canvas(self, bg="#EFEFEF", bd=0, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.row_height = 60
        self.col_width = 150
        self.num_rows = 5
        self.num_cols = 3

        # Example data
        self.data = [
            ["Index", "Type", "Extra Information"],
            ["1", "John Doe", "Developer"],
            ["2", "Jane Smith", "Designer"],
            ["3", "Mike Brown", "Manager"],
            ["4", "Lisa White", "Analyst"]
        ]

        self.draw_table()

    def draw_table(self):
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                # Get data for each cell
                cell_value = self.data[row][col]

                # Draw a rounded rectangle
                self.draw_rounded_rect(col * self.col_width, row * self.row_height,
                                       (col + 1) * self.col_width, (row + 1) * self.row_height,
                                       radius=10, fill="#FFF", outline="#000")

                # Insert text into the cell
                self.canvas.create_text((col * self.col_width) + self.col_width / 2,
                                        (row * self.row_height) + self.row_height / 2,
                                        text=cell_value, font=("Helvetica", 14), fill="black")

    def draw_rounded_rect(self, x1, y1, x2, y2, radius=25, **kwargs):
        """Draws a rounded rectangle on the canvas."""
        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1
        ]

        return self.canvas.create_polygon(points, smooth=True, **kwargs)


# Tkinter app setup
root = tk.Tk()
root.title("Custom Table Example")
root.geometry('600x400')

# Create and display the custom table
table = CustomTable(root)
table.pack(fill="both", expand=True)

# Run the app
root.mainloop()
