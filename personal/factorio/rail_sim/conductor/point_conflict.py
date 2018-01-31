import random
import math
import numpy as np

from .window import *
from .edge_window import *

DEBUG = False


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

        yield self.schedule.__class__(self.schedule.route, self.schedule.t_0 + t)
    

    def try_speed_decrease(self, t):
        # reduce speed of edge before point p in order to avoid reserved window of p
        # previous points should not be affected

        route = self.schedule.route
        
        if not route.allow_speed_decrease: return
        
        p = self.w0.point

        i = route.point_index(p)
        if i == 0: return

        s = self.schedule.copy()

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



