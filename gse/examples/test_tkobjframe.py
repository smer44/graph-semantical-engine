from  gse.tkobjframe import ObjectDisplayFrame
import tkinter as tk

# Example usage
class ExampleClass:
    def __init__(self, field1, field2, field3):
        self.field1 = field1
        self.field2 = field2
        self.field3 = field3

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Object Display")

    obj = ExampleClass("value1", None, 123)

    displayed_fields = ['field1', 'field2', 'field3']
    immutable_fields = ['field2']

    frame = ObjectDisplayFrame(root, obj, displayed_fields, immutable_fields)
    frame.pack(padx=10, pady=10)

    root.mainloop()
