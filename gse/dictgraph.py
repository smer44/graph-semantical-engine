from gse.dump import dumps_indents
from gse.inbox import InboxValue

class DictGraph:

    def __init__(self):
        self.nodes = dict()
        self.edges_of_node = dict()
        self.node_edge_nodes = dict()
        self.node_node_edges = dict()
        self.inbox = True
        self.dumps = lambda node: dumps_indents(node,
                                                self.children,
                                                )


    def new_node(self,value):
        assert value not in self.nodes
        if self.inbox:
            node = InboxValue(value)
        else:
            node = value
        self.nodes[value] = node
        return node

    def get_value(self,node):
        if self.inbox:
            return node.value
        return node

    def add_child(self,parent,child, edge= None):
        row = self.edges_of_node.setdefault(parent, set())
        row.add(edge)
        row = self.node_edge_nodes.setdefault((parent,edge),set())
        row.add(child)
        row = self.node_node_edges.setdefault((parent, child), set())
        row.add(edge)



    def children(self,node):
        edges = self.edges_of_node.get(node,None)
        if not edges:
            return None
        ret = []
        for edge in edges:
            ret.extend(self.node_edge_nodes[(node,edge)])
        return ret

    def children_edge(self,node,edge):
        return self.node_edge_nodes.get((node,edge), None)







