import tkinter as tk

from tkinter import simpledialog
from gse.gutil import ViewNode
from gse.gio import load,load_lines,dumps
from gse.gutil import ViewGraph
from gse.inbox import InboxValue

from tkinter import (
    Frame,
    Label,
    Menu,
    StringVar,
    filedialog,
    simpledialog,
)
from gse.gcanvas import GraphCanvas



class GraphToView:
    def __init__(self):
        self.add_edge = self.__add_edge_view_item__
        self.to_view_node = self.__to_view_item__

    #def __to_view_item__(self,object):
    #    return Item(None,None,None,None,object,object.value)

    def __add_edge_view_item__(self,view_item_fro, edge_type, view_item_to ):
        row = view_item_fro.children_refs.setdefault(edge_type, set())
        assert view_item_to not in row
        row.add(view_item_to)

    def linear_convert_nodes(self,nodes,edges):
        converted_items = dict()
        for node in nodes:
            if node not in converted_items:
                view_item = self.to_view_node(node)
                converted_items[node] = view_item
        for fro,edge_type,to in edges:
            view_item_fro = converted_items[fro]
            view_item_to = converted_items[to]
            #row = view_item_fro.children_refs.setdefault(edge_type, set())
            self.add_edge(view_item_fro,edge_type, view_item_to)
        return converted_items

    def pp(self, converted_items):
        for node, view_item in converted_items.items():
            for edge_type, view_item_children in view_item.children_refs.items():
                print(" : " ,view_item, edge_type, view_item_children )



class App:
    def __init__(self, root):
        self.root = root
        self._add_menubar()
        self.variable_status = StringVar(self.root, 'не сохранено')
        self.variable_filename = StringVar(self.root, 'Новый файл')
        self._add_status_bar()
        self.file_name_graph = None
        #self.canvas = tk.Canvas(root, width=800, height=600, bg='white')

        self.canvas = GraphCanvas(root,800,600)
        self.root.bind("<Shift-X>", self.canvas.on_shift_x_press)


    def _add_menubar(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)

        # file menu:
        file_menu = Menu(menubar)
        file_menu.add_command(label='Save', command=self._on_save_graph)
        file_menu.add_command(label='Open', command=self._on_open_graph)
        file_menu.add_command(label='Create New ', command=self._on_new_graph)
        menubar.add_cascade(label="File", menu=file_menu)
        # edit menu:



        #help menu:
        help_menu = Menu(menubar)
        help_menu.add_command(label='Keymap', command=self._show_help_keymap)
        menubar.add_cascade(label="Help", menu=help_menu)

    def _show_help_keymap(self):
        text = """
        Left mouse click = select 
        Shift + Left mouse clicks = select multiple        
        
        Ctrl + Left mouse click = create new node 
        Alt + Left mouse click = delete node
        
        Right mouse click = select node for edge connection
        Second right mouse click = connect two nodes with the 
                                    edge
        
        Alt +  Left mouse click = delete the node
        Alt +  Second right mouse click = delete edge between 
                                            two nodes
        
        """
        tk.messagebox.showinfo("Keymap", text)


    def _add_status_bar(self):
        frame = Frame(self.root)
        label_status = Label(frame, textvariable=self.variable_status)
        label_status.pack(side=tk.LEFT)
        label_filename = Label(frame, textvariable=self.variable_filename)
        label_filename.pack(side=tk.LEFT)
        frame.pack(side=tk.BOTTOM)

    def _print_to_filename_bar(self, message):
        cut_message = message if len(message) < 40 else f'{message[:19]}...{message[-18:]}'
        self.variable_filename.set(cut_message)

    def _on_save_graph(self):
        """Method to save the graph to a file"""
        file_name_graph = filedialog.asksaveasfilename(
            filetypes=(('TXT files', '*.txt'), ('YAML files', '*.yaml')),
            initialfile=self.file_name_graph,
        )
        if file_name_graph:
            with open(file_name_graph, 'w', encoding='utf-8') as file_graph:
                pass

            self.file_name_graph = file_name_graph
            self._print_to_filename_bar(file_name_graph)
            self.variable_status.set('сохранено')

    def _on_open_graph(self):
        """Method to open a graph from the file"""
        file_name_graph = filedialog.askopenfilename(filetypes=(('TXT files', '*.txt'), ('YAML files', '*.yaml')))
        if file_name_graph:
            with open(file_name_graph, 'r', encoding='utf-8') as file_graph:
                #file_name_graph is str.
                lines = file_graph.readlines()
                if file_name_graph.endswith("_pc.txt"):
                    format = "parent_child"
                elif file_name_graph.endswith("_en.txt"):
                    format = "entities"
                else:
                    format = "indents"
                og, roots = load_lines(lines,format,gtype="dict")
                if not roots:
                    print("--- EMPTY Graph loaded: ---")
                    return

                print("--- Graph loaded: ---")
                #print(dumps(og,roots[0], inbox = False))
                #TODO currently, loading pure graph and then creates a viewgraph
                #og, roots = load(file_graph)
                vg = ViewGraph()
                vg.view_filter(og, roots, None, 5)


                vg.place_stretch_min(vg.roots, 10, 20, 800 - 10, 600 - 20, 3, 200,100)
                vg.finalize_places()
                self.canvas.delete_all()
                self.canvas.reset_graph(og,vg)

            self.file_name_graph = file_name_graph
            self._print_to_filename_bar(file_name_graph)

    def _on_new_graph(self):
        self.file_name_graph = None
        self.variable_status.set('не сохранено')
        self._print_to_filename_bar('Новый файл')

#-----------------------------------------


def run():
    root = tk.Tk()
    app = App(root)
    root.mainloop()


if __name__ == "__main__":
    run()
