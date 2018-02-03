import math

def quadratic(a, b, c):
    d = math.sqrt(b**2 - 4 * a * c)
    return (-b + d) / 2 / a, (-b - d) / 2 / a


def correct_answer(x, y):
    if (x < 0) and (y > 0): return y
    if (x > 0) and (y < 0): return x
    raise RuntimeError()


