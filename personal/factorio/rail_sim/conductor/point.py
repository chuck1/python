import random
import math
import numpy as np
import matplotlib.pyplot as plt


class Point:
    def __init__(self, position):
        self.position = position
        
        self.edges = []

        self.reserved = []

    def check_window(self, w1):

        for w in self.reserved:
            if w1.t_1 <= w.t_0:
                continue

            if w1.t_0 >= w.t_1 - 1e10:
                continue
            
            print(w1.t_1 - w.t_0)
            print(w.t_1 - w1.t_0)

            print('trying to reserve window  {:8.2f} {:8.2f}'.format(w1.t_0, w1.t_1))
            print('but conflicts with window {:8.2f} {:8.2f}'.format(w.t_0, w.t_1))
            raise RuntimeError()

    def reserve(self, w):
        self.check_window(w)
        self.reserved.append(w)

        #for e in self.edges:
        #    W = e.route.time_to_point(self)
        #    e.route.windows.append(Window(t_0 - W.t_1, t_1 - W.t_0))


