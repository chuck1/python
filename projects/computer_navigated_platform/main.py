import copy
import math
import re
import functools
import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import mpl_toolkits.mplot3d as a3
import scipy.optimize
#import mpl_toolkits.mplot3d.art3d

from platform_ import *


def circle(i, z):
    period_in_frames = 60
    a = math.pi * 2 / period_in_frames * i
    r = 0.25
    x = r * math.sin(a)
    y = r * math.cos(a)
    z = z
    return np.array([x, y, z])

fps = 20

AXIS = {'X':0,'Y':1,'Z':2}

def make_path(p, q, n):
    v = q - p
    return [p + v * (i+1)/n for i in np.arange(n)]

class Program:
    def __init__(self, platform, fps):
        self.platform = platform
        self.feed_rate = .02
        self.fps = fps
        self.lines = []
        self.frames = []

    def read_line(self):
        if not self.lines:
            return None

        s = self.lines.pop(0)
        
        print(s)
        
        pat = re.compile("G1 ([XYZ])(\d+\.?\d*)")
        m = pat.match(s)
        if m:
            print(m.groups())
            p = float(m.group(2)) / 1000
            
            o1 = np.array(self.platform.tool.o)
            o2 = np.array(o1)
            
            axis = AXIS[m.group(1)]

            o2[axis] = p

            d = np.linalg.norm(o2 - o1)
            
            duration = d / self.feed_rate
            print('d',d)
            print('fr',self.feed_rate)
            frames = duration * self.fps
            
            path = make_path(o1, o2, frames)
            
            new_frames = [functools.partial(self.platform.move_tool, o, self.platform.tool.q) for o in path]
            
            print('added {} frames'.format(frames))

            self.frames += new_frames

            return

        raise RuntimeError('invalid gcode command {}'.format(repr(s)))

    def next_frame(self):

        if not self.frames:
            self.read_line()
        
        if not self.frames:
            return None

        return self.frames.pop(0)

def update_plot_(num, p, prog):
    #p.move_tool(circle(num, -0.5), p.tool.q)
    #p.move_arms([(0, p.arms[0].l + 0.001 / fps)])
    
    print('frame {}'.format(num))
    f = prog.next_frame()
    if f: f()

    #print(' '.join(['{:.8f}'.format(a.l) for a in p.arms]))

    p.plot_update()
    
    yield from p.tool.lines
    
    for a in p.arms:
        yield a.line

def update_plot_2d_(num, p, prog):
    print('frame {}'.format(num))
    f = prog.next_frame()
    if f: f()

    p.plot_update()

    yield from p.tool.lines_2dx
    yield from p.tool.lines_2dy
    yield from p.tool.lines_2dz
    
    for a in p.arms:
        yield a.line_2dx
        yield a.line_2dy
        yield a.line_2dz

def update_plot(num, p, prog):
    return list(update_plot_(num, p, prog))

def update_plot_2d(num, p, prog):
    return list(update_plot_2d_(num, p, prog))

def calculate_length_delta(l0, platform, p, q):
    platform.move_tool(p, q)

    l = platform.get_lengths()

    #print('l0',l0)
    #print('l ',l)

    return l - l0

def func_home(X, p, q, platform, length_delta_list, tip_z_list, verbose):
    p_0 = X[:3]
    q_0 = X[3:]
    q_0 = q_0 / np.linalg.norm(q_0)

    if verbose: print('tool starting position guess p = {:+.4e} {:+.4e} {:+.4e} q = {}'.format(p_0[0], p_0[1], p_0[2], q_0))
    
    #platform.move_tool(p_0, q)
    platform.move_tool(p_0, q_0)
    
    l_0 = platform.get_lengths()

    e = 0

    for length_delta, z in zip(length_delta_list, tip_z_list):
        length = l_0 + length_delta
        
        platform.move_arms([(i, l) for i, l in zip(range(6), length)])
            
        e += (platform.tool.tip()[2] - z)**2
    
    e = math.sqrt(e)

    if verbose: print('home error', e)

    return e

def plot_2d_homing_func(o, q0, p, length_delta_list, pos_list):
    s = 0.50
    x = np.linspace(o[0]-s, o[0]+s, 11)
    y = np.linspace(o[1]-s, o[1]+s, 11)
    X, Y = np.meshgrid(x, y)

    def f(x, y):
        return func_home(np.array([x, y, -.4]), o, q0, p, length_delta_list, pos_list, False)

    Z = np.log10(np.vectorize(f)(X, Y))

    c = plt.contourf(X, Y, Z)
    plt.colorbar(c)
    plt.show()

def calculate_tip_pos(platform, p, q):
    platform.move_tool(p, q)
    return platform.tool.tip()

def create_test_points(platform, l0):
    # list of tool positions
    n = 3
    pos_list = []
    for x in np.linspace(-.1, .1, n):
        for y in np.linspace(-.1, .1, n):
            p = np.array([x, y, -0.5])
            #q = quaternion_multiply(axis_angle(), axis_angle(Z, 0))
            #q = np.array(platform.tool.q)
            q = axis_angle(X, x/.1*math.pi/4)

            pos_list.append((p, q))
    
    # list of arm length deltas associated with the list of positions
    length_delta_list = [calculate_length_delta(l0, platform, p, q) for p, q in pos_list]

    tip_z_list = [calculate_tip_pos(platform, p, q)[2] for p, q in pos_list]

    print('length delta list')
    for z, pos, length_delta in zip(tip_z_list, pos_list, length_delta_list):
        print(z, pos, length_delta)
    
    return tip_z_list, length_delta_list

def test_home(o, q):
    print('home program')
    print('actual starting position')

    # actual starting position
    p = Platform(o, q)

    print(p.tool.o)
    
    # original arm lengths
    l0 = p.get_lengths()
    
    print('actual starting arm length')
    print(l0)
    
    pos_list, length_delta_list = create_test_points(p, l0)

    #plot_2d_homing_func(o, q, p, length_delta_list, pos_list)

    #print(pos_list)
    #print(length_delta_list)

    # test objective function
    e = func_home(np.concatenate((o, q)), o, q, p, length_delta_list, pos_list, True)
    print('test objective function:', e)

    bounds = [(-1,1),(-1,1),(-1,0),(-1,1),(-1,1),(-1,1),(-1,1)]

    for x in np.linspace(-.1, .1, 3):
        p0 = np.array([x, 0, -0.4])
        p0 = np.array([0.05, 0, -0.35])
        q0 = axis_angle(Z, math.pi/6)

        #x0 = p0
        x0 = np.concatenate((p0, q0))
        
        r = scipy.optimize.minimize(
                func_home, 
                x0, 
                (o, q, p, length_delta_list, pos_list, True), 
                bounds=bounds,
                options = {'eps': 1e-5})
        
        if r.success:
            break
    
    assert(r.success)

    print(r)
    
    print('p')
    print(r.x[:3])
    print(o)
    print('q')
    print(r.x[3:])
    print(q)

def test_math():
    print(rotate(X, axis_angle(Y, math.pi/2)))
    print(rotate(X, axis_angle(Z, math.pi/2)))
    print(rotate(Y, axis_angle(X, math.pi/2)))
    print(rotate(Y, axis_angle(Z, math.pi/2)))
    print(rotate(Z, axis_angle(X, math.pi/2)))
    print(rotate(Z, axis_angle(Y, math.pi/2)))

    q = from_vectors(X, Y)
    print(Y)
    print(rotate(X, q))
    
    q = from_vectors(X, Z)
    print(Z)
    print(rotate(X, q))


#axis_angle(X, math.pi/2)

def test():
    p = Platform()

    p.print_()

    fig = plt.figure()
    fig2d = plt.figure()

    p.plot(fig, fig2d)

    frames = 60

    prog = Program(p, fps)
    prog.lines.append("G1 X100")

    #line_ani_3d = animation.FuncAnimation(fig, update_plot, frames, fargs=(p, prog), interval=1000/fps, blit=True)
    line_ani_2d = animation.FuncAnimation(fig2d, update_plot_2d, frames, fargs=(p, prog), interval=1000/fps, blit=True)
    
    plt.show()


#######################

if False:
    p.plot()
    plt.show()

test_home(np.array([.05, 0, -0.35]), axis_angle(Z, math.pi/6))



