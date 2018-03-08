
def wrap(f):
    def wrapper(*args):
        return f(*args)
    return wrapper

def foo(): return 0

w = wrap(foo)



