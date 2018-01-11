
def Xor(x, y):
    return x != y

def Or(x, y):
    return x or y

def Nor(x, y):
    return not (x or y)

def Not(x):
    return not x

def And(x, y):
    return x and y

def pulse_1(X):
    a, b, c = X
    return a, Xor(a, c), Or(a, b)

def pulse_2(X):
    a, b, c, d = X
    return a, Xor(c, d), Nor(a, b), Or(a, b)

def pulse_3(X):
    a, b, c, d, e = X
    return a, Not(a), Not(b), Xor(a, c), And(a, d)

def latch(X):
    a, b, c, d = X

    return a, b, Nor(a, d), Nor(b, c)

def show(X):
    print(' '.join(str(1 if x else 0) for x in X))

def run(X, f):
    while True:
        show(X)
        
        X1 = list(f(X))
        
        if X1==X: 
            print('stable')
            break
    
        X = X1
   
    return X

def test_latch():

    X = [True, False, False, False]
    
    X = run(X, latch)
    
    X[0] = False

    X = run(X, latch)

    X[1] = True

    X = run(X, latch)

    X[1] = False

    X = run(X, latch)



def test_pulse():

    f = pulse_3

    X = [False, False, False, False, False]

    X = run(X, f)

    X[0] = True

    X = run(X, f)

    X[0] = False

    X = run(X, f)


test_pulse()


