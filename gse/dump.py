from gse.entitygraph import Entity, EntityGraph


def outbox_value_str (node):
    return str(node.value)

def dumpsi(graph,entity):
    children_fn = lambda entity : graph.fields_values_if_entity_else_none(entity)
    return "".join(dumps_indents(entity,children_fn))

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
            children = list(children)
            children.reverse()
            new_indent = f'{ident_symbol}{indent}'
            for child in children:
                stack.append((child, new_indent))
    #return "".join(output_lines)



def dumps(graph,obj):
    lines = []
    __dumps_indents_decide__(graph,obj,"","\t", "",  lines, 1,1)
    return "\n".join(lines)

def __dumps_indents_decide__(graph,obj,indent,addprefix,first_indent,lines,deep_sparents,deep_fields):
    if isinstance(obj,Entity):
        assert isinstance(graph,EntityGraph), f"__dumps_indents_decide__: obj is Entity, but graph is not EntityGraph"
        __dump_indents_entity__(graph,obj,indent,addprefix,first_indent, lines,deep_sparents,deep_fields)
        return
    elif isinstance(obj,(tuple,list,set)):
        if isinstance(graph,EntityGraph):
            tuple_header = f"{first_indent}{type(obj).__name__}"
            lines.append(tuple_header)
            tuple_item_header = f"{indent}{addprefix}.."
            next_indent = indent + addprefix
            #deep_sparents-=1
            #deep_fields-=1
            for child_obj in obj:
                __dumps_indents_decide__(graph, child_obj, next_indent, addprefix, tuple_item_header, lines, deep_sparents, deep_fields)
            return
    line = f"{first_indent}{obj}"
    lines.append(line)









def __dump_indents_entity__(graph,entity,indent,addprefix,first_indent,lines,deep_sparents,deep_fields):
    if entity.parent is None:
        header = f"{first_indent}{entity.name}"
    else:
        header = f"{first_indent}{entity.name} :{entity.parent}"
    lines.append(header)
    next_indent = indent + addprefix
    sparent_first_indent = next_indent + "+"
    next_deep_sparents = deep_sparents - 1
    next_deep_fields = deep_fields-1
    if deep_sparents > 0:

        for sp in entity.sparents:
            next_obj = graph.entities_dict.get(sp,sp)
            __dumps_indents_decide__(graph, next_obj,next_indent, addprefix, sparent_first_indent,lines,next_deep_sparents,deep_fields)
    else:
        for sp in entity.sparents:
            lines.append(f"{sparent_first_indent}{sp}")


    if deep_fields > 0:

        for k, v in entity.fields.items():
            field_first_indent = f"{next_indent}-{k} : "
            if v is not None:
                #lines.append( f"{prefix}-{k}: {v}")
                #if not isinstance(v,list):
                #    next_obj = graph.entities_dict.get(v, v)
                #else
                __dumps_indents_decide__(graph, v, next_indent, addprefix, field_first_indent, lines, next_deep_sparents, next_deep_fields)
            else:
                lines.append(field_first_indent)
    else:
        for k, v in entity.fields.items():
            if v is not None:
                lines.append(f"{next_indent}-{k}: {v}")
            else:
                lines.append(f"{next_indent}-{k}")

    #return  "\n\t".join(lines) + "\n"





