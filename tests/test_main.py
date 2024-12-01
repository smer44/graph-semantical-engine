from io import StringIO
from gse.objgraph import ObjGraph


def text2graph(text, alignment=4):
    gr = ObjGraph()
    gol = Gol(gr, output_root_only=True, alignment=alignment)
    lines = text.splitlines()

    result = StringIO()
    items = list(gol.load_gen(lines))
    for ctx, root in items:
        result.write(repr(root))
        result.write('\n')
        result.write(root.dumps())
        result.write('\n')

    return result.getvalue()


TEXT_1 = '''Item1
    SubItem1 # this is a sub item
    SubItem2
        SubSubItem1
            SubSubSubItem1
    SubItem3

Item2
    SubItem3'''

RESULT_1 = '''<Item1: SubItem1, SubItem2, SubItem3>
Item1#0
\tSubItem1#0
\tSubItem2#0
\t\tSubSubItem1#0
\t\t\tSubSubSubItem1#0
\tSubItem3#0

<Item2: SubItem3>
Item2#0
\tSubItem3#0\n\n'''

TEST_2 = '''Project
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
            '''

RESULT_2 = '''<Project: Planning, Development>
Project#0
\tPlanning#0
\t\tMilestone1#0
\t\t\tTask1#0
\t\t\tTask2#0
\t\tMilestone2#0
\t\t\tTask3#0
\tDevelopment#0
\t\tPhase1#0
\t\t\tTask4#0
\t\t\tTask5#0
\t\tPhase2#0
\t\t\tTask6#0

<Documentation: Draft, Subs>
Documentation#0
\tDraft#0
\t\tSection1#0
\tSubs#0\n\n'''

TEXT_3 = '''Documentation1
    Draft
        Section1
    Section2Misplaced
        Section3
            Section33
Draft2Mislpaced
    Section22
    Section23
        Section234
            Section2344


Documentation2          
    Draft3Mislpaced
Subs
            '''

RESULT_3 = '''<Documentation1: Draft, Section2Misplaced>
Documentation1#0
\tDraft#0
\t\tSection1#0
\tSection2Misplaced#0
\t\tSection3#0
\t\t\tSection33#0

<Draft2Mislpaced: Section22, Section23>
Draft2Mislpaced#0
\tSection22#0
\tSection23#0
\t\tSection234#0
\t\t\tSection2344#0

<Documentation2: Draft3Mislpaced>
Documentation2#0
\tDraft3Mislpaced#0

<Subs>
Subs#0\n\n'''

TEXT_4 = '''a
    a1
b
'''

RESULT_4 = '''<a: a1>
a#0
\ta1#0

<b>
b#0\n\n'''

TEST_ALIGNMENT_1 = '''Documentation1
 Draft2Mislpaced
  Section22
 Draft3Mislpaced
Subs
       '''

RESULT_ALIGNMENT_1 = '''<Documentation1: Draft2Mislpaced, Draft3Mislpaced>
Documentation1#0
\tDraft2Mislpaced#0
\t\tSection22#0
\tDraft3Mislpaced#0

<Subs>
Subs#0\n\n'''

TEST_C_CODE = '''\npublic void fn(n):
    n = n+1
    return n\n\n'''

RESULT_C_CODE = '''<public void fn(n):: n = n+1, return n>
public void fn(n):#0
\tn = n+1#0
\treturn n#0\n\n'''

TEXT_CORRECT = '''
root 
        aligned
well_placed
'''

RESULT_CORRECT = '''<root: aligned>
root#0
\taligned#0

<well_placed>
well_placed#0\n\n'''


def test_1():
    assert text2graph(TEXT_1) == RESULT_1


def test_2():
    assert text2graph(TEST_2) == RESULT_2


def test_3():
    assert text2graph(TEXT_3) == RESULT_3


def test_4():
    assert text2graph(TEXT_4) == RESULT_4


def test_alignment_1():
    assert text2graph(TEST_ALIGNMENT_1, 1) == RESULT_ALIGNMENT_1


def test_incorrect():
    '''Проверяет выброс исключения и текст ошибки при неправильном отступе'''
    text_incorrect = '''
root 
        aligned
    misplaced
    '''
    with pytest.raises(AssertionError) as excinfo:
        text2graph(text_incorrect)

    assert excinfo.value.args[0] == 'misplaced current_level=4, having  ctx_indent=0, prev_indent=8'


def test_correct():
    assert text2graph(TEXT_CORRECT) == RESULT_CORRECT


def test_c_code():
    assert text2graph(TEST_C_CODE) == RESULT_C_CODE
