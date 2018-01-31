import random
import math
import numpy as np

from .window import *
from .edge_window import *

DEBUG = False

        
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




