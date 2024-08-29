import tkinter as tk
from tkinter import simpledialog

#TODO - item is view.
class Item:
    def __init__(self, x0, y0, x1, y1, value,text):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.text = text
        self.value = value
        #self.selected = False
        self.rect_id = None

        self.text_id = None
        self.children = dict()  # List to store pairs (rect_id, arrow_id) of children by given arrows
        self.parents = dict() # List to store pairs (rect_id, arrow_id) of parents by given arrows

        self.children_refs = dict()

    def __repr__(self):
        return f"<!{self.rect_id}:{self.text}!>"

class GraphToView:

    def __init__(self):
        self.add_edge = self.__add_edge_view_item__
        self.to_view_node = self.__to_view_item__

    def __to_view_item__(self,object):
        return Item(None,None,None,None,object,object.value)

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


class gViewRechtPlaser:

    def __init__(self):
        pass
    #TODO - copy plaser











class App:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=800, height=600, bg='white')
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.selected_items = dict()
        self.selected_for_connect = None
        self.items = dict()
        self.drag_data = {"x": 0, "y": 0}

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        self.canvas.bind("<ButtonPress-3>", self.on_right_click)
        self.canvas.bind("<Double-1>", self.edit_text)
        #("<KeyPress-Shift_L>", shift_press)
        root.bind("<Shift-X>", self.on_shift_x_press)
        self.create_counter = 0
        self.create_items()





    def create_items(self):
        # Initialize some Item objects

        positions = [(100,75),(250,75),(400,75)]
        for x,y in positions:
            self.create_new_item(x,y)

    def create_arrow(self, from_item, to_item):
        if to_item.rect_id in from_item.children:
            assert from_item.rect_id in to_item.parents
            return

        # Calculate starting and ending points for the arrow
        coords = self.calc_arrow_coords(from_item, to_item)
        # Create the arrow
        arrow_id = self.canvas.create_line(*coords, arrow=tk.LAST, smooth=True)

        # Store arrow info in the from_item's children list
        from_item.children[to_item.rect_id] = arrow_id
        to_item.parents[from_item.rect_id] = arrow_id
        #print("line created : ",  from_item, to_item)

    def delete_arrow(self,from_item, to_item):
        if to_item.rect_id in from_item.children:
            assert from_item.rect_id in to_item.parents
            arrow_id = from_item.children[to_item.rect_id]
            check_arrow_id = to_item.parents[from_item.rect_id]
            assert arrow_id == check_arrow_id
            del from_item.children[to_item.rect_id]
            del to_item.parents[from_item.rect_id]
            self.canvas.delete(arrow_id)

    def update_arrows(self,item):
        for child_id, arrow_id in item.children.items():
            child_item  = self.items[child_id]
            coords = self.calc_arrow_coords(item,child_item)

            self.canvas.coords(arrow_id, *coords)
        for parent_id,arrow_id in item.parents.items():
            parent_item = self.items[parent_id]
            coords = self.calc_arrow_coords(parent_item, item)
            self.canvas.coords(arrow_id, *coords)

    def calc_arrow_coords_4sided(self,fro,to):
        fro_mid_x, fro_mid_y = (fro.x0 + fro.x1) / 2, (fro.y0 + fro.y1) / 2
        to_mid_x, to_mid_y = (to.x0 + to.x1) / 2, (to.y0 + to.y1) / 2
        dx =fro_mid_x - to_mid_x
        dy = fro_mid_y - to_mid_y
        dx_abs = abs(dx)
        dy_abs = abs(dy)
        if dx_abs > dy_abs:
            if dx > 0 :
                coords = fro.x0, fro_mid_y, to.x1, to_mid_y
            else:
                coords = fro.x1, fro_mid_y, to.x0, to_mid_y
        else:
            if dy > 0:
                coords = fro_mid_x, fro.y0,to_mid_x, to.y1
            else:
                coords = fro_mid_x, fro.y1, to_mid_x, to.y0
        return coords

    def calc_arrow_coords(self,fro,to):
        if fro.rect_id == to.rect_id:
            assert fro == to
            return self.calc_arrow_loopback_coords(fro)
        else:
            return self.calc_arrow_line_coords(fro,to)


    def calc_arrow_line_coords(self,fro,to):
        fro_mid_x, fro_mid_y = (fro.x0 + fro.x1) / 2, (fro.y0 + fro.y1) / 2
        to_mid_x, to_mid_y = (to.x0 + to.x1) / 2, (to.y0 + to.y1) / 2
        dx =fro_mid_x - to_mid_x
        dy = fro_mid_y - to_mid_y
        dx_abs = abs(dx)
        dy_abs = abs(dy)
        y_mid =   (fro_mid_y + to_mid_y)//2

        if dy > 0:
                coords = fro_mid_x, fro.y0, fro_mid_x,y_mid, to_mid_x,y_mid,  to_mid_x, to.y1
        else:
                coords = fro_mid_x, fro.y1,fro_mid_x, y_mid, to_mid_x, y_mid, to_mid_x, to.y0
        return coords

    def calc_arrow_loopback_coords(self,item):
        dx = 20
        dy = 10
        mid_x, mid_y = (item.x0 + item.x1) / 2, (item.y0 + item.y1) / 2

        coords = mid_x, item.y1, mid_x,item.y1+dy,item.x1+dx,item.y1+dy, item.x1+dx, mid_y, item.x1, mid_y,
        return coords




    def add_item_to_canvas(self, item):
        rect_id = self.canvas.create_rectangle(item.x0, item.y0, item.x1, item.y1, outline='gray',width=2)
        item.rect_id =rect_id
        #item.rect_id = self.canvas.create_rectangle(item.x0-2, item.y0-2, item.x1+2, item.y1+2, outline='gray', width=2)
        item.text_id = self.canvas.create_text((item.x0 + item.x1) / 2, (item.y0 + item.y1) / 2, text=item.value)
        #self.canvas.tag_bind(item.rect_id, '<Button-1>', lambda event, item=item: self.on_item_click(event, item))
        #self.canvas.tag_bind(item.text_id, '<Button-1>', lambda event, item=item: self.on_item_click(event, item))
        self.items[rect_id]=item

    def deselect_all(self,exclude):
        keyset = set(self.selected_items.keys())
        if exclude:
            keyset.discard(exclude)
        ids = list(keyset)
        for id in ids:
            self.switch_item(self.selected_items[id])
        #self.selected_items.clear()


    def switch_item(self, item):
        assert isinstance(item, Item), f"switch_item called with wrong key type : {type(item)=}"

        #print(f"switch_item called for {item}")
        id = item.rect_id
        if item.rect_id in self.selected_items:
            del self.selected_items[id]
        else:
            self.selected_items[id]= item

        self.update_color(item)

    def update_color(self,item):
        id = item.rect_id
        if id in self.selected_items:
            if self.selected_for_connect is not None and id == self.selected_for_connect.rect_id:
                outline = "purple"
            else:
                outline = "blue"
        else:
            if self.selected_for_connect is not None and id == self.selected_for_connect.rect_id:
                outline = "red"
            else:
                outline = "gray"

        self.canvas.itemconfig(id, outline=outline)



    def on_shift_x_press(self,event):
        #print("on_shift_x_press called")
        pairs = list(self.selected_items.items())
        for id, item in pairs:
            for child_id, arrow_id in item.children.items():
                if child_id not in self.selected_items:
                    self.switch_item(self.items[child_id])


    def on_button_press(self, event):
        item = self.find_closest_item(event.x, event.y)
        self.last_item = item
        self.last_event = event
        self.tasks_after = None
        self.dragged = False
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y
        #print("on_button_press: event: " , event.state)

        if event.state & 0x0004:#if CTRL is pressed:
            if item:
                self.tasks_after = "connect if drag"
            else:
                #TODO - create if no drag
                self.tasks_after = "create"

        elif event.state & 0x020000:# Check if ALT key is held to delete an item - 131080
            if item:
                self.tasks_after = "delete"
            else:
                self.deselect_all(None)

        elif event.state & 0x0001: # if shift pressed:
            if item:
                if item.rect_id in self.selected_items:
                    self.tasks_after = "switch if no drag"
                else:
                    self.switch_item(item)
        else:
            if item:
                if item.rect_id in self.selected_items:
                    self.tasks_after = "deselect and switch if no drag"
                else:
                    self.deselect_all(None)
                    self.switch_item(item)
            else:
                self.deselect_all(None)



    def execute_task(self, item,event):

        if self.tasks_after =="create":
            self.create_new_item(event.x,event.y)
        elif self.tasks_after == "delete":
            self.delete_item(item)

        elif self.tasks_after == "switch if no drag":
            if not self.dragged:
                self.switch_item(item)
        elif self.tasks_after == "deselect and switch if no drag":
            if not self.dragged:
                self.deselect_all(None)
                self.switch_item(item)

    def on_button_release(self, new_event):
        item = self.last_item
        event = self.last_event
        self.execute_task(item, event)

    def on_mouse_drag(self, event):
        self.dragged = True
        #print("on_mouse_drag called")
        assert isinstance(self.selected_items,dict)
        #item = self.drag_data["item"]
        items = self.selected_items.values()
        #print("dragging items : " , items)
        for item in items:
            dx = event.x - self.drag_data["x"]
            dy = event.y - self.drag_data["y"]
            self.canvas.move(item.rect_id, dx, dy)
            self.canvas.move(item.text_id, dx, dy)


            item.x0 += dx
            item.y0 += dy
            item.x1 += dx
            item.y1 += dy
            self.update_arrows(item)
            #self.canvas.coords(item.rect_id, item.x0,item.y0, item.x1, item.y1 )
            #self.canvas.coords(item.text_id, (item.x0 + item.x1) / 2, (item.y0 + item.y1) / 2,)
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y
        self.canvas.configure(bg='white')

    def on_right_click(self, event):
        item = self.find_closest_item(event.x, event.y)
        if item:
            if self.selected_for_connect ==None:
                self.selected_for_connect = item
            else:
                if  event.state & 0x020000:# Check if ALT key is held
                    #if ALT is pressed, delete edge if exists.
                    self.delete_arrow(self.selected_for_connect,item)
                else:
                    self.create_arrow(self.selected_for_connect,item)
                old_selected_item = self.selected_for_connect
                self.selected_for_connect = None
                self.update_color(old_selected_item)
            self.update_color(item)
        else:
            old_selected_item = self.selected_for_connect
            if old_selected_item is not None:
                self.selected_for_connect = None
                self.update_color(old_selected_item)




    def find_closest_item(self, x, y):
        for item in self.items.values():
            if item.x0 <= x <= item.x1 and item.y0 <= y <= item.y1:
                return item
        return None

    def edit_text(self, event):
        item = self.find_closest_item(event.x, event.y)
        if item:
            new_text = simpledialog.askstring("Input", "Edit text:", initialvalue=item.text)
            if new_text:
                item.text = new_text
                self.canvas.itemconfig(item.text_id, text=new_text)



    def create_new_item(self, x, y):
        print ("create_new_item: " , x, y )
        dx0,dy0,dx1,dy1 = -50,-25,50,25  # Define the size of the new item
        #print("create_new_item: items:" , self.items)#
        text = f"New Item {self.create_counter}"
        #TODO - this must be changed to creating a node out of text value
        new_item = Item(x+dx0, y+dy0, x + dx1, y + dy1, text,text )
        self.create_counter+=1
        self.add_item_to_canvas(new_item)


    def delete_item(self, item):
        print("delete_item: ", item)
        assert item.rect_id in self.items
        # Remove item from canvas
        self.canvas.delete(item.rect_id)
        self.canvas.delete(item.text_id)
        #Remove all arrows from and to this item:
        self.delete_arrows(item)
        # Remove item from items list
        if item.rect_id in self.selected_items:
            del self.selected_items[item.rect_id]
            del self.items[item.rect_id]

    def delete_arrows(self,item):
        for rect_id, arrow_id in item.children.items():
            self.canvas.delete(arrow_id)
            other_item = self.items[rect_id]
            del other_item.parents[item.rect_id]
        for rect_id, arrow_id in item.parents.items():
            self.canvas.delete(arrow_id)
            other_item = self.items[rect_id]
            del other_item.children[item.rect_id]

def run():
    root = tk.Tk()
    app = App(root)
    root.mainloop()


if __name__ == "__main__":
    run()
