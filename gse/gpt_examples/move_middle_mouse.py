import tkinter as tk

class DragCanvasExample(tk.Tk):
    def __init__(self):
        super().__init__()

        # Set up the main window
        self.title("Tkinter Canvas Drag Example")
        self.geometry("800x600")

        # Set up the canvas
        self.canvas = tk.Canvas(self, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Create some example content on the canvas
        self.create_content()

        # Bind mouse events for dragging
        self.canvas.bind("<ButtonPress-2>", self.on_middle_button_press)  # Middle mouse button pressed
        self.canvas.bind("<B2-Motion>", self.on_middle_button_drag)  # Middle mouse button dragged

        # Store the start position of the drag
        self.drag_data = {"x": 0, "y": 0}

    def create_content(self):
        """Create some simple shapes and text on the canvas."""
        self.canvas.create_rectangle(50, 50, 200, 200, fill="blue", tags="content")
        self.canvas.create_oval(300, 100, 500, 300, fill="red", tags="content")
        self.canvas.create_text(400, 400, text="Drag me around!", font=("Arial", 24), tags="content")

    def on_middle_button_press(self, event):
        """Store the initial position when the middle mouse button is pressed."""
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

    def on_middle_button_drag(self, event):
        """Move the content on the canvas when dragging with the middle mouse button."""
        # Calculate the distance moved
        delta_x = event.x - self.drag_data["x"]
        delta_y = event.y - self.drag_data["y"]

        # Move all canvas items
        self.move_all(delta_x, delta_y)

        # Update the drag start position
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

    def move_all(self, delta_x, delta_y):
        """Move all items on the canvas by a given offset."""
        self.canvas.move("content", delta_x, delta_y)

if __name__ == "__main__":
    app = DragCanvasExample()
    app.mainloop()
