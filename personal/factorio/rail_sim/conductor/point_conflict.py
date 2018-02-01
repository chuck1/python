import random
import math
import numpy as np
import matplotlib.pyplot as plt
import crayons

from .window import *
from .edge_window import *
from .acceleration_event import *
from .debug import *

def acc_dec(T, X, v0, v1):

    a = -(v1 - v0)**2 / (X - v1 * T)

    T1 = T - 2 * (v1 - v0) / a
    T0 = (T - T1) / 2

    X1 = v1 * T1
    X0 = (X - X1) / 2
 
    return a, T0, T1

def acc_dec2(T, X, v0):

    a = (X - v0 * T) / T**2 * 4

    v1 = T * a / 2 + v0

    return a, v1

   
    

"""
window w0 of scheulde conflicts with reserved window w1
"""
class PointWindowConflict:
    def __init__(self, schedule, w0, w1):
        self.schedule = schedule
        self.w0 = w0
        self.w1 = w1

    def __str__(self):
        return "Point conflict [{:8.2f} {:8.2f}] [{:8.2f} {:8.2f}]".format(
                self.w0.t_0,
                self.w0.t_1,
                self.w1.t_0,
                self.w1.t_1,
                )

    """
    generator of Schedules that should not produce this same conflict
    """
    def fixes(self):

        t = self.w1.t_1 - self.w0.t_0

        if Debug.level >= 10:
            print("fix point conflict with point ({:8.2f} {:8.2f}) move start by {:8.2f} to {:8.2f}".format(
                self.w0.point.position[0],
                self.w0.point.position[1],
                t, self.schedule.t_0 + t))

        #s = self.try_speed_decrease(t)
        #if s is not None: yield s

        yield self.try_speed_decrease(t)

        yield self.schedule.__class__(self.schedule.route, self.schedule.t_0 + t)
    

    def try_speed_decrease(self, t):
        # reduce speed of edge before point p in order to avoid reserved window of p
        # previous points should not be affected

        route = self.schedule.route

        if not route.allow_speed_decrease: return

        # conflict point
        p = self.w0.point
        
        # conflict point index
        i = route.point_index(p)

        if i == 0: return
        
        # edge before conflict point
        e = route.edges[i-1]
        
        # previous point
        p0 = e.p0
        
        # need to move w0.t_0 forward by t
        # create an acceleration event after the train leaves the previous point

        w0 = self.schedule.point_window(p0)

        # make sure there are no acceleration beyond that time
        events = [e for e in self.schedule.acceleration_events if e.t >= w0.t_1]
        if events:
            if Debug.level >= 10:
                print(crayons.yellow("acceleration event after point where we want to insert acceleration event. abort speed decrease"))
            return
        
        # state when the train exits the previous point
        state0 = self.schedule.state_at_time(w0.t_1)
        
        # pretty sure this should be true
        # but since I can instantaneously change acceleration, this shouldnt matter
        # given that I made sure there are no other acceleration events after w0.t_1
        assert(state0.a == 0)
        
        x0 = route.point_distance(p0) + route.train_length

        if abs(x0 - state0.x) > 1e-10:
            print("w0.t_1 = {:8.2f}".format(w0.t_1))
            print(x0 - state0.x)
            print(x0)
            print(state0.x)

            self.schedule.plot()
            plt.show()

            raise RuntimeError()
        
        # we will acceleration (or decelerate) from when the train exits the previous point to when
        # the train enters the conflict point

        x1 = route.point_distance(p)
             
        X = x1 - x0

        t0 = w0.t_1
        t1 = self.w1.t_1
        
        T = t1 - t0
        
        if Debug.level >= 10:
            print("point 0 is at   {:8.2f}".format(route.point_distance(p0)))
            print("point 1 is at   {:8.2f}".format(route.point_distance(p)))
            print("train length is {:8.2f}".format(route.train_length))

        if abs(X) < 1e-10: return

        if Debug.level >= 10:
            print("accelerate from to")
            print("\tt={:8.2f} x={:8.2f}".format(t0, x0))
            print("\tt={:8.2f} x={:8.2f}".format(t1, x1))
        
        if X==0:
            self.schedule.plot()
            plt.show()
        
        def acc_dec_events(v1):
            a, T0, T1 = acc_dec(T, X, state0.v, v1)
            
            if T0 < 0: return

            if Debug.level >= 10:
                print()
                print("need acceleration of", a)
                print("T  = {:8.2f}".format(T))
                print("v1 = {:8.2f}".format(v1))
                print("T0 = {:8.2f}".format(T0))
                print("T1 = {:8.2f}".format(T1))
            
            assert(abs((2 * T0 + T1) - T) < 1e-10)
            
            if t1 <= (t0 + T0 + T1):
                print("need acceleration of", a)
                print("T  = {:8.2f}".format(T))
                print("v1 = {:8.2f}".format(v1))
                print("T0 = {:8.2f}".format(T0))
                print("T1 = {:8.2f}".format(T1))
                raise RuntimeError()

            return [
                    AccelerationEvent(t0, a),
                    AccelerationEvent(t0 + T0, 0),
                    AccelerationEvent(t0 + T0 + T1, -a),
                    AccelerationEvent(t1, 0),
                    ]

        def acc_dec2_events():
            a, v1 = acc_dec2(T, X, state0.v)

            if v1 < route.speed_min:
                return
            
            return [
                    AccelerationEvent(t0, a),
                    AccelerationEvent(t0 + T / 2, -a),
                    AccelerationEvent(t1, 0),
                    ]

        if abs(state0.v - route.speed_min) < 1e-10: return
        
        events = acc_dec2_events()
        
        if events is None:

            events = acc_dec_events(route.speed_min)
        
            if events is None:
                return
                raise RuntimeError()
        

        #a = (X - state0.v * T) / (0.5 * T**2)

        if Debug.level >= 20:
            print("need acceleration of", a)
            print("T  = {:8.2f}".format(T))
            print("v1 = {:8.2f}".format(v1))
            #print("T0 = {:8.2f}".format(T0))
            #print("T1 = {:8.2f}".format(T1))
       
        #v0 = state0.v
        #V = a * T
        #v1 = v0 + V

        #if v1 < 0:
        #    print("negative speed", v1)
        #    raise RuntimeError()
        
        #assert(abs(t - T) < 1e-10)

        s = self.schedule.copy()

        s.acceleration_events += events
        
        w = s.point_window(p)
        
        if self.w1.check_conflict(w):
            Debug.level = 100
            self.w1.check_conflict(w)

            fig = plt.figure()
            ax = fig.add_subplot(111)
            
            self.schedule.plot(ax)

            w.plot(ax, route.point_distance(p))
            self.w1.plot(ax, route.point_distance(p))

            plt.show()

            raise RuntimeError()


        """


        l = route.edges[i-1].length()

        speed0 = s.speed[i-1]
        T0 = l / speed0
        T1 = T0 + t
        speed1 = l / T1
        
        if speed1 < route.speed_min: return

        #print('reduce speed from {} to {} for edge {}'.format(speed0, speed1, i-1))

        #Route.count_speed_decrease += 1

        #print('to avoid window {:8.2f} {:8.2f}'.format(w.t_0, w.t_1))

        s.speed[i-1] = speed1
        

        e = route.edges[i-1]
        w = s.edge_window(e)
        
        if not e.check_window(w):
            #s.speed[i-1] = speed0
            return
        """

        return s



