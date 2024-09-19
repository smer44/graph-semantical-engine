from gse.dump import dumps_indents
from gse.inbox import InboxValue

class DictGraph:

    def __init__(self):
        self.values = dict()# id -> value
        self.ids = dict()#value -> id
        self.edges_of_node = dict()#node
        self.node_edge_nodes = dict()
        self.node_node_edges = dict()
        #self.unique_values= true

        self.dumps = lambda node: dumps_indents(node,
                                                self.children,
                                                )
    def new_node(self,id,value):
        assert value not in self.ids, f"DictGraph.new_node : trying to create new node with exising {id=}"
        assert id not in self.value, f"DictGraph.new_node : trying to create new node with exising {value=}"
        self.values[id] = value
        self.ids[value] = id
        return value

    def get_value(self,id):
        return self.values[id]

    def add_child_by_id(self,parent,child, edge):
        row = self.edges_of_node.setdefault(parent, set())
        row.add(edge)
        row = self.node_edge_nodes.setdefault((parent,edge),set())
        row.add(child)
        row = self.node_node_edges.setdefault((parent, child), set())
        row.add(edge)

    def add_child_by_value(self, parent, child, edge):
        parent_id = self.ids[parent]
        child_id = self.ids[child]
        self.add_child_by_id(parent_id,child_id,edge)


    def remove_child_by_id(self,parent,child,edge = None):
        row = self.edges_of_node[parent]
        row.remove(edge)
        row = self.node_edge_nodes[(parent,edge)]
        row.remove(child)
        row = self.node_node_edges[(parent,child)]
        row.remove(edge)


    def remove_child_by_value(self, parent, child, edge):
        parent_id = self.ids[parent]
        child_id = self.ids[child]
        self.remove_child_by_id(parent_id,child_id,edge)



    def children_by_id_all(self,id):
        edges = self.edges_of_node.get(id,None)
        return self.children_edges(id,edges)


    def children_by_id_and_edges(self,id,edges):
        if not edges:
            return None
        ret = []
        for edge in edges:
            ret.extend(self.node_edge_nodes[(id,edge)])
        return ret




    def children_by_id_and_edge(self,id,edge):
        return self.node_edge_nodes.get((id,edge), None)







