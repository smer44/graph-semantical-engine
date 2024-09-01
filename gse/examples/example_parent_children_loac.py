from gse.load import loads_parent_children , loads_indents
from gse.dummy import DummyNode ,child_react_dummy_node, convert_fn_dummy_node,children_dummy_node
from gse.dump import dumps_parent_children

text_ind = """Project
    Planning
        Milestone1
    #some comment
            Task1 # this is a task
            Task2
        Milestone2#some other comment#and another comment
            Task3
    Development
        Phase1
            Task4
            Task5
        Phase2
            Task6
Documentation
    Draft
        Section1
    Subs
            """



text = """
#this is the parent : children version of text_ref graph
Project : Planning, Development
Documentation : Draft ,,, Subs
Planning : Milestone1, Milestone2,
Milestone1: Task1, Task2
Milestone2 : Task3

Development:Phase1, Phase2,,
Phase1:Task4, Task5
Phase2: Task6
Draft : Section1

"""

lines_ind = text_ind.splitlines()
lines = text.splitlines()

def test_parent_child_no_inbox_all():
    print("--- parent - child ,no inbox: --- \n")
    for parent, child in loads_parent_children(lines,
                                              inbox_fn=None,
                                              child_react=None,
                                              output_root_only=False):
        print(parent, child)



def test_parent_child_inbox_dummy_all():
    print("--- parent - child , inbox to dummy node --- \n")
    for parent, child in loads_parent_children(lines,
                                              inbox_fn=convert_fn_dummy_node,
                                              child_react=child_react_dummy_node,
                                              output_root_only=False):
        print(parent, child)

def test_indents_no_inbox_all():
    print("--- indents , no inbox ---\n")

    for parent, child in loads_indents(lines_ind,
                                      inbox_fn=None,
                                      child_react=None,
                                      output_root_only=False):
        print(parent, child)

def test_indents_inbox_root():
    print("--- indents , inbox, root: ---\n")
    #first you need to parse it full :
    pairs = [pair for pair in loads_indents(lines_ind,
                                      inbox_fn=convert_fn_dummy_node,
                                      child_react=child_react_dummy_node,
                                      output_root_only=True)]

    for (parent, child) in pairs:
        print(" -- !! dump of root !! -- ", child, children_dummy_node(child))
        for line in dumps_parent_children(child,
                                          children_fn=children_dummy_node,
                                          ):
            print(line)
#Execute tests:

test_indents_inbox_root()