from gse.objgraph import ObjGraph
from gse.dictgraph import DictGraph
from gse.load import loads_indents, loads_parent_children
from gse.dump import dumps_indents, dumps_parent_children


def loads(text,format = "indents", gtype = "dict"):
    lines = text.splitlines()
    return load_lines(lines,format,gtype)

def load(file,format = "indents", gtype = "dict"):
    lines = file.readlines()
    return load_lines(lines,format,gtype)


def load_lines(lines,format = "indents", gtype = "dict"):
    """
    loads the graph object from the text
    :return graph, list of root nodes
    """
    kwargs ={}
    if gtype =="d" or gtype == "dict":
        graph = DictGraph()
        kwargs["inbox_fn"] = graph.new_node
    elif gtype =="d-" or gtype == "dict-":
        graph = DictGraph()
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


    return graph, [item for ctx, item in load_fn(lines,**kwargs)]



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
