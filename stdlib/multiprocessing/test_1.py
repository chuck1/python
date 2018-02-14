import multiprocessing
import time


def func(x):
    with open(x, 'w') as f:
        print('opened', x)
        time.sleep(2)
        f.write('hi\n')
    return 0

if __name__ == '__main__':
    with multiprocessing.Pool(2) as p:
        print(p.map(func, ['test.txt', 'test.txt']))

