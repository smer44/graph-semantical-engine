from gse.dummy import *
from gse.load import *

text = """
Object: Entity 
Action : Entity 
#Action : Object#this should not be allowed if is_tree= True,
"""
g = DummyGraph()
roots = loads_parent_child(text.splitlines(),
                                inbox_fn = g.inbox_fn,
                                output_root_only = True ,
                                is_tree= True,
                                one_root = True ,
                                child_react = child_react_dummy_node,
                               )
print("One root test:")
for root in roots:
    print(root, root.children)


text = """
#comment1 
Object: Entity #comment2 #comment3 
Action : Entity 

Trait:Attribute
"""

g = DummyGraph()
roots = loads_parent_child(text.splitlines(),
                                inbox_fn = g.inbox_fn,
                                output_root_only = True ,
                                #is_tree= False,
                                one_root = False ,
                                child_react = child_react_dummy_node,
                              )
print("Many roots test:")
for root in roots:
    print(root, root.children)

