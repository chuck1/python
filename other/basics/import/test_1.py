
m1 = __import__('test_mod')

print(m1)

g = dict(globals())
g['a']=1

m2 = __import__('test_mod', globals=g)

print(m2)

