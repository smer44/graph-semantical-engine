from gse.dump import dumps_indents
from gse.inbox import InboxValue

class DictGraph:

    def __init__(self):
        self.values = dict()# id -> value
        self.ids = dict()#value -> id
        self.edges_of_node = dict()#node
        self.node_edge_nodes = dict()
        self.node_node_edges = dict()
        self.max_id = 0
        #self.unique_values= true
        self.children_edge = self.children_by_id_and_edge
        self.children = self.children_by_id_all
        self.root_node_ids = []
        self.dumps = lambda node: dumps_indents(node,
                                                children_fn = self.children,
                                                shallow_str = lambda id: self.values[id]
                                                )
    def dumps_roots(self):
        lines = []
        for root_node_id in self.root_node_ids:
            for line in self.dumps(root_node_id):
                lines.append(line)
        return "\n".join(lines)

    def replace_value(self,old_value,new_value):
        id = self.ids[old_value]
        del self.ids[old_value]
        self.ids[new_value] = id
        self.values[id] = new_value

    def new_node(self,value, id = None):
        """
        Creates a node inside a dictgraph about a value
        :param value: Value given
        :param id: Id of a value int, what will be used in graph operations.
        Give None to
        :return:
        """
        assert id is None or isinstance(id,int), f"DictGraph.new_node : id must be int or None {id=}"
        assert value not in self.ids, f"DictGraph.new_node : trying to create new node with exising {value=}"
        assert id not in self.values, f"DictGraph.new_node : trying to create new node with exising {id=}"
        if id is None:
            id = self.max_id
        self.max_id = max (id+1,self.max_id)
        self.values[id] = value
        self.ids[value] = id
        self.root_node_ids.append(id)
        return id

    def get_value(self,id):
        assert isinstance(id,int), f"DictGraph.get_value : wrong: {id=} , {type(id)=}"
        return self.values[id]

    def add_child_by_id(self,parent,child, edge= None):
        row = self.edges_of_node.setdefault(parent, set())
        row.add(edge)
        row = self.node_edge_nodes.setdefault((parent,edge),set())
        row.add(child)
        row = self.node_node_edges.setdefault((parent, child), set())
        row.add(edge)
        #if parent != child:
        #    assert child in self.root_node_ids, f"dictgraph.add_child_by_id, not it roots = {self.root_node_ids}: {child=}"
        #    self.root_node_ids.remove(child)

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
        return self.children_by_id_and_edges(id,edges)


    def children_by_id_and_edges(self,id,edges):
        if not edges:
            return None
        ret = []
        for edge in edges:
            ret.extend(self.node_edge_nodes[(id,edge)])
        return ret




    def children_by_id_and_edge(self,id,edge):
        assert isinstance(id, int) , f"children_by_id_and_edge: id is not an int: {id=}"
        return self.node_edge_nodes.get((id,edge), None)

    def children_by_value_and_edge(self,value,edge):

        id = self.ids[value]
        assert isinstance(id, int), f"children_by_id_and_edge: id is not an int: {id=}"
        return self.node_edge_nodes.get((id,edge), None)







