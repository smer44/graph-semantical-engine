from gse.load import load_one_indent
from gse.entitygraph import EntityGraph
from gse.dump import dumps_indents
from gse.gio import load_entities_with_fields

text = """
PhysicalObject: Object
    +Physical # secondary parent
    -size
    -shape

AssumedObject: Object,Assumed # multiple parents
#and no fields


InfoObject: Info, Object # order check
    -infotype      
"""

eg = EntityGraph()




def dump_entity_indents(graph,entity):
    children_fn = graph.fields_names
    shallow_str = lambda entity: repr(entity)
    text = "".join(dumps_indents(entity,children_fn,shallow_str))
    return text

def dump_entity_children(graph,entity):
    children_fn = graph.children
    shallow_str = lambda entity: repr(entity)
    text = "".join(dumps_indents(entity,children_fn,shallow_str))
    return text


eg,roots = load_entities_with_fields(text)

for root in roots:
    print("---")
    print(root.dump_debug())

print(eg.entities)
for node in eg.entities:
    print("-+-")
    print(dump_entity_children(eg,node))

