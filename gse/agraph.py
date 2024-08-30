def dumps(graph, root, indent="", ident_symbol="\t"):
    stack = [(root, indent)]
    output_lines = []
    dejavu = set()
    while stack:
        node, indent = stack.pop()

        line = f'{indent}{graph.shallow_str(node)}\n'
        output_lines.append(line)
        if node in dejavu:
            continue
        dejavu.add(node)

        children = graph.children(node)
        if children:
            children.reverse()
            new_indent = f'{ident_symbol}{indent}'
            for child in children:
                stack.append((child, new_indent))
    return "".join(output_lines)


class InboxValue:

    def __init__(self, value):
        self.value = value

    def set(self,value):
        self.value = value

    def __hash__(self):
        return hash(self.value)

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return repr(self.value)
