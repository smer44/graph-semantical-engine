class DummyNode:

    def __init__(self, value):
        self.value = value
        self.children = []

    def __str__(self):
        return f"<D {self.value} D>"

    def __repr__(self):
        return f"<D {self.value} D>"


def child_react_dummy_node(parent,child):
    #print(f"append to {parent=}.{parent.children} :   {child=}")
    parent.children.append(child)

def convert_fn_dummy_node(value):
    return DummyNode(value)

def children_dummy_node(node):
    return node.children


class DummyGraph:

    def __init__(self):
        self.nodes = dict()

    def inbox_fn(self,node_name):
        if node_name in self.nodes:
            return self.nodes[node_name]
        else:
            node = DummyNode(node_name)
            self.nodes[node_name] = node
            return node
