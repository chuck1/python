#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy
import math

def func_r(r_e, r, d):
    f = 0.5 * (1.0 + d)
    r_2 = r_e*(r_e-r)/(r_e-f*r)
    
    if math.isnan(r_2):
        print('r_e',r_e)
        print('r  ',r)
        print('d  ',d)
        raise ValueError('nan in func_r')
    
    return r_2

def func_a(r1,r2): return (r1+r2)/2

def func_s(mu,a,r):
    return numpy.sqrt(mu*(2/r-1/a))

def func_s_2(mu, r_e, r, d):
    r_2 = func_r(r_e, r, d)
    a = func_a(r, r_2)
    s = func_s(mu, a, r)
    return s

def plot_arc(ax,r,v0,v1,args=tuple()):
    v0 = v0 / numpy.linalg.norm(v0)
    v1 = v1 / numpy.linalg.norm(v1)
    xaxis = numpy.array([1,0])
    
    d0 = numpy.dot(xaxis,v0)
    d1 = numpy.dot(xaxis,v1)
    
    print('plot arc')
    print(v0,v1)
    print(d0,d1)

    t0=numpy.arccos(d0)
    t1=numpy.arccos(d1)

    t = numpy.linspace(t0,t1,100)

    x = r*numpy.cos(t)
    y = r*numpy.sin(t)

    ax.plot(x, y, *args)

class Ftor_apo(object):
    def __init__(self, r0, r1, a):
        self.r0=r0
        self.r1=r1
        self.a=a
    def __call__(self, t):
        x = t / (math.pi / 2)
        y = (1 - numpy.exp(-self.a * x)) / (1 - numpy.exp(-self.a))
        return self.r0 + (self.r1 - self.r0) * y

def step(vec_r_0, vec_v_0, mu, ftor_apo, a_t_max):

    dt = 1
    
    r_0 = numpy.linalg.norm(vec_r_0)
    v_0 = numpy.linalg.norm(vec_v_0)
    
    t_0 = numpy.arccos(numpy.dot(vec_v_0, vec_r_0)/v_0/r_0)

    apo_0 = ftor_apo(t_0)

    v_0_tar = func_s_2(mu, apo_0, r_0, numpy.cos(math.pi - 2 * t_0))
    
    a_t = 10

    if 0:
        print('vec_r_0',vec_r_0)
        print('vec_v_0',vec_v_0)
        print('t_0  ',t_0)
        print('apo_0',apo_0)
        print('v_0    ',v_0)
        print('v_0 tar',v_0_tar)
   
    for i in range(5):
 
        if a_t > a_t_max:
            #print('a_t limited')
            a_t = a_t_max
   
        vec_a_t = a_t * vec_v_0 / v_0
        
        vec_a = vec_a_t - mu/r_0/r_0 * vec_r_0/r_0
        
        vec_v_1 = vec_v_0 + vec_a * dt
    
        vec_r_1 = vec_r_0 + vec_v_0 * dt
 
        if a_t > a_t_max: break
       
        r_1 = numpy.linalg.norm(vec_r_1)
        v_1 = numpy.linalg.norm(vec_v_1)
        
        t_1 = numpy.arccos(numpy.dot(vec_v_1, vec_r_1)/r_1/v_1)
        
        if math.isnan(t_1):
            print('r_1',r_1)
            print('v_1',v_1)
            raise ValueError()

        apo_1 = ftor_apo(t_1)
        
        v_1_tar = func_s_2(mu, apo_1, r_1, numpy.cos(math.pi - 2 * t_1))
    
        dv = v_1_tar - v_1
 
        a_t += dv / dt * 0.9
        
        if numpy.any(numpy.isnan(vec_r_1)):
            print('i      ',i)
            print('vec_v_1',vec_v_1)
            print('t_1    ',t_1)
            print('apo_1  ',apo_1)
            print('v_1    ',v_1)
            print('v_1 tar',v_1_tar)
            print('dv     ',dv)
            print('a_t    ',a_t)

            raise ValueError('nan')


    return vec_r_1, vec_v_1


def ascent(a,t0,v0,fig_map,fig_alt):
    
    r_orbit = 670000
    r_surf =  600000
    
    kerbin_mu = 3.5316E12
    
    r_0 = r_surf + 1000
    vec_r = numpy.array([[0,r_surf]])
    
    vec_v = numpy.array([[v0*numpy.sin(t0),v0*numpy.cos(t0)]])
    
    # angle from vertical
    theta = numpy.linspace(0,math.pi/2)
    
    ftor_apo = Ftor_apo(r_0, r_orbit, a)
    
    #apo = numpy.sin(a) * r_orbit
    apo = ftor_apo(theta)
    
    # dot product of focal point to ship vectors
    d = numpy.cos(math.pi - 2 * theta)
    
    r_2 = func_r(apo[0], r_surf, d[0])
    #a = func_a(r_surf,r_2)
    
    #s = func_s(kerbin_mu,a,r_surf)
    
    print('theta',theta[0])
    print('apo  ',apo[0])
    print('r_1  ',r_surf)
    print('r_2  ',r_2)
    print('d    ',d[0])
    #print('a    ',a)
    #print('s    ',s)
    
    g_surf = kerbin_mu / r_surf**2
    
    for i in range(360):
        vec_r_1, vec_v_1 = step(vec_r[-1], vec_v[-1], kerbin_mu, ftor_apo, g_surf*2.0)
    
        vec_r = numpy.append(vec_r, numpy.reshape(vec_r_1,(1,2)), axis=0)
        vec_v = numpy.append(vec_v, numpy.reshape(vec_v_1,(1,2)), axis=0)
        
        r = numpy.linalg.norm(vec_r_1)
        v = numpy.linalg.norm(vec_v_1)
        
        t = numpy.arccos(numpy.dot(vec_v_1, vec_r_1)/v/r)
    
        if t > math.pi/2:
            break
        

    if 0:
        plt.plot(theta,Ftor_apo(r_0, r_orbit, 5)(theta), label='5')
        plt.plot(theta,Ftor_apo(r_0, r_orbit, 10)(theta), label='10')
        plt.plot(theta,Ftor_apo(r_0, r_orbit, 20)(theta), label='20')
        plt.xlabel('angle')
        plt.legend()
        plt.ylabel('apo')
    
    if 1:
        fig_map.plot(vec_r[:,0],vec_r[:,1],label="a={} t0={}".format(a,t0))
    
        plot_arc(fig_map, r_surf, vec_r[0], vec_r[-1])
    
        fig_map.axis('equal')

    if 1:
        fig_alt.plot(numpy.arange(numpy.shape(vec_r)[0]), numpy.linalg.norm(vec_r,axis=1),label="a={} t0={}".format(a,t0))

fig_map = plt.figure()
fig_alt = plt.figure()

ax_map = fig_map.add_subplot(1,1,1)
ax_alt = fig_alt.add_subplot(1,1,1)

ascent(1, .01, 1, ax_map, ax_alt)
ascent(1, .02, 1, ax_map, ax_alt)

ax_map.legend()
ax_alt.legend()

plt.show()
    
    
    
