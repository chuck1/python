import copy
import random
import math
import numpy as np
import matplotlib.pyplot as plt

from .event import *

class Point:
    def __init__(self, position):
        self.position = position
        
        self.edges = []

        self.reserved = []
        self.reserved0 = []

        # key is Route
        self.t_0 = {}
        
    def occupancy(self):
    
        events = []

        for w in self.reserved0:
            events.append(Event(w.t_0, 1))
            events.append(Event(w.t_1, -1))

        events = sorted(events, key=lambda e: e.t)

        x = [0]
        y = [0]

        for e in events:
            x.append(e.t)
            y.append(y[-1])

            x.append(e.t)
            y.append(y[-1] + e.y)

        return x, y

    def check_window(self, w1):
        
        self.reserved0 = sorted(self.reserved0, key=lambda w: w.t_0)
        
        for w in self.reserved0:
            if w1.t_1 <= w.t_0 + 1e-10:
                continue

            if w1.t_0 >= w.t_1 - 1e-10:
                continue
            
            print(w1.t_1 - w.t_0)
            print(w.t_1 - w1.t_0)

            print('trying to reserve window  {:8.2f} {:8.2f}'.format(w1.t_0, w1.t_1))
            print('but conflicts with window {:8.2f} {:8.2f}'.format(w.t_0, w.t_1))
            raise RuntimeError()

    def check(self):
        #print('check')

        self.reserved0 = sorted(self.reserved0, key=lambda w: w.t_0)
        
        #for w in self.reserved0:
        #    print('[{:8.2f} {:8.2f}]'.format(w.t_0, w.t_1))

        for w0 in self.reserved0:
            for w1 in self.reserved0:
                if w0 == w1: continue
                if w1.t_0 < w0.t_0: continue
                
                #print('[{:8.2f} {:8.2f}] [{:8.2f} {:8.2f}]'.format(w0.t_0, w0.t_1, w1.t_0, w1.t_1))

                if w0.t_1 <= w1.t_0 + 1e-10:
                    #print('w0.t_1 <= w1.t_0')
                    continue
                
                if w0.t_0 >= w1.t_1 - 1e-10:
                    #print('w0.t_0 >= w1.t_1')
                    continue

                print(w1.t_1 - w0.t_0)
                print(w0.t_1 - w1.t_0)

                #print('trying to reserve window  {:8.2f} {:8.2f}'.format(w1.t_0, w1.t_1))
                #print('but conflicts with window {:8.2f} {:8.2f}'.format(w.t_0, w.t_1))
                
                raise RuntimeError()

    def min_t_0(self):

        for route in self.routes():
            for p in route.points_up_to(self):
                if not p.t_0_set():
                    return 0

        for route in self.routes():
            if route not in self.t_0:
                return 0

        #T = self.t_0.values()
        
        #if not T:
        #    return 0
        
        #return min(T)
        
        T = []
        for route in self.routes():
            p0 = route.point_first()
            if p0 == self:
                T.append(self.t_0[route])
            else:
                T.append(p0.min_t_0())

        return min(T)

    def t_0_set(self):
        for route in self.routes():
            if route not in self.t_0:
                return False
        return True

    def routes(self):
        ret = []
        for e in self.edges:
            for route in e.routes:
                if route not in ret:
                    ret.append(route)
        return ret

    def cleanup(self):
        t_0 = self.min_t_0()
        i = 0

        self.reserved = sorted(self.reserved, key=lambda w: w.t_0)

        for w in self.reserved:

            if w.t_1 <= t_0 - 10:
                i += 1
            else:
                break

        self.reserved = self.reserved[i:]

    def reserve(self, w):

        self.check_window(w)
        self.reserved.append(w)#copy.deepcopy(w))
        self.reserved0.append(w)#copy.deepcopy(w))

    def find_conflict_visit(self, s):
        yield from s.find_conflict_point(self)



