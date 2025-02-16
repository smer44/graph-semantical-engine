from gse.dictgraph import DictGraph

gr = DictGraph()

gr.new_node("Pants")

gr.new_node("Chair")

gr.new_node("Room")

gr.new_node("Table")

gr.new_node("T-Shirt")

gr.add_child_by_value("Room", "Chair", "in")
gr.add_child_by_value("Room", "Table", "in")
gr.add_child_by_value("Chair", "T-Shirt", "on")
gr.add_child_by_value("Chair", "Pants", "on")

print(gr.children_by_value_and_edge("Room", "in"))

print(gr.ids)
print(f"room children")
for item in gr.children_by_value_and_edge("Room", "in"):
    print(gr.get_value(item))

print(f"chair children")
for item in gr.children_by_value_and_edge("Chair", "on"):
    print(gr.get_value(item))

gr.replace_value("Chair", "Bed")

print(gr.ids)
for item in gr.children_by_value_and_edge("Room", "in"):
    print(gr.get_value(item))

print(f"Bed children")
for item in gr.children_by_value_and_edge("Bed", "on"):
    print(gr.get_value(item))
