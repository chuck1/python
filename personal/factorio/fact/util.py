import math

def floor_(x, y):
    return int(x - (x % y))

def ceil_(x, y):
    return int(x + (x % y))

def quadratic(a, b, c):
    d = math.sqrt(b**2 - 4 * a * c)
    return (-b + d) / 2 / a, (-b - d) / 2 / a

def correct_answer(x, y):
    if (x < 0) and (y > 0): return y
    if (x > 0) and (y < 0): return x
    raise RuntimeError()

def spread(a, b):
    # example
    #   spread(3, 7) -> 0, 0, 0, 1, 1, 2, 2
        
    print('spread')
    print(a, b)
    print(list(range(b % a)), b // a + 1)
    print(list(range(b % a, a)), b // a)

    for i in range(b % a):
        for j in range(b // a + 1):
            yield i

    for i in range(b % a, a):
        for j in range(b // a):
            yield i

