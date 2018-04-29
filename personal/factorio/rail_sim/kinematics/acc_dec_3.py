
import sympy

T, T_0, T_1, T_2 = sympy.symbols('T T_0 T_1 T_2')
v_0, v_1 = sympy.symbols('v_0 v_1')
a_0, a_2 = sympy.symbols('a_0 a_2')

# deceleration

X_0 = v_0 * T_0 + a_0 / 2 * T_0**2

# constant velocity

X_1 = v_1 * T_1

# acceleration

X_2 = v_1 * T_2 + a_2 / 2 * T_2**2

X = X_0 + X_1 + X_2

print(X)

X = X.subs(v_1, v_0 + a_0 * T_0)

print(X)

X = X.subs(T_1, T - T_0 - T_2)

print(X)

X = X.subs(T_2, -a_0 * T_0 / a_2)

print(X)

X = sympy.expand(X)

print(X)

X = sympy.collect(X, T_0)

print(X)

print(X.coeff(T_0, 0))
print(X.coeff(T_0, 1))
print(X.coeff(T_0, 2))

