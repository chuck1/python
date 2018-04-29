import functools
import sys
import random
import math
import numpy as np
import matplotlib.pyplot as plt
import argparse

"""
t_0 - time at which the front of a train enters the edge
t_1 - time at which the front of a train exits the edge
"""
class EdgeWindow:
    def __init__(self, edge, schedule, t_0, t_1, t_0_back, t_1_back):
        self.edge = edge
        self.schedule = schedule
        self.t_0 = t_0
        self.t_1 = t_1
        self.t_0_back = t_0_back
        self.t_1_back = t_1_back

    def __add__(self, t):
        return EdgeWindow(self.edge, self.schedule, self.t_0 + t, self.t_1 + t)


