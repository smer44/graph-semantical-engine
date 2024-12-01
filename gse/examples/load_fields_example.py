from gse.load import load_one_indent
from gse.entitygraph import EntityGraph
from gse.dump import dumps_indents #, dump_entity
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






def dump_entity_indents(graph,entity):
    children_fn_fields = lambda node : graph.fields_names_if_entity(node, "-")
    shallow_str = lambda entity: repr(entity)
    text = "".join(dumps_indents(entity,children_fn_fields,shallow_str))
    return text

def dump_entity_children(graph,entity):
    children_fn_fields = lambda node : graph.fields_names_if_entity(node)
    shallow_str = lambda entity: repr(entity)
    text = "".join(dump_entity(entity))
    return text

eg = EntityGraph()

lines = text.splitlines()
eg,roots = load_entities_with_fields(lines)

for root in roots:
    print("-- root --")
    print(root.dump_debug())

print(eg.entities)
for node in eg.entities:
    print("-+-")
    print(dump_entity_children(eg,node))

