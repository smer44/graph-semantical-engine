from pathlib import Path

from gse import load,dumps

file = open(Path(__file__).parent / "load_me.txt", "r")

graph, roots = load(file)
file.close()

for root in roots:
    print('--- root ---')
    print(dumps(graph,root))


