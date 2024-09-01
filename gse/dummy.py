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