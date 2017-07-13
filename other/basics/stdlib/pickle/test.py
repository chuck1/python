import pickle

from mod1 import submod1
#import mod1.submod1

class Foo:
    pass

foo = Foo()
foo.bar = submod1.Bar()
#foo.bar = mod1.submod1.Bar()

print(globals().keys())

with open('file', 'wb') as f:
    pickle.dump(foo, f)

#del mod1
del submod1

print(globals().keys())

with open('file', 'rb') as f:
    foo = pickle.load(f)



