def loads_parent_children(lines,
                         inbox_fn = None,
                         splitchr = ":",
                         komma = ",",
                         commentchr = "#",
                         inverse = False,
                         output_root_only = False,
                         child_react = None):
    known_values = dict()
    known_children = set()
    line_counter = 0
    for raw_line in lines:
        line = raw_line.strip()
        if line:
            line = line.split(commentchr)[0]
            if line:
                parent_children_split = line.split(splitchr)
                assert len(parent_children_split) == 2
                parent, children = parent_children_split
                parent = parent.strip()
                assert parent
                children_raw = children.strip()
                assert children_raw
                known_parent = known_values.get(parent,None)
                if known_parent:
                    parent = known_parent
                else:
                    if inbox_fn:
                        value = inbox_fn(parent)
                    else:
                        value = parent
                    known_values[parent] = value
                    #roots[parent] = value
                    parent = value
                    #print(roots)

                for child_raw in children_raw.split(komma):
                    child = child_raw.strip()
                    if child:
                        known_child = known_values.get(child, None)
                        if known_child:
                            child = known_child
                        else:
                            known_children.add(child)
                            if inbox_fn:
                                child = inbox_fn(child)
                        if not output_root_only:
                            if inverse:
                                if child_react:
                                    child_react(child,parent)
                                yield child, parent
                            else:
                                if child_react:
                                    child_react(parent,child)
                                yield parent, child
        line_counter +=1
    if output_root_only:
        print(f"{known_children=}")
        roots = known_values.keys() - known_children
        #at last , yield only roots:
        for root in roots:
            yield None, known_values[root]



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
        assert current_level%alignment == 0, f"yLinesToObjectsByIndents.__iter__ : wrong indent {current_level} for {alignment=} for line = '{raw_line}'"
        #print(" - !! - current_level, line =" , current_level, line)
        if not line:
            continue
        #currently, i assign every same line to the same node.
        #TODO - rename item to node
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
                yield ctx, item

        # Update previous indentation level
        prev_item  = item
        prev_indent = current_level

