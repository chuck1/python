import matplotlib.pyplot as plt
import math
import numpy as np

import theory
from rocket import *
from stage import *
from engine import *
from util import *

def breakpoint(): import pdb; pdb.set_trace();

class Simulation:
    def __init__(self, V_dir=np.array([0, 1])):
        self.V_dir = V_dir
        self.t1 = 10000
        self.dt = 0.1
        self.n = int(self.t1 // self.dt) + 1
        self.V = np.zeros((self.n,2))
        self.X = np.zeros((self.n,2))
        self.altitude = np.zeros(self.n)

        self.v_vert = np.zeros(self.n)
        self.v_hori = np.zeros(self.n)

    def vertical_speed(self, i):
        return np.dot(self.X[i] / mag(self.X[i]), self.V[i])

    def simulate(self, r, plot=False):
        T = np.linspace(0, self.t1, self.n)
        a_para = np.zeros(self.n)
        A = np.zeros((self.n,2))
        self.X[0,1] = theory.radius_earth + 0e3
        TR = np.zeros(self.n)
        DR = np.zeros(self.n)
        mass = np.zeros(self.n)
    
        for s in r.stages:
            s.init_sim(self)
    
        stages = list(r.stages)
        stages_drag = list(r.stages)
        
        mass[0] = r.mass_wet
    
        stages[0].activate(0)
   
        self.i_stop = self.n

        #mass_prop = [s.mass_prop for s in stages]
    
        for i in range(1, self.n):
    
            thrust = sum(s.sim.thrust for s in stages)
    
            speed0 = mag(self.V[i-1])

            drag = sum(s.drag(speed0, self.altitude[i-1]) for s in stages_drag)
            
            if speed0 == 0:
                V_dir = self.V_dir
                V_dir /= mag(V_dir)
            else:
                V_dir = self.V[i-1] / speed0
    
            Drag = -V_dir * drag
    
            Thrust = V_dir * thrust
    
            TR[i] = thrust
            DR[i] = drag
            
            up = self.X[i-1] / mag(self.X[i-1])
            right = np.array([self.X[i-1][1], self.X[i-1][0]]) / mag(self.X[i-1])

            vec_grav = -up * theory.grav(mag(self.X[i-1]))
    
            A[i] = (Thrust + Drag) / mass[i-1] + vec_grav
    
            if np.any(np.isnan(A[i])):
                print(Thrust)
                print(Drag)
                print(vec_grav)
                breakpoint()
            
            a_para[i] = np.dot(A[i], V_dir)
    
            self.V[i] = self.V[i-1] + A[i] * self.dt
   
            self.v_vert[i] = np.dot(self.V[i], up)
            self.v_hori[i] = np.dot(self.V[i], right)

            self.X[i] = self.X[i-1] + self.V[i] * self.dt

            self.altitude[i] = alt(self.X[i])
    
            if np.any(np.isnan(self.X[i])):
                breakpoint()
    
            if alt(self.X[i]) < 0:
                self.t_stop = T[i]
                self.i_stop = i
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
    
                stages[0].sim.mass_prop[i] = stages[0].sim.mass_prop[i-1] - mdot * self.dt
                
                for s in stages[1:]:
                    s.sim.mass_prop[i] = s.sim.mass_prop[i-1]
    
                if stages[0].sim.mass_prop[i] < 0:
    
                    stages[0].sim.i_off = i
                    stages[0].sim.t_off = T[i]
    
                    stages.pop(0)
                
    
                    if len(stages_drag) > 1:
                        stages_drag.pop(0)
    
            mass[i] = sum(s.sim.mass(i) for s in stages_drag)
    
            if stages:
                if not stages[0].sim.active:
                    stages[0].activate(i)
        
        if not plot: return


        fig, axs = plt.subplots(2, 3)
    
        axs[0, 0].plot(T[:i], np.linalg.norm(self.V[:i], axis=1))
        axs[0, 0].plot([T[0], T[i]], [343, 343])
        axs[0, 0].set_ylabel('speed (m/s)')
    
        axs[0, 1].plot(T[:i], np.linalg.norm(self.X[:i], axis=1) - theory.radius_earth)
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
        self.plot_xy(ax)
        plt.show()
   
    def plot_xy(self, ax):
        i = self.i_stop
        theta = np.arctan2(self.X[:i,1], self.X[:i,0])
        ax.plot(self.X[:i,0], self.X[:i,1])
        ax.plot(theory.radius_earth * np.cos(theta), theory.radius_earth * np.sin(theta))
        ax.axis('equal')

def plot_mach_factor():
    M = np.linspace(0, 10, 1000)
    f = [mach_factor(M1) for M1 in M]
    plt.plot(M, f)
    plt.show()

class Callback:
    def __init__(self, f):
        self.f = f

    def __call__(self, *args):
        self.f(*args)

class StageDelayed(Stage):
    
    

    def activate(self, i):
        if self.sim.sim.vertical_speed(i) < self.s_vert_activate:
            super(StageDelayed, self).activate(i)

def test1(s_vert_activate=50):
    r = Rocket()
    
    e0 = Engine(0.014)

    s1 = Stage(200, 20, 0.200, [e0, e0])

    s2 = Stage(100, 10, 0.100, [e0])
    
    s1.co_staged = [s2]

    s3 = StageDelayed(40, 10, 0.000, [Engine(0.005)])
    s3.s_vert_activate = s_vert_activate
    
    r.stages = [
            s1, 
            s2, 
            s3,
            ]
    
    
    return r

def test2(x, plot=False):
    r = test1(s_vert_activate=x)

    #s = Simulation(V_dir=np.array([x, 1]))
    s = Simulation(V_dir=np.array([0.72, 1]))

    s.simulate(r, plot=plot)
    
    try:
        y = np.min(s.altitude[r.stages[-1].sim.i_off:s.i_stop])
    except:
        y = 0
    
    return y

def test3():
    
    #plot_mach_factor()
    
    #A = np.linspace(0.50, 1.5, 10) # launch angle
    A = np.linspace(10, 100, 5) # s_vert activate third stage
    Y = []
    
    for a in A:
        y = test2(a)
        print(f'{a:16.4f} {y:16.1f}')
        Y.append(y)
    
    #r.print_info()
    
    #radio = Radio()
    #print radio.power(400e3, 5e-6)
    
    a = A[np.argmax(Y)]
    
    print('use a =', a)

    test2(a, plot=True)
    
def test4():
    r = test1()
    s = Simulation(V_dir=np.array([0.722, 1]))
    s.simulate(r, plot=True)

test3()





