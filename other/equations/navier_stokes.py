from sympy import *

# 2D
# x-momentum

t, P, n = symbols('t, P, n')

u_w, u_e, u_s, u_n = symbols('u_w u_e u_s u_n')
v_s, v_n = symbols('v_s v_n')

uu_w, uu_e = symbols('uu_w uu_e')

u_t0, u_t1 = symbols('u_t(0:2)')

u = symbols('u')

dx, dy = symbols('dx dy')

P_w, P_e = symbols('P_w P_e')

expr = -Derivative(u,t) 
expr += uu_w * dy - uu_e * dy + u_s * v_s * dx - u_n * v_n * dx
expr += P_w * dy - P_e * dy
expr += - nu * dudx_w * dy + 


pprint(expr)


#expr = Derivative(u[i],t) + Derivative(u[i]*u[j], x[j]) + Derivative(P, x[i])



