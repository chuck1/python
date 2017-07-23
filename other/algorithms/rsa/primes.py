import math
import random

primes = [2]

def is_prime(a):
    for p in primes:
        if p > math.sqrt(a):
            break
        if a % p == 0:
            return False
    return True

def calc_primes(lower):
    global primes

    a = primes[-1]
    
    if a > lower:
        return
    
    while True:
        a += 1
        if is_prime(a):
            primes.append(a)
            if a > lower:
                return

def get_prime(lower):
    calc_primes(lower)

    for p in primes:
        if p > lower: return p


def pair(lower):
    random.seed()

    calc_primes(lower * 2)

    i_lower = 0
    while primes[i_lower] < lower:
        i_lower += 1

    global primes
    a = random.randint(i_lower, len(primes)-1)
    b = random.randint(i_lower, len(primes)-1)
    while a == b:
        b = random.randint(i_lower, len(primes)-1)
    a = primes[a]
    b = primes[b]
    return a, b


