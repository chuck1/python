import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import numpy as np

random.seed()

class Food:
    def __init__(self, sim, energy):
        self.energy = energy

class Creature:
    def __init__(self, sim, energy):
        self.sim = sim
        self.energy = energy
    
        self.cost_replicate = 2
        self.energy_eat = 1
        self.energy_move = 1
        self.energy_thresh_replicate = 50

        self.direction = None

    def any_empty_neighbors(self):
        for n in self.neighbors():
            if n is None: return True
        return False
 
    def empty_neighbors(self):
        for x, y in self.neighbor_indices():
            if self.sim.board[x, y] is None: yield x, y
   
    def random_empty_neighbor(self):
        n = list(self.empty_neighbors())
        return n[random.randrange(len(n))]
    
    def neighbor_indices(self):
        w = np.shape(self.sim.board)[0]
        h = np.shape(self.sim.board)[1]
        x, y = self.p[0], self.p[1]
        yield np.array([x-1, y])
        yield np.array([(x+1) % w, y])
        yield np.array([x, y-1])
        yield np.array([x, (y+1) % h])

    def neighbors(self):
        for p in self.neighbor_indices():
            yield self.sim.board[p[0], p[1]]

    def neighbors2(self, f):
        for n in self.neighbors():
            if f(n): yield n

    def any_neighbor_food(self):
        for n in self.neighbors():
            if isinstance(n, Food):
                return True
        return False

    def random_neighbor_food(self):
        def f(n):
            return isinstance(n, Food)

        n = list(self.neighbors2(f))
        return n[random.randrange(len(n))]

    def step(self):
        # replicate
        if (self.energy > self.energy_thresh_replicate) and (self.any_empty_neighbors()):
            p = self.random_empty_neighbor()
            self.energy -= self.cost_replicate
            c = Creature(self.sim, self.energy / 2)
            self.energy /= 2
            self.sim.add_creature(c, p)

        # eat
        elif self.any_neighbor_food():
            n = self.random_neighbor_food()
            e = min(self.energy_eat, n.energy)
            self.energy += e
            n.energy -= e

            if n.energy == 0:
                self.sim.board[n.x, n.y] = None
        
        elif self.any_empty_neighbors():
            # move

            if self.direction is None:
                p = self.random_empty_neighbor()
                self.direction = p - self.p
            else:
                p = self.sim.position_add(self.p, self.direction)
                if self.sim.is_empty(p):
                    pass
                else:
                    p = self.random_empty_neighbor()
                    self.direction = p - self.p


            self.energy -= self.energy_move
            self.sim.move(self.p, p)
            
            if self.energy <= 0:
                self.sim.board[self.p[0], self.p[1]] = None
                self.sim.creatures.remove(self)

        print('creature {} energy = {:03}'.format(id(self), self.energy))

def board_to_color(x):
    if x is None:
        return np.array([0,0,0])
    elif isinstance(x, Food):
        return np.array([1,0,0])
    elif isinstance(x, Creature):
        return np.array([0,0,1])

    raise RuntimeError(str(x))

class Simulation:
    def __init__(self, w, h):
        self.board = np.empty((w,h), dtype=object)
        self.creatures = []

        for i in range(10):
            self.add_creature(Creature(self, 30), self.random_empty_position())

        for i in range(10):
            self.add_food(Food(self, 100), self.random_empty_position())

        self.im = plt.imshow(self.image(), animated=True)

    def position_add(self, x, y):
        z = x + y
        z[0] = z[0] % np.shape(self.board)[0]
        z[1] = z[1] % np.shape(self.board)[1]
        return z

    def is_empty(self, p):
        return self.board[p[0], p[1]] is None

    def indices(self):
        for i in range(np.shape(self.board)[0]):
            for j in range(np.shape(self.board)[1]):
                yield i, j

    def indices_empty(self):
        for i, j in self.indices():
            if self.board[i, j] is None:
                yield np.array([i, j])
    
    def random_empty_position(self):
        p = list(self.indices_empty())
        return p[random.randrange(len(p))]

    def move(self, p, q):
        n = self.board[p[0], p[1]]
        assert n is not None
        assert self.board[q[0], q[1]] is None
        self.board[q[0], q[1]] = n
        self.board[p[0], p[1]] = None
        n.p = q

    def add_creature(self, c, p):
        self.creatures.append(c)
        c.p = p
        x, y = p[0], p[1]
        assert(self.board[x,y] is None)
        self.board[x,y] = c

    def add_food(self, c, p):
        x, y = p[0], p[1]
        c.p = p
        assert(self.board[x,y] is None)
        self.board[x,y] = c

    def step(self):
        for c in self.creatures:
            c.step()

    def image(self):
        z = np.zeros(np.shape(self.board) + (3,))

        for i in range(np.shape(self.board)[0]):
            for j in range(np.shape(self.board)[1]):
                z[i, j] = board_to_color(self.board[i, j])
        
        return z

    def updatefig(self, *args):
        self.step()
        self.im.set_array(self.image())
        return self.im,

s = Simulation(100,100)

fig = plt.figure()

ani = animation.FuncAnimation(fig, s.updatefig, interval=50, blit=True)
plt.show()



