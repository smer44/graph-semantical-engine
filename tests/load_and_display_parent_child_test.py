from gse.dummy import *
from gse.load import *

text = """
Object: Entity 
Action : Entity
Subject:Object
Subject:Action
"""

g = DummyGraph()

roots = loads_parent_child(text.splitlines(),
                                inbox_fn = g.inbox_fn,
                                output_root_only = True ,
                                is_tree= False,
                                one_root = True ,
                                child_react = child_react_dummy_node,
                               )
print("Load and display test:")
for root in roots:
    print(root, root.children)