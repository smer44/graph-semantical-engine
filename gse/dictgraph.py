from agraph import dumps

class DictGraph:

    def __init__(self):
        self.deepsizes = dict()
        self.edges_of_node = dict()
        self.node_edge_nodes = dict()
        self.node_node_edges = dict()
        self.dumps = lambda node: dumps(self,node)


    def new_node(self,value):
        assert value not in self.deepsizes
        self.deepsizes[value] = 0
        return value

    def get_value(self,value):
        return value

    def add_child(self,parent,child, edge= None):
        row = self.edges_of_node.setdefault(parent, set())
        row.add(edge)
        row = self.node_edge_nodes.setdefault((parent,edge),set())
        row.add(child)
        row = self.node_node_edges.setdefault((parent, child), set())
        row.add(edge)

    def reset_deepsize(self):
        keys = list(self.deepsizes.keys())
        for key in keys:
            self.deepsizes[key] = 0

    def deepsize(self,node):
        return self.deepsizes[node]

    def set_deepsize(self,node,value):
        self.deepsizes[node] = value

    def children(self,node):
        edges = self.edges_of_node.get(node,None)
        if not edges:
            return None
        ret = []
        for edge in edges:
            ret.extend(self.node_edge_nodes[(node,edge)])
        return ret









