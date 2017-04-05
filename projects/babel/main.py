import functools
import operator
import sys

chars = ' abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789,.?:;'

alphanum = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

def get_page_num(levels):
    x = 0
    for l in levels:
        if l[2] > l[1]: raise Exception('value out of range')
        x *= l[1]
        x += l[2]
    return x

def get_page_num_rev(x, levels):
    
    for l in reversed(levels):
        n = l[1]

        y = x % n
        x -= y
        x //= n

        l[2] = y

def get_page_rev(string):
    x = 0
    for s in reversed(string):
        x *= len(chars)
        x += chars.index(s)
    return x

def get_page(x, n):
    s = ''
    for i in range(n):
        n = len(chars)
        
        y = x % n
        x -= y
        x //= n

        s += chars[y]
    return s

def int_to_alphanum(x):
    s = ''
    while True:
        m = len(alphanum) + 1
        
        y = x % m
        x -= y
        x //= m

        s += alphanum[y-1]

        if x == 0: break
    return s

def alphanum_to_int(string):
    x = 0
    for s in reversed(string):
        y = alphanum.index(s) + 1
        x *= len(alphanum) + 1
        x += y
    return x

def block_print(s, w, h):
    s = get_page(x, 64)
    print('+'+'-'*w+'+')
    for i in range(h):
        print('|'+s[i*h:i*h+w]+'|')
    print('+'+'-'*w+'+')

######################################################33

#x = alphanum_to_int('abcd')
#s = int_to_alphanum(x)
#print(x,s)
#sys.exit(0)

levels = [
    ['room',     36**100,   0],
    ['bookcase',       4,   0],
    ['shelf',          5,   0],
    ['volume',        32,   0],
    ['page',         410,   0]
    ]

get_page_num_rev(get_page_rev(' hello'), levels)

n = functools.reduce(operator.mul, [l[1] for l in levels], 1)

x = get_page_num(levels)

w = 8
h = 8

s = get_page(x, w*h)

block_print(s, w, h)


