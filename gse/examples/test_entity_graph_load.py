from gse.dump import  dump_entity
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
    print(dump_entity(root))


