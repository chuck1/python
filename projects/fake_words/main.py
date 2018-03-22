
import random
import time

import argparse

SOUND_COUNT = 100

def breakpoint():
    import pdb
    pdb.set_trace()

def vowel_sounds():
    yield 'a'
    yield 'e'
    yield 'i'

def consonant_sounds():
    yield 'b'
    yield 'c'
    yield 'd'
    yield 'f'
    yield 'g'
    yield 'th'
    yield 'ch'

def repeat_func(f):
    while True:
        for i in f():
            yield i

def repeat(iterable):
    while True:
        for i in iterable:
            yield i

def ith(iterable, i):

    it = iter(repeat_func(iterable))
    j = 0

    while j < i:
        next(it)
        j += 1

    return next(it)

def create_word():

    s = ''
    
    f_iter = iter(repeat((consonant_sounds, vowel_sounds)))

    for i in range(random.randint(3, 5)):

        f = next(f_iter)
        
        s += ith(f, random.randint(0, SOUND_COUNT)) 
        
    return s

def main():

    parser = argparse.ArgumentParser()

    args = parser.parse_args()

    random.seed(int(time.time()))

    print(create_word())


if __name__ == '__main__':
    main()

