def loads_parent_children(lines,
                         inbox_fn = None,
                         splitchr = ":",
                         komma = ",",
                         commentchr = "#",
                         inverse = False,
                         output_root_only = False,
                         child_react = None,
                         values_to_nodes_dict = None):
    if values_to_nodes_dict is None:
        values_to_nodes_dict = dict()


    known_children = set()
    line_counter = 0
    for raw_line in lines:
        line = raw_line.strip()
        if line:
            line = line.split(commentchr)[0]
            if line:
                parent_children_split = line.split(splitchr)
                assert len(parent_children_split) == 2
                parent_value, children = parent_children_split
                parent_value = parent_value.strip()
                assert parent_value
                children_raw = children.strip()
                assert children_raw

                parent = values_to_nodes_dict.get(parent_value,None)
                if parent is  None:
                    if inbox_fn:
                        parent = inbox_fn(parent_value)
                    else:
                        parent = parent_value
                    values_to_nodes_dict[parent_value] = parent


                for child_raw in children_raw.split(komma):
                    child_value = child_raw.strip()
                    if child_value:
                        child = values_to_nodes_dict.get(child_value,None)
                        if child is None:
                            if inbox_fn:
                                child = inbox_fn(child_value)
                            else:
                                child = child_value
                        values_to_nodes_dict[child_value] = child

                        if inverse:
                            known_children.add(parent_value)
                            if child_react:
                                child_react(child,parent)
                            if not output_root_only:
                                yield child, parent
                        else:
                            known_children.add(child_value)
                            if child_react:
                                child_react(parent,child)
                            if not output_root_only:
                                yield parent, child
        line_counter +=1
    if output_root_only:
        print(f"{known_children=}")
        roots = values_to_nodes_dict.keys() - known_children
        #at last , yield only roots:
        for root in roots:
            yield  values_to_nodes_dict[root]



def __line_to_level_line__(line,one_line_comment):
    line = line.split(one_line_comment)[0].rstrip()
    if not line:
        return 0, ""

    line_strip = line.lstrip()
    current_indent = len(line) - len(line_strip)
    return current_indent, line_strip


def loads_indents(lines,
                 inbox_fn,
                 commentchr = "#",
                 alignment = 4,
                 not_allow_misplacing = True,
                 output_root_only = False,
                 child_react = None):
    stack = []
    ctx_indent = -1
    prev_indent = 0
    prev_item = None
    ctx = None

    known_lines = dict()
    for raw_line in lines:
        # Remove comments
        current_level, line = __line_to_level_line__(raw_line, commentchr)
        if not line:
            continue
        assert current_level%alignment == 0, f"loads_indents : wrong indent {current_level} for {alignment=} for line = '{raw_line}'"
        #print(" - !! - current_level, line =" , current_level, line)

        #currently, i assign every same line to the same node.

        item =  known_lines.get(line, None)
        if not item:
            if inbox_fn:
                item = inbox_fn(line)
            else:
                item = line
            known_lines[line] = item
        #print("ctx  ", stack[-1], "level " , current_level)
        # Adjust stack based on indentation level
        if current_level > prev_indent:
            #print(" - !! - append to  stack : ", ctx, prev_indent)
            stack.append((ctx,ctx_indent))
            ctx = prev_item
            ctx_indent = prev_indent
        else:
            while current_level <= ctx_indent:
                #print(" - !! - return from ", ctx, ctx_indent)
                prev_indent = ctx_indent
                ctx,ctx_indent = stack.pop()
                #print(" - !! - returned to ", ctx, ctx_indent)

            if not_allow_misplacing and ctx_indent < current_level < prev_indent:
                assert False, f"misplaced {current_level=}, having  {ctx_indent=}, {prev_indent=}"

        # Current context is the last item in stack or None
        #print(' - !! - stack : ' , stack, ", ctx: " , ctx)
        if ctx is not None:
            if child_react:
                child_react(ctx,item)
            if not output_root_only:
                yield ctx, item
        else:
            if output_root_only:
                yield item
            else:
                yield ctx, item

        # Update previous indentation level
        prev_item  = item
        prev_indent = current_level


def load_one_indent(lines,
                    inbox_fn,
                    commentchr = "#",
                    alignment = 4,
                    output_root_only = False,
                    child_react = None):
    known_lines = dict()
    last_item = None
    for raw_line in lines:
        current_level, line = __line_to_level_line__(raw_line, commentchr)
        if not line:
            continue
        assert current_level == 0 or current_level == alignment and last_item is not None, f"load_one_indent : wrong indent {current_level} for {alignment=} for {raw_line=}"
        item = known_lines.get(line, None)
        if not item:
            if inbox_fn:
                item = inbox_fn(line)
            else:
                item = line
            known_lines[line] = item

        if current_level == 0:
            last_item = item
            if output_root_only:
                yield item
            else:
                yield None, item

        else:
            if child_react:
                child_react(last_item,item)
            if not output_root_only:
                yield last_item, item









