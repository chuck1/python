#!/usr/bin/env python3

import numpy
import math
import matplotlib.pyplot as plt
import scipy.optimize

import ksp

import geometry
from geometry import Ellipse

def func4():
    
    e1 = Ellipse()
    e1.a = 2
    e1.b = 1
    e1.alpha = math.pi
    e1.calc()
    
    e2 = Ellipse()
    #e2.a = 0.6
    e2.b = 0.3
    e2.alpha = 4.7 * math.pi / 4
    
    a2 = scipy.optimize.fsolve(func3, 0.9, (e1, e2))[0]
    #a2 = [0.9]
    
    print('e2.alpha', e2.alpha)
    print('a2      ',a2)
    
    #func3(a2, e1, e2)
    
    #pair_plot(e1, e2)
    
    #plt.show()
    

def func5(alpha2):
    e1 = Ellipse()
    e1.a = 2
    e1.b = 1
    e1.alpha = math.pi
    e1.calc()
    
    e2 = Ellipse()
    e2.a = 0.6
    e2.b = 0.3
    e2.alpha = alpha2
    e2.calc()

    y = get_f_gamma_equal(e1, e2)
    y1 = numpy.min(y)
    y2 = numpy.max(y)
    return y1,y2

def func6():
    #numpy.array([5/4*math.pi])
    alpha2 = numpy.linspace(0,2*math.pi)
    y1,y2 = numpy.vectorize(func5)(alpha2)
    
    plt.plot(alpha2,y1,'-o')
    plt.plot(alpha2,y2,'-o')

    plt.savefig('/var/www/html/fig1.png')

def get_f_gamma_equal_at_closest(e1, e2):
    f1_gamma_equal, f2_gamma_equal = geometry.get_f_gamma_equal(e1, e2)
    
    distance_gamma_equal = e1.radius_from_true_anomaly(f1_gamma_equal) - e2.radius_from_true_anomaly(f2_gamma_equal)
    
    i = numpy.argmin(numpy.abs(distance_gamma_equal))
    
    return f1_gamma_equal[i], f2_gamma_equal[i]

def func7a(apo, t, e1, e2):
    # find the apoapsis for e2 for which
    # e1 and e2 intersect and are tangent at the point of intersection

    e2.apo = apo
    e2.calc_per_apo()
    
    f1_gamma_equal, f2_gamma_equal = geometry.get_f_gamma_equal(e1, e2)
    
    distance_gamma_equal = e1.radius_from_true_anomaly(f1_gamma_equal) - e2.radius_from_true_anomaly(f2_gamma_equal)
    
    i = numpy.argmin(numpy.abs(distance_gamma_equal))
    
    #return numpy.min(numpy.abs(distance_gamma_equal))

    y = distance_gamma_equal[i]

    return y

class func7(object):
    def __call__(self, t, e1, c2):
        # constants
        # e1 c2
        
        # variables
        # t - time at which satellite 2 will execute transfer burn
        
        print('func7 t=',t)
    
        # time 1
        E2 = c2.eccentric_anomaly_from_time(t)
        M2 = c2.mean_anomaly_from_eccentric_anomaly(E2)
        f2 = c2.true_anomaly_from_eccentric_anomaly(E2)
        f1 = f2 + c2.alpha - e1.alpha
        
        r1 = e1.radius_from_true_anomaly(f1 + math.pi)
        
        e2 = Ellipse()
        e2.body = c2.body
        e2.per = c2.per
        e2.alpha = c2.alpha + f2
        
        scipy.optimize.fsolve(func7a, r1, (t, e1, e2))
    
        e2.meananomalyatepoch = M2 - 2 * math.pi / e2.period * t
    
        # time 2
        _, f2 = get_f_gamma_equal_at_closest(e1, e2)
        
        E2 = e2.eccentric_anomaly_from_true_anomaly(f2)
        
        A = e2.area_swept_from_eccentric_anomaly(numpy.array([0]), E2)
    
        t = t + e2.time_delta_from_area_delta(A)
        
        f1 = e1.true_anomaly_from_time(t)
     
        self.e1 = e1
        self.e2 = e2
        self.f1 = f1
        self.f2 = f2
        
        
        y = f1 + e1.alpha - f2 - e2.alpha
    
        #y = numpy.mod(y + 2 * math.pi, 2 * math.pi)
    
        print(y)
    
        return y
    
    def plot(self):
        geometry.pair_plot(self.e1, self.e2)
        self.e1.plot_points_from_true_anomaly(self.f1)
        self.e2.plot_points_from_true_anomaly(self.f2)

def func8():
    e1 = ksp.gilly.obt

    c2 = Ellipse()
    c2.body = ksp.eve
    c2.apo = c2.per = ksp.eve.radius * 2
    c2.meananomalyatepoch = 0
    c2.alpha = math.pi
    c2.calc_per_apo()
    
    #func7(0, e1, c2)
    #func7(c2.period/4, e1, c2)
    
    ftor = func7()

    scipy.optimize.fsolve(ftor, 1000, (e1, c2))
    #scipy.optimize.minimize(ftor, 0, (e1, c2))

    ftor.plot()

    if True:
        plt.figure()
        t = numpy.linspace(0,2000)
        z = numpy.vectorize(ftor)(t, e1, c2)
        plt.plot(t,z)

def test_angle_transform():

    s = 0.66434

    a1 = numpy.linspace(0,2*math.pi)
    
    a2 = numpy.arctan(s * numpy.tan(a1))

    a2[a1>(math.pi/2)] += math.pi
    a2[a1>(3*math.pi/2)] += math.pi
    
    plt.figure()
    plt.plot(a1,a2)
    
    plt.show()

func8()

plt.show()




