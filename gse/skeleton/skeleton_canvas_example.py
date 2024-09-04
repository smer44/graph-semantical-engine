import tkinter as tk
from  math import radians , atan2,sqrt, sin, cos

class SceletonNode:
    _id_counter = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.children = set()
        self.disp_item = None
        self.line_from_parent=None
        self.parent = None
        self.id = SceletonNode._id_counter
        self.r = 10
        self.selected = False
        self.unmovable = False


        SceletonNode._id_counter += 1

    def add_child(self, node):
        self.children.add(node)
        assert node.parent is None
        node.parent = self

    def remove_child(self, node):
        self.children.discard(node)

    def __hash__(self):
        return self.id

    def __str__(self):
        return f"(({self.x}:{self.y}))"

    def __repr__(self):
        return f"(({self.x}:{self.y}))"

class SceletonCanvas(tk.Canvas):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(fill=tk.BOTH, expand=True)
        self.bind("<Button-1>", self.on_left_click)
        self.bind("<B1-Motion>", self.on_drag)
        self.bind("<Shift-B1-Motion>", self.on_drag_deep)
        self.bind("<ButtonRelease-1>", self.on_drop)
        self.bind("<Button-3>", self.on_right_click)
        self.bind("<Alt-Button-3>", self.on_alt_right_click)
        self.bind("<MouseWheel>", self.on_mouse_wheel)
        self.bind("<Shift-MouseWheel>", self.on_mouse_wheel_deep)

        self.nodes = set()
        self.skeleton_root = None
        self.selected_node = None
        self.drag_data = {"item": None}
        self.add_chain = True

    def on_mouse_wheel(self, event):
        if self.selected_node:
            child = self.selected_node
            parent = child.parent
            if parent:
                angle_delta = radians(5)  # Rotate by 5 degrees
                if event.delta < 0 :
                    angle_delta = -angle_delta
                self.rotate_node(parent, child, angle_delta )
                self.redraw_parent_line(child)
                self.redraw_deep(child)

    def on_mouse_wheel_deep(self, event):
        if self.selected_node:
            child = self.selected_node
            parent = child.parent
            if parent:
                angle_delta = radians(5)  # Rotate by 5 degrees
                if event.delta < 0:
                    angle_delta = -angle_delta
                self.rotate_deep(parent, child, angle_delta)
                self.redraw_parent_line(child)
                self.redraw_deep(child)

    def rotate_deep(self,parent,child,angle_delta):
        self.rotate_node(parent, child, angle_delta)
        for chichi in child.children:
            self.rotate_deep(parent,chichi,angle_delta)


    def rotate_node(self, parent, child, angle_delta):
        # Calculate current angle
        dx = child.x - parent.x
        dy = child.y - parent.y
        current_angle = atan2(dy, dx)

        # Calculate new angle
        new_angle = current_angle + angle_delta

        # Calculate new position
        distance = sqrt(dx ** 2 + dy ** 2)
        child.x = parent.x + distance * cos(new_angle)
        child.y = parent.y + distance * sin(new_angle)






    def dump_gen(self):
        r = self.skeleton_root
        rx,ry = r.x, r.y
        for n in self.nodes:
            p = n.parent
            if p:
                px, py= p.x-r.x, p.y-r.y
                yield f"{px} {py} {n.x - r.x} {n.y - r.y}"
            else:
                px,py = None, None
                yield f"{px} {py} {n.x} {n.y}"

    def dumpp(self):
        for line in self.dump_gen():
            print(line)

    def int_default(self,value):
        try:
            value = int(value)
        except ValueError:
            pass
        return value

    def load_lines(self, lines):
        by_coords = dict()
        for line in lines:
            line = line.strip()
            if line:
                px, py, x, y = [self.int_default(x.strip()) for x in line.split()]
                if px == "None":
                    assert  py == "None" and self.skeleton_root == None
                    self.skeleton_root = SceletonNode(x, y)
                    assert (x,y) not in by_coords
                    by_coords[(x,y)] = self.skeleton_root
                else:
                    r = self.skeleton_root
                    assert r, "load_lines: skeleton_root must be the first entry"
                    rx, ry = r.x, r.y
                    px, py, x, y = px+rx, py+ry, x+rx, y +ry
                    parent=  by_coords.get((px,py),None)
                    if not parent:
                        parent = SceletonNode(px, py)
                        by_coords[(px,py)] = parent
                    child = by_coords.get((x,y),None)
                    if not child:
                        child = SceletonNode(x, y)
                        by_coords[(x, y)] = child
                    parent.add_child(child)
        self.nodes.update(by_coords.values())
        self.redraw_deep(self.skeleton_root)







    def node_selected(self,node,x,y):
        return abs(node.x - x) <=node.r and abs(node.y - y) <=node.r
    def on_left_click(self, event):
        x,y = event.x , event.y
        for node in self.nodes:
            if self.node_selected(node,x,y):
                self.select(node)
                self.drag_data["item"] = node
                #print("on_left_click: self.drag_data:", self.drag_data["item"])
                return
        self.select(None)

    def on_drag(self, event):
        node = self.drag_data["item"]
        if node:
            dx = event.x - node.x
            dy = event.y - node.y
            self.move(node.disp_item, dx, dy)
            node.x = event.x
            node.y = event.y
            self.redraw_parent_line(node)
            self.redraw_deep(node)



    def deep_move(self,node,dx,dy):
        self.move(node.disp_item, dx, dy)
        node.x += dx
        node.y += dy
        for child in node.children:
            self.deep_move(child,dx,dy)


    def on_drag_deep(self,event):
        node = self.drag_data["item"]
        if node:
            dx = event.x - node.x
            dy = event.y - node.y
            self.deep_move(node,dx,dy)
            self.redraw_parent_line(node)
            self.redraw_deep(node)






    def on_drop(self, event):
        self.drag_data["item"] = None

    def on_right_click(self, event):
        self.add_node(event.x, event.y)


    def add_node(self,x,y):

        if self.skeleton_root == None:
            new_node = SceletonNode(x, y)
            self.nodes.add(new_node)
            self.skeleton_root = new_node
            self.select(new_node)
            self.redraw(self.selected_node)
        elif self.selected_node:
            new_node = SceletonNode(x, y)
            self.nodes.add(new_node)
            self.selected_node.add_child(new_node)
            self.redraw(self.selected_node)
            if self.add_chain:
                self.select(new_node)

    def select(self,node):
        if self.selected_node:
            self.selected_node.selected = False
            self.redraw_shallow(self.selected_node)
        self.selected_node = node
        if node:
            node.selected = True
            self.redraw_shallow(node)










    def on_alt_right_click(self, event):
        x,y = event.x, event.y
        for node in self.nodes:
            if self.node_selected(node,x,y):
                if self.selected_node == node:
                    self.selected_node = None
                if node.parent:
                    node.parent.remove_child(node)
                    self.delete(node.line_from_parent)
                else:
                    self.skeleton_root = None

                self.clear_display_deep(node)
                break

    def clear_display_deep(self,node):
        self.delete(node.disp_item)
        self.nodes.remove(node)
        for child in node.children:
            self.delete(child.line_from_parent)
            self.clear_display_deep(child)

    def redraw_parent_line(self,child):
        if child.line_from_parent:
            x,y,w,u = self.coords(child.line_from_parent)
            self.coords(child.line_from_parent, x, y, child.x, child.y)


    def redraw_shallow(self,node):
        r = node.r
        #print(f'redraw {node=}')
        if node.disp_item == None:
            node.disp_item = self.create_oval(
                node.x - r, node.y - r, node.x + r, node.y + r, fill="black"
            )
        else:
            self.moveto(node.disp_item, node.x - r, node.y - r)
        fill = ["black","blue"][node.selected]
        self.itemconfig(node.disp_item,fill =fill)

    def redraw_deep(self, node):
        self.redraw_shallow(node)

        for child in node.children:
            if child.line_from_parent == None:
                child.line_from_parent = self.create_line(node.x, node.y, child.x, child.y)
            else:
                self.coords(child.line_from_parent, node.x, node.y, child.x, child.y)
            self.redraw_deep(child)



class SceletonApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Skeleton Positioning Tool")
        self.geometry("1200x800")
        self.canvas = SceletonCanvas(self)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        self.canvas.dumpp()  # Print node-circle mappings before quitting
        self.destroy()  # Correctly close the program


human_skeleton = """
None None 609 458
0 0 0 -71
0 -71 -3 -257
-3 -257 -3 -346
0 -71 37 -247
0 -71 -39 -244
-39 -244 -68 -51
-68 -51 -94 8
37 -247 65 -51
65 -51 94 1
0 0 46 1
0 0 -43 0
-43 0 -43 147
-43 147 -45 285
-45 285 -70 308
46 1 41 145
41 145 41 280
41 280 64 305
"""


if __name__ == "__main__":
    app = SceletonApp()
    app.canvas.load_lines(human_skeleton.splitlines())
    app.mainloop()
