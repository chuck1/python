import math
import matplotlib.pyplot as plt
import numpy as np
from cycler import cycler

n = 100

def color_cycle(colors):
    while True:
        for c in colors:
            yield c

cc = color_cycle(['r', 'g', 'b', 'y', 'c', 'm'])

class Line:
    def __init__(self):
        self.color = next(cc)

    def plot(self):
        plt.plot(self.x, self.y, color = next(cc))

    def transform_log(self):
        m = np.sqrt(self.x**2 + self.y**2)
        a = np.arctan(self.y / self.x)
        self.x = np.log(m)
        self.y = a

    def transform_exp(self):
        x = np.exp(self.x) * np.cos(self.y)
        y = np.exp(self.x) * np.sin(self.y)
        self.x = x
        self.y = y

    def transform_mul(self, ar, ai):
        x = self.x * ar - self.y * ai
        y = self.y * ar + self.x * ai
        self.x = x
        self.y = y

line_length = 16 * math.pi

class LineV(Line):
    def __init__(self, x, s):
        super(LineV, self).__init__()
        self.x = np.ones((n,)) * x
        if s == -1:
            self.y = np.linspace(-line_length, 0, n + 1)[:-1]
        elif s == 1:
            self.y = np.linspace(0, line_length, n + 1)[1:]

class LineH(Line):
    def __init__(self, y, s):
        super(LineH, self).__init__()
        if s == -1:
            self.x = np.linspace(-line_length, 0, n + 1)[:-1]
        elif s == 1:
            self.x = np.linspace(0, line_length, n + 1)[1:]
        self.y = np.ones((n,)) * y

x_rng = np.linspace(0, math.pi, 3)
y_rng = np.linspace(-math.pi, math.pi, 5)

class Grid:
    def __init__(self):
        self.lines = []
        for s in [-1, 1]:
            self.lines += [LineV(x, s) for x in x_rng]
            self.lines += [LineH(y, s) for y in y_rng]

    def plot(self):
        for l in self.lines:
            l.plot()

    def transform_log(self):
        for l in self.lines:
            l.transform_log()

    def transform_exp(self):
        for l in self.lines:
            l.transform_exp()

    def transform_mul(self, ar, ai):
        for l in self.lines:
            l.transform_mul(ar, ai)

g = Grid()

ax = plt.subplot(111)

g.plot()

g.transform_mul(1,2)

g.plot()

ax.set_xlim([-2*math.pi, 2*math.pi])
ax.set_ylim([-2*math.pi, 2*math.pi])

plt.show()


