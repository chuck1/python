
def func():
    yield None


print(list(f for f in func() if f is not None))

for x in func():
    print(x)

