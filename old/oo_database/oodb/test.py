
class foo:

    def f(self):
        return 1


f = foo()
b = foo()

print(f.f)

f.f = 2

print(f.f)

print(b.f)
