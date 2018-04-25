import sys

from CoolProp.CoolProp import PropsSI



def open_decoupled():

    """
    states
    1 - pump inlet
    2 - pump outlet, engine cooling channels inlet
    3 - engine cooling channels outlet, turbine input
    4 - turbine outlet, chamber inlet
    """
    
    # mass flow of fuel
    m = 1 # kg / s

    # cooling rate
    # arbitrary
    q_chamber = 1e5 # W

    e_pump = 0.9
    e_turb = 0.8

    f = "Ethanol"

    # based on chamber pressure
    p_4 = 6.89e6 # Pa

    # arbitrary
    p_3 = p_4 - dp_3_4 # Pa

    p_2 = p_3

    # tank pressure
    p_1 = 5e5 # Pa
    
    # tank temperature (room temperature fuel)
    T_1 = 293 # K
    
    h_1 = PropsSI("H", "T", T_1, "P", p_1, f)
    s_1 = PropsSI("S", "T", T_1, "P", p_1, f)

    
    s_2s = s_1

    h_2s = PropsSI("H", "P", p_2, "S", s_2s, f)

    h_2 = (h_2s - h_1 + h_1 * e_pump) / e_pump

    # assume saturated vapor out of cooling channels
    #h_3 = PropsSI("H", "P", p_3, "Q", 1, f)

    # use cooling requirement
    h_3 = h_2 + q_chamber * m
   
    s_3 = PropsSI("S", "H", h_3, "P", p_3, f)

    s_4s = s_3

    h_4s = PropsSI("H", "P", p_4, "S", s_4s, f)

    h_4 = (h_4s - h_3 + h_3 * e_turb) / e_turb
    
    pow_pump = m * (h_2 - h_1)

    pow_turb = m * (h_3 - h_4)

    print(f'h_1           {h_1:10.0f}')
    print(f'h_2           {h_2:10.0f}')
    print(f'h_3           {h_3:10.0f}')
    print(f'h_4           {h_4:10.0f}')
    print(f'pump power    {pow_pump:10.0f}')
    print(f'turbine power {pow_turb:10.0f}')
    print(f'power frac    {pow_turb / pow_pump:10.3f}')


open_decoupled(float(sys.argv[1]))



