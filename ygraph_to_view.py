import yaml

class GraphNode:
    def __init__(self, value, children=None):
        self.value = value
        self.children = children if children is not None else []


node4 = GraphNode('Node 4')
node5 = GraphNode('Node 5')
node6 = GraphNode('Node 6')
node7 = GraphNode('Node 7')

node2 = GraphNode('Node 2', [node4, node5])
node3 = GraphNode('Node 3', [node6, node5])

root = GraphNode('Root', [node2, node3])


yaml_string = yaml.dump(root, sort_keys=False)


print(yaml_string)


