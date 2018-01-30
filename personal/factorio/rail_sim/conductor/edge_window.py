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
    def __init__(self, edge, schedule, t_0, t_1):
        self.edge = edge
        self.schedule = schedule
        self.t_0 = t_0
        self.t_1 = t_1

    def __add__(self, t):
        return EdgeWindow(self.edge, self.t_0 + t, self.t_1 + t)


