from gse.dictgraph import DictGraph
from gse.gutil import ViewGraph
from gse import dumps
from gse import loads
from gse.examples.dummy_display import ViewNodeDummyDisplay

#load graph from string:

#file = open("./load_me.txt", "r")

text = """
Living room
    Sofa
    TV
Bedroom
    Bed
    Sofa
"""

og, roots = loads(text)



vg = ViewGraph()

vg.view_filter(og,roots,None,3)
nodes = vg.nodes
print("nodes:" , nodes)



vg.place_stretch_min(vg.roots, 10,20,800-10,600-20,3)
vg.finalize_places()
print(dumps(vg,vg.roots[0]))
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
for vnode in nodes:
    app.add_item_to_canvas(vnode)
    #print("recht_id children: ", vnode.children)
for vnode in nodes:
    for child in vg.children(vnode):
        app.create_arrow(vnode,child)
root.mainloop()




