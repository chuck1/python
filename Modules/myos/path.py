import os

def pathlist(h):
    l = []
    while h:
        h,t = os.path.split(h)
        l.insert(0,t)

    return l

