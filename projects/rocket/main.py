
from flight.simulation import *

import cycle.cycle

def test4():
    r = rocket_0()
    s = Simulation(V_dir=np.array([0.722, 1]))
    s.simulate(r, plot=True)
    r.print_info()

def test5():
    r = rocket_1()
    s = Simulation(V_dir=np.array([0.01, 1]))
    s.simulate(r, plot=False)
    
    s.print_post()
    
    r.print_info()

def test_cycles():
    energy_comb_frac = 0.008
    power_frac=1.5

    c0 = cycle.cycle.OpenDecoupled(
            #pr=1.3, 
            power_frac=power_frac,
            energy_comb_frac=energy_comb_frac)
    c0.solve()
    c0.print_()

    c1 = cycle.cycle.ClosedDecoupledPreheat(
            #bypass=0.1,
            power_frac=power_frac,
            energy_comb_frac=energy_comb_frac)
    c1.solve()
    c1.print_()



test5()


test_cycles()



