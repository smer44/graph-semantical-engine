from gse.objgraph import ObjGraph
from gse.gol import Gol

def loads(text):
    """
    loads the graph object from the text
    :return graph, list of root nodes
    """
    graph = ObjGraph()
    gol = Gol(graph,output_root_only=True)

    return graph, [item for ctx, item in gol.load_gen(text.splitlines())]


def load( file):
    """
    loads the text into the text file
    :return graph, list of root nodes
    """
    graph = ObjGraph()
    gol = Gol(graph,output_root_only=True)

    return graph, [item for ctx, item in gol.load_gen(file.readlines())]


def dumps(graph,item):
    gol = Gol(graph, output_root_only=True)
    return "".join(gol.dump_gen(item, "", "\t"))

def dump(graph,item,file):
    gol = Gol(graph, output_root_only=True)
    for line in gol.dump_gen(item, "", "\t"):
        file.write(line)