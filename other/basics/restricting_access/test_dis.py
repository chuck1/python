import dis




c = compile('open', '<string>', 'eval')

for x in dis.Bytecode(c):
    print(x)

print()

c = compile('open(\'a.txt\')', '<string>', 'eval')

for x in dis.Bytecode(c):
    print(x)


print()

c = compile('func.__func__.__globals__', '<string>', 'eval')

for x in dis.Bytecode(c):
    print(x)

print()

c = compile('getattr(func, \'__func__\').__globals__', '<string>', 'eval')

for x in dis.Bytecode(c):
    print(x)



