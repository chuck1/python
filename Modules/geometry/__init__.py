#!/usr/bin/env python3

import numpy
import math
import matplotlib.pyplot as plt
import scipy.optimize

def angle_transform(a1, s):
    a2 = numpy.arctan(s * numpy.tan(a1))
    a2[a1>(math.pi/2)] += math.pi
    a2[a1>(3*math.pi/2)] += math.pi
    return a2

def func1(E1, e1, e2):

    f1 = e1.true_anomaly_from_eccentric_anomaly(E1)

    f2 = f1 + e1.alpha - e2.alpha
    
    rho1 = e1.tangent_angle_from_true_anomaly(f1)

    rho2 = e2.tangent_angle_from_true_anomaly(f2)
    
    return rho1 - rho2

def func2(E1, e1, e2):

    f1 = e1.true_anomaly_from_eccentric_anomaly(E1)

    f2 = f1 + e1.alpha - e2.alpha
    
    g1 = e1.foci_angle_from_true_anomaly(f1)

    g2 = e2.foci_angle_from_true_anomaly(f2)
    
    return g1 - g2


class Ellipse(object):

    def calc_per_apo(self):
        self.a = (self.apo + self.per) / 2
        self.c = self.a - self.per
        self.b = math.sqrt(self.a**2 - self.c**2)
        self.e = math.sqrt(1 - self.b**2 / self.a**2)
        self.period = 2 * math.pi * math.sqrt(self.a**3 / self.body.mu)
        
    def calc_a_b(self):
        
        if self.b > self.a:
            self.a, self.b = self.b, self.a

        self.c = math.sqrt(self.a**2 - self.b**2)
        self.e = math.sqrt(1 - self.b**2 / self.a**2)
        self.period = 2 * math.pi * math.sqrt(self.a**3 / self.body.mu)

    def mean_anomaly_from_time(self, t):
        return self.meananomalyatepoch + 2 * math.pi / self.period * t
    
    def mean_anomaly_from_eccentric_anomaly(self, E):
        return E - self.e * numpy.sin(E)

    def radius_from_true_anomaly(self, true_anomaly):
        a = self.a
        e = self.e
        r = a * (1 - e**2) / (1 + e * numpy.cos(true_anomaly))
        return r
    
    def radius_from_eccentric_anomaly(self, eccentric_anomaly):
        a = self.a
        e = self.e
        f = self.true_anomaly_from_eccentric_anomaly(eccentric_anomaly)
        r = a * (1 - e**2) / (1 + e * numpy.cos(f))
        return r

    def tangent_angle_from_true_anomaly(self, true_anomaly):

        gamma = self.foci_angle_from_true_anomaly(true_anomaly)
        
        rho = gamma / 2 + math.pi / 2
        
        return rho

    def foci_angle_from_true_anomaly(self, true_anomaly):
        f = true_anomaly

        a = self.a
        c = self.c

        r = self.radius_from_true_anomaly(f)

        #gamma = numpy.arcsin(2 * c * numpy.sin(math.pi-f) / (2 * a - r))
        
        gamma = numpy.arctan(numpy.sin(f) / (r / 2 / c + numpy.cos(f)))

        z = numpy.cos(f) + r / 2 / c

        bool1 = numpy.logical_and(z < 0, f < math.pi)
        bool2 = numpy.logical_and(z < 0, f > math.pi)

        gamma[bool1] = gamma[bool1] + math.pi
        gamma[bool2] = gamma[bool2] - math.pi

        return gamma

    def tan_foci_angle_from_true_anomaly(self, true_anomaly):
        f = true_anomaly

        a = self.a
        c = self.c

        r = self.radius_from_true_anomaly(f)

        #gamma = numpy.arcsin(2 * c * numpy.sin(math.pi-f) / (2 * a - r))
        
        tan_gamma = numpy.sin(f) / (r / 2 / c + numpy.cos(f))

        return tan_gamma

    def eccentric_anomaly_from_true_anomaly(self, f):
        f = numpy.array([f])
        z1 = math.sqrt(1 - self.e**2) * numpy.sin(f)
        z2 = self.e + numpy.cos(f)
        z3 = z1/z2
        E = numpy.arctan(z3)
        E[z2<0] += math.pi
        E[numpy.logical_and(z1<0,z2>0)] += 2 * math.pi
        return E

    def eccentric_anomaly_from_mean_anomaly(self, M):
        e = self.e
        
        def f(E,M):
            return (E - e * numpy.sin(E)) - M
        
        M = numpy.mod(M, 2 * math.pi)

        E = 2 * numpy.arcsin(M / math.pi - 1) + math.pi
        
        E = scipy.optimize.fsolve(f,E,(M,))

        return E

    def eccentric_anomaly_from_time(self, t):
        return self.eccentric_anomaly_from_mean_anomaly(self.mean_anomaly_from_time(t))

    def true_anomaly_from_time(self, t):
        M = self.mean_anomaly_from_time(t)
        E = self.eccentric_anomaly_from_mean_anomaly(M)
        return self.true_anomaly_from_eccentric_anomaly(E)

    def true_anomaly_from_eccentric_anomaly(self, eccentric_anomaly):
        E = eccentric_anomaly
        e = self.e
        z1 = math.sqrt((1 + e) / (1 - e))
        f = 2 * numpy.arctan(z1 * numpy.tan(E / 2))
        f[f<0] = f[f<0] + 2 * math.pi
        return f

    def area_swept_from_eccentric_anomaly(self, E1, E2):
        A1 = angle_transform(E1, self.a / self.b)
        A2 = angle_transform(E2, self.a / self.b)
        return (A2 - A1) * self.a * self.b / 2
    
    def time_delta_from_area_delta(self, A):
        return self.period / math.pi / self.a / self.b * A

    def plot(self):
        # xp,yp is coordinate system centered on focal point with xp alligned with major axis
        # f true anomaly
        # r distance from focal point
        
        a = self.a
        b = self.b
        c = self.c
        e = self.e
        alpha = self.alpha

        E = numpy.linspace(0,math.pi*2,100)
        
        f = self.true_anomaly_from_eccentric_anomaly(E)
        
        r = self.radius_from_true_anomaly(f)

        xp = r * numpy.cos(f)
        yp = r * numpy.sin(f)
        
        x = xp * numpy.cos(alpha) - yp * math.sin(alpha)
        y = xp * numpy.sin(alpha) + yp * math.cos(alpha)
        
        plt.plot(x,y,'-')
        #plt.plot([0,2*c*math.cos(alpha+math.pi)],[0,2*c*math.sin(alpha+math.pi)])

    def plot_points_from_true_anomaly(self, f):
        
        c = self.c

        r = self.radius_from_true_anomaly(f)

        alpha = self.alpha

        xp = r * numpy.cos(f)
        yp = r * numpy.sin(f)
        
        X = xp * numpy.cos(alpha) - yp * math.sin(alpha)
        Y = xp * numpy.sin(alpha) + yp * math.cos(alpha)
        
        x_foci = 2 * c * math.cos(alpha + math.pi)
        y_foci = 2 * c * math.sin(alpha + math.pi)
        
        def func(x,y):
            plt.plot([0,x],[0,y],'-r',linewidth=0.1)
            plt.plot([x_foci,x],[y_foci,y],'-b',linewidth=0.1)

        numpy.vectorize(func)(X,Y)

##########################

def get_f_gamma_equal(e1, e2):
    E1_gamma_equal = scipy.optimize.fsolve(func2, 0, (e1,e2))
    
    E1_gamma_equal = numpy.append(E1_gamma_equal, E1_gamma_equal+math.pi)
    
    E1_gamma_equal = numpy.mod(E1_gamma_equal, 2 * math.pi)
    
    f1_gamma_equal = e1.true_anomaly_from_eccentric_anomaly(E1_gamma_equal)
    
    f2_gamma_equal = f1_gamma_equal + e1.alpha - e2.alpha

    return f1_gamma_equal, f2_gamma_equal

def func3(a2, e1, e2):

    e2.a = a2[0]
    
    print('a2',a2)

    e2.calc()

    f1_gamma_equal, f2_gamma_equal = get_f_gamma_equal(e1, e2)
    
    distance_gamma_equal = numpy.abs(e1.radius_from_true_anomaly(f1_gamma_equal) - e2.radius_from_true_anomaly(f2_gamma_equal))
    
    print('E1_gamma_equal      ',E1_gamma_equal)
    print('distance_gamma_equal',distance_gamma_equal)
    
    
    
    if False:
        plt.figure()
    
        E1 = numpy.linspace(0,2*math.pi,100)
        
        f1 = e1.true_anomaly_from_eccentric_anomaly(E1)
        
        f2 = f1 + e1.alpha - e2.alpha
        
        rho1 = e1.tangent_angle_from_true_anomaly(f1)
        
        rho2 = e2.tangent_angle_from_true_anomaly(f2)
        
        plt.plot(E1/math.pi,rho1/math.pi,'-o')
        plt.plot(E1/math.pi,rho2/math.pi,'-o')
        for E1 in E1_rho_equal:
            plt.plot([E1/math.pi,E1/math.pi],[0,1])
    
    if False:
        fig = plt.figure()
    
        E1 = numpy.linspace(0,2*math.pi,100)
        
        f1 = e1.true_anomaly_from_eccentric_anomaly(E1)
        
        f2 = f1 + e1.alpha - e2.alpha
        
        gamma1 = e1.foci_angle_from_true_anomaly(f1)
        
        gamma2 = e2.foci_angle_from_true_anomaly(f2)
    
        tan_gamma1 = e1.tan_foci_angle_from_true_anomaly(f1)
        
        tan_gamma2 = e2.tan_foci_angle_from_true_anomaly(f2)
        
        ax1 = fig.add_subplot(111)
    
        ax1.plot(E1/math.pi, gamma1/math.pi,'-o')
        ax1.plot(E1/math.pi, gamma2/math.pi,'-o')
        
        r1 = e1.radius_from_true_anomaly(f1)
        r2 = e2.radius_from_true_anomaly(f2)
    
        if True:
            for E1 in E1_gamma_equal:
                ax1.plot([E1/math.pi,E1/math.pi],[-1,1])
    
    print(numpy.min(distance_gamma_equal))
    
    return numpy.min(distance_gamma_equal)



def pair_plot(e1, e2, b=False):

    e1.plot()
    e2.plot()
    
    if b:
        f1_gamma_equal, f2_gamma_equal = get_f_gamma_equal(e1, e2)
    
        e1.plot_points_from_true_anomaly(f1_gamma_equal)
        e2.plot_points_from_true_anomaly(f2_gamma_equal)

    plt.axis('equal')

