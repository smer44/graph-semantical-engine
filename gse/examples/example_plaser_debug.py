from gse.dictgraph import DictGraph
from gse.gutil import ViewGraph
from gse.gio import dumps, loads

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


xmin,ymin = 100,50
vg.place_stretch_min(vg.roots, 10,20,800-10,600-20,3,xmin,ymin)
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
app.canvas.reset_graph(og,vg)
root.mainloop()




