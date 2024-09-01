def dumps_parent_children(  root,
                            children_fn,
                            shallow_str = str,
                            splitchr=":",
                            komma=",",
                            ):

    stack = [root]
    dejavu = set()
    if komma[-1]!= " ":
        komma +=" "
    while stack:
        node = stack.pop()
        if node in dejavu:
            continue
        node_str=shallow_str(node)
        dejavu.add(node)
        children = children_fn(node)
        if children:
            children_str = komma.join(shallow_str(child) for child in children)
            line = f'{node_str}{splitchr} {children_str}\n'
            yield line
        children.reverse()
        stack.extend(children)






def dumps_indents(root,
          children_fn,
          shallow_str = str,
          indent="",
          ident_symbol="\t"):
    stack = [(root, indent)]
    dejavu = set()
    while stack:
        node, indent = stack.pop()

        line = f'{indent}{shallow_str(node)}\n'
        yield line
        #output_lines.append(line)
        if node in dejavu:
            continue
        dejavu.add(node)

        children = children_fn(node)
        if children:
            children.reverse()
            new_indent = f'{ident_symbol}{indent}'
            for child in children:
                stack.append((child, new_indent))
    #return "".join(output_lines)







