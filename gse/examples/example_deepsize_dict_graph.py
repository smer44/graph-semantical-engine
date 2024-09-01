from gse.gutil import *
#from gse.dictgraph import DictGraph

og = ViewGraph()

root = og.new_node("root")

a = og.new_node("a")
b = og.new_node("b")
ab = og.new_node("ab")
ab1 = og.new_node("ab1")
ab2 = og.new_node("ab2")
ab3 = og.new_node("ab3")

og.add_child(root,a)
og.add_child(root,b)
og.add_child(a,ab)
og.add_child(b,ab)
og.add_child(ab,ab1)
og.add_child(ab,ab2)
og.add_child(ab,ab3)


#print(root.dumps())


gu = gUtil()

gu.calc_deepsize(og,[root])

print("Acyclic graph should run fine:")
print(og.dumps(root))


print("Now, lets try cyclic graph, this also should produce reasonable size:")

og = ViewGraph()

root = og.new_node("root")

a = og.new_node("a")
b = og.new_node("b")
c = og.new_node("c")

og.add_child(root,a)
og.add_child(a,b)
og.add_child(a,c)
og.add_child(b,root)
og.add_child(c,root)

gu.calc_deepsize(og,[root])

print(og.dumps(root))


