import json
import pickle

class Foo:
    a = 10

d = {'b': 'hello'}

foo = Foo()

with open('file', 'wb') as f:
    pickle.dump(d, f)
    pickle.dump(foo, f)

with open('file', 'rb') as f:
    d = pickle.load(f)
    foo = pickle.load(f)

print(d)
print(foo)


