from gse.dictgraph import DictGraph
from gse.gutil import ViewGraph
from gse.gio import dumps, load


#dummy graph:
og = DictGraph()

root = og.new_node("root")
a = og.new_node("a")
b = og.new_node("b")
ab = og.new_node("ab")

og.add_child_by_id(root,a,None)
og.add_child_by_id(root,b,None)
og.add_child_by_id(a,ab,None)
og.add_child_by_id(b,ab,None)

#load graph from file:

file = open("./load_me.txt", "r")
og, roots = load(file)



vg = ViewGraph()

vg.view_filter(og,roots,None,3)
nodes = vg.nodes
print("nodes:" , nodes)

print(dumps(vg,vg.roots[0]))

#vg.place(vg.roots, 10,20,800-10,600-20,3)

vg.place_stretch_min(vg.roots, 10,20,800-10,600-20,3,200,100)
vg.finalize_places()

print(dumps(vg,vg.roots[1]))

nodes = vg.nodes
print("nodes:" , nodes)

#call dummy displayer:
#app = ViewNodeDummyDisplay(nodes)
#app.mainloop()
from gse.gui import App
import tkinter as tk

root = tk.Tk()
app = App(root)
app.canvas.original_graph = og
for vnode in nodes: # no, this is view node
    #print(f"!! {vnode}, {type(vnode)} ,  {vnode.value}, {type(vnode.value)} ")
    item = vnode#og.values[vnode.value]
    app.canvas.add_item_to_canvas(item)
    #print("recht_id children: ", vnode.children)
for vnode in nodes:
    from_item = vnode#og.values[vnode.value]
    for child in vg.children(vnode):
        to_item = child#og.values[child.value]
        app.canvas.create_arrow(from_item,to_item)
root.mainloop()




