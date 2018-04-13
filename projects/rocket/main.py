import matplotlib.pyplot as plt
import math
import numpy as np

import theory
from rocket import *
from stage import *
from engine import *
from util import *

def breakpoint(): import pdb; pdb.set_trace();

def simulate(r):
    t1 = 800
    dt = 0.05
    n = int(t1 // dt) + 1
    T = np.linspace(0, t1, n)
    a_para = np.zeros(n)
    A = np.zeros((n,2))
    V = np.zeros((n,2))
    X = np.zeros((n,2))
    X[0,1] = theory.radius_earth + 0e3
    TR = np.zeros(n)
    DR = np.zeros(n)
    mass = np.zeros(n)

    for s in r.stages:
        s.init_sim(n)

    stages = list(r.stages)
    stages_drag = list(r.stages)
    
    mass[0] = r.mass_wet

    stages[0].activate()

    #mass_prop = [s.mass_prop for s in stages]

    for i in range(1, n):

        thrust = sum(s.sim.thrust for s in stages)

        speed0 = mag(V[i-1])

        drag = sum(s.drag(speed0, alt(X[i-1])) for s in stages_drag)
        
        if speed0 == 0:
            V_dir = np.array([.01, 1])
            V_dir /= mag(V_dir)
        else:
            V_dir = V[i-1] / speed0

        Drag = -V_dir * drag

        Thrust = V_dir * thrust

        TR[i] = thrust
        DR[i] = drag
        
        vec_grav = -X[i-1] / mag(X[i-1]) * theory.grav(mag(X[i-1]))

        A[i] = (Thrust + Drag) / mass[i-1] + vec_grav

        if np.any(np.isnan(A[i])):
            print(Thrust)
            print(Drag)
            print(vec_grav)
            breakpoint()
        
        a_para[i] = np.dot(A[i], V_dir)

        V[i] = V[i-1] + A[i] * dt

        X[i] = X[i-1] + V[i] * dt

        if np.any(np.isnan(X[i])):
            breakpoint()

        if alt(X[i]) < 0:
            print('stop')
            break

        if np.any(np.isnan(A[i])): breakpoint()

        for s in stages:
            for e in s.engines:
                e.sim.mdot[i] = e.mdot
                e.sim.mdot_fuel[i] = e.mdot_fuel
                e.sim.mdot_oxidizer[i] = e.mdot_oxidizer

        mdot = sum(s.sim.mdot for s in stages)

        
        if stages:
            #print(f'{T[i]:8.2f} {mdot:8.2f} {mag(V[i]):8.2f} {mass[i-1]} {stages[0].sim.mass_prop[i-1]}')

            stages[0].sim.mass_prop[i] = stages[0].sim.mass_prop[i-1] - mdot * dt
            
            for s in stages[1:]:
                s.sim.mass_prop[i] = s.sim.mass_prop[i-1]

            if stages[0].sim.mass_prop[i] < 0:

                stages[0].sim.t_off = T[i]

                stages.pop(0)
            
                if stages:
                    if not stages[0].sim.active:
                        stages[0].activate()

                if len(stages_drag) > 1:
                    stages_drag.pop(0)

        mass[i] = sum(s.sim.mass(i) for s in stages_drag)

    theta = np.arctan2(X[:i,1], X[:i,0])
    
    fig, axs = plt.subplots(2, 3)

    axs[0, 0].plot(T[:i], np.linalg.norm(V[:i], axis=1))
    axs[0, 0].plot([T[0], T[i]], [343, 343])
    axs[0, 0].set_ylabel('speed (m/s)')

    axs[0, 1].plot(T[:i], np.linalg.norm(X[:i], axis=1) - theory.radius_earth)
    axs[0, 1].set_ylabel('altitude (m)')

    axs[0, 2].plot(T[:i], TR[:i])
    axs[0, 2].plot(T[:i], DR[:i])

    axs[1, 0].plot(T[:i], a_para[:i] / 9.81, label='flight direction')
    axs[1, 0].set_ylabel('accel (g)')
    axs[1, 0].legend()

    def plot_flow(ax):
        for s in r.stages:
            for e in s.engines:
                ax.plot(T, e.sim.mdot_fuel / e.density_f * 1000, label='F')
                ax.plot(T, e.sim.mdot_oxidizer / e.density_o * 1000, label='O')
        ax.legend()
        ax.set_ylabel('flow rate (L/s)')

    def plot_mass(ax):
        ax.plot(T[:i], mass[:i])
        ax.set_ylabel('mass (kg)')

    plot_mass(axs[1, 1])
    plot_flow(axs[1, 2])
    

    fig, ax = plt.subplots(1, 1)
    ax.plot(X[:i,0], X[:i,1])
    ax.plot(theory.radius_earth * np.cos(theta), theory.radius_earth * np.sin(theta))
    ax.axis('equal')
    plt.show()
    
def plot_mach_factor():
    M = np.linspace(0, 10, 1000)
    f = [mach_factor(M1) for M1 in M]
    plt.plot(M, f)
    plt.show()

def test1():
    r = Rocket()

    s1 = Stage(100, 20, 0.200, [Engine(0.005), Engine(0.005)])

    s2 = Stage( 50, 10, 0.100, [Engine(0.005)])
    
    s1.co_staged = [s2]

    s3 = Stage(20, 10, 0.100, [Engine(0.005)])
    
    r.stages = [
            s1, 
            s2, 
            s3,
            ]
    
    print('delta v total:', r.deltav())
    
    return r

def test2():
    r = Rocket()
    s1 = Stage()
    
    s1.Isp = 200.
    s1.m_wet = 20.0
    s1.m_dry = 10.0
    
    r.stages = [s1]
    
    print(r.deltav())


#plot_mach_factor()

r = test1()

simulate(r)

r.print_info()

#radio = Radio()
#print radio.power(400e3, 5e-6)




