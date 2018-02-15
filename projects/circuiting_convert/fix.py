import sys

with open(sys.argv[1]) as f:
    raw = f.read()

lines = raw.split('\n')

with open(sys.argv[2], 'w') as f:

    f.write(lines.pop(0)+'\n')
    f.write(lines.pop(0)+'\n')
    f.write(lines.pop(0)+'\n')

    while True:
        line0 = lines.pop(0)
        if not line0: break
        f.write(line0+'\n')
        
        Y = [9-int(y) for y in lines.pop(0).split(',')]
        f.write(','.join(str(y) for y in Y) + '\n')


