import math

def quadratic(a, b, c):
    d = math.sqrt(b**2 - 4 * a * c)

    x0 = (-b + d) / 2 / a
    x1 = (-b - d) / 2 / a

    if (x0 < 0) and (x1 < 0):
        raise RuntimeError()

    if (x0 > 0) and (x1 > 0):
        return min(x0, x1)

    return max(x0, x1)

def acc_dec_1(T, X, v0, v1):

    a = -(v1 - v0)**2 / (X - v1 * T)

    T1 = T - 2 * (v1 - v0) / a
    T0 = (T - T1) / 2

    X1 = v1 * T1
    X0 = (X - X1) / 2
 
    return a, T0, T1, X0, X1

def acc_dec_2(T, X, v0):

    a = (X - v0 * T) / T**2 * 4

    v1 = T * a / 2 + v0

    return a, v1

def acc_dec_3(T, X, v_0, a_0, a_2):

    T_0 = quadratic(a_0**2 / 2 / a_2 - a_0 / 2, T * a_0, T * v_0 - X)
    
    T_2 = -a_0 * T_0 / a_2

    T_1 = T - T_0 - T_2

    v_1 = v_0 + a_0 * T_0

    X_0 = v_0 * T_0 + a_0 / 2 * T_0**2
    X_1 = v_1 * T_1

    return T_0, T_1, X_0, X_1, v_1
 

