import random
import math
import numpy as np

from .window import *
from .edge_window import *

DEBUG = False

"""
for implementing adjustable speed

store:
list of speeds corresponding to edges
start time
"""
class Schedule:
    def __init__(self, route, t_0, speed=None):
        self.route = route
        self.t_0 = t_0
        
        # track the current feature we are testing for conflicts
        self.feature0 = self.route.point_first()

        if speed is not None:
            self.speed = list(speed)
        else:
            self.speed = [self.route.speed] * len(self.route.edges)

    """
    return the entry and exit times for point p
    """
    def point_window(self, p0):

        t_0 = self.t_0

        if self.route.point_first() == p0:
            return Window(p0, t_0, t_0 + self.route.train_length / self.route.speed, None, self.route.edges[0])

        for e, s in zip(self.route.edges, self.speed):
            p = e.p1

            t_0 += e.length() / s

            if p == p0:
                return Window(p0, t_0, t_0 + self.route.train_length / self.route.speed, e, self.route.edge_next(e))
        
        raise RuntimeError()

    def edge_speed(self, edge):
        for e, s in zip(self.route.edges, self.speed):
            if e == edge:
                return s

    def edge_window(self, e):

        w0 = self.point_window(e.p0)
        w1 = self.point_window(e.p1)

        return EdgeWindow(e, self, w0.t_0, w1.t_0)

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
            yield from f.find_conflict_visit(self)


    def find_conflict_point(self, p):
        
        W0 = self.point_window(p)

        for w in p.reserved:

            if W0.t_1 < w.t_0 + 1e-10:
                continue

            if W0.t_0 > w.t_1 - 1e-10:
                continue

            yield PointWindowConflict(self, W0, w)

    def find_conflict_edge(self, e):

        w0 = self.edge_window(e)

        #def check_window(self, w0):
        
        for w in e.windows():
            if w.schedule == w0.schedule:
                continue

            assert(w.edge == w0.edge)
            
            if w0.t_0 < w.t_0:
                w1, w2 = w0, w
                case = 1
            else:
                w1, w2 = w, w0
                case = 2
            
            assert(w1.t_0 < w2.t_0)
            
            # w1 enters first so change w1 to the back of the train
            
            W1 = w1 + w1.schedule.route.train_length /  w1.schedule.edge_speed(w1.edge)

            W2 = w2 + w2.schedule.route.train_length /  w2.schedule.edge_speed(w2.edge)

            if W1.t_0 > w2.t_0 + 1e-10:
                
                if case == 1:
                    t = W2.t_0 - w1.t_0
                elif case == 2:
                    t = W1.t_0 - w2.t_0

                if DEBUG:                
                    print('conflict at entrance case {} t {:16.4e} schedule t_0: {:12.4f}'.format(case, t, self.t_0))
                    print('\tw1 {:12.4f} {:12.4f}'.format(w1.t_0, w1.t_1))
                    print('\tW1 {:12.4f} {:12.4f}'.format(W1.t_0, W1.t_1))
                    print('\tw2 {:12.4f} {:12.4f}'.format(w2.t_0, w2.t_1))
                    print('\tW2 {:12.4f} {:12.4f}'.format(W2.t_0, W2.t_1))

                yield EdgeWindowConflictEntrance(self, w0, t)

            if W1.t_1 > w2.t_1 + 1e-10:
                
                if case == 1:
                    t = W2.t_1 - w1.t_1
                elif case == 2:
                    t = W1.t_1 - w2.t_1

                if DEBUG:            
                    print('conflict at exit     case {} t {:16.4e} schedule t_0: {:12.4f}'.format(case, t, self.t_0))
                    print('\tw1 {:12.4f} {:12.4f}'.format(w1.t_0, w1.t_1))
                    print('\tW1 {:12.4f} {:12.4f}'.format(W1.t_0, W1.t_1))
                    print('\tw2 {:12.4f} {:12.4f}'.format(w2.t_0, w2.t_1))
                    print('\tW2 {:12.4f} {:12.4f}'.format(W2.t_0, W2.t_1))

                yield EdgeWindowConflictExit(self, w0, t)
        
class EdgeWindowConflictEntrance:
    def __init__(self, schedule, w0, t):
        self.schedule = schedule
        self.w0 = w0
        self.t = t

    def fixes(self):

        #s = self.try_speed_decrease(t)
        #if s is not None: yield s

        #yield self.try_speed_decrease(self.t)

        yield Schedule(self.schedule.route, self.schedule.t_0 + self.t)

class EdgeWindowConflictExit:
    def __init__(self, schedule, w0, t):
        self.schedule = schedule
        self.w0 = w0
        self.t = t

    def fixes(self):

        #s = self.try_speed_decrease(t)
        #if s is not None: yield s

        #yield self.try_speed_decrease(self.t)
        self.try_speed_decrease(self.t)

        yield Schedule(self.schedule.route, self.schedule.t_0 + self.t)

    def try_speed_decrease(self, t):
        # reduce speed of edge before point p in order to avoid reserved window of p
        # previous points should not be affected

        route = self.schedule.route
        
        if not route.allow_speed_decrease: return
        
        e = self.w0.edge
        
        i = route.edges.index(e)
        if i == 0: return

        s = Schedule(self.schedule.route, self.schedule.t_0, self.schedule.speed)

        l = e.length()

        speed0 = s.speed[i]
        T0 = l / speed0
        T1 = T0 + t
        speed1 = l / T1
        
        if speed1 < route.speed_min: return

        #print('reduce speed from {} to {} for edge {}'.format(speed0, speed1, i-1))

        #Route.count_speed_decrease += 1

        #print('to avoid window {:8.2f} {:8.2f}'.format(w.t_0, w.t_1))

        s.speed[i] = speed1

        w = self.schedule.edge_window(e)
        if not e.check_window(w):
            #print('speed decrease fix for edge conflict causes another conflict')
            pass
        else:
            print('speed decrease fix for edge conflict SUCCESS')

        #    s.speed[i-1] = speed0
        #    return False

        return s


"""
window w0 of scheulde conflicts with reserved window w1
"""
class PointWindowConflict:
    def __init__(self, schedule, w0, w1):
        self.schedule = schedule
        self.w0 = w0
        self.w1 = w1

    """
    generator of Schedules that should not produce this same conflict
    """
    def fixes(self):

        t = self.w1.t_1 - self.w0.t_0

        #s = self.try_speed_decrease(t)
        #if s is not None: yield s

        yield self.try_speed_decrease(t)

        yield Schedule(self.schedule.route, self.schedule.t_0 + t)
    

    def try_speed_decrease(self, t):
        # reduce speed of edge before point p in order to avoid reserved window of p
        # previous points should not be affected

        route = self.schedule.route
        
        if not route.allow_speed_decrease: return
        
        p = self.w0.point

        i = route.point_index(p)
        if i == 0: return

        s = Schedule(self.schedule.route, self.schedule.t_0, self.schedule.speed)

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

        return s



