import random
import math
import numpy as np

from .window import *
from .edge_window import *
from .schedule import *

DEBUG = False
       

def schedule(s):

    C = s.find_conflict()
    
    #if c is None:
    #    return s
    
    for c in C:
        for s1 in c.fixes():
            if s1 is None: continue

            try:
                s2 = schedule(s1)
                if s2 is not None:
                    return s2
            except RecursionError:
                print(crayons.yellow('resursion exception caught'))
                #s1.plot()
                pass
            
        
        return None
    
    return s

class Route:
    speed_max = 1.2
    speed = 1
    count_speed_decrease = 0
    
    def __init__(self, edges, train_length=1, allow_speed_decrease=True, speed_min=0.5):
        self.edges = edges
        
        self.train_length = train_length

        self.allow_speed_decrease = allow_speed_decrease
        self.speed_min = speed_min

        for e in self.edges:
            e.routes.append(self)

        self.departures = []
        self.schedules = []

        # first possible t_0 for first point
        #self.t_0 = 0


    def point_index(self, p0):
        points = list(self.points())
        for i, p in zip(range(len(points)), points):
            if p == p0:
                return i
        raise RuntimeError()

    def time_to_point(self, p):
        t = 0
        
        if p == self.edges[0].p0:
            return Window(p, t, t + self.train_length / self.speed, None, self.edges[0])

        for e in self.edges:
            t += e.length() / self.speed
            if e.p1 == p:
                return Window(p, t, t + self.train_length / self.speed, e, self.edge_next(e))

    def try_reduce_speed(self, p, t, s, t_d, w):
        # reduce speed of edge before point p in order to avoid reserved window of p
        # previous points should not be affected

        if not self.allow_speed_decrease: return False

        i = self.point_index(p)
        if i == 0: return False


        speed0 = s.speed[i-1]
        dur0 = self.edges[i-1].length() / s.speed[i-1]
        dur1 = dur0 + t_d

        speed1 = self.edges[i-1].length() / dur1
        
        if speed1 < self.speed_min: return False

        #print('reduce speed from {} to {} for edge {}'.format(speed0, speed1, i-1))

        Route.count_speed_decrease += 1

        #print('to avoid window {:8.2f} {:8.2f}'.format(w.t_0, w.t_1))

        s.speed[i-1] = speed1

        e = self.edges[i-1]
        w = s.edge_window(e)

        if not e.check_window(w):
            s.speed[i-1] = speed0
            return False

        return True

    def check_point(self, p, t, s):
        
        p.reserved = sorted(p.reserved, key=lambda w: w.t_0)
        
        W0 = s.point_window(p)
        
        if DEBUG:
            print('route points')
            for p0 in self.points():
                print("{} t_0_set = {:5} min_t_0 = {:8.2f} t_0 = {:8.2f}".format(self.point_index(p0), str(p0.t_0_set()), p0.min_t_0(), p0.t_0[self] if self in p0.t_0 else -1))

            print("t =                  {}".format(t))
            print("check_point {}".format(self.point_index(p)))
            print("\tt_0_set =            {}".format(p.t_0_set()))
            print("\tmin_t_0 =            {}".format(p.min_t_0()))
            print("\tW0.t_0 =             {}".format(W0.t_0))
            if self in p.t_0:
                print("\tt_0 for this route = {}".format(p.t_0[self]))

            print('reserved')
            for w in p.reserved:
                print("\t{:8.2f} {:8.2f}".format(w.t_0, w.t_1))

        if W0.t_0 < p.min_t_0():
            raise RuntimeError()

        for w in p.reserved:

            #W0 = w0 + t
            
            W0 = s.point_window(p)
        
            if W0.t_1 <= w.t_0:

                #print("W0.t_1 <= w.t_0")
                #print("{} <= {}".format(W0.t_1, w.t_0))

                p.check_window(W0)

                return t, False
            
            elif W0.t_0 < w.t_1 - 1e-10:
                
                t_d = w.t_1 - W0.t_0
                
                if self.try_reduce_speed(p, t, s, t_d, w): 

                    W0 = s.point_window(p)

                    if DEBUG:
                        print("speed decrease")
                        print("window       {:8.2f} {:8.2f}".format(W0.t_0, W0.t_1))
                        print("avoid window {:8.2f} {:8.2f}".format(w.t_0, w.t_1))
                    
                    #p.check_window(W0)

                    #break
                else:
                    #print('{} < {}'.format(W0.t_0, w.t_1))
                    #print('t changed ', t, w.t_1 - w0.t_0)

                    w0 = self.time_to_point(p)
                    t = w.t_1 - w0.t_0
                    return t, True
        
        return t, False

    def features(self):
        yield self.point_first()
        for e in self.edges:
            yield e
            yield e.p1

    def features_starting_with(self, feature0):
        features = iter(self.features())
        
        for f in features:
            if f == feature0:
                yield f
                break

        for f in features:
            yield f

    def schedule(self, t):

        t = max(t, self.point_first().min_t_0())
        
        # find valid time
        
        #self.t_0 = self.point_first().first_possible_t_0(self.t_0, self.train_length / self.speed)
        #t = self.t_0
        #print('schedule t = {:8.2f}'.format(t))
    

        if True:

            # try new method
            s = schedule(Schedule(self, t))
            if s is not None:
                #print("new method success")
                pass
            else:
                print("new method failure!!!!!!")
        
        else:        

            t_changed = True
            while t_changed:
            
                #print('check points {:8.2f}'.format(t))

                s = Schedule(self, t)
            
                for p in self.points():
                    t, t_changed = self.check_point(p, t, s)
                    if t_changed: break
        
        if s is None: raise RuntimeError()

        #self.t_0 = t
        #self.point_first().t_0[self] = t

        #self.point_first().cleanup()

        s.cleanup_points()

        # reserve times in points

        s.reserve()

        self.departures.append(t)
        self.schedules.append(s)

    def point_first(self):
        return self.edges[0].p0

    def point_last(self):
        return self.edges[-1].p1

    def points(self):
        yield self.edges[0].p0
        for e in self.edges:
            yield e.p1

    def points_up_to(self, p):
        yield self.edges[0].p0
        if self.edges[0].p0 == p: return

        for e in self.edges:
            yield e.p1
            if e.p1 == p: return

    def points_not_first(self):
        for e in self.edges:
            yield e.p1

    def show(self):

        widths = [s.width() for s in self.schedules]

        print('route')
    
        if False:
            print('\tpoints')
            for p in self.points():
                print('\t\t{:16}'.format(str(p.position)))

            print('\twindows')
            for w in self.windows:
                print('\t\t{:8.1f} {:8.1f}'.format(w.t_0, w.t_1))

            print('\tdepartures')
            print('\t\t{}'.format(self.departures))

        print('\tschedule width average {:8.2f} std {:8.2f}'.format(np.average(widths), np.std(widths)))

    def throughput(self):

        t_1 = [s.point_window(self.point_last()).t_1 for s in self.schedules]
        
        #return len(self.departures) / max(self.departures)
        return len(self.departures) / max(t_1)

    def plot(self, ax):
    
        X = [self.edges[0].p0.position[0]] + [e.p1.position[0] for e in self.edges]
        Y = [self.edges[0].p0.position[1]] + [e.p1.position[1] for e in self.edges]

        ax.plot(X, Y, '-o')

    def edge_next(self, e0):
        
        edges = iter(self.edges)

        for e in edges:
            if e == e0:
                break
        
        try:
            return next(edges)
        except StopIteration:
            return None
        





