

class Entity:
    id_counter = 0
    def __init__(self,name,idn,**kwargs):
        self.name = name
        self.fields = kwargs
        if idn is None:
            idn = Entity.id_counter
        self.idn = idn
        Entity.id_counter = idn+1

    def add_field(self,field_entity):
        name = field_entity.name
        assert name not in self.fields
        self.fields[name] = field_entity

    def __repr__(self):
        return f"{self.idn}.{self.name}"

    def get_displayed_fields(self):
        return self.fields.keys()


class EntityGraph:

    def __init__(self):
        self.entities = []
        self.entities_dict = dict()

    def new_node_from_str(self,id_dot_name):
        spl = id_dot_name.split(".")
        if len(spl) == 1:
            idn, name = None, spl[0]
        elif len(spl) ==2:
            idn, name = spl
        else:
            raise ValueError(f"EntityGraph.new_node_from_str : wrong str:{id_dot_name}")

        assert name not in self.entities_dict
        node = Entity(name,idn)
        self.entities.append(node)
        self.entities_dict[name] = node
        return node

    def add_child(self, parent, child):
        parent.add_field(child)

    def children(self,node):
        return node.fields.values()












