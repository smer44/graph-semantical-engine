import tkinter as tk


class CustomClass:
    def __init__(self, name, age, occupation, location):
        self.name = name
        self.age = age
        self.occupation = occupation
        self.location = location


class DrawNode:
    def __init__(self, canvas):
        self.canvas = canvas

    def draw(self, instance, fields, x, y):
        class_name = instance.__class__.__name__

        # Prepare the text lines
        field_lines = [f"{field} = {getattr(instance, field)}" for field in fields]
        all_lines = [class_name] + field_lines

        # Determine the width of the rectangle
        max_width = 0
        for line in all_lines:
            temp_text_id = self.canvas.create_text(0, 0, text=line, anchor='w')
            bbox = self.canvas.bbox(temp_text_id)
            line_width = bbox[2] - bbox[0]
            if line_width > max_width:
                max_width = line_width
            self.canvas.delete(temp_text_id)

        line_height = 20  # Assuming a fixed line height for simplicity

        # Draw the class name box
        self.canvas.create_rectangle(x, y, x + max_width+2 , y + line_height +2, fill="light blue")
        self.canvas.create_text(x + max_width/2, y + line_height/2, anchor='center', text=class_name)

        # Draw the main rectangle with fields
        y += line_height
        rect_height = len(field_lines) * line_height
        self.canvas.create_rectangle(x, y, x + max_width+2 , y + rect_height+2, fill="LightCyan1")

        for i, line in enumerate(field_lines):
            self.canvas.create_text(x + 5, y + i * line_height + 5, anchor='nw', text=line)


# Tkinter setup
root = tk.Tk()
root.title("DrawNode Example")

canvas = tk.Canvas(root, width=400, height=300)
canvas.pack()

# Example usage
instance = CustomClass("Alice                       very very long name ", 30, "Engineer", "Wonderland")
drawer = DrawNode(canvas)
drawer.draw(instance, ["name", "occupation"], 50, 50)

root.mainloop()
