from gse.entitygraph import EntityGraph
from gse.load import loads_indents
from gse.dump import dumps_indents

text = """
action
    time
    place
    
object
    form
    place
    
place
    xcoord
    ycoord
    zcoord
"""



#TODO - need special dump what does not go deeper lvl 2

def load_entities(text):
    eg = EntityGraph()
    inbox_fn = eg.new_node_from_str
    output_root_only = True
    child_react = eg.add_child
    lines = text.splitlines()
    roots = [x for x in loads_indents(lines,inbox_fn,output_root_only=output_root_only,child_react=child_react)]
    return eg,roots

def dump_entity(graph,entity):
    children_fn = graph.children
    shallow_str = lambda entity: repr(entity)
    text = "".join(dumps_indents(entity,children_fn,shallow_str))
    return text

eg,roots = load_entities(text)

for root in roots:
    print("---")
    print(dump_entity(eg,root))


