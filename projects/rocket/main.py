import sys
import math
import scipy.optimize
import matplotlib.pyplot as plt
import numpy

G = 6.67E-11

# J kg K Pa

def air_density(h):

    # temperature lapse rate K/m
    L = 0.0065
    g = 9.8
    R = 8.31
    M = 0.02896
    T0 = 288.15
    p0 = 101325
   
    a = L * h / T0

    if a > 1:
        return 0

    p = p0 * (1.0 - a)**(g * M / R / L)
    
    T = T0 - L * h

    d = p * M / R / T
     
    if math.isnan(d):
        print "L * h / T0",(L * h / T0)
        print "h",h
        print "p",p
        print "T",T
        raise Exception()

    return d

def orbital_speed(h):
    r_E = 6371000
    r = r_E + h
    v = numpy.sqrt(G * 6E24 / r)
    return v

class Flight(object): pass

def ascent(stages, res, a0, plot=False):
    steps = 1000

    d_x, d_y, v_x, v_y = res
    
    d_X = numpy.zeros(steps * len(stages) + 1)
    d_Y = numpy.zeros(steps * len(stages) + 1)
    v_X = numpy.zeros(steps * len(stages) + 1)
    v_Y = numpy.zeros(steps * len(stages) + 1)
    a_X = numpy.zeros(steps * len(stages) + 1)
    a_Y = numpy.zeros(steps * len(stages) + 1)
    D = numpy.zeros(steps * len(stages) + 1)
    m = numpy.zeros(steps * len(stages) + 1)
    a = numpy.zeros(steps * len(stages) + 1)
    t = numpy.zeros(steps * len(stages) + 1)
    v_term = numpy.zeros(steps * len(stages) + 1)

    d_X[0] = d_x[-1]
    d_Y[0] = d_y[-1]
    v_X[0] = v_x[-1]
    v_Y[0] = v_y[-1]

    i = 1

    c = 343
    
    for stage in stages:

        mass_dry = stage.mass_dry
        mass_wet = stage.mass_wet
        mass_flow = stage.mass_flow
        T = stage.T
        CdA = stage.CdA

        t1 = (mass_wet - mass_dry) / mass_flow
        
        dt = t1 / steps
    
        m[i-1] = mass_wet

        g = 9.8
        
        j = 0

        while j < steps:

            t[i] = t[i-1] + dt

            if v_Y[i-1] == 0:
                a[i] = a0
            elif v_X[i-1] == 0:
                a[i] = math.pi/2.0
            else:
                a[i] = math.atan(v_Y[i-1] / v_X[i-1])
          
            if a[i] < 0:
                break;

            ad = air_density(d_Y[i-1])
            D[i] = 0.5 * CdA * ad * (v_X[i-1]**2 + v_Y[i-1]**2)
            W = m[i-1] * g
            
            v_term[i] = math.sqrt(2 * m[i-1] * g / ad / stage.CdA)

            if 0:
                print "i",i
                print D[i]
                print "a",a
                print m
    
            a_X[i] = ((T - D[i]) * math.cos(a[i])    ) / m[i-1]
            a_Y[i] = ((T - D[i]) * math.sin(a[i]) - W) / m[i-1]
    
            if math.isnan(a_Y[i]):
                print "m[i-1]", m[i-1]
                print "a[i]  ", a[i]
                print "ad ", ad
                print "D  ", D[i]
                print "d_X", d_x
                print "d_Y", d_y
                print "v_X", v_x
                print "v_Y", v_Y[i-1]
                print "a_Y", a_Y[i]
                raise Exception()
    
            v_X[i] = v_X[i-1] + a_X[i] * dt
            v_Y[i] = v_Y[i-1] + a_Y[i] * dt
    
            d_X[i] += d_X[i-1] + v_X[i] * dt
            d_Y[i] += d_Y[i-1] + v_Y[i] * dt
    
            m[i] = m[i-1] - mass_flow * dt
    
            if math.isnan(v_Y[i]) | math.isnan(d_Y[i]):
                print "d_X", d_x
                print "d_Y", d_y
                print "D  ", D[i]
                print "v_X", v_x
                print "v_Y", v_Y[i]
                print "v_Y", v_Y[i-1]
                print "a_Y", a_Y[i]
                raise Exception()

            i += 1
            j += 1

    # post

    v = numpy.sqrt(numpy.power(v_Y, 2) + numpy.power(v_X, 2))

    # plots
    
    if plot:
        plt.figure()
        
        if numpy.max(D) > 0:
            p = plt.plot(t, D / numpy.max(D), label='drag')
        
        p = plt.plot(t, a / math.pi, label='a / pi')
        p = plt.plot(t, a_Y / g, label='a_Y / g')
        #p = plt.plot(t, v_Y / v_term, label='v_Y / v_term')
        #p = plt.plot(t, v / c, label='mach')
        plt.xlabel('t')
        
        plt.legend()
        
        # trajectory
    
        plt.figure()
        plt.plot(d_X, d_Y)
        
        for i in range(len(stages)):
            j = steps * i - 1
            plt.plot(d_X[j], d_Y[j], 'o')
    
        plt.xlabel('x')
        plt.ylabel('y')
        plt.axis('equal')
    
        # horizontal speed
    
        plt.figure()
        plt.plot(t, v_X / orbital_speed(d_Y))
        plt.xlabel('t')
        plt.ylabel('v_x / v_orbit')
    
        plt.show()
   
    #return d_X, d_Y, v_X, v_Y

    flight = Flight()

    flight.v_X_scaled = v_X / orbital_speed(d_Y)

    return flight

def tank_length(V, r):

    def f(X, V, r):

        L = X[0]
    
        V2 = 4.0/3.0 * math.pi * r**3.0 + math.pi * r**2.0 * L

        return V - V2

    return scipy.optimize.fsolve(f, [r], (V, r))[0]

class Tank(object):
    def __init__(self):
        pass

    def length(self):
        return tank_length(self.volume, self.r)

    def m_dry(self):
        d = 2700
        L = tank_length(self.volume, self.r)
       
        A = 4.0 * math.pi * self.r**2.0 + 2.0 * math.pi * self.r * L

        V = A * self.t

        m = d * V

        return m

class Other(object): pass

class Vessel(object):
    parts = list()

    def mass_dry(self):
        y = 0
        for p in self.parts:
            y += p.m_dry()
        return y

    def mass_wet(self):
        y = 0
        for p in self.parts:
            y += p.m_wet()
        return y


def f1(X, A_e):
    x1 = X[0]

    a = g1**(-g2)

    b = 1.0 + (g-1.0)/2.0 * x1**2.0

    x2 = a * b**g2 / A_e * A_s

    return [x1 - x2]

def f2(A_e):
    return scipy.optimize.fsolve(f1, [100], (A_e))[0]

####################################################

d_o = 1141
d_f = 719.7

M_o = 16
M_f = 114.23

mol_f = 2
mol_o = 25

n_CO2 = 16
n_H2O = 18

M_CO2 = 44
M_H2O = 18

M_products = (n_CO2 * M_CO2 + n_H2O * M_H2O) / (n_CO2 + n_H2O)
M_products = 22

g = 1.22
R = 8.314 / M_products * 1000

ratio_area = 7.0

r_e = 30E-3


p_0 = 101300

T_t = 3533
#T_t = 4000

p_t = 6.89E6
p_t = numpy.linspace(5E6, 10E6, 100)
p_t = 7e6

###########################################################

A_e = math.pi * r_e**2.0


A_s = A_e / ratio_area

r_s = numpy.sqrt(A_s / math.pi)

g1 = (g+1.0)/2.0
g2 = (g+1.0)/2.0/(g-1.0)

m = A_s * p_t / math.sqrt(T_t) * math.sqrt(g / R) * (g1)**(-g2)

f2v = numpy.vectorize(f2)

M_e = f2(A_e)

a = 1 + (g-1)/2 * numpy.power(M_e, 2)

p_e = p_t / numpy.power(a, g/(g-1))

T_e = T_t / a

V_e = M_e * numpy.sqrt(g * R * T_e)

F = m * V_e + (p_e - p_0) * A_e

if 0:
    print "{:<16}{:16.2f}".format("m",m)
    print "{:<16}{:16.2f}".format("M_e",M_e)
    print "{:<16}{:16.2f}".format("T_e",T_e)
    print "{:<16}{:16.2f}".format("p_e",p_e)
    print "{:<16}{:16.2f}".format("F",F)

if 0:
    plt.figure()
    plt.plot(p_t, p_e)
    plt.xlabel("p_t")
    plt.ylabel("p_e")

    plt.figure()
    plt.plot(p_t, V_e)
    plt.xlabel("p_t")
    plt.ylabel("V_e")

    plt.show()

    sys.exit(0)

if 0:
    plt.figure()
    plt.plot(r_e, M_e, '-')

    plt.figure()
    plt.plot(r_e, V_e)
    plt.ylabel("V_e")
 
    plt.figure()
    plt.plot(r_e, T_e)
    plt.ylabel("T_e")
   
    plt.figure()
    plt.plot(r_e, p_t)
    plt.plot(r_e, p_e)

    plt.show()

    sys.exit(0)

dV = 9000

mr = numpy.exp(dV / V_e) 

g3 = (g-1.0)/g

V_e2 = numpy.sqrt(T_t * R * 2.0 / g3 * (1.0 - numpy.power(p_e / p_t, g3) ))





mass_ratio_f = mol_f * M_f / (mol_f * M_f + mol_o * M_o)
o_ratio = 1 - mass_ratio_f

f_V_ratio = mass_ratio_f / d_f / (mass_ratio_f / d_f + o_ratio / d_o)
o_V_ratio = 1 - f_V_ratio

d = 1 / (mass_ratio_f / d_f + o_ratio / d_o)

print "{:<32}{:16.2e}".format("propellent mixture density",d)

tank_f = Tank()
tank_o = Tank()

tank_f.volume = 0.1
tank_o.volume = tank_f.volume / f_V_ratio * o_V_ratio

tank_f.t = 0.006
tank_o.t = 0.006

tank_f.r = 0.15
tank_o.r = 0.15

print "{:<32}{:16.2e}".format("f volume ratio",f_V_ratio)
print "{:<32}{:16.2e}".format("o volume ratio",o_V_ratio)

#print "{:<32}{:16.2e}".format("tank dry mass",tank.m_dry)
#print "{:<32}{:16.2e}".format("tank wet mass",tank.volume * d + tank.m_dry)


m_f_1 = tank_f.volume * d_f
m_o_1 = m_f_1 / mass_ratio_f * o_ratio
V_o_1 = m_o_1 / d_o
ff_o_1 = V_o_1 / tank_o.volume

m_o_2 = tank_o.volume * d_o
m_f_2 = m_o_2 / o_ratio * mass_ratio_f
V_f_2 = m_f_2 / d_f
ff_f_2 = V_f_2 / tank_f.volume


print "{:<32}{:16.2e}".format("fill fraction o 1",ff_o_1)
print "{:<32}{:16.2e}".format("fill fraction f 2",ff_f_2)

if ff_o_1 < ff_f_2:
    m_f = m_f_1
    m_o = m_o_1
else:
    m_f = m_f_2
    m_o = m_o_2

print "{:<32}{:16.2e}".format("mass f",m_f)
print "{:<32}{:16.2e}".format("mass o",m_o)

tank_f.m_wet = lambda: tank_f.m_dry() + m_f
tank_o.m_wet = lambda: tank_o.m_dry() + m_o


vessel = Vessel()

t_burn = (m_f + m_o) / m

other = Other()
other.m_dry = other.m_wet = lambda: 8.0

vessel.parts.append(tank_f)
vessel.parts.append(tank_o)
vessel.parts.append(other)

print "{:<32}{:16.1f} mm".format("r_s",r_s*1000)
print "{:<32}{:16.1f} mm".format("r_e",r_e*1000)
print "{:<32}{:16.2e}".format("g",g)
print "{:<32}{:16.2e}".format("g1",g1)
print "{:<32}{:16.2e}".format("g2",g2)
print "{:<32}{:16.2e}".format("A_s",A_s)
print "{:<32}{:16.2e}".format("R",R)
print "{:<32}{:16.2e}".format("M_products",M_products)
print "{:<32}{:16.2e}".format("p_e",p_e)
print "{:<32}{:16.2e}".format("T_e",T_e)
print "{:<32}{:16.2e}".format("V_e",V_e)
print "{:<32}{:16.2e}".format("V_e",V_e2)
print "{:<32}{:16.2e}".format("M_e",M_e)
print "{:<32}{:16.2e}".format("dV",dV)
print "{:<32}{:16.2e}".format("mr",mr)
print "{:<32}{:16.2e}".format("mass ratio f",mass_ratio_f)
print "{:<32}{:16.2e}".format("burn time",t_burn)
print "{:<32}{:16.2e}".format("tank f mass ratio",tank_f.m_wet() / tank_f.m_dry())
print "{:<32}{:16.2e}".format("tank o mass ratio",tank_o.m_wet() / tank_o.m_dry())
print "{:<32}{:16.2e}".format("tank f volume    ",tank_f.volume)
print "{:<32}{:16.2e}".format("tank o volume    ",tank_o.volume)
print "{:<32}{:16.2e}".format("tank f length    ",tank_f.length())
print "{:<32}{:16.2e}".format("tank o length    ",tank_o.length())
print "{:<32}{:16.2e}".format("tank f L/D       ",tank_f.length() / tank_f.r / 2.0)
print "{:<32}{:16.2e}".format("tank o L/D       ",tank_o.length() / tank_o.r / 2.0)
print "{:<32}{:16.2e}".format("tank f radius    ",tank_f.r)
print "{:<32}{:16.2e}".format("tank o radius    ",tank_o.r)
print "{:<32}{:16.2e}".format("density f        ",d_f)
print "{:<32}{:16.2e}".format("density o        ",d_o)
print "{:<32}{:16.2e}".format("mass flow        ",m)

print "{:<32}{:16.2e}".format("vessel mass dry",vessel.mass_dry())
print "{:<32}{:16.2e}".format("vessel mass wet",vessel.mass_wet())
print "{:<32}{:16.2e}".format("vessel mass ratio",vessel.mass_wet() / vessel.mass_dry())

weight = vessel.mass_wet() * 9.81

TWR = F / weight

print "{:<32}{:16.2e}".format("TWR",TWR)



# ascent rate

r1 = 0.2
r2 = 0.1

class Stage(object): pass

s1 = Stage()
s1.mass_dry =   93.5
s1.mass_wet =  442.0
s1.mass_flow =   3.17
s1.T =        8729.1
s1.CdA = math.pi * r1**2 * 0.75

s2 = Stage()
s2.mass_dry =     7.8
s2.mass_wet =    73.2
s2.mass_flow =    0.6
s2.T =         1671.0
s2.CdA = math.pi * r2**2 * 0.75





for a in numpy.linspace(0.0015, 0.0020, 10):
    flight = ascent([s1,s2], ([0], [0], [0], [0]), math.pi/2 - a)

    print numpy.max(flight.v_X_scaled)

















