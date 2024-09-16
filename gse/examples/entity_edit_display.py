from gse.tkobjframe import *
from gse.entitygraph import *
import tkinter as tk

eg = EntityGraph()

action = eg.new_node_or_field_from_str("action", )

speed = eg.new_node_or_field_from_str("speed", )

eg.add_field(action,speed)

root = tk.Tk()

frame = ObjectDisplayFrame(root, eg, action)

frame.pack()

root.mainloop()
