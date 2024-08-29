




class gUtil:
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
        deepsize = graph.deepsize
        children_fn = graph.children
        set_deepsize = graph.set_deepsize
        #mark_visiting = self.mark_visiting
        #is_visiting = self.is_visiting

        while stack:
            node = stack.pop()
            #if is_visiting(graph,node):
                #set_deepsize(graph, node, 1)
                #continue
            dsize = deepsize(node)
            if dsize == 0:
                children_list = children_fn(node)
                if children_list:
                    #mark_visiting(graph,node,False)
                    set_deepsize(node,1)
                    stack.append(node)
                    for child in children_list:
                        if deepsize(child) == 0:
                            stack.append(child)

                    #stack.extend(children_list)
                else:
                    set_deepsize(node, 1)
            else:
                children_list = children_fn(node)

                assert deepsize(node) == 1, f"gUtil.calc_deepsize: wrong case: {node=} visited again was not marked as 1"
                assert children_list, "gUtil.calc_deepsize: wrong case: node was marked as 1 while having no children"
                s = 0
                for child in children_list:
                    s+= deepsize(child)
                set_deepsize(node, s)










