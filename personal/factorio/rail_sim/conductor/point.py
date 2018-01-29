import random
import math
import numpy as np
import matplotlib.pyplot as plt


class Point:
    def __init__(self, position):
        self.position = position
        
        self.edges = []

        self.reserved = []
        self.reserved0 = []

        self.t_0 = {}

    def check_window(self, w1):
        
        self.reserved0 = sorted(self.reserved0, key=lambda w: w.t_0)

        for w in self.reserved0:
            if w1.t_1 <= w.t_0:
                continue

            if w1.t_0 >= w.t_1 - 1e10:
                continue
            
            print(w1.t_1 - w.t_0)
            print(w.t_1 - w1.t_0)

            print('trying to reserve window  {:8.2f} {:8.2f}'.format(w1.t_0, w1.t_1))
            print('but conflicts with window {:8.2f} {:8.2f}'.format(w.t_0, w.t_1))
            raise RuntimeError()

    def min_t_0(self):
        T = self.t_0.values()
        if not T:
            return 0
        return min(T)

    def routes(self):
        ret = []
        for e in self.edges:
            if e.route not in ret:
                ret.append(e.route)
        return ret

    def cleanup(self):
        t_0 = self.min_t_0()
        i = 0

        self.reserved = sorted(self.reserved, key=lambda w: w.t_0)

        for w in self.reserved:

            if w.t_1 <= t_0:
                i += 1
            else:
                break

        self.reserved = self.reserved[i:]

    def reserve(self, w):
        self.check_window(w)
        self.reserved.append(w)
        self.reserved0.append(w)





