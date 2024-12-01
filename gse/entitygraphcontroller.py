from gse.entitygraph import to_prefix_field_pair_of_entity


class EntityGraphController:

    def __init__(self):
        pass

    def update_all_fields_for_gui(self,entity,updates_items):
        """
        :param entity: entity, what is changed
        :param updates_items:
        :return: updated field names and values of entity what will be displayed,
        in the same amount and order as updates_items
        """
        update_displayed_items=[]
        sparents = []
        fields = dict()
        for prefix_field_name, value in updates_items:
            edge_type, field_name = to_prefix_field_pair_of_entity(prefix_field_name)
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



    def gen_immutable_fields(self,entity):
        if False:
            yield entity.parent

    def gen_field_names_for_gui(self,entity):
        if entity.parent is not None:
            yield f"++{entity.parent}"
        yield from self.gen_secondary_field_names(entity)

    def gen_secondary_field_names(self,entity):
        for sp in entity.sparents:
            yield f"+{sp}"
        for k in entity.fields:
            yield f"-{k}"


    def gen_secondary_field_name_values(self,entity):
        for sp in entity.sparents:
            yield f"+{sp}"
        for k in entity.fields:
            yield f"-{k}:{entity.fields[k]}"


    def gen_field_names_values_for_gui(self,entity):
        ret = []
        ret.append((f"++{entity.parent}", f"{entity.parent}"))
        #ret[f"++{entity.parent}"]= entity.parent
        for sp in entity.sparents:
            ret.append((f"+{sp}", ""))
        for k,v in entity.fields.items():
            ret.append((f"-{k}",  f"{v}"))
        return ret

    def replace_field_by_old_value_deprecated(self,entity,prefix_field_name, value,old_value):
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


    def replace_field_name_value_by_old_name_value_deprecated(self,entity,new_prefix_field_name,old_prefix_field_name, value,old_value):
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


    def add_field_or_parent_deprecated(self,entity,prefix_field_name, value):
        print(f"add_field_or_parent_for_gui : {prefix_field_name=} , {value=}")
        edge_type, field_name = to_prefix_field_pair_of_entity(prefix_field_name)
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


    def check_new_field_name_for_add_for_gui_deprecated(self,entity,prefix_field_name):
        try:
            prefix, field_name = to_prefix_field_pair_of_entity(prefix_field_name)
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

    def check_new_field_name_for_replace_for_gui_deprecated(self,entity,prefix_field_name):
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

    def add_field_for_gui_deprecated(self,node,field_name,field_value):
        if not field_name or field_name in node.fields:
            return None
        node.fields[field_name] = field_value
        return "-"+field_name


    def remove_field_or_parent_for_model(self,entity,prefixed_field_name):
        edge_type, field_name = to_prefix_field_pair_of_entity(prefixed_field_name)
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


    def remove_field_for_gui(self,node,gui_field_name):
        print(f"remove_field_for_gui : {gui_field_name=} , {node=}")
        prefix, field_name =  to_prefix_field_pair_of_entity(gui_field_name)
        if prefix == "++":
            node.parent = None
            return
        if prefix == "+":
            node.sparents.remove[field_name]
            return
        if prefix == "-":
            del node.fields[field_name]
            return




    def get_prefixed_field_value(self,entity,gui_field_name):
        prefix, field_name  = to_prefix_field_pair_of_entity(gui_field_name)
        if prefix == "++":
            return entity.parent

        if prefix == "+":
            for sp in entity.sparents:
                if field_name == sp:
                    return sp
        elif prefix == "-":
            return entity.fields[field_name]


    def header_for_text(self,entity):
        if entity.parent is None:
            return f"{entity.name}"
        else:
            return f"{entity.name} :{entity.parent}"

    def dump_field_names(self,entity):
        header =[self.header_for_text(entity)]
        fields = "\n".join(self.gen_secondary_field_names(entity))
        return header + fields


    def dump_field_name_values(self, entity):
        header = self.header_for_text(entity)
        fields = "\n\t".join(self.gen_secondary_field_name_values(entity))
        return header + "\n\t" + fields


    def dump_debug(self, entity):
        if entity.parent is None:
            text = [f"{entity.idn=}.{entity.name=}\n"]
        else:
            text = [f"{entity.name=} :{entity.parent.name=}\n"]
        for secondary_parent in entity.sparents:
            text.append(f"\t+{secondary_parent.name=}\n")
        for field_name in entity.fields:
            text.append(f"\t-{field_name=}\n")
        s = "".join(text)
        return s

    def add_new_field_for_gui(self,entity):
        new_field_name = f"NewField{len(entity.fields)}"
        new_field_value ="NewValue"
        n = len(entity.fields)
        while new_field_name in entity.fields:
            n+=1
            new_field_name = f"NewField{n}"

        entity.fields[new_field_name] = new_field_value
        prefix_field_name = "-" + new_field_name
        return prefix_field_name


    def validate_all(self,master):
        field_frames = master.field_frames
        dejavu = set()
        was_root = False
        for n,x in enumerate(field_frames):
            field_name = x.name_var.get().strip()
            if not field_name:
                return False , n, field_name
            if field_name in dejavu:
                return False , n, field_name
            dejavu.add(field_name)
            if field_name[0] != "-" and field_name[0] != "+":
                return False, n, field_name + "field_name[0] is neither - nor +"
            else:
                if len(field_name) == 1:
                    return False, n, field_name + "len(field_name) == 1"

            if field_name.startswith("++"):
                if was_root or len(field_name) == 2:
                    return False, n, field_name
                was_root = True
        return True, -1, None