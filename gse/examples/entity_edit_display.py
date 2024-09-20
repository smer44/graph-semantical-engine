from gse.tkeditobjframe import *
from gse.entitygraph import *
import tkinter as tk

eg = EntityGraph()

action = eg.get_or_create_node("action", )

speed = eg.add_field(action, "speed", "fast" )

root = tk.Tk()

frame = TkEditObjectFrame(root, action)

frame.pack()

root.mainloop()
