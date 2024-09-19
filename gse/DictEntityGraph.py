from gse.dictgraph import DictGraph


class DictEntityGraph(DictGraph):

    def __init__(self):
        DictGraph.__init__(self)
        self.edge_types = "++","+","-"
        #self.children_types = None

    #WRONG:
    def get_all_fields_for_gui_by_id(self,id):
        return self.children_by_id_and_edges(id,self.edge_types)

    def get_all_immutable_fields_for_gui_by_id(self, id):
        return None

    def get_header_by_id(self,id):
        node_name =self.values[id]
        parent = list(self.children_by_id_and_edge(id,"++"))
        assert len(parent) == 1
        header = f"{node_name} : {parent[0]}"
        return header

    def get_field_type_name_value_by_id(self,id):
        common_field_names = self.edges_of_node[id] - self.edge_types

        for value in self.children_by_id_and_edge(id,"++"):
                yield "++" , value, value

        for value in self.children_by_id_and_edge(id,"+"):
            yield "+", value, value



