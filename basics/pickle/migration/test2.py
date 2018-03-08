import pickle

"""
class Foo(object):
    def __init__(self):
        self.a = 'hello'
"""

f = pickle.load(open('a.bin','rb'))

print(f)

