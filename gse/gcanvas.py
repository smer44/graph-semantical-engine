from tkinter import Canvas, simpledialog, BOTH,LAST
from gse.inbox import InboxValue
from gse.gutil import ViewNode
from gse.gCanvasObjItemRender import gCanvasStringItemRenderer
from gse.gitemovalrenderer import gCanvasStringOvalItemRenderer
from gse.gitemclzrenderer import gCanvasClzItemRenderer
class GraphCanvas(Canvas):
    def __init__(self,tk_root,width,height):
        super().__init__(tk_root, width=width, height=height,bg='white')
        self.pack(fill=BOTH, expand=True)
        self.selected_items = dict()
        self.selected_for_connect = None
        self.items = dict()
        self.drag_data = {"x": 0, "y": 0}
        self.renderer = gCanvasClzItemRenderer()
        self.bind("<ButtonPress-1>", self.on_button_press)
        self.bind("<B1-Motion>", self.on_mouse_drag)
        self.bind("<ButtonRelease-1>", self.on_button_release)
        self.bind("<ButtonPress-3>", self.on_right_click)
        self.bind("<Double-1>", self.edit_text)

        self.bind("<ButtonPress-2>", self.on_middle_button_press)  # Middle mouse button pressed
        self.bind("<B2-Motion>", self.on_middle_button_drag)  # Middle mouse button dragged

        # Store the start position of the drag
        self.middle_drag_data = {"x": 0, "y": 0}

        self.create_counter = 0

    def create_default_items(self):
        # Initialize some Item objects

        positions = [(100,75),(250,75),(400,75)]
        for x,y in positions:
            self.create_new_item(x,y)

    def create_arrow(self, from_item, to_item):
        #print(f"{to_item=}, {to_item.rect_id=} , {from_item.children=}")
        if to_item.rect_id in from_item.children:
            assert from_item.rect_id in to_item.parents
            return

        # Calculate starting and ending points for the arrow
        coords = self.calc_arrow_coords(from_item, to_item)
        # Create the arrow
        arrow_id = self.create_line(*coords, arrow=LAST, smooth=True)

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
            self.delete(arrow_id)

    def update_arrows(self,item):
        for child_id, arrow_id in item.children.items():
            child_item  = self.items[child_id]
            coords = self.calc_arrow_coords(item,child_item)

            self.coords(arrow_id, *coords)
        for parent_id,arrow_id in item.parents.items():
            parent_item = self.items[parent_id]
            coords = self.calc_arrow_coords(parent_item, item)
            self.coords(arrow_id, *coords)


    def calc_arrow_coords_4sided(self,fro,to):
        fro_mid_x, fro_mid_y = (fro.left + fro.right) / 2, (fro.bottom + fro.top) / 2
        to_mid_x, to_mid_y = (to.left + to.right) / 2, (to.bottom + to.top) / 2
        dx =fro_mid_x - to_mid_x
        dy = fro_mid_y - to_mid_y
        dx_abs = abs(dx)
        dy_abs = abs(dy)
        if dx_abs > dy_abs:
            if dx > 0 :
                coords = fro.left, fro_mid_y, to.right, to_mid_y
            else:
                coords = fro.right, fro_mid_y, to.left, to_mid_y
        else:
            if dy > 0:
                coords = fro_mid_x, fro.bottom,to_mid_x, to.top
            else:
                coords = fro_mid_x, fro.top, to_mid_x, to.bottom
        return coords

    def calc_arrow_coords(self,fro,to):
        if fro.rect_id == to.rect_id:
            assert fro == to
            return self.calc_arrow_loopback_coords(fro)
        else:
            return self.calc_arrow_line_coords(fro,to)

    def calc_arrow_line_coords(self,fro,to):
        fro_mid_x, fro_mid_y = (fro.left + fro.right) / 2, (fro.bottom + fro.top) / 2
        to_mid_x, to_mid_y = (to.left + to.right) / 2, (to.bottom + to.top) / 2
        dx =fro_mid_x - to_mid_x
        dy = fro_mid_y - to_mid_y
        dx_abs = abs(dx)
        dy_abs = abs(dy)
        y_mid =   (fro_mid_y + to_mid_y)//2

        if dy > 0:
                coords = fro_mid_x, fro.bottom, fro_mid_x,y_mid, to_mid_x,y_mid,  to_mid_x, to.top
        else:
                coords = fro_mid_x, fro.top,fro_mid_x, y_mid, to_mid_x, y_mid, to_mid_x, to.bottom
        return coords

    def calc_arrow_loopback_coords(self,item):
        dx = 20
        dy = 10
        mid_x, mid_y = (item.left + item.right) / 2, (item.bottom + item.top) / 2

        coords = mid_x, item.top, mid_x, item.top + dy, item.right + dx, item.top + dy, item.right + dx, mid_y, item.right, mid_y,
        return coords


    def add_item_to_canvas(self, item):
        #print(f"add_item_to_canvas : Left: {item.left}, Bottom: {item.bottom}, Right: {item.right}, Top: {item.top}")
        #assert item.left is not None and item.bottom is not None and item.right is not None and item.top is not None
        #item.text_id = self.create_text((item.left + item.right) / 2, (item.bottom + item.top) / 2, text=item.value.value)
        self.renderer.create_visual_item(self,item)
        self.items[item.rect_id]=item



    def deselect_all(self,exclude):
        keyset = set(self.selected_items.keys())
        if exclude:
            keyset.discard(exclude)
        ids = list(keyset)
        for id in ids:
            self.switch_item(self.selected_items[id])

    def switch_item(self, item):
        #assert isinstance(item, ViewNode), f"switch_item called with wrong key type : {type(item)=}"

        #print(f"switch_item called for {item}")
        id = item.rect_id
        if item.rect_id in self.selected_items:
            del self.selected_items[id]
        else:
            self.selected_items[id]= item

        self.update_color(item)


    def update_color(self,item):
        id = item.rect_id
        is_selected = id in self.selected_items
        is_selected_for_connect = self.selected_for_connect is not None and id == self.selected_for_connect.rect_id
        self.renderer.update_color(self,item,is_selected, is_selected_for_connect)


    def on_shift_x_press(self,event):
        print("on_shift_x_press: called")
        pairs = list(self.selected_items.items())
        for id, item in pairs:
            #print(f"on_shift_x_press: selected pair: {id=}, {item=}")
            for child_id, arrow_id in item.children.items():
                if child_id not in self.selected_items:
                    self.switch_item(self.items[child_id])


    def on_button_press(self, event):
        print("on_button_press: event: ", event.state)
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

            self.renderer.move_visual_item(self,item,dx, dy)

            item.left += dx
            item.bottom += dy
            item.right += dx
            item.top += dy

            self.update_arrows(item)
            #self.coords(item.rect_id, item.x0,item.y0, item.x1, item.y1 )
            #self.coords(item.text_id, (item.x0 + item.x1) / 2, (item.y0 + item.y1) / 2,)
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y
        self.configure(bg='white')


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
            #left,bottom,right,top = item.rect_id
            if item.left <= x <= item.right and item.bottom <= y <= item.top:
                return item
        return None


    def edit_text(self, event):
        item = self.find_closest_item(event.x, event.y)
        if item:
            new_text = simpledialog.askstring("Input", "Edit text:", initialvalue=str(item.value))
            if new_text:
                self.renderer.update_text_on_item(self,item,new_text)


    #TODO - this should be removed to some creator:
    def create_new_item(self, x, y):
        print ("create_new_item: " , x, y )
        dx0,dy0,dx1,dy1 = -50,-25,50,25  # Define the size of the new item
        #print("create_new_item: items:" , self.items)#
        text_var = InboxValue(f"New Item {self.create_counter}")
        #TODO - this must be changed to creating a node out of text value
        new_item = ViewNode(text_var)
        new_item.set_coords(x+dx0, y+dy0, x + dx1, y + dy1)
        self.create_counter+=1
        self.add_item_to_canvas(new_item)


    def delete_item(self, item):
        print("delete_item: ", item)
        assert item.rect_id in self.items
        # if this is currently selected item for connect, remove selected_for_connect item
        if self.selected_for_connect is not None and  item.rect_id == self.selected_for_connect.rect_id:
            #print(f"removed {item.rect_id} from self.selected_for_connect")
            self.selected_for_connect = None
        #if this item is in selection, remove it from selection:
            if item.rect_id in self.selected_items:
                #print(f"removed {item.rect_id} from selected_items")
                del self.selected_items[item.rect_id]


        # Remove item from canvas
        self.renderer.delete_visual_item(self,item)
        #Remove all arrows from and to this item:
        self.delete_arrows(item)
        # Remove item from items list
        if item.rect_id in self.selected_items:
            del self.selected_items[item.rect_id]
            del self.items[item.rect_id]

    def delete_arrows(self,item):
        for rect_id, arrow_id in item.children.items():
            self.delete(arrow_id)
            other_item = self.items[rect_id]
            del other_item.parents[item.rect_id]
        for rect_id, arrow_id in item.parents.items():
            self.delete(arrow_id)
            other_item = self.items[rect_id]
            del other_item.children[item.rect_id]


    def on_middle_button_press(self, event):
        """Store the initial position when the middle mouse button is pressed."""
        print("on_middle_button_press called")
        self.middle_drag_data["x"] = event.x
        self.middle_drag_data["y"] = event.y

    def on_middle_button_drag(self, event):
        """Move the content on the canvas when dragging with the middle mouse button."""
        #print("on_middle_button_drag called")
        # Calculate the distance moved
        delta_x = event.x - self.middle_drag_data["x"]
        delta_y = event.y - self.middle_drag_data["y"]

        # Move all canvas items
        self.move_all(delta_x, delta_y)

        # Update the drag start position
        self.middle_drag_data["x"] = event.x
        self.middle_drag_data["y"] = event.y


    def move_all(self, dx, dy):
        """Move all items on the canvas by a given offset."""
        #self.move("content", delta_x, delta_y)
        #self.configure(bg='white')

        for item in self.items.values():
            self.move(item.rect_id, dx, dy)
            self.move(item.text_id, dx, dy)

            item.left += dx
            item.bottom += dy
            item.right += dx
            item.top += dy

            self.update_arrows(item)
        self.configure(bg='white')



    def add_nodes(self,viewgraph,nodes):
        for vnode in nodes:
            self.add_item_to_canvas(vnode)
            # print("recht_id children: ", vnode.children)
        for vnode in nodes:
            for child in viewgraph.children(vnode):
                self.create_arrow(vnode, child)


    def delete_all(self):
        self.delete("all")
        #self.configure(bg='white')
        self.selected_items = dict()
        self.selected_for_connect = None
        self.items = dict()