import tkinter as tk
from tkinter import font

class TextRectangleDemo(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Text in a Rectangle")

        # Create a canvas
        self.canvas = tk.Canvas(self, width=400, height=300)
        self.canvas.pack()

        # Example text
        text = "This is line 1\nThis is line 2\nThis is the longest line of text\nThis is line 4" + "\n"*6

        # Draw the text inside a dynamically sized rectangle
        self.display_text_in_rectangle(text)

    def display_text_in_rectangle(self, text):
        # Split the text into lines

        text_obj = self.canvas.create_text(200, 150, text=text, anchor='center')
        bounds = self.canvas.bbox(text_obj)

        # Draw the rectangle
        self.canvas.create_rectangle(*bounds, outline="black")



if __name__ == "__main__":
    app = TextRectangleDemo()
    app.mainloop()
