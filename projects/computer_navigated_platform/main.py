import math
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d as a3
#import mpl_toolkits.mplot3d.art3d

X = np.array([1,0,0])
Y = np.array([0,1,0])
Z = np.array([0,0,1])

def solve(X_, p):
    for i in range(6):
        p.arms[i].q = X_[4*i:4*i+4]
    
    p.tool.o = X_[24:27]
    p.tool.q = X_[27:31]
    
    Y = np.zeros(31)

    for i in range(6):
        j = (i-i%2)//2

        y = p.arms[i].p() - p.tool.point(j)
        
        Y[k:k+3] = y
        k += 3

        y = np.linalg.norm(p.arms[i].q) - 1

        Y[k] = y
        k += 1

    

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

    def plot(self, ax):
        o = self.o
        p = self.p()
        ax.plot(
                [o[0], p[0]],
                [o[1], p[1]],
                [o[2], p[2]])

class Tool:
    def __init__(self, l, o, q):
        self.l = l
        self.o = o
        self.q = q
        
    def point(self, i):
        v = rotate(rotate(X, axis_angle(Z, math.pi * 2 / 3 * i)), self.q)
        return self.o + self.l * v

class Platform:
    def __init__(self):

        self.tool = Tool(0.1, np.array([0,0,-0.4]), axis_angle(X, math.pi/2))
        
        arm_anchor_radius = 0.5

        self.arms = []
        for i in range(6):
            j = (i-i%2)//2
            print(i, j)

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

    def plot(self):
        fig = plt.figure()
        #ax = fig.add_subplot(111, projection='3d')
        ax = a3.Axes3D(fig)
        for arm in self.arms:
            arm.plot(ax)
        
        verts = [[self.tool.point(i) for i in range(3)]]
        print(verts)
        tri = a3.art3d.Poly3DCollection(verts)
        ax.add_collection3d(tri)
        
        p = [-.5,.5]
        ax.plot(p,p,p)
    
p = Platform()

if False:
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

p.plot()
plt.show()



