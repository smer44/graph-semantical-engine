class ObjNode:
    ident_symbol = '\t'
    ids = 0
    def __init__(self, value):
        self.value = value
        self.children = []
        self.id = ObjNode.ids
        ObjNode.ids += 1
        self.deepsize = 0
        #not used now:
        #self.visiting = False

    def __repr__(self):
        if self.children:
            return f"<{self.value}: {', '.join(x.value for x in self.children)}>"
        else:
            return f"<{self.value}>"
        #return f"<{self.value}#{self.id}:  {self.children}>"

    def dumps(self, indent="",ident_symbol = "\t"):
        stack = [(self, indent)]
        output_lines = []
        dejavu = set()
        while stack:
            node, indent = stack.pop()
            if node in dejavu:
                continue
            dejavu.add(node)
            line = f'{indent}{node.value}#{node.deepsize}\n'
            output_lines.append(line)
            children = list(node.children)
            children.reverse()
            if children:
                new_indent = f'{ident_symbol}{indent}'
                for child in children:
                    stack.append((child,new_indent))
        return "".join(output_lines)

    def add_child(self,child):
        self.children.append(child)


class ObjGraph:

    def __init__(self):
        self.nodes = []

    def new_node(self,value):
        node = ObjNode(value)
        self.nodes.append(node)
        return node

    def get_value(self,node):
        return node.value

    def add_child(self,parent,child):
        parent.add_child(child)

    def reset_deepsize(self):
        for node in self.nodes:
            node.deepsize = 0

    def deepsize(self, node):
        return node.deepsize

    def set_deepsize(self,node,value):
        node.deepsize = value

    def children(self,node):
        return node.children
