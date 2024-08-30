


class ViewNode:

    def __init__(self,node,depth = 0):
        self.value = node
        self.deepsize = 0
        self.depth = depth
        self.top = 0
        self.left = 0
        self.bottom = 0
        self.right = 0
        self.view_children = []
        self.view_parents = []
        self.roots_sum = 0
        #self.rect = None
        self.rect_id = None
        self.text_id = None
        self.children = dict()  # List to store pairs (rect_id, arrow_id) of children by given arrows
        self.parents = dict() # List to store pairs (rect_id, arrow_id) of parents by given arrows

    def set_coords(self,left, bottom, right, top):
        self.left = left
        self.bottom = bottom
        self.right = right
        self.top = top

    def __repr__(self):
        return f"<!{self.value}!>"






class ViewGraph:

    def __init__(self):
        self.nodes = []
        #self.roots = []

    def new_node(self,value,depth = 0):
        node = ViewNode(value,depth)
        self.nodes.append(node)
        return node

    def get_value(self,node):
        return node

    def add_child(self, parent,child):
        parent.view_children.append(child)
        child.view_parents.append(parent)

    def children(self,viewnode):
        return viewnode.view_children

    def parents(self,viewnode):
        return viewnode.view_parents

    def reset_deepsize(self):
        for node in self.nodes:
            node.deepsize = 0

    def deepsize(self,node):
        return node.deepsize

    def set_deepsize(self,node,value):
        node.deepsize = value

    #def add_children_filter_edge(self,graph,viewnode,edge):
    #    filtered_children = graph.children_edge(viewnode.node,edge)
    #    for fchild in filtered_children:
    #        viewchild= self.new_node(fchild)
    #        self.add_child(viewnode, viewchild)

    def shallow_str(self, node):
        if node.right > 0 :
            return f"{node.value}#{node.left=},{node.bottom=},{node.right=},{node.top=}"
        else:
            return f"{node.value}#{node.deepsize},{node.depth}"



#TODO - replace maxdepth with self.depth ?
    def view_filter(self,graph, roots,edge, maxdepth):
        self.roots = [self.new_node(root) for root in roots]
        stack = [root for root in self.roots]
        dejavu = dict()
        while stack:
            viewnode = stack.pop()
            dejavu[viewnode.value] = viewnode
            if viewnode.deepsize == 0:
                viewnode.deepsize = 1
                next_depth = viewnode.depth + 1
                if next_depth <= maxdepth:
                    filtered_children = graph.children_edge(viewnode.value, edge)
                    if filtered_children:
                        stack.append(viewnode)
                        for fchild in filtered_children:
                            viewchild = dejavu.get(fchild,None)
                            if viewchild is None:
                                viewchild = self.new_node(fchild,next_depth)
                                self.add_child(viewnode,viewchild)
                                stack.append(viewchild)
                                print("created child for node ", viewnode, viewchild, "stack : ", stack)
                            else:
                                self.add_child(viewnode, viewchild)
                                print("appended child for node ", viewnode, viewchild, "stack : ", stack)


            else:
                    assert viewnode.deepsize == 1
                    view_children = self.children(viewnode)
                    assert view_children
                    s = 0
                    for viewchild in view_children:
                        assert viewchild.deepsize > 0
                        s+= viewchild.deepsize
                    viewnode.deepsize = s
        self.roots_sum = 0
        for root in self.roots:
            self.roots_sum += root.deepsize


    def finalize_bounds(self,node, left, bottom, right, top):

        mx = (left+right)/2
        my = (bottom + top)/2
        dx = right - left
        dy = top - bottom
        ddx = min(50,dx/2.3)
        ddy = min(25,dy/2.3)

        #self.left = mx-ddx
        #self.bottom = my-ddy
        #self.right = mx+ddx
        #self.top = my+ddy
        node.set_coords(mx-ddx, my-ddy,mx+ddx,my+ddy )

    def place(self, roots, left,top,right,bottom,max_depth):

        dx = right - left
        dy = top - bottom

        xone_step = dx/self.roots_sum
        yone_step = dy/(max_depth+1)
        sibling_left = left
        #xcell = xstep * (1.0 - 2*xborder)
        #ycell = ystep * (1.0 - 2*yborder)

        stack = []
        root_top = bottom+yone_step
        for root in roots:
            left = sibling_left
            step = xone_step * root.deepsize
            sibling_left += step
            right = sibling_left
            #bottom = bottom
            top = root_top
            stack.append((root,left,bottom))
            self.finalize_bounds(root,left,bottom,right,top)

        while stack :
            node,child_left,child_bottom  = stack.pop()
            children = self.children(node)
            if children:
                child_bottom = child_bottom + yone_step
                child_top = child_bottom + yone_step
                for child in children:
                    parents = self.parents(node)
                    if len(parents) > 1 :
                        #TODO what to do with multiple parents?
                        # get the most left and most right value of a parent:
                        pass

                    left = child_left
                    step = xone_step * child.deepsize
                    child_left+=step
                    right = child_left
                    bottom = child_bottom
                    top = child_top
                    stack.append((child,left,bottom))
                    self.finalize_bounds(child,left,bottom,right,top)




















class gUtil:

    def inbox_filter(self,graph,roots,max_depth,children_filter_fn = None):
        if children_filter_fn is None:
            children_filter_fn = graph. children


    def calc_deepsize(self,graph,roots):
        """
        Calculates relative deep size of a graph.
        Designed to work "most" correctly in acyclic graph,
        but also produce some more or less reasonable "deep size"
        for cyclic graph, assuming if nodes are visited
        again, they have size of 1.
        :param graph: graph object
        :param roots: roots or placed nodes,for what we calculate their placing
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










