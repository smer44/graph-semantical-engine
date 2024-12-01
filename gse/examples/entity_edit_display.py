from gse.tkeditobjframe import *
from gse.entitygraph import *
import tkinter as tk
from gse.entitygraphcontroller import EntityGraphController

#TODO : on delete sparent : TypeError: 'builtin_function_or_method' object is not subscriptable


eg = EntityGraph()

action = eg.get_or_create_node("action", )

speed = eg.add_field(action, "speed", "fast" )


controller = EntityGraphController()
root = tk.Tk()

frame = TkEditObjectFrame(root, action, controller)

frame.pack()

root.mainloop()
