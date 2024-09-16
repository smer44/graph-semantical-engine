import tkinter as tk
from tkinter import messagebox


class IdentityConverter:

    def tostr(self,value):
        return value

    def fromstr(self, value):
        return value


class StrToValueConverter:

    def __init__(self):
        self.known_fromstr = {"false" : False,
                      "False": False,
                      "true" : True,
                      "True" : True,
                      "None": None,
                      "none": None}

    def tostr(self,value):
        return str(value)

    def fromstr(self, value):
        try:
            return int(value)
        except ValueError:
            pass
        try:
            return float(value)
        except ValueError:
            pass

        return self.known_fromstr.get(value,value)






class ObjectDisplayFrame(tk.Frame):
    def __init__(self, master, graph,node,  *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.graph = graph
        self.node = node
        #self.displayed_fields = displayed_fields
        #self.immutable_fields = immutable_fields if immutable_fields is not None else []
        #TODO - this should be in the controller
        self.displayed_fields = None
        self.get_field = None
        self.set_field = None
        self.immutable_fields =None

        self.init_functions_for_entitygraph(graph,node)

        self.init_ui()

    def init_functions_for_entitygraph(self,graph,node):
        self.displayed_fields = list(node.gen_show_edit_fields())
        self.get_field = lambda field_name : node.get_field_or_sparent(field_name)
        self.set_field = lambda text : graph.add_field_or_parent_line(node,text)
        self.immutable_fields =node.gen_immutable_fields()

    def init_functions_for_python_object(self,graph,obj):
        self.displayed_fields = [ x for x in  dir(obj) if not x.startswith("_")]
        self.get_field = lambda field_name :  getattr(obj,field_name)
        self.set_field = lambda field_name,text : setattr(obj,field_name,text)
        self.immutable_fields = set()



    def init_ui(self):
        # Display the short class name above
        obj = self.node
        class_name_label = tk.Label(self, text=f"Class: {obj.__class__.__name__}")
        class_name_label.pack(side=tk.TOP, pady=5)


        # Create a frame for each field
        #self.field_frames = {}
        for field in self.displayed_fields:
            #if not hasattr(obj, field):
            #    raise AttributeError(f"Field '{field}' does not exist in the object.")
            #value = getattr(obj, field)
            #value = self.get_field(obj,field)
            field_frame = ObjectFieldDisplayFrame(self,field)
            field_frame.pack(side=tk.TOP, fill=tk.X, pady=2)

        # Warning label for displaying errors
        self.warning_label = tk.Label(self, text="", fg="red")
        self.warning_label.pack(side=tk.BOTTOM, fill=tk.X, pady=5)

        # Add button to create new field-value pair
        add_button = tk.Button(self, text="Add Field", command=self.add_new_field)
        add_button.pack(side=tk.BOTTOM, pady=5)

        # Add button to print object
        print_button = tk.Button(self, text="Print Object", command=self.print_object)
        print_button.pack(side=tk.BOTTOM, pady=5)




    def add_new_field(self):
        new_field_name = "NewField"
        if new_field_name in self.displayed_fields:
            messagebox.showerror("Error", "Field name 'NewField' already exists. Please rename it first.")
            return
        #if not hasattr(self.obj,new_field_name):
        #    setattr(self.obj, new_field_name, None)
        #self.displayed_fields.append(new_field_name)


        field_frame = ObjectFieldDisplayFrame(self,self.obj,new_field_name)
        field_frame.pack(side=tk.TOP, fill=tk.X, pady=2)

    def print_object(self):
        obj = self.node
        print(f"Object of type: {obj.__class__.__name__}")
        for field in self.displayed_fields(obj):
            value =  self.get_field(obj,field)# getattr(obj, field)
            print(f"{field}: {value.__class__.__name__}: {value}")

class ObjectFieldDisplayFrame(tk.Frame):

    def __init__(self, display_frame, field_name):
        super().__init__(display_frame)
        self.field_name = field_name
        self.is_immutable = field_name in display_frame.immutable_fields
        self.converter = IdentityConverter()#StrToValueConverter()
        self.init_ui()

    def init_ui(self):
        delete_button = tk.Button(self, text="Delete", command=self.delete_field)
        delete_button.pack(side=tk.LEFT, padx=5)
        if self.is_immutable:
            delete_button.config(state=tk.DISABLED)

        name_var = tk.StringVar(value=self.field_name)
        self.name_var = name_var
        name_entry = tk.Entry(self, textvariable=name_var)
        name_entry.pack(side=tk.LEFT, padx=5)

        if self.is_immutable:
            name_entry.config(state=tk.DISABLED)
        else:
            name_entry.bind("<Return>",self.update_field_name)
            name_entry.bind("<KeyRelease>", self.update_field_name)

        value = self.master.get_field(self.field_name) # getattr(self.obj,self.field_name)
        # Field value entry
        value_var = tk.StringVar(value="none" if value is None else str(value))
        self.value_var = value_var
        value_entry = tk.Entry(self, textvariable=value_var)
        value_entry.pack(side=tk.LEFT,fill = tk.BOTH, padx=5)
        value_entry.bind("<Return>", self.update_field_value)
        value_entry.bind("<KeyRelease>", self.update_field_value)

    def update_field_name(self, event):
        if not self.is_immutable:
            new_field_name = self.name_var.get().strip()
            old_field_name = self.field_name
            if new_field_name and new_field_name != old_field_name:
                arr = self.master.displayed_fields
                if new_field_name in arr:
                    self.master.warning_label.config(text= f"Field name {new_field_name} already exists!")
                else:
                    self.master.warning_label.config(text="")
                    self.field_name = new_field_name
                    field_value = self.converter.fromstr(self.value_var.get().strip())
                    delattr(self.obj, old_field_name)
                    setattr(self.obj, new_field_name, field_value)

                    arr[arr.index(old_field_name)] = new_field_name


    def update_field_value(self, event):
        print(" !! update_field_value")
        new_value = self.converter.fromstr(self.value_var.get().strip())
        field_name = self.name_var.get().strip()
        if field_name == self.field_name:
            self.master.set_field(self.field_name, new_value)
            #setattr(self.obj, self.field_name, new_value)
        else:
            self.master.warning_label.config(text=f"Field name {self.field_name} is not properly modifyed!")


    def delete_field(self):
        if self.is_immutable:
            messagebox.showwarning("Warning", f"Field '{self.field_name}' cannot be deleted.")
            return

        # Remove the attribute from the object
        delattr(self.obj, self.field_name)
        self.master.displayed_fields.remove(self.field_name)
        self.destroy()



