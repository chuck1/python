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
        
    def point(self, i):
        v = rotate(rotate(X, axis_angle(Z, math.pi * 2 / 3 * i)), self.q)
        return self.o + self.l * v

    def plot_data(self, i):
        o = np.reshape(self.point(i), (3,1))
        p = np.reshape(self.point((i+1)%3), (3,1))
        data = np.concatenate((o, p), 1)
        return data

    def plot(self, ax, ax_2dx, ax_2dy, ax_2dz):
        self.lines = []
        self.lines_2dx = []
        self.lines_2dy = []
        self.lines_2dz = []

        for i in range(3):
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
        for i in range(3):
            data = self.plot_data(i)
            
            line = self.lines[i]
            line.set_data(data[0:2])
            line.set_3d_properties(data[2])

            self.lines_2dx[i].set_data(data[np.array([1,2])])
            self.lines_2dy[i].set_data(data[np.array([0,2])])
            self.lines_2dz[i].set_data(data[np.array([0,1])])

class Platform:
    def __init__(self, tool_o, tool_q):

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
        for i, l in moves:
            self.arms[i].l = l

        solve(self)

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
        print('    {}'.format(self.tool.o))
        print('    {}'.format(self.tool.q))
        print('arms')
        for a in self.arms:
            print('    {}'.format(a.o))
            print('    {}'.format(a.l))


if False:
    p.plot()
    plt.show()

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

def calculate_length_delta(l0, p, o, q):
    p.move_tool(o, p.tool.q)

    l = p.get_lengths()

    #print('l0',l0)
    #print('l ',l)

    return l - l0

def func_home(X, p, q, platform, length_delta_list, pos_list, verbose):
    p_0 = X[:3]
    q_0 = X[3:]

    if verbose: print('tool starting position guess', p_0, q_0)
    
    #platform.move_tool(p_0, q)
    platform.move_tool(p_0, q_0)
    
    l_0 = platform.get_lengths()

    e = 0

    for length_delta, pos in zip(length_delta_list, pos_list):
        p_1, q_1 = pos
            
        length = l_0 + length_delta
        
        platform.move_arms([(i, l) for i, l in zip(range(6), length)])
            
        e += abs(platform.tool.o[2] - p_1[2])
    
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

def create_test_points(platform, l0):
    # list of tool positions
    n = 2
    pos_list = []
    for x in np.linspace(-.1, .1, n):
        for y in np.linspace(-.1, .1, n):
            pos_list.append((np.array([x,y,-.5]), axis_angle(Z, 0)))
    
    # list of arm length deltas associated with the list of positions
    length_delta_list = [calculate_length_delta(l0, platform, p, q) for p, q in pos_list]

    print('length delta list')
    for pos, length_delta in zip(pos_list, length_delta_list):
        print(pos, length_delta)

    return pos_list, length_delta_list

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
        q0 = axis_angle(Z, 0)

        #x0 = p0
        x0 = np.concatenate((p0, q0))
        
        r = scipy.optimize.minimize(func_home, x0, (o, q, p, length_delta_list, pos_list, True), bounds=bounds)
        
        if r.success:
            break
    
    assert(r.success)

    print(r)
    

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
    p = Platform(axis_angle(Z,2*math.pi/12))

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

test_home(np.array([.05, 0, -0.35]), axis_angle(Z, 2*math.pi/12))



