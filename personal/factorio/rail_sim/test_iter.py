
g = iter(range(10))

for a in g:
    print('first', a)
    if a == 5:
        break

for a in g:
    print(a)

