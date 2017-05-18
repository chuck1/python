import pickle

class Foo(object):
    def __init__(self):
        self.a = 'hello'

f = Foo()

pickle.dump(f, open('a.bin','wb'))


