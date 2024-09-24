from gse.dump import  dumps
from gse.gio import load_entities_with_fields

text = """
action
    -time
    -place
    
object
    -form
    -place
    
place
    -xcoord
    -ycoord
    -zcoord
"""

eg,roots = load_entities_with_fields(text.splitlines())

for root in roots:
    print("---")
    print(dumps(eg,root))


