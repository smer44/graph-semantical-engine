import tkinter as tk

class MyCanvas(tk.Canvas):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.bind("<Shift-X>", self.on_shift_x_press)

    def on_shift_x_press(self, event):
        print("Shift-X pressed on canvas!")

root = tk.Tk()
canvas = MyCanvas(root, width=400, height=300)
canvas.pack()

# Ensure the canvas has focus
canvas.focus_set()

root.mainloop()
