#from gse.entitygraph import EntityGraph


#print(str(EntityGraph))
#stores as class name, entries in form of <class 'gse.entitygraph.EntityGraph'>


class EntityDisplayOptions:

    #def __init__(self,class_name):
    #    self.class_name = class_name

    def get_field(self,entity,line):
        if line[0] == "+":
            sp_name = line[1:]
            for sp in entity.sparents:
                if sp.name == sp_name:
                    return sp
        elif line [0] == "-":
            field_name = line[1:]
            return entity.fields[field_name]

    def get_immutable_fields(self):
        return set()



