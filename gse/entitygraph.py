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



    #this must be in the controller



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

    def add_or_replace_field(self,node,field,value):
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



    def add_field(self,node,field_name,field_value):
        assert field_name not in node.fields
        node.fields[field_name] = field_value

    def add_field_for_gui(self,node,field_name,field_value):
        if not field_name or field_name in node.fields:
            return None
        node.fields[field_name] = field_value
        return "-"+field_name

    def remove_field_for_gui(self,node,gui_field_name):
        prefix, field_name =  self.to_edge_type_field_name_pair(gui_field_name)
        if prefix == "++":
            node.parent = None
            return
        if prefix == "+":
            node.sparents.remove[field_name]
            return
        if prefix == "-":
            del node.fields[field_name]
            return



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

        assert name not in self.entities_dict, f"EntityGraph.new_node_from_str : entity with name {name} already exists"
        node = Entity(name,idn)
        self.entities.append(node)
        self.entities_dict[name] = node
        return node



    def inbox_header_line_wrong(self,line):
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


    def get_field_or_parent(self,entity,gui_field_name):
        prefix, field_name  = self.to_edge_type_field_name_pair(gui_field_name)
        if prefix == "++":
            return entity.parent

        if prefix == "+":
            for sp in entity.sparents:
                if field_name == sp:
                    return sp
        elif prefix == "-":
            return entity.fields[field_name]



    def gen_immutable_fields(self,entity):
        pass

    def gen_all_field_names_for_gui(self,entity):
        if entity.parent is not None:
            yield f"++{entity.parent}"
        for sp in entity.sparents:
            yield f"+{sp}"
        for k in entity.fields:
            yield f"-{k}"

    def gen_all_prefixed_fields_and_values_for_gui(self,entity):
        yield  "++", entity.parent, entity.parent
        for sp in entity.sparents:
            yield  "+", f"{sp}" , f"{sp}"
        for k,v in self.fields.items():
            yield "-" , f"{k}" , f"{v}"

    def gen_all_fields_and_values_for_gui(self,entity):
        ret = dict()
        ret[f"++{entity.parent}"]= entity.parent
        for sp in entity.sparents:
            ret[f"+{sp}"] = f"{sp}"
        for k,v in entity.fields.items():
            ret[f"-{k}"]  = f"{v}"
        return ret

    def add_field_or_parent(self,entity,prefix_field_name, value):
        print(f"add_field_or_parent : {prefix_field_name=} , {value=}")
        edge_type, field_name = self.to_edge_type_field_name_pair(prefix_field_name)
        if edge_type == "++":
            #assert field_name == value, f"add_field_or_parent: {field_name=} is unequal to {value=}"
            assert entity.parent == None
            entity.parent = value
        elif edge_type == "+":
            #assert field_name == value , f"add_field_or_parent: {field_name=} != {value=}"
            assert value not in entity.sparents
            entity.sparents.append(value)
        elif edge_type == "-":
            assert field_name not in entity.fields
            entity.fields[field_name] = value


    def replace_field_by_old_value_for_gui(self,entity,prefix_field_name, value,old_value):
        print(f"replace_field_by_old_value_for_gui : {prefix_field_name=}, {value=}, {old_value=}")
        edge_type, field_name = self.to_edge_type_field_name_pair(prefix_field_name)
        if edge_type == "++":
            assert entity.parent ==old_value
            entity.parent = value
            return f"++{value}", value
        elif edge_type == "+":
            assert field_name == old_value, f"replace_field_by_old_value_for_gui: {field_name=} unequal to {old_value=}"
            sps = entity.sparents
            for n in  range(len(sps)):
                if sps[n] == old_value:
                    sps[n] = value
                    return f"+{value}", value
        elif edge_type == "-":
            assert entity.fields[field_name] == old_value
            entity.fields[field_name] = value
            return f"-{field_name}", value
        raise ValueError(f"replace_field_by_old_value_for_gui: wrong {prefix_field_name,value,old_value=}")


    def replace_field_name_value_by_old_name_value(self,entity,new_prefix_field_name,old_prefix_field_name, value,old_value):
        print(f"replace_field_name_value_by_old_name_value : {new_prefix_field_name=},{old_prefix_field_name=}, {value=}, {old_value=}")
        old_edge_type, old_field_name = self.to_edge_type_field_name_pair(old_prefix_field_name)
        new_edge_type, new_field_name = self.to_edge_type_field_name_pair(new_prefix_field_name)
        #replace similar edge type or delete other edge type:
        if old_edge_type == "++":
            if new_edge_type == "++":
                #assert entity.parent == old_value
                #assert entity.parent == old_field_name
                entity.parent = new_field_name
                return new_prefix_field_name, new_field_name
            entity.parent =None
        elif old_edge_type == "+":
            sps = entity.sparents
            if new_edge_type == "+":
                for n in  range(len(sps)):
                    if sps[n] == old_value:
                        sps[n] = new_field_name
                        return new_prefix_field_name, new_field_name
            for n in  range(len(sps)):
                if sps[n] == old_value:
                    del sps[n]
        elif old_edge_type == "-":
            assert entity.fields[old_field_name] == old_value
            del entity.fields[old_field_name]
        else:
            raise  ValueError(f"replace_field_or_parent_by_old_value: wrong {old_edge_type=}")
            entity.fields[new_field_name] = value
            return new_prefix_field_name, value
        #try to add other edge type:
        return self.add_field_or_parent_for_gui(entity, new_prefix_field_name,value)
        #return new_prefix_field_name, value

    def add_field_or_parent_for_gui(self,entity,prefix_field_name, value):
        print(f"add_field_or_parent_for_gui : {prefix_field_name=} , {value=}")
        edge_type, field_name = self.to_edge_type_field_name_pair(prefix_field_name)
        if edge_type == "++":
            #assert field_name == value, f"add_field_or_parent: {field_name=} is unequal to {value=}"
            assert entity.parent == None
            entity.parent = field_name
            return prefix_field_name, field_name
        elif edge_type == "+":
            #assert field_name == value , f"add_field_or_parent: {field_name=} != {value=}"
            assert field_name not in entity.sparents
            entity.sparents.append(field_name)
            return prefix_field_name, field_name

        elif edge_type == "-":
            assert field_name not in entity.fields
            entity.fields[field_name] = value
            return prefix_field_name, value

    #TODO - move these methods to controller
    def update_all_fields_for_gui(self,entity,updates_items):
        update_displayed_items=[]
        sparents = []
        fields = dict()
        for prefix_field_name, value in updates_items:
            edge_type, field_name = self.to_edge_type_field_name_pair(prefix_field_name)
            if edge_type == "++":
                entity.parent = field_name
                field_name_gui = prefix_field_name
                field_value_gui = field_name
            elif edge_type == "+":
                sparents.append(field_name)
                field_name_gui = prefix_field_name
                field_value_gui = field_name
            elif edge_type == "-":
                fields[field_name] = value
                field_name_gui = prefix_field_name
                field_value_gui = value
            update_displayed_items.append((field_name_gui, field_value_gui))
        entity.sparents = sparents
        entity.fields = fields
        return update_displayed_items








    def to_edge_type_field_name_pair(self,prefix_field_name):
        if prefix_field_name[0] == "+":
            if len(prefix_field_name) >1 and prefix_field_name[1] == "+":
                return "++", prefix_field_name[2:]
            return "+", prefix_field_name[1:]
        elif prefix_field_name[0] == "-":
            return "-", prefix_field_name[1:]
        else:
            raise ValueError(f"to_edge_type_field_name_pair: wrong {prefix_field_name=}")

    def check_new_field_name_for_add_for_gui(self,entity,prefix_field_name):
        try:
            prefix, field_name = self.to_edge_type_field_name_pair(prefix_field_name)
            if not field_name:
                return False
            if prefix == "++":
                return entity.parent is None
            if prefix == "+":
                return not field_name in entity.sparents
            if prefix == "-":
                return not field_name in entity.fields
        except ValueError:
            return False


    def check_new_field_name_for_replace_for_gui(self,entity,prefix_field_name):
        try:
            prefix, field_name = self.to_edge_type_field_name_pair(prefix_field_name)
            if not field_name:
                return False
            if prefix == "++":
                return True#entity.parent is None
            if prefix == "+":
                return not field_name in entity.sparents
            if prefix == "-":
                return not field_name in entity.fields
        except ValueError:
            return False

    def remove_field_or_parent(self,entity,field_name):
        edge_type, field_name = self.to_edge_type_field_name_pair(field_name)
        if edge_type == "++":
            assert entity.parent == None
            entity.parent = None
            return
        elif edge_type == "+":
            entity.sparents.remove(field_name)
        elif edge_type == "-":
            del entity.fields[field_name]
        else:
            raise ValueError(f"remove_field_or_parent : wrong {edge_type=}")

        old_parent = self.entities[field_name]
        old_parent.children.remove[entity]


    def fields_names(self,node):
        if isinstance(node, str):
            return None
        return node.fields.keys()


    def children(self,node,edge):
        if edge is None:
            return node.children
        elif edge == "+":
            return node.sparents
        elif edge == "-":
            return node.fields.values()

    def children_edge(self,node,edge):
        assert edge is None
        return node.children

#d = dict((("a",3) ,("b",4) ))
#print(d)













