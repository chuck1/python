from sympy import symbols, latex, pprint, Derivative, Integral
import sympy

Q, W, E, e, t, rho, A = symbols('Q W E e t rho A')

V, CS, CV, Vdotn, uhat, Vel, g, z = symbols('V CS CV Vdotn uhat Vel g z')

hhat, p = symbols('hhat, p')

# control volume energy
cv_energy = Derivative(Q,t) - Derivative(W,t) - Derivative(E,t)

pprint(cv_energy)

# Reynolds Transport Theorem
def rtt(B, beta):
    l  = Derivative(B,t)
    r  = Derivative(Integral(beta * rho, (V, CV)), t)
    r -= Integral(beta * rho * Vdotn, (A, CS))
    return l,r

pprint(rtt(E,e))

# energy per unit mass
spec_energy = uhat + V**2/2 + g * z - e

# enthalpy definition
spec_enthalpy = hhat - uhat - p/rho

pprint(spec_energy)
pprint(spec_enthalpy)

print('sympy.solve(spec_enthalpy, uhat)[0]')
pprint(sympy.solve(spec_enthalpy, uhat)[0])

spec_energy = spec_energy.subs(uhat, sympy.solve(spec_enthalpy, uhat)[0])


temp = rtt(E, e)

cv_energy = cv_energy.subs(temp[0], temp[1])

pprint(cv_energy)

cv_energy = cv_energy.subs(e, sympy.solve(spec_energy, e)[0])

pprint(cv_energy)
