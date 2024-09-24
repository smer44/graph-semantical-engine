def to_prefix_field_pair_of_entity(prefix_field_name):
    assert isinstance(prefix_field_name,str), f"to_prefix_field_pair_of_entity : wrong {type(prefix_field_name)=}"
    if prefix_field_name[0] == "+":
        if len(prefix_field_name) > 1 and prefix_field_name[1] == "+":
            return "++", prefix_field_name[2:]
        return "+", prefix_field_name[1:]
    elif prefix_field_name[0] == "-":
        return "-", prefix_field_name[1:]
    else:
        raise ValueError(f"to_edge_type_field_name_pair: wrong {prefix_field_name=}")




class Entity:
    id_counter = 0
    def __init__(self,name,idn,**kwargs):
        self.name = name
        self.parent = None
        self.sparents = []
        self.fields = kwargs if kwargs is not None else dict()
        self.children = []
        if idn is None:
            idn = Entity.id_counter
        self.idn = idn
        Entity.id_counter = idn+1

    def __repr__(self):
        return f"{self.idn}.{self.name}"

    def __str__(self):
        return f"{self.name}"



class EntityGraph:

    def __init__(self):
        self.entities = []
        self.entities_dict = dict()
        self.new_node = self.get_or_create_node
        #self.get_value = lambda node_name : self.entities_dict[node_name]
        self.get_value = lambda entity: entity

    def set_field(self,node,field,value):
        node.fields[field]  = value
        return value

    def gen_roots(self):
        """
        Generator what returns all roots
        in the given graph. A root is an entity
        who has no main parent, and then also
        must not have secondary parents
        :return:
        """
        for entity in self.entities:
            if entity.parent is None:
                assert not entity.sparents, f"gen_roots : {entity=} has secondary parents but not main parent"
                yield entity
            #else:
            #    parent = self.get_or_create_node(entity.parent,True)
            #    yield parent

    def gen_primary_roots(self):
        dejavu = set()
        for entity in self.entities:
            parent = entity.parent
            if parent:
                if parent.parent is None:
                    assert not parent.sparents, f"gen_primary_roots : {parent=} has secondary parents but not the main parent"
                if parent.idn not in dejavu:
                    dejavu.add(parent.idn)
                    yield parent

    def add_field(self,node,field_name,field_value = None):
        assert field_name not in node.fields
        node.fields[field_name] = field_value

    def load_header(self, line, split_name_parent = ":", split_between_parents = ","):
        name_parents = line.split(split_name_parent)
        ln = len(name_parents)
        assert ln == 1 or ln == 2, f"load_header : wrong {split_name_parent=} for {line=}"
        parents = []
        if len(name_parents) == 2:
            name, parents_row = name_parents
        else:
            name, parents_row = name_parents[0], None
        name = name.strip()
        entity = self.get_or_create_node(name)
        if parents_row:
            for x in parents_row.split(split_between_parents):
                parent_name = x.strip()
                if parent_name:
                    parents.append(parent_name)
                    parent = self.get_or_create_node(parent_name, True)
                    parent.children.append(entity)
        self.set_parents(entity,parents)
        return entity, name






    def set_parents(self,node,parents):
        if parents:
            node.parent = parents[0]
            node.sparents = parents[1:]


    def add_parent(self, node, parent_name):
        #assert node not in parent.children
        assert isinstance(parent_name,str)
        assert parent_name != node.parent and parent_name not in node.sparents, f"add_parent: to {node=} ,adding {parent_name=} the second time"

        if not node.parent:
            node.parent = parent_name
            #parent.children.append(node)
        else:
            node.sparents.append(parent_name)
        parent_entity = self.get_or_create_node(parent_name,True)
        parent_entity.children.append(node)



    def get_node(self,id_dot_name):
        spl = id_dot_name.split(".")
        if len(spl) == 1:
            idn, name = None, spl[0]
        elif len(spl) ==2:
            idn, name = spl
        if idn is None:
            return self.entities_dict[name]
        else:
            idn = int(idn)
            node = self.entities[idn]
            node2 = self.entities_dict[name]
            assert node is node2 , f"get_node: id and node name mismatch for {id_dot_name}"
            return node




    def get_or_create_node(self,id_dot_name,get_if_exists=False):

        spl = id_dot_name.split(".")
        if len(spl) == 1:
            idn, name = None, spl[0]
        elif len(spl) ==2:
            idn, name = spl
        else:
            raise ValueError(f"EntityGraph.new_node_from_str : wrong str:{id_dot_name}")

        if get_if_exists:
            node = self.entities_dict.get(name, None)
            if node:
                assert idn is None or node.idn == idn, f"EntityGraph.new_node_from_str : wrong  {idn=} for {node=}"
                return node

        assert name not in self.entities_dict, f"EntityGraph.new_node_from_str : entity with {name=} already exists"
        node = Entity(name,idn)
        self.entities.append(node)
        self.entities_dict[name] = node
        return node


    def fields_names_if_entity(self,node):
        if isinstance(node, Entity):
            return self.children_edge(node, "-")
        return node


    def fields_values_if_entity_else_none(self,node):
        if isinstance(node, Entity):
            return [self.fields_names_if_entity(ename)  for ename in self.children_edge(node, "-") ]
        return None

    def children_edge(self,node,edge= None):
        if edge is None:
            return node.children
        elif edge == "++":
            return [self.entities_dict[node.parent]]
        elif edge == "+":
            return [self.entities_dict[sp] for sp in node.sparents]
        elif edge == "-":
            return node.fields.values()


    def line_to_prefix_field_name_value(self,line, split_symbol = ":"):
        prefix_field_name_value = line.split(split_symbol)
        if len(prefix_field_name_value) == 1:
            prefix_field_name, value = prefix_field_name_value[0], None
        else:
            assert len(prefix_field_name_value) == 2, f"add_field_or_parent_from_line : wrong {split_symbol=} amount in {line=}"
            prefix_field_name, value = prefix_field_name_value
        return prefix_field_name, value

    def load_field(self,entity, line, split_symbol = ":"):
        prefix_field_name, value = self.line_to_prefix_field_name_value(line,split_symbol)
        edge_type, field_name = to_prefix_field_pair_of_entity(prefix_field_name)
        self.add_prefix_field_value_for_load(entity, edge_type, field_name, value)
        return field_name

    def add_prefix_field_value_for_load(self,entity,edge_type, field_name, value):
        print(f"add_field_or_parent_for_load : {edge_type, field_name=} , {value=}")

        #assert edge_type != "++"
        if edge_type == "+":
            self.add_parent(entity,field_name)

        elif edge_type == "-":
            assert field_name not in entity.fields
            entity.fields[field_name] = value
        else:
            raise ValueError(f"add_prefix_field_value_for_load: wrong field prefix {edge_type}")



    def add_prefix_field_value(self,entity,prefix_field_name, value):
        print(f"add_field_or_parent_for_load : {prefix_field_name=} , {value=}")
        edge_type, field_name = to_prefix_field_pair_of_entity(prefix_field_name)
        if edge_type == "++":
            #assert field_name == value, f"add_field_or_parent: {field_name=} is unequal to {value=}"
            assert entity.parent == None
            entity.parent = field_name
        elif edge_type == "+":
            #assert field_name == value , f"add_field_or_parent: {field_name=} != {value=}"
            assert field_name not in entity.sparents
            entity.sparents.append(field_name)
        elif edge_type == "-":
            assert field_name not in entity.fields
            entity.fields[field_name] = value















