from gse.dictgraph import DictGraph
from gse.gutil import ViewGraph
from gse.agraph import dumps
from gse import load
from gse.examples.dummy_display import ViewNodeDummyDisplay

#dummy graph:
og = DictGraph()

root = og.new_node("root")
a = og.new_node("a")
b = og.new_node("b")
ab = og.new_node("ab")

og.add_child(root,a)
og.add_child(root,b)
og.add_child(a,ab)
og.add_child(b,ab)

#load graph from file:

file = open("./load_me.txt", "r")
og, roots = load(file)



vg = ViewGraph()

vg.view_filter(og,roots,None,3)
nodes = vg.nodes
print("nodes:" , nodes)

print(dumps(vg,vg.roots[0]))

vg.place(vg.roots, 10,800-20,600-10,20,3)

print(dumps(vg,vg.roots[0]))

nodes = vg.nodes
print("nodes:" , nodes)

#call dummy displayer:
#app = ViewNodeDummyDisplay(nodes)
#app.mainloop()
from gse.gui import App
import tkinter as tk

root = tk.Tk()
app = App(root)
for vnode in nodes:
    app.add_item_to_canvas(vnode)
    #print("recht_id children: ", vnode.children)
for vnode in nodes:
    for child in vg.children(vnode):
        app.create_arrow(vnode,child)
root.mainloop()




