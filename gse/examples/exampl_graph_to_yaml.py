import yaml

class DummyNode:
    def __init__(self, value, children=None):
        self.value = value
        self.children = children if children is not None else []


node4 = DummyNode('Node 4')
node5 = DummyNode('Node 5')
node6 = DummyNode('Node 6')
node7 = DummyNode('Node 7')

node2 = DummyNode('Node 2', [node4, node5])
node3 = DummyNode('Node 3', [node6, node5])

root = DummyNode('Root', [node2, node3])


yaml_string = yaml.dump(root, sort_keys=False)


print(yaml_string)


