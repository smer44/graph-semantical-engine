
class Gol:
    """
    Performs conversions of a graph data
    from strings to objects and backwards
    different formats possible.


    """

    def __init__(
            self,
            graph,
            #convert_fn=None,
            #child_react=None,
            output_root_only=False,
            one_line_comment="#",
            alignment=4,
    ):

        self.graph = graph
        self.output_root_only = output_root_only
        self.one_line_comment = one_line_comment
        self.verbose = False
        self.alignment = alignment

        self.not_allow_misplacing = True

        self.get_children_fn = lambda item: item.children
        self.get_value_fn = lambda item: item.value
        self.convert_fn = lambda graph, value: graph.new_node(value)
        self.child_react = lambda graph,parent,child:graph.add_child(parent,child)

    def dump_gen(self,item,indent,ident_symbol = "\t"):
        stack = [(item,indent)]
        while stack:
            item,indent = stack. pop()
            line = f'{indent}{self.get_value_fn(item)}\n'
            yield line
            children = list(self.get_children_fn(item))
            children.reverse()
            if children:
                new_indent = f'{ident_symbol}{indent}'
                for child in children:
                    stack.append((child,new_indent))

    def dumps(self,item):
        return "".join(self.dump_gen(item, "", "\t"))

    def dump(self,item,file):
        for line in self.dump_gen(item, "", "\t"):
            file.write(line)



    def child_react_set_child(self,parent, child):
        #print("append " , parent, child)
        parent.children.append(child)

    def pp(self,*text):
        if self.verbose:
            print(*text)

    def __line_to_level_line__(self, line):
        one_line_comment = self.one_line_comment

        line = line.split(one_line_comment)[0].rstrip()
        if not line:
            return 0, ""

        line_strip = line.lstrip()
        current_indent = len(line) - len(line_strip)
        return current_indent, line_strip


    def loads(self,text):
        return [item for ctx,item in self.load_gen(text.splitlines())]

    def load(self, file):
        return [item for ctx,item in self.load_gen(file.readlines())]



    def load_gen(self,lines):
        stack = []
        ctx_indent = -1
        prev_indent = 0
        prev_item = None
        convert_fn = self.convert_fn
        ctx = None
        pp = self.pp
        alignment = self.alignment
        child_react = self.child_react
        output_root_only = self.output_root_only
        graph = self.graph
        for raw_line in lines:
            # Remove comments
            current_level, line = self.__line_to_level_line__(raw_line)
            assert current_level%alignment == 0, f"yLinesToObjectsByIndents.__iter__ : wrong indent {current_level} for {alignment=} for line = '{raw_line}'"
            pp(" - !! - current_level, line =" , current_level, line)
            if not line:
                continue
            if convert_fn:
                item = convert_fn(graph,line)
            else:
                item = line
            #print("ctx  ", stack[-1], "level " , current_level)
            # Adjust stack based on indentation level
            if current_level > prev_indent:
                pp(" - !! - append to  stack : ", ctx, prev_indent)
                stack.append((ctx,ctx_indent))
                ctx = prev_item
                ctx_indent = prev_indent
            else:
                while current_level <= ctx_indent:
                    pp(" - !! - return from ", ctx, ctx_indent)
                    prev_indent = ctx_indent
                    ctx,ctx_indent = stack.pop()
                    pp(" - !! - returned to ", ctx, ctx_indent)

                if self.not_allow_misplacing and ctx_indent < current_level < prev_indent:
                    assert False, f"misplaced {current_level=}, having  {ctx_indent=}, {prev_indent=}"

            # Current context is the last item in stack or None
            pp(' - !! - stack : ' , stack, ", ctx: " , ctx)
            if ctx is not None:
                if child_react:
                    child_react(graph,ctx,item)
                if not output_root_only:
                    yield ctx, item
            else:
                if output_root_only:
                    yield ctx, item

            # Update previous indentation level
            prev_item  = item
            prev_indent = current_level
