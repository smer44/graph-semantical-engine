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

    def gen_shown_fields(self):
        for sp in self.sparents:
            yield f"+{sp.name}" , f"{sp}"
        for k,v in self.fields.items():
            yield f"-{k}" , f"{v}"

    #this must be in the controller
    def gen_show_edit_fields(self):
        for sp in self.sparents:
            yield f"+{sp.name}"
        for k in self.fields:
            yield f"-{k}"

    def gen_immutable_fields(self):
        return set()

    def get_field_or_sparent(self,line):
        if line[0] == "+":
            sp_name = line[1:]
            for sp in self.sparents:
                if sp.name == sp_name:
                    return sp
        elif line [0] == "-":
            field_name = line[1:]
            return self.fields[field_name]






    def add_field(self,field_name,field_entity):
        assert field_name not in self.fields
        self.fields[field_name] = field_entity

    def add_parent(self, parent):
        assert self not in parent.children

        if not self.parent:
            self.parent = parent
            #we add parent to children only if he is primary??
            parent.children.append(self)
            return

        assert parent not in parent.sparents
        self.sparents.append(parent)


    def __repr__(self):
        return f"{self.idn=}.{self.name}"

    def __str__(self):
        return f"{self.name}"

    def get_displayed_fields(self):
        return self.fields.keys()

    def dump(self):
        if self.parent is None:
            text = [f"{self.name}\n"]
        else:
            text = [f"{self.name} :{self.parent.name}\n"]
        for sp in self.sparents:
            text.append(f"\t+ {sp.name}\n")
        for field_name in self.fields:
            text.append(f"\t- {field_name}\n")
        s = "".join(text)
        return s

    def dump_debug(self):
        if self.parent is None:
            text = [f"{self.idn=}.{self.name=}\n"]
        else:
            text = [f"{self.name=} :{self.parent.name=}\n"]
        for secondary_parent in self.sparents:
            text.append(f"\t+{secondary_parent.name=}\n")
        for field_name in self.fields:
            text.append(f"\t-{field_name=}\n")
        s = "".join(text)
        return s

class EntityGraph:

    def __init__(self):
        self.entities = []
        self.entities_dict = dict()

    def add_field(self,node,field):
        node.add_field(field.name,field)


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

    def inbox_field_or_parent_line(self,line):
        return line[0] == "-" or line[0] == "+"
    def new_node_or_field_from_str(self,id_dot_name):
        print(" - new_node_or_field_from_str of :" , id_dot_name)
        if self.inbox_field_or_parent_line(id_dot_name):
            return id_dot_name
        return self.inbox_header_line(id_dot_name)

    def new_node_from_str(self,id_dot_name,get_if_exists=False):

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

        assert name not in self.entities_dict, f"EntityGraph.new_node_from_str : entity with name {name} already exists"
        node = Entity(name,idn)
        self.entities.append(node)
        self.entities_dict[name] = node
        return node





    def add_field_or_parent_line(self,node,line):
        if line[0] == "-":
            node.add_field(line[1:],None)
        if line[0] == "+":
            parent_str = line[1:].strip()
            if parent_str:
                parent = self.new_node_from_str(parent_str, True)
                node.add_parent(parent)



    def inbox_header_line(self,line):
        if line[0] == "-" or line[0] == "+":
            raise ValueError(f"inbox_header_line : field instead of a header : {line}")
        item_str_parent_str = line.split(":")
        ln = len(item_str_parent_str)
        if ln == 1:
            item_str = item_str_parent_str[0]
            item_str = item_str.strip()
            item = self.new_node_from_str(item_str, True)
            return item
        if ln == 2:
            item_str, parent_str = item_str_parent_str
            item_str = item_str.strip()
            parent_str = parent_str.strip()
            assert item_str and parent_str
            item = self.new_node_from_str(item_str, True)
            parent_strs =  parent_str.split(",")
            assert parent_strs
            for parent_str in parent_strs:
                parent_str  = parent_str.strip()
                parent = self.new_node_from_str(parent_str, True)
                item.add_parent(parent)
            return item
        raise ValueError(f"inbox_header_line : wrong amount of colon in a header : {line}")



    def fields(self,node):
        return node.fields.values()

    def fields_names(self,node):
        if isinstance(node, str):
            return None
        return node.fields.keys()

    def children(self,node):
        return node.children

    def children_edge(self,node,edge):
        assert edge is None
        return node.children














