#!/usr/bin/env python3

import itertools


def level_097(x):
    
    y = [None]*20

    y[0] = x[1] and x[2]
    y[1] = x[3] or x[4]
    y[2] = x[5] or x[6]
    y[3] = x[0] and y[0]
    y[4] = y[0] != y[1]
    y[5] = y[1] != y[2]
    y[6] = y[2] and x[7]
    y[7] = y[4] and (not x[8])
    y[8] = y[4] and x[8]
    y[9] = y[5] and (not x[9])
    y[10] = y[5] and x[9]
    y[11] = y[3] and (not y[7])
    y[12] = y[8] and (not y[9])
    y[13] = y[6] != y[10]
    y[14] = (not y[12]) and (not x[10])
    y[15] = (not y[12]) and x[10]
    y[16] = (not y[3]) or (not y[11])
    y[17] = y[11] != y[14]
    y[18] = y[13] != y[15]
    y[19] = y[6] and y[13]

    return (not y[16]) and y[17] and (not y[18]) and y[19]

def solve1(func, n):
    for c in itertools.product([True,False], repeat=n):
        res = func(c)
        if res:
            yield c

def solve(func, n):

    comb = list(solve1(func, n))

    m = [sum(c) for c in comb]

    comb = [c for c in comb if sum(c) == min(m)]

    return comb

comb = solve(level_097, 11)

for c in comb:
    print(c)

