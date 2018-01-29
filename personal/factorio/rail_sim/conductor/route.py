import random
import math

from .window import *

"""
for implementing adjustable speed

store:
list of speeds corresponding to edges
start time
"""
class Schedule:
    def __init__(self, route, t_0):
        self.route = route
        self.t_0 = t_0
        self.speed = [self.route.speed] * len(self.route.edges)

    """
    return the entry and exit times for point p
    """
    def point_window(self, p0):

        t_0 = self.t_0

        if self.route.point_first() == p0: return Window(t_0, t_0 + self.route.train_length / self.route.speed)

        for e, s in zip(self.route.edges, self.speed):
            p = e.p1

            t_0 += e.length() / s

            if p == p0: return Window(t_0, t_0 + self.route.train_length / self.route.speed)
        
        raise RuntimeError()


class Route:
    speed_max = 1.2
    speed_min = 0.8
    speed = 1
    
    

    def __init__(self, edges, train_length=1, allow_speed_reduce=True):
        self.edges = edges
        
        self.train_length = train_length

        self.allow_speed_reduce = allow_speed_reduce

        for e in self.edges:
            e.route = self

        self.departures = []

    def point_index(self, p0):
        points = list(self.points())
        for i, p in zip(range(len(points)), points):
            if p == p0:
                return i
        raise RuntimeError()

    def time_to_point(self, p):
        t = 0
        
        if p == self.edges[0].p0:
            return Window(t, t + self.train_length / self.speed)

        for e in self.edges:
            t += e.length() / self.speed
            if e.p1 == p:
                break

        return Window(t, t + self.train_length / self.speed)

    def try_reduce_speed(self, p, t, s, t_d, w):
        # reduce speed of edge before point p in order to avoid reserved window of p
        # previous points should not be affected

        if not self.allow_speed_reduce: return False

        i = self.point_index(p)
        if i == 0: return False


        speed0 = s.speed[i-1]
        dur0 = self.edges[i-1].length() / s.speed[i-1]
        dur1 = dur0 + t_d

        speed1 = self.edges[i-1].length() / dur1
        
        if speed1 < self.speed_min: return False

        #print('reduce speed from {} to {} for edge {}'.format(speed0, speed1, i-1))
        #print('to avoid window {:8.2f} {:8.2f}'.format(w.t_0, w.t_1))

        s.speed[i-1] = speed1

        return True

    def check_point(self, p, t, s):

        w0 = self.time_to_point(p)
        
        t_changed = False

        p.reserved = sorted(p.reserved, key=lambda w: w.t_0)
        
        #print("check_point", p.position)
        if False:
            print('reserved')
            for w in p.reserved:
                print("\t{:8.2f} {:8.2f}".format(w.t_0, w.t_1))

        
        restart_point_check = True
        while restart_point_check:
            restart_point_check = False
            for w in p.reserved:
    
                #W0 = w0 + t
                
                W0 = s.point_window(p)
            
                if W0.t_1 <= w.t_0:
                    return t, t_changed
                
                elif W0.t_0 < w.t_1 - 1e-10:
                    
                    t_d = w.t_1 - W0.t_0
                    
                    if self.try_reduce_speed(p, t, s, t_d, w): 
                        #restart_point_check = True

                        W0 = s.point_window(p)
                        
                        p.check_window(W0)
                        #assert((W0.t_1 <= w.t_0) or (W0.t_0 >= w.t_1))

                        #break
                    else:
                        #print('{} < {}'.format(W0.t_0, w.t_1))
                        #print('t changed ', t, w.t_1 - w0.t_0)
                        t = w.t_1 - w0.t_0
                        t_changed = True
        
        return t, t_changed

    def schedule(self, t):
        

        # find valid time
        
        t_changed = True
        while t_changed:
            
            #print('check points {:8.2f}'.format(t))

            #s = Schedule(self, self.time_to_point(self.point_first()) + t)
            s = Schedule(self, t)
            
            for p in self.points():
                t, t_changed = self.check_point(p, t, s)
                if t_changed: break


        # reserve times in points

        for p in self.points():
            #w = self.time_to_point(p)
            #W = w + t
            
            W = s.point_window(p)

            p.reserve(W)

        self.departures.append(t)

    def point_first(self):
        return self.edges[0].p0

    def points(self):
        yield self.edges[0].p0
        for e in self.edges:
            yield e.p1

    def points_not_first(self):
        for e in self.edges:
            yield e.p1

    def show(self):
        print('route')
        print('\tpoints')
        for p in self.points():
            print('\t\t{:16} {:16}'.format(str(p.position), str(self.time_to_point(p))))
        print('\twindows')
        for w in self.windows:
            print('\t\t{:8.1f} {:8.1f}'.format(w.t_0, w.t_1))
        print('\tdepartures')
        print('\t\t{}'.format(self.departures))

    def throughput(self):
        return len(self.departures) / max(self.departures)

    def plot(self, ax):
    
        X = [self.edges[0].p0.position[0]] + [e.p1.position[0] for e in self.edges]
        Y = [self.edges[0].p0.position[1]] + [e.p1.position[1] for e in self.edges]

        ax.plot(X, Y, '-o')



