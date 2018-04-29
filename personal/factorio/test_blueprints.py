from blueprints.blueprint import *
from blueprints.group import *
from blueprints.entity import *


e = Entity({'name':'test'}, [0,0])

g = Group(tile(e, 4, 1, x=5))

g2 = Group(tile(g, 1, 2, y=5))

for e in g2.entities:
    for e1 in e.entities:
        print(e1.group, e1.position)



