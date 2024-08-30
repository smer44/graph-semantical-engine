from gse.objgraph import ObjGraph
from gse.dictgraph import DictGraph
from gse.gol import Gol

def loads(text,gtype = "dict"):
    """
    loads the graph object from the text
    :return graph, list of root nodes
    """
    if gtype == "dict":
        graph = DictGraph()
    elif gtype == "dict-":
        graph = DictGraph()
        graph.inbox = False
    elif gtype == "obj":
        graph = ObjGraph()
    else:
        raise ValueError(f"loads: unknown graph type: {gtype}")

    gol = Gol(graph,output_root_only=True)
    return graph, [item for ctx, item in gol.load_gen(text.splitlines())]


def load( file,gtype = "dict"):
    """
    loads the text into the text file
    :return graph, list of root nodes
    """
    if gtype == "dict":
        graph = DictGraph()
    elif gtype == "dict-":
        graph = DictGraph()
        graph.inbox = False
    elif gtype == "obj":
        graph = ObjGraph()
    else:
        raise ValueError(f"loads: unknown graph type: {gtype}")

    gol = Gol(graph,output_root_only=True)
    return graph, [item for ctx, item in gol.load_gen(file.readlines())]


def dumps(graph,item):
    gol = Gol(graph, output_root_only=True)
    return "".join(gol.dump_gen(item, "", "\t"))

def dump(graph,item,file):
    gol = Gol(graph, output_root_only=True)
    for line in gol.dump_gen(item, "", "\t"):
        file.write(line)