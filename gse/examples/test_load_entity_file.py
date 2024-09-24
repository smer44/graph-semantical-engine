file = "test_en.txt"
from gse.gio import load,load_lines, load_entities_with_fields
from gse.dump import dumps

with open(file, 'r', encoding='utf-8') as file_graph:
    lines = file_graph.readlines()
    og, roots = load_entities_with_fields(lines,False)
    if not roots:
        print("empty loaded")
    for root in roots:
        print(dumps(og,root))

