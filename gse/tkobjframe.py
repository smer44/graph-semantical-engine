import tkinter as tk
from tkinter import messagebox
from gse.converter import IdentityConverter, StrToSimpleValueConverter



class ObjectDisplayFrame(tk.Frame):
    def __init__(self, master, graph,node,  *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.graph = graph
        self.node = node
        #self.displayed_fields = displayed_fields
        #self.immutable_fields = immutable_fields if immutable_fields is not None else []
        #TODO - this should be in the controller
        self.init_functions_for_entitygraph(graph,node)
        self.field_frames = []

        self.init_ui()

    def init_functions_for_entitygraph(self,graph,node):
        self.displayed_field_values = lambda : graph.gen_all_field_names_for_gui(node)
        #self.displayed_fields = list(node.gen_show_edit_fields())
        self.replace_field_value = lambda field_name,value,old_value : graph.replace_field_by_old_value_for_gui(node,field_name,value,old_value)
        self.replace_field_name_and_value  = lambda new_field_name,old_field_name,value,old_value : \
            graph.replace_field_name_value_by_old_name_value(node,new_field_name,old_field_name,value,old_value)
        self.immutable_fields =graph.gen_immutable_fields(node)
        self.get_field = lambda gui_field_name : graph.get_field_or_parent(node,gui_field_name)
        #self.check_field_name_for_replace = lambda field_name : graph.check_new_field_name_for_replace_for_gui(node,field_name)
        #self.check_field_name_for_add = lambda field_name : graph.check_new_field_name_for_add_for_gui(node,field_name)
        self.add_field = lambda  field_name,field_value: graph.add_field_for_gui(node,field_name,field_value)
        self.remove_field = lambda gui_field_name : graph.remove_field_for_gui(node,gui_field_name)
        self.update_all_obj = lambda update_dict:graph.update_all_fields_for_gui(node,update_dict)
        self.valiate_all = self.validate_field_names_for_entity

    def init_functions_for_python_object(self,obj):

        self.displayed_fields = self.get_any_obj_variable_names_values_dict(obj)
        self.get_field = lambda field_name :  getattr(obj,field_name)
        self.set_field = lambda field_name,text : setattr(obj,field_name,text)
        self.add_field = self.set_field
        self.remove_field = lambda gui_field_name: delattr(obj, gui_field_name)
        self.immutable_fields = set()

    def get_any_obj_variable_names_values_dict(self,obj):
        ret = dict()
        for k in dir(obj):
            if not k.startswith("_"):
                v = getattr(obj,k)
                if not callable(v):
                    ret[k]=v
        return ret



    def init_ui(self):
        # Display the short class name above
        obj = self.node
        class_name_label = tk.Label(self, text=f"Class: {obj.__class__.__name__}")
        class_name_label.pack(side=tk.TOP, pady=5)


        # Create a frame for each field
        #self.field_frames = {}
        for field_name in self.displayed_field_values():
            print(f"init : {field_name=}")
            #if not hasattr(obj, field):
            #    raise AttributeError(f"Field '{field}' does not exist in the object.")
            #value = getattr(obj, field)
            #value = self.get_field(obj,field)
            field_frame = ObjectFieldDisplayFrame(self,field_name)
            self.field_frames.append(field_frame)
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
        #new field name for an entity:
        new_field_name = "NewField"
        new_field_value ="NewValue"
        prefix_field_name = self.add_field(new_field_name, new_field_value)
        #if not self.check_new_field_name(new_field_name):
        if prefix_field_name is None:
            messagebox.showerror("Error", f"Wrong new field name: {new_field_name}")
            return
        #if not hasattr(self.obj,new_field_name):
        #    setattr(self.obj, new_field_name, None)
        #self.displayed_fields.append(new_field_name)

        #add new field:
        #prefix_field_name =  self.add_field(new_field_name, new_field_value)
        #TODO - WORKS ONLY FOR ENTITY:
        #prefix_field_name = "-" + new_field_name
        field_frame = ObjectFieldDisplayFrame(self,prefix_field_name)
        self.field_frames.append(field_frame)
        field_frame.pack(side=tk.TOP, fill=tk.X, pady=2)

    def print_object(self):
        obj = self.node
        print(f"Object of type: {obj.__class__.__name__}")
        for field_name in self.displayed_field_values():
            value =  self.get_field(field_name)# getattr(obj, field)
            print(f"{field_name}: {value.__class__.__name__}: {value}")

    def validate_field_names_for_entity(self):
        dejavu = set()
        was_root = False
        for n,x in enumerate(self.field_frames):
            field_name = x.name_var.get().strip()
            if not field_name:
                return False , n, field_name
            if field_name in dejavu:
                return False , n, field_name
            dejavu.add(field_name)
            if field_name[0] != "-" and field_name[0] != "+":
                return False, n, field_name + "field_name[0] or field_name[0]"
            else:
                if len(field_name) == 1:
                    return False, n, field_name + "len(field_name) == 1"

            if field_name.startswith("++"):
                if was_root or len(field_name) == 2:
                    return False, n, field_name
                was_root = True
        return True, -1, None


    def update_all_field_names_and_values(self):
        updates_items =[]
        for x in self.field_frames:
            field_name = x.name_var.get().strip()
            field_value = x.value_var.get().strip()
            updates_items.append((field_name,field_value))
        update_displayed_items = self.update_all_obj(updates_items)
        for (new_field_name,new_value), frame in zip(update_displayed_items,self.field_frames):
            frame.name_var.set(new_field_name)
            frame.value_var.set(new_value)




class ObjectFieldDisplayFrame(tk.Frame):

    def __init__(self, display_frame, field_name):
        super().__init__(display_frame)
        self.field_name = field_name

        self.is_immutable =display_frame.immutable_fields is not None and field_name in display_frame.immutable_fields
        self.converter = IdentityConverter()# StrToSimpleValueConverter()
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
            #name_entry.bind("<Return>",self.update_field_name)
            #name_entry.bind("<KeyRelease>", self.update_all_values)
            name_entry.bind("<Return>",self.update_all_values)
            name_entry.bind("<KeyRelease>", self.update_all_values)

        value = self.master.get_field(self.field_name) # getattr(self.obj,self.field_name)
        str_value = self.converter.tostr(value)
        print(f"get_field : {str_value=}")
        self.old_value = value
        # Field value entry
        value_var = tk.StringVar(value=str_value)
        self.value_var = value_var
        value_entry = tk.Entry(self, textvariable=value_var)
        value_entry.pack(side=tk.LEFT,fill = tk.BOTH, padx=5)
        #value_entry.bind("<Return>", self.update_field_value)
        value_entry.bind("<Return>", self.update_all_values)
        #value_entry.bind("<KeyRelease>", self.update_field_value)#update_all_values
        value_entry.bind("<KeyRelease>", self.update_all_values)


    def update_field_name(self, event):
        if not self.is_immutable:
            new_field_name = self.name_var.get().strip()
            old_field_name = self.field_name
            if new_field_name and new_field_name != old_field_name:
                #arr = self.master.displayed_field_values()
                #if not self.master.check_field_name_for_replace(new_field_name):
                correct_fields, wrong_field_number, wrong_field_name = self.master.validate_field_names_for_entity()
                if not correct_fields:
                    self.master.warning_label.config(text= f"Wrong field number {wrong_field_number} name {wrong_field_name}!")
                else:
                    self.master.warning_label.config(text="")
                    self.field_name = new_field_name
                    field_value = self.converter.fromstr(self.value_var.get().strip())
                    #assert self.old_value == field_value, f"update_field_name: {field_value=} unequal to {self.old_value=}"

                    field_name,new_field_value = self.master.replace_field_name_and_value(new_field_name,old_field_name,field_value,field_value )
                    if field_value !=new_field_value:
                        self.old_value = new_field_value
                        self.value_var.set(new_field_value)
                    #delattr(self.obj, old_field_name)
                    #setattr(self.obj, new_field_name, field_value)

                    #arr[arr.index(old_field_name)] = new_field_name
            else:
                self.master.warning_label.config(text="")


    def update_all_values(self,event):
        """
        To check the correction and get feedback from any object
        you must send him all changes and update all values simultaneously
        :param event:
        :return:
        """
        print(" !! update_all_values")
        is_correct, wrong_field_number, wrong_field_name = self.master.valiate_all()
        if not is_correct:
            self.master.warning_label.config(text=f"Field number {wrong_field_number} : {wrong_field_name} is incorrect!")

        else:
            self.master.warning_label.config(text="")
            self.master.update_all_field_names_and_values()



    def update_field_value(self, event):
        print(" !! update_field_value")
        new_value = self.converter.fromstr(self.value_var.get().strip())
        field_name = self.name_var.get().strip()
        if field_name == self.field_name:
            old_value = self.old_value
            field_name, field_value = self.master.replace_field_value(self.field_name, new_value, old_value)
            self.old_value = new_value
            if field_name != self.field_name:
                self.field_name = field_name
                self.name_var.set(field_name)
            #setattr(self.obj, self.field_name, new_value)
        else:
            self.master.warning_label.config(text=f"Field name {self.field_name} is not properly modifyed!")


    def delete_field(self):
        if self.is_immutable:
            messagebox.showwarning("Warning", f"This should not be called! Field '{self.field_name}' has immutable name.")
            return

        # Remove the attribute from the object
        self.master.remove_field(self.field_name)
        #delattr(self.obj, self.field_name)
        #self.master.displayed_fields.remove(self.field_name)
        self.master.field_frames.remove(self)
        self.destroy()



