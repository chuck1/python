import copy
import math
import re
import functools
import numpy as np
import matplotlib
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import mpl_toolkits.mplot3d as a3
import scipy.optimize
#import mpl_toolkits.mplot3d.art3d

X = np.array([1,0,0])
Y = np.array([0,1,0])
Z = np.array([0,0,1])

def solve1(X_, p):
    p.tool.o = X_[0:3]
    p.tool.q = X_[3:7]
    
    Y = np.zeros(7)
   
    Y[0] = np.linalg.norm(p.tool.q) - 1

    for i in range(6):
        j = (i-i%2)//2
        
        l = np.linalg.norm(p.arms[i].o - p.tool.point(j))

        Y[i + 1] = l - p.arms[i].l
    
    return Y

def solve(p):
    x = scipy.optimize.fsolve(solve1, np.concatenate((p.tool.o, p.tool.q)), (p,))

    y = solve1(x, p)
    print('solve y = {}'.format(y))
    
    if np.any(np.abs(y) > 1e-6):
        raise RuntimeError()

    p.tool.o = x[0:3]
    p.tool.q = x[3:7]
    p.update_arms()

def quaternion_multiply(quaternion1, quaternion0):
    w0, x0, y0, z0 = quaternion0
    w1, x1, y1, z1 = quaternion1
    return np.array([
        -x1 * x0 - y1 * y0 - z1 * z0 + w1 * w0,
         x1 * w0 + y1 * z0 - z1 * y0 + w1 * x0,
        -x1 * z0 + y1 * w0 + z1 * x0 + w1 * y0,
         x1 * y0 - y1 * x0 + z1 * w0 + w1 * z0
        ])

def quaternion_reciprocal(q):
    w, x, y, z = q
    return np.array([w, -x, -y, -z])

def rotate(v, q):
    a = np.concatenate(([0], v))
    qp = quaternion_reciprocal(q)
    b = quaternion_multiply(q, quaternion_multiply(a, qp))
    return b[1:]

def axis_angle(v, a):
    w = math.cos(a/2)
    v = v * math.sin(a/2)
    return np.concatenate(([w], v))

def from_vectors(v1, v2):
    v1 = v1 / np.linalg.norm(v1)
    v2 = v2 / np.linalg.norm(v2)

    a = np.cross(v1, v2);
    w = math.sqrt((np.linalg.norm(v1)**2) * (np.linalg.norm(v2)**2)) + np.dot(v1, v2)
    ret = np.concatenate(([w], a))
    l = np.linalg.norm(ret)
    ret /= l
    return ret

class Arm:
    def __init__(self, l, o, q):
        self.l = l
        self.o = o
        self.q = q

    def p(self):
        return self.o + self.l * rotate(X, self.q)

    def get_plot_data(self):
        o = np.reshape(self.o, (3,1))
        p = np.reshape(self.p(), (3,1))
        data = np.concatenate((o, p), 1)
        return data

    def plot(self, ax, ax_2dx, ax_2dy, ax_2dz, linewidth):
        data = self.get_plot_data()
        self.line, = ax.plot(data[0], data[1], data[2], linewidth=linewidth)
        self.line_2dx, = ax_2dx.plot(data[1], data[2], linewidth=linewidth)
        self.line_2dy, = ax_2dy.plot(data[0], data[2], linewidth=linewidth)
        self.line_2dz, = ax_2dz.plot(data[0], data[1], linewidth=linewidth)

    def plot_update(self):
        data = self.get_plot_data()

        self.line.set_data(data[0:2])
        self.line.set_3d_properties(data[2])
        
        self.line_2dx.set_data(data[np.array([1,2])])
        self.line_2dy.set_data(data[np.array([0,2])])
        self.line_2dz.set_data(data[np.array([0,1])])

class Tool:
    def __init__(self, l, o, q):
        self.l = l
        self.o = o
        self.q = q
        assert len(self.o) == 3
        
    def point(self, i):
        v = rotate(rotate(X, axis_angle(Z, math.pi * 2 / 3 * i)), self.q)
        return self.o + self.l * v

    def tip(self):
        return self.o + 0.1 * rotate(-Z, self.q)

    def plot_data(self, i):

        if i == 3:
            o = np.reshape(self.o, (3,1))
            p = np.reshape(self.tip(), (3,1))
            data = np.concatenate((o, p), 1)
            return data

        o = np.reshape(self.point(i), (3,1))
        p = np.reshape(self.point((i+1)%3), (3,1))
        data = np.concatenate((o, p), 1)
        return data

    def plot(self, ax, ax_2dx, ax_2dy, ax_2dz):
        self.lines = []
        self.lines_2dx = []
        self.lines_2dy = []
        self.lines_2dz = []

        for i in range(4):
            data = self.plot_data(i)
            
            line, = ax.plot(data[0], data[1], data[2])
            self.lines.append(line)
    
            line, = ax_2dx.plot(data[1], data[2])
            self.lines_2dx.append(line)

            line, = ax_2dy.plot(data[0], data[2])
            self.lines_2dy.append(line)

            line, = ax_2dz.plot(data[0], data[1])
            self.lines_2dz.append(line)

    def plot_update(self):
        for i in range(4):
            data = self.plot_data(i)
            
            line = self.lines[i]
            line.set_data(data[0:2])
            line.set_3d_properties(data[2])

            self.lines_2dx[i].set_data(data[np.array([1,2])])
            self.lines_2dy[i].set_data(data[np.array([0,2])])
            self.lines_2dz[i].set_data(data[np.array([0,1])])

class Platform:
    def __init__(self,
            tool_o=np.array([0, 0, -0.4]),
            tool_q=axis_angle(Z, math.pi/6)
            ):

        self.tool = Tool(0.1, tool_o, tool_q)
        
        arm_anchor_radius = 0.5

        self.arms = []
        for i in range(6):
            j = (i-i%2)//2

            a = i * math.pi * 2 / 6

            x = math.cos(a)
            y = math.sin(a)
            z = 0
            
            o = np.array([x,y,z]) * arm_anchor_radius
            
            p = self.tool.point(j)
            v = p - o

            q = from_vectors(X, v)

            #print(q)

            arm = Arm(np.linalg.norm(v), o, q)

            self.arms.append(arm)

    def move_tool(self, o, q):
        self.tool.o = o
        self.tool.q = q
        self.update_arms()
    
    def move_arms(self, moves):

        l0 = self.get_lengths()
        l1 = np.array(l0)
        
        for i, l in moves:
            self.arms[i].l = l

            l1[i] = l
        
        print('move arms')
        print(l0)
        print(l1)
        
        try:
            solve(self)
        except RuntimeError as e:

            print(e)
            
            for i in range(6):
                self.arms[i].l = l0[i]

            l = l0 + (l1-l0)*0.1
            
            moves2 = [(i,l[i]) for i in range(6)]
            self.move_arms(moves2)

            raise

    def update_arms(self):
        for i in range(6):
            j = (i-i%2)//2

            o = self.arms[i].o
            
            p = self.tool.point(j)
            v = p - o

            self.arms[i].l = np.linalg.norm(v)

            q = from_vectors(X, v)

            self.arms[i].q = q

    def get_lengths(self):
        return np.array([a.l for a in self.arms])

    def get_tool_verts(self):
        return [[self.tool.point(i) for i in range(3)]]

    def plot(self, fig, fig2d):
        ax = a3.Axes3D(fig)
        
        ax_2dx = fig2d.add_subplot(2,2,1)
        ax_2dy = fig2d.add_subplot(2,2,2)
        ax_2dz = fig2d.add_subplot(2,2,3)

        for i, arm in zip(range(6), self.arms):
            linewidth = 3 if i == 0 else 1
            arm.plot(ax, ax_2dx, ax_2dy, ax_2dz, linewidth)
       
        self.tool.plot(ax, ax_2dx, ax_2dy, ax_2dz)

        p = np.array([-0.5,0.5])
        ax.set_xlim3d(p)
        ax.set_ylim3d(p)
        ax.set_zlim3d(p-0.5)

    def plot_update(self):
        for arm in self.arms:
            arm.plot_update()
        
        self.tool.plot_update()

    def print_(self):
        print('tool')
        print('    p   = {}'.format(self.tool.o))
        print('    q   = {}'.format(self.tool.q))
        print('    tip = {}'.format(self.tool.tip()))
        print('arms')
        for a in self.arms:
            print('    {}'.format(a.o))
            print('    {}'.format(a.l))


