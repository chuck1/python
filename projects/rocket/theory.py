import math

R = 8.314

def thrust(mdot, v_e, p_e, p_o, A_e):
    """
    mdot mass flow rate
    v_e exit velocity
    p_e exit pressure
    p_o free stream pressure
    """
    return mdot * v_e + (p_e - p_o) * A_e

def choked_flow(A, p_t, T_t, gamma):
    return A * p_t / math.sqrt(T_t) * math.sqrt(gamma / R) * ((gamma + 1) / 2)**(-(gamma + 1)/2/(gamma - 1))

