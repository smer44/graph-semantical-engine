from gse.entitygraph import EntityGraph
from gse.objgraph import ObjGraph
from gse.dictgraph import DictGraph
from gse.load import loads_indents, loads_parent_children,load_one_indent
from gse.dump import dumps_indents, dumps_parent_children


def loads(text,format = "indents", gtype = "dict"):
    lines = text.splitlines()
    return load_lines(lines,format,gtype)

def load(file,format = "indents", gtype = "dict"):
    lines = file.readlines()
    return load_lines(lines,format,gtype)



def load_entities_with_fields(lines):
    eg = EntityGraph()
    inbox_fn = eg.new_node_or_field_from_str
    output_root_only = True
    child_react = eg.add_field_or_parent_line
    roots = [x for x in load_one_indent(lines,
                                        inbox_fn,
                                        output_root_only=output_root_only,
                                        child_react=child_react)
             ]
    return eg,roots


def load_lines(lines,format = "indents", gtype = "dict"):
    """
    loads the graph object from the text
    :return graph, list of root nodes
    """
    print(f"type of lines: {type(lines)}")
    if format == "entities"  or format == "entities":
        return load_entities_with_fields(lines)

    kwargs ={}
    if gtype =="d" or gtype == "dict":
        graph = DictGraph()
        kwargs["inbox_fn"] = graph.new_node
        #kwargs["get_known_node"] = graph.get_node_by_value_or_none
    elif gtype =="d-" or gtype == "dict-":
        graph = DictGraph()
        #kwargs["get_known_node"] = graph.get_node_by_value_or_none
    elif gtype =="o" or gtype == "obj":
        graph = ObjGraph()
        kwargs["inbox_fn"] = graph.new_node
    elif gtype =="o-" or gtype == "obj-":
        graph = ObjGraph()
    else:
        raise ValueError(f"loads: unknown graph type: {gtype}")

    kwargs["child_react"] = graph.add_child
    kwargs["output_root_only"] =  True
    if format == "indents":
        load_fn = loads_indents
    elif format == "parent_child":
        load_fn = loads_parent_children
        kwargs["inverse"] = False
    elif format == "child_parent":
        load_fn = loads_parent_children
        kwargs["inverse"] = True
    else:
        raise ValueError(f"loads: unknown format: {format}")

    #if kwargs["output_root_only"]:
    #    return graph, [item for item in load_fn(lines,**kwargs)]
    # else:
    return graph, [item for item in load_fn(lines, **kwargs)]

#TODO - extract that to loading/dumping options

def dumps(graph,item, format = "indents",inbox = True):
    return "".join(dump_lines(graph,item,format,inbox))

def dump(graph,item,file, format = "indents",inbox = True):
    for line in dump_lines(graph,item,format,inbox):
        file.write(line)


def dump_lines(graph,item, format = "indents",inbox = True ):
    kwargs = {}
    if format == "indents":
        dump_fn = dumps_indents
    elif format == "parent_child":
        dump_fn = dumps_parent_children
        kwargs["inverse"] = False
    elif format == "child_parent":
        dump_fn = dumps_parent_children
        kwargs["inverse"] = True
    else:
        raise ValueError(f"loads: unknown format: {format}")

    if inbox:
        shallow_str = lambda node: str(node.value)
    else:
        shallow_str = str
    return dump_fn(item,graph.children,shallow_str)
