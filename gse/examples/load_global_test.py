from pathlib import Path

from gse.gio import load
from gse.dump import dumps


print("-- Load into DictGraph with inboxing of values ")
file = open(Path(__file__).parent / "load_me.txt", "r")

graph, roots = load(file)
file.close()
#print(type(roots[0]))
for root in roots:
    print('--- root ---')
    print(dumps(graph,root))


print("-- Load into DictGrapg without inboxing of values")
file = open(Path(__file__).parent / "load_me.txt", "r")

graph, roots = load(file,"dict-")
file.close()
#print(type(roots[0]))
for root in roots:
    print('--- root ---')
    print(dumps(graph,root))


print("-- Load into ObjGraph")
file = open(Path(__file__).parent / "load_me.txt", "r")
graph, roots = load(file,"obj")
file.close()
#print(type(roots[0]))
for root in roots:
    print('--- root ---')
    print(dumps(graph,root))