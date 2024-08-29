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


class gUtil:

    def __init__(self):
        self.deepsize = lambda graph, node: node.deepsize
        self.children_fn = lambda graph, node : node.children
        self.set_deepsize = self.set_deepsize_ObjGraph
        # not used now:
        #self.mark_visiting = self.mark_visiting_ObjGraph
        #self.is_visiting = self.is_visiting_ObjGraph

    def set_deepsize_ObjGraph(self,graph, node, value):
        node.deepsize = value

    #def mark_visiting_ObjGraph(self,graph, node, value):
    #    node.visiting = value

    #def is_visiting_ObjGraph(self,graph, node):
    #    return node.visiting

    def calc_deepsize(self,graph,roots):
        """
        Calculates relative deep size of a graph.
        Designed to work "most" correctly in acyclic graph,
        but also produce some more or less reasonable "deep size"
        for cyclic graph, assuming if nodes are visited
        again, they have size of 1.
        :param graph: graph object
        :param roots: roots, from what we calculate deepsize
        :return:None. the method marks node objects in the graph to have some size.
        """

        stack = list(roots)
        deepsize = self.deepsize
        children_fn = self.children_fn
        set_deepsize = self.set_deepsize
        #mark_visiting = self.mark_visiting
        #is_visiting = self.is_visiting

        while stack:
            node = stack.pop()
            #if is_visiting(graph,node):
                #set_deepsize(graph, node, 1)
                #continue
            dsize = deepsize(graph,node)
            if dsize == 0:
                children_list = children_fn(graph,node)
                if children_list:
                    #mark_visiting(graph,node,False)
                    set_deepsize(graph,node,1)
                    stack.append(node)
                    for child in children_list:
                        if deepsize(graph,child) == 0:
                            stack.append(child)

                    #stack.extend(children_list)
                else:
                    set_deepsize(graph, node, 1)
            else:
                children_list = children_fn(graph, node)

                assert deepsize(graph,node) == 1, f"gUtil.calc_deepsize: wrong case: {node=} visited again was not marked as 1"
                assert children_list, "gUtil.calc_deepsize: wrong case: node was marked as 1 while having no children"
                s = 0
                for child in children_list:
                    s+= deepsize(graph,child)
                set_deepsize(graph, node, s)










