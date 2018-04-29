import time

def Xor(x, y):
    return 1 if (x != y) else 0

def Or(x, y):
    return x or y

def Nor(x, y):
    return not (x or y)

def Not(x):
    return not x

def And(x, y):
    return 1 if (x and y) else 0

def pulse_3(X):
    a, b, c, d, e = X
    return a, Not(a), Not(b), Xor(a, c), And(a, d)

def pulse_4(X):
    a, b, c = X
    return a, Not(a), And(a, b)

def latch(X):
    a, b, c, d = X

    return a, b, Nor(a, d), Nor(b, c)

def counter_1(X):
    a, b = X
    return a, a + b

def counter_2(X):
    a, b, c, d = X
    return a, 1 - a, 1 if And(a, b) else 0, c + d

def process_input(X):
    return [next(x) if hasattr(x, '__next__') else x  for x in X]

class Simulator:
    def __init__(self, inputs, Y):
        self.inputs = [iter(i) for i in inputs]
        self.Y = Y
        
        self.counter = list(Y)

    def run(self, n=20):
        for i in range(n):
            X = [next(i) for i in self.inputs]
        
            self.step1(X)
            
            print(['{:2}'.format(x) for x in X], ', '.join('{:2}'.format(x) for x in self.Y))

    def step1(self, X):
        self.Y = self.step(X, self.Y)
        
        self.counter = [c + y for c, y in zip(self.counter, self.Y)]

    def output(self):
        return self.Y[-1]

class Delay(Simulator):
    def __init__(self, X, n):
        super(Delay, self).__init__(X, [0]*(n+1))
        self.n = n

    def step(self, X, Y):
        Y1 = [0]*(self.n + 1)

        Y1[0] = X[0]
        for i in range(1, self.n + 1):
            Y1[i] = Y[i-1]

        return Y1

class Counter2(Simulator):
    def __init__(self, X):
        super(Counter2, self).__init__(X, [0]*7)
        self.clock = ClockReset([])
        self.pulse = Pulse()
        self.pulse_lengthener = PulseLengthener()
        self.delay = Delay([], 1)

    def step(self, X, Y):
        Y = [
                self.Y[5], #self.delay.Y[self.delay.n-1],
                1 if (Y[3] and (Y[4] > 5)) else 0, #Y[3],
                self.pulse.Y[1],
                Y[0] - Y[2],
                self.clock.Y[0],
                X[0] + Y[3],
                self.pulse_lengthener.output(),
                ]

        self.clock.step1([self.Y[6]])
        self.pulse.step1([self.Y[1]])
        self.pulse_lengthener.step1([self.Y[2]])
        self.delay.step1([self.Y[5]])

        return Y

class Counter4(Simulator):
    def __init__(self, X, a):
        super(Counter4, self).__init__(X, [0]*7)
        self.clock = ClockReset([])
        self.pulse = Pulse()
        self.pulse_lengthener = PulseLengthener()
        self.delay = Delay([], 1)
        self.a = a

    def step(self, X, Y):
        Y1 = [
                X[0] + Y[5],
                Y[0], #self.delay.output(),
                self.clock.Y[0],
                1 if (Y[0] and (Y[2] > self.a)) else 0,
                self.pulse.Y[1],
                Y[1] - Y[3],
                self.pulse_lengthener.output(),
                ]

        self.clock.step1([self.Y[6]])
        self.pulse.step1([self.Y[3]])
        self.pulse_lengthener.step1([Y[4]])
        self.delay.step1([self.Y[0]])

        return Y1

class Decrementer(Simulator):
    def __init__(self, a):
        super(Decrementer, self).__init__([], [0]*7)
        self.clock = ClockReset([])
        self.pulse = Pulse()
        self.pulse_lengthener = PulseLengthener()
        self.delay = Delay([], 1)
        self.a = a

    def step(self, X, Y):
        Y1 = [
                X[0],#self.delay.output(),
                self.clock.Y[0],
                1 if (X[0] and (Y[1] > self.a)) else 0,
                self.pulse.Y[1],
                Y[0] - Y[2],
                self.pulse_lengthener.output(),
                ]

        self.clock.step1([self.Y[5]])
        self.pulse.step1([self.Y[2]])
        self.pulse_lengthener.step1([Y[3]])
        self.delay.step1([X[0]])

        return Y1

class Dispatcher(Simulator):
    def __init__(self, X):
        super(Dispatcher, self).__init__(X, [0]*10)

        self.accu = Accumulator([])
        self.dec0 = Decrementer(10)
        self.dec1 = Decrementer(10)

    def step(self, X, Y):
        Y1 = [
                X[0] + Y[3],
                self.accu.Y[2],
                self.dec0.Y[4],
                self.dec1.Y[4],
                # dec pulses
                self.dec0.Y[3],
                self.dec1.Y[3],
                ]

        self.accu.step1([Y[0]])
        self.dec0.step1([Y[1]])
        self.dec1.step1([Y[2]])

        return Y1


class Counter3(Simulator):
    def __init__(self, X):
        super(Counter3, self).__init__(X, [0]*6)
        self.clock = Clock(5)

    def step(self, X, Y):
        Y = [
                1 - X[0], 
                1 if And(X[0], Y[0]) else 0, 
                Y[1] + Y[4],
                Y[4], #delay
                Y[2] - Y[3],
                self.clock.Y[3],
                ]

        self.clock.step1([])

        return Y

class Pulse(Simulator):
    def __init__(self):
        super(Pulse, self).__init__([], [0]*2)

    def step(self, X, Y):
        return [
                1 - X[0],
                1 if (X[0] and Y[0]) else 0]

class PulseLengthener(Simulator):
    def __init__(self, X=[]):
        super(PulseLengthener, self).__init__(X, [0]*2)

    def step(self, X, Y):
        return [
                X[0],
                1 if (X[0] or self.Y[0]) else 0]
    
    def output(self):
        return self.Y[1]

class Clock(Simulator):
    def __init__(self, a):
        super(Clock, self).__init__([], [0]*4)
        self.a = a
        self.pulse = Pulse()

    def step(self, X, Y):
        Y = [
                Y[2] + 1,
                1 if Y[0] > self.a else 0,
                0 if Y[1] else Y[0],
                self.pulse.Y[1]]

        self.pulse.step1([Y[1]])
        
        return Y

class Clock2(Simulator):
    def __init__(self, a):
        super(Clock2, self).__init__([], [0]*5)
        self.a = a
        self.pulse = Pulse()
        self.pulse_lengthener = PulseLengthener()

    def step(self, X, Y):
        Y1 = [
                1 + Y[4],
                1 if ((Y[0] > self.a)) else 0,
                self.pulse.output(),
                self.pulse_lengthener.output(),
                0 if Y[3] else Y[0],
                ]

        self.pulse.step1([Y[1]])
        self.pulse_lengthener.step1([Y[2]])

        return Y1

    def output(self): return self.Y[2]

class Accumulator(Simulator):
    def __init__(self, X):
        super(Accumulator, self).__init__(X, [0]*10)
        self.clock = Clock2(3)
        self.delay = Delay([], 0)

    def step(self, X, Y):
        Y1 = [
                X[0] + Y[4],
                self.clock.output(),
                
                # one at a time
                #1 if (Y[0] and Y[1]) else 0,

                # send the full value
                Y[0] if (Y[0] and Y[1]) else 0,

                Y[0],#self.delay.output(),
                Y[3] - Y[2],
                #self.pulse_lengthener.output(),
                ]
        
        self.clock.step1([Y[3]])
        self.delay.step1([Y[0]])
    
        return Y1

class PulseLimiter(Simulator):
    def step(self, X, Y):
        return [
                X[0],
                Xor(X[0], Y[0]),
                And(Y[0], Y[1]),
                ]

class ClockReset(Simulator):
    def __init__(self, X):
        super(ClockReset, self).__init__(X, [0]*2)

    def step(self, X, Y):
        Y = [
                Y[1] + 1,
                0 if X[0] else Y[0]]

        return Y

def counter_3(X):
    a, b, c, d, e, f = X
    return (
            a, 
            1 - a, 
            1 if And(a, b) else 0, 
            c + f,
            f, 
            d - e)

def show(X):
    print(X)

def run(X, f):
    while True:
        show(X)
    
        time.sleep(1 / 30)

        X1 = list(f(X))
        
        if X1==X: 
            print('stable')
            break
    
        X = X1
   
    return X

def run2(X, f):
    for i in range(20):
        show(X)

        time.sleep(1/60)

        X = list(f(X))

def test_latch():

    X = [True, False, False, False]
    
    X = run(X, latch)
    
    X[0] = 0

    X = run(X, latch)

    X[1] = True

    X = run(X, latch)

    X[1] = False

    X = run(X, latch)

def test_pulse(f):

    X = [0, 0, 0, 0, 0, 0]

    X = run(X, f)

    X[0] = 1

    X = run(X, f)

    X[0] = 0

    X = run(X, f)

def test_pulse2(f):
    X = [low_to_high(), 0, 0, 0, 0, 0]

    X = run(X, f)

def test_1(f):
    X = [0, 0, 0, 0]

    X = run(X, f)

    X[0] = 1

    X = run(X, f)

def low_to_high():
    for i in range(5):
        yield 0

    while True:
        yield 1

def pulse(d, n):
    for i in range(6):
        yield 0
    
    for i in range(n):
        yield 1

        for j in range(d):
            yield 0

    while True:
        yield 0

#test_pulse(pulse_4)

#test2(counter_3)


#Counter3([low_to_high()]).run()

#Clock(5).run(60)

#Clock2(10).run(60)

#Accumulator([pulse(0,5)]).run(120)

#PulseLimiter([pulse(1,2)], [0]*2).run()

#Counter4([pulse(10, 2)], 20).run(120)

n = 10

d = Dispatcher([pulse(0, n)])
d.run(300)

print(d.counter)
assert(d.counter[4] + d.counter[5] == n)



