from gse.entitygraph import EntityGraph
from gse.dump import dumpsi, dumps

eg = EntityGraph()

superman = eg.get_or_create_node("superman")
eg.add_parent(superman,"Superhero")
eg.add_field(superman,"name_variants", ("Clarc Kent" , "superman"))
eg.add_field(superman,"race", "cryptonian") # ? set cryptonian is from crypton or smth
eg.add_field(superman,"grew up in", "earth")

lazer_eyes = eg.get_or_create_node("lazer_eyes")
eg.add_parent(lazer_eyes,"Skill")
#eg.add_field(lazer_eyes, "instance", True)
eg.add_field(lazer_eyes, "source", "body")
eg.add_field(lazer_eyes, "type", "ray")
eg.add_field(lazer_eyes, "target", "look at")
eg.add_field(lazer_eyes, "working type", "emit")
eg.add_field(lazer_eyes, "emit from", "eyes")


body_flight = eg.get_or_create_node("body_flight")
eg.add_parent(body_flight,"Skill")
#eg.add_field(body_flight, "instance", True)
eg.add_field(body_flight, "source", "body")
eg.add_field(body_flight, "type", "kinesis")
eg.add_field(body_flight, "target", "self")
eg.add_field(body_flight, "working type", "emit")
eg.add_field(body_flight, "emit from", "body")


eg.add_field(superman,"powers", (body_flight, lazer_eyes))
#eg.add_field(superman,"powers", body_flight)


spiderman = eg.get_or_create_node("spiderman")
eg.add_parent(spiderman,"Superhero")
eg.add_field(spiderman,"name_variants", ("Peter Parker" , "Spiderman"))
eg.add_field(spiderman,"race", "human")
eg.add_field(spiderman,"grew up in", "earth")


spider_body_strength = eg.get_or_create_node("spider_body_strength")
eg.add_parent(spider_body_strength,"Skill")
eg.add_field(spider_body_strength, "source", "body")
eg.add_field(spider_body_strength, "type", "strength")
eg.add_field(spider_body_strength, "target", "self")
eg.add_field(spider_body_strength, "working type", "permanent")

web_shot = eg.get_or_create_node("body_strength")
eg.add_parent(web_shot,"Skill")
eg.add_field(web_shot, "source", ("body","gadget"))
eg.add_field(web_shot, "type", "projectile")
eg.add_field(web_shot, "target", "point at")
eg.add_field(web_shot, "working type", "emit")
eg.add_field(web_shot, "emit from", "hands")

eg.add_field(spiderman,"powers", (spider_body_strength,web_shot))




#print(dumps(eg, superman))
print(dumps(eg, spiderman))
#print(dumps(eg,lazer_eyes))
#print(dump_entity(body_flight))

