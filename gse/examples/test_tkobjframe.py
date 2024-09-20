from  gse.tkeditobjframe import TkEditObjectFrame
import tkinter as tk

# Example usage
class ExampleClass:
    def __init__(self, field1, field2, field3):
        self.field1 = field1
        self.field2 = field2
        self.field3 = field3

    def __str__(self):
        return "ExampleClass\n" + "\n".join(str(f"{k}:{type(v)}:{v}") for k,v in self.__dict__.items())

class ExampleController:

    def __init__(self):
        self.validate_all = self.validate_field_names_for_obj

    def gen_field_names_for_gui(self,obj):
        yield "field1"
        yield "field2"
        yield "field3"

    def gen_immutable_fields(self, obj):
            yield "field2"

    def get_prefixed_field_value(self,obj,field_name):
        return getattr(obj,field_name)

    def dump_field_name_values(self,obj):
        return str(obj)

    def add_new_field_for_gui(self,obj):
        n = len(obj.__dict__)
        field_name = f"field{n}"
        while hasattr(obj,field_name):
            n+=1
            field_name = f"field{n}"
        setattr(obj,field_name, "NewValue")
        return field_name

    def validate_field_names_for_obj(self, master):
        #obj = master.node
        field_frames = master.field_frames
        dejavu = set()
        for n, x in enumerate(field_frames):
            field_name = x.name_var.get().strip()
            if not field_name:
                return False , n, field_name
            if field_name in dejavu:
                return False , n, field_name
        return True, -1, None


    def update_all_fields_for_gui(self,obj,updates_items):
        for old_field_name in list(obj.__dict__.keys()):
            delattr(obj,old_field_name)
        for prefix_field_name, value in updates_items:
            #delattr(obj,)
            setattr(obj, prefix_field_name, value)
        return []

    def remove_field_for_gui(self,obj,field_name):
        delattr(obj, field_name)




if __name__ == "__main__":
    root = tk.Tk()
    root.title("Object Display")

    obj = ExampleClass("value1", None, 123)

    displayed_fields = ['field1', 'field2', 'field3']
    immutable_fields = ['field2']

    controller = ExampleController()
    frame = TkEditObjectFrame(root, obj, controller)
    frame.pack(padx=10, pady=10)

    root.mainloop()
