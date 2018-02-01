import random
import math
import numpy as np
import matplotlib.pyplot as plt

from .window import *
from .edge_window import *
from .point_conflict import *
from .edge_conflict import *
from .acceleration_event import *


def pythag(a, b, c):
    d = math.sqrt(b**2 - 4 * a * c)

    x0 = (-b + d) / 2 / a
    x1 = (-b - d) / 2 / a

    if (x0 < 0) and (x1 < 0):
        raise RuntimeError()

    if (x0 > 0) and (x1 > 0):
        return min(x0, x1)

    return max(x0, x1)


class State:
    def __init__(self, t, a, v, x):
        self.t = t
        self.a = a
        self.v = v
        self.x = x

    def __str__(self):
        return "t={:8.2f} a={:8.2f} v={:8.2f} x={:8.2f}".format(self.t, self.a, self.v, self.x)

"""
for implementing adjustable speed

store:
list of speeds corresponding to edges
start time
"""
class Schedule:
    def __init__(self, route, t_0, acceleration_events=[], feature0=None):
        self.route = route
        self.t_0 = t_0
                
        # track the current feature we are testing for conflicts
        self.feature0 = feature0 or self.route.point_first()

        #if speed is not None:
        #    self.speed = list(speed)
        #else:
        #    self.speed = [self.route.speed] * len(self.route.edges)

        self.acceleration_events = acceleration_events

    def states(self):
        self.acceleration_events = sorted(self.acceleration_events, key=lambda w: w.t)
        
        state0 = State(self.t_0, 0, self.route.speed, 0)
        yield state0

        for e in self.acceleration_events:
            T = e.t - state0.t
            
            x = state0.x + state0.v * T + 0.5 * state0.a * T**2
            v = state0.v + state0.a * T

            state0 = State(e.t, e.a, v, x)

            yield state0

    def plot(self, ax=None):

        if ax is None:
            fig = plt.figure()
            ax = fig.add_subplot(111)
        
        s0 = None
        for s1 in self.states():

            ax.plot([s1.t], [s1.x], 'o')

            if s0 is None: 
                s0 = s1
                continue
            
            t = np.linspace(s0.t, s1.t)

            x = s0.x + s0.v * (t - s0.t) + 0.5 * s0.a * (t - s0.t)**2
            
            #print("plotting", t, x)
            
            ax.plot(t, x)

            s0 = s1

        for p in self.route.points():
            state = self.state_at_position(self.route.point_distance(p))
            
            ax.plot(state.t, state.x, 's')

    def state_before_time(self, t):
        state0 = None
        for state in self.states():
            if state.t > t: break
            state0 = state
        return state0

    def state_before_position(self, x):
        state0 = None
        for state in self.states():
            if state.x > x: break
            state0 = state
        return state0

    def state_at_time(self, t):
        #print("state_at_time", t)

        state0 = self.state_before_time(t)
                
        T = t - state0.t
        X = state0.v * T + 0.5 * state0.a * T**2
        V = state0.a * T

        return State(t, state0.a, state0.v + V, state0.x + X)

    def state_at_position(self, x):
        if x == 0: return next(self.states())

        state0 = self.state_before_position(x)
        
        # p0 is the last position before the desired position
       
        x0 = state0.x
        x1 = x
        
        if abs(x1 - x0) < 1e-10:
            return state0

        d = x - state0.x
        
        if state0.a == 0:
            # d = v * t 
            # t = d / v
            T = d / state0.v
        else:
            # d = v * t + 0.5 * a * t**2
            T = pythag(0.5 * state0.a, state0.v, -d)
        
        if Debug.level >= 20:
            print("state at position")
            print("x0 = {:8.2f}".format(state0.x))
            print("x1 = {:8.2f}".format(x))
            print("T =  {:8.2f}".format(T))
            print("x0 == x1 = {}".format(x0==x1))
            #print("state " + str(p0))
            #print("time to position", x, p0.t + t)
       
        V = state0.a * T

        state1 = State(state0.t + T, state0.a, state0.v + V, x)

        return state1


    def copy(self):
        return Schedule(self.route, self.t_0, self.acceleration_events)

    def point_window_start_position(self, p):
        """
        the position of the front of the train when it enters a point
        """
        pass

    def point_window_end_position(self, p):
        """
        the position of the front of the train when it exits a point
        """
        pass

    def time_to_position(self, x):
        """
        time at which the front of the train reach a position along the route
        """
        if x == 0: return self.t_0

        state0 = self.state_before_position(x)

        # p0 is the last position before the desired position
        
        d = x - p0.x

        if p0.a == 0:
            # d = v * t 
            # t = d / v
            t = d / p0.v
        else:
            # d = v * t + 0.5 * a * t**2
            t = pythag(0.5 * p0.a, p0.v, -d)
        
        print("state " + str(p0))
        print("t_0", self.t_0)
        print("time to position", x, p0.t + t)
        
        return p0.t + t

    """
    return the entry and exit times for point p
    """
    def point_window(self, p0):
        
        d = self.route.point_distance(p0)
        #t0 = self.time_to_position(d)
        #t1 = self.time_to_position(d + self.route.train_length)
        state0 = self.state_at_position(d)
        state1 = self.state_at_position(d + self.route.train_length)
        t0 = state0.t
        t1 = state1.t
        return Window(self.route, p0, t0, t1)

        t_0 = self.t_0
        
        l = self.route.train_length

        e = self.route.edges[0]
        
        if self.route.point_first() == p0:
            T = l / self.speed[0]
            return Window(self.route, p0, t_0, t_0 + T)

        for e, s in zip(self.route.edges, self.speed):
            p = e.p1

            t_0 += e.length() / s
            
            e1 = self.route.edge_next(e)

            if p == p0:
                if e1 is None:
                    T = l / self.route.speed
                else:
                    T = l / self.edge_speed(e1)
                
                return Window(self.route, p0, t_0, t_0 + T)
        
        raise RuntimeError()

    def edge_speed(self, edge):
        for e, s in zip(self.route.edges, self.speed):
            if e == edge:
                return s

    def edge_window(self, e):

        w0 = self.point_window(e.p0)
        w1 = self.point_window(e.p1)

        return EdgeWindow(e, self, w0.t_0, w1.t_0, w0.t_1, w1.t_1)

    def cleanup_points(self):
        """
        when a route creates a schedule, we know that when the route creates the next schedule
        the second schedule will have values of t_0 for each point greater than those for the first schedule
        """
        
        t_0 = self.point_window(self.route.point_first()).t_0
        
        for p in self.route.points():

            #w = self.point_window(p)
            
            #p.t_0[self.route] = w.t_0

            w = self.route.time_to_point(p)

            p.t_0[self.route] = t_0 + w.t_0

            p.cleanup()

    def width(self):
        t0 = self.point_window(self.route.point_first()).t_0
        t1 = self.point_window(self.route.point_last()).t_1
        return t1 - t0

    def find_conflict(self):
        for f in self.route.features_starting_with(self.feature0):
        #for f in self.route.points():

            c = f.find_conflict_visit(self)

            if c is not None:
                return c

            self.feature0 = f


    def find_conflict_point(self, p):
        
        W0 = self.point_window(p)

        for w in p.reserved:

            if W0.t_1 < w.t_0 + 1e-10:
                continue

            if W0.t_0 > w.t_1 - 1e-10:
                continue
            
            c = PointWindowConflict(self, W0, w)
            return c

    def find_conflict_edge(self, e):

        w0 = self.edge_window(e)

        #def check_window(self, w0):
        
        for w in e.windows():
            if w.schedule == w0.schedule:
                continue

            assert(w.edge == w0.edge)
            
            if w0.t_0 < w.t_0:
                # the front of this train enters first

                # w1, w2 = w0, w
                
                if w0.t_0_back > w.t_0 + 1e-10:
                    # the back of this train enters after 
                    # the front of the refernce train

                    t = w.t_0_back - w0.t_0
                    
                    print("edge conflict at entrance")

                    #return EdgeWindowConflictEntrance(self, w0, t)
                    raise RuntimeError()

                if w0.t_1_back > w.t_1 + 1e-10:
                    # the back of this train exits after
                    # the front of the reference train exits

                    t = w.t_1_back - w0.t_1

                    t = max(t, 0.1)

                    if Debug.level >= 10:
                        print("edge conflict at exit. this train overtaken.")

                    return EdgeWindowConflictExit(self, w0, t)

            else:
                # the front of the reference train enters first

                if w.t_0_back > w0.t_0 + 1e-10:
                    # the back of the reference train enters after
                    # the front of this train

                    t = w.t_0_back - w0.t_0
    
                    print("edge conflict at entrance")

                    #return EdgeWindowConflictEntrance(self, w0, t)
                    raise RuntimeError()

                if w.t_1_back > w0.t_1 + 1e-10:

                    t = w.t_1_back - w0.t_1
                    
                    t = max(t, 0.1)

                    if Debug.level >= 10:
                        print("edge conflict at exit. reference train overtaken. t = {:12.2e}".format(t))

                    return EdgeWindowConflictExit(self, w0, t)

            
            # w1 enters first so change w1 to the back of the train
            
            #W1 = w1 + w1.schedule.route.train_length /  w1.schedule.edge_speed(w1.edge)

            #W2 = w2 + w2.schedule.route.train_length /  w2.schedule.edge_speed(w2.edge)

            """
                    print('conflict at entrance case {} t {:16.4e} schedule t_0: {:12.4f}'.format(case, t, self.t_0))
                    print('\tw1 {:12.4f} {:12.4f}'.format(w1.t_0, w1.t_1))
                    print('\tW1 {:12.4f} {:12.4f}'.format(W1.t_0, W1.t_1))
                    print('\tw2 {:12.4f} {:12.4f}'.format(w2.t_0, w2.t_1))
                    print('\tW2 {:12.4f} {:12.4f}'.format(W2.t_0, W2.t_1))
            """

    def t_1(self):
        return self.point_window(self.route.point_last()).t_0

    def reserve(self):
        for p in self.route.points():
            W = self.point_window(p)
            p.reserve(W)
        
        for e in self.route.edges:
            W = self.edge_window(e)
            e.reserve(W)
    
    def coordinates_at_time(self, t):
        
        if t <= self.t_0: return
        if t >= self.t_1(): return

        state = self.state_at_time(t)
        x = state.x

        for p1 in self.route.points():
            if x < self.route.point_distance(p1): break
        
        p0 = self.route.point_prev(p1)
        
        x0 = self.route.point_distance(p0)
        x1 = self.route.point_distance(p1)

        v = p1.position - p0.position
        
        c = p0.position + v * (x - x0) / (x1 - x0)

        return np.reshape(c, (2,1))


