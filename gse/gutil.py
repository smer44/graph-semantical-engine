from gse.dump import dumps_indents
from gse.inbox import InboxValue

class ViewNode:

    def __init__(self,node,depth = 0):
        self.value = node
        self.deepsize = 0
        self.depth = depth
        self.top = None
        self.left = None
        self.bottom = None
        self.right = None
        self.view_children = []
        self.view_parents = []
        self.roots_sum = 0
        #self.rect = None
        self.rect_id = None
        self.text_id = None
        self.flags = 255
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
        self.dumps = lambda node : "".join(dumps_indents(node,self.children))
        #self.roots = []

    def new_node(self,value,depth = 0):
        node = ViewNode(value,depth)
        self.nodes.append(node)
        return node

    def new_inboxed_node(self,value,depth=0):
        value = InboxValue(value)
        self.new_node(value,depth)



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
        if node.right is not None :
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

    def correct_narrow(self, xmin):
        for node in self.nodes:
            if node.right - node.left < xmin:
                node.right = node.left + xmin

    def finalize_places(self):
        for node in self.nodes:
            self.finalize_bounds(node,node.left,node.bottom,node.right,node.top)

    def place_stretch_min(self, roots, left,bottom,right,top, max_depth, xmin = 100):
        dx = right - left
        dy = top - bottom
        xone_step = dx/self.roots_sum

        for node in self.nodes:
            node.deepsize = max(xmin, xone_step*node.deepsize)

        #now, deepsize contains the scaled value.
        #now, place nodes according to node_dx:

        ystep = dy / (max_depth + 1)
        root_top = bottom + ystep
        global_left = left
        stack = [(root, True) for root in roots]
        for root in roots:
            root.bottom = bottom
            root.top = root_top
        dejavu = set()
        while stack:
            node, first_time = stack.pop()
            dejavu.add(node)
            children = self.children(node)
            if children:
                children = list(children)
                child_bottom = node.top
                child_top = child_bottom + ystep
                if first_time:
                    # if we visit node in the first time:
                    stack.append((node, False))
                    children.reverse()
                    for child in children:
                        child.bottom = child_bottom
                        child.top = child_top
                        if child in dejavu:
                            continue
                        stack.append((child,True))

                else:
                    #if we visit node the second time, after its children is processed:

                    if node.left is not None:
                        continue
                    #select first child not used for parent size:
                    unused_child_id = None
                    unused_child = None
                    for (n,child) in enumerate(children):
                        if child.flags == 255:
                            unused_child_id = n
                            unused_child = child
                            break
                    if unused_child_id is None:
                        node.left = global_left
                        global_left += node.deepsize
                        node.right = global_left
                    else:
                        child_left = unused_child.left
                        assert child_left is not None , f"visit second time {node=} with {children[0]=}, where child_left is None"
                        ds = 0
                        for child in children[unused_child_id:]:
                            if child.flags == 255:
                                child.flags = 0
                                ds += child.deepsize
                                child.flags = 0
                        node.deepsize = ds
                        #make sure that the most left is for the first child?
                        node.left = child_left
                        node.right = child_left+ds

            else:
                #if it is a node without children:
                node.left = global_left
                global_left+=node.deepsize
                node.right = global_left

















    def place(self, roots, left,bottom,right,top,max_depth):

        dx = right - left
        dy = top - bottom

        xone_step = dx/self.roots_sum
        print(f"{xone_step=}")
        yone_step = dy/(max_depth+1)
        sibling_left = left
        #xcell = xstep * (1.0 - 2*xborder)
        #ycell = ystep * (1.0 - 2*yborder)
        min_xstep = 100

        stack = []
        root_top = bottom+yone_step
        for root in roots:
            left = sibling_left
            step =  xone_step * root.deepsize
            sibling_left += step
            right = sibling_left
            #bottom = bottom
            top = root_top
            stack.append((root,left,bottom,False))
            self.finalize_bounds(root,left,bottom,right,top)

        while stack :
            node,child_left,child_bottom,to_finish  = stack.pop()
            children = self.children(node)
            if children:
                if to_finish:
                    child_min, child_max = 10000,-1
                    for child in children:
                        #if child.
                        pass

                child_bottom = child_bottom + yone_step
                child_top = child_bottom + yone_step
                for child in children:
                    parents = self.parents(node)
                    if len(parents) > 1 :
                        #TODO what to do with multiple parents?
                        # get the most left and most right value of a parent:
                        pass
                    #check, if child is finished
                    left = child_left
                    step = xone_step * child.deepsize
                    child_left+=step
                    right = child_left
                    bottom = child_bottom
                    top = child_top
                    stack.append((child,left,bottom,False))
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










