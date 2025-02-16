from gse.load import loads_indents
class Dummy:

    def __init__(self,header):
        self.header = header
        self.children = []

    def __stra__(self):
        return f"<Dummy:{self.header}: {self.children}>"

    def __repra__(self):
        return f"<Dummy:{self.header}: {self.children}>"

    def __str__(self):
        return f"<Dummy:{self.header}>"

    def __repr__(self):
        return f"<Dummy:{self.header}>"

text = """
my_house House
    first_room Room
        item Table
        size 10
    second_room Room
        item Char
        size 20 

"""
inbox_fn = lambda line : Dummy(line)
child_react = lambda node, field : node.children.append(field)

for item in loads_indents(text.splitlines(), inbox_fn, child_react = child_react):
    print(item)


