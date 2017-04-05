from sympy import *

r, m, x, y, z, t = symbols("r m x y z t")
u = Function('u')(x,y,z)
v = Function('v')(x,y,z)
w = Function('w')(x,y,z)
p = Function('p')(x,y,z)


T = diff( m * ( diff(u, x) + diff(u, x) ), x) + diff( m * ( diff(u, y) + diff(v, x) ), y) + diff( m * ( diff(u, z) + diff(w, x) ), z)



expr = Derivative(r*u, t) + Derivative(r*u*v, y) + Derivative(r*u*w, z) + Derivative(r*u*u, x) + Derivative(p, x) - T

pprint(expr)



