from gse.entitygraph import EntityGraph


eg = EntityGraph()

superman = eg.new_node_or_field_from_str("superman")
eg.add_or_set_field(superman,"instance", True)

print(superman.dump_debug())

name_variants = eg.new_node_or_field_from_str("name_variants")
eg.add_or_set_field(name_variants,"instance", True)



eg.add_or_set_field(superman,"name",name_variants)
