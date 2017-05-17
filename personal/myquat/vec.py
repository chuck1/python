from sympy import *

o0,o1,o2 = symbols('o0:3')
o0d,o1d,o2d = symbols('o0:3d')

t,td,tdd = symbols('t,td,tdd')


o = Matrix([o0,o1,o2])
od = Matrix([o0d,o1d,o2d])

f = Matrix([0,0,t])
fd = Matrix([0,0,td])
fdd = Matrix([0,0,tdd])


pprint(o)
pprint(fd)


c = fd + f.cross(o)

pprint(c)

d = fdd + 2 * fd.cross(o) + f.cross(od) + (f.cross(o)).cross(o)

pprint(d)



