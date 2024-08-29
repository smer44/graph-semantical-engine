def dumps(graph, root, indent="", ident_symbol="\t"):
    stack = [(root, indent)]
    output_lines = []
    dejavu = set()
    while stack:
        node, indent = stack.pop()
        if node in dejavu:
            continue
        dejavu.add(node)
        line = f'{indent}{graph.get_value(node)}#{graph.deepsize(node)}\n'
        output_lines.append(line)
        children = graph.children(node)
        if children:
            children.reverse()
            new_indent = f'{ident_symbol}{indent}'
            for child in children:
                stack.append((child, new_indent))
    return "".join(output_lines)