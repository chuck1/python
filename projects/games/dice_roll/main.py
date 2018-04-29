import time
import random

while True:

    s = input('enter a number from 2 to 12: ')

    if s == '':
        print('goodbye')
        break

    try:
        i = int(s)
    except:
        print('thats not a valid integer, try again')
        continue

    if i < 2:
        print('that number is too small')
        continue

    if i > 12:
        print('that number is too large')
        continue

    print('you entered:', i)

    print('rolling...')

    time.sleep(1)

    a = random.randint(1,6)
    b = random.randint(1,6)
    
    print('I rolled:', a, 'and', b)

    if a + b == i:
        print('you win!')
    else:
        print('you lose!')


