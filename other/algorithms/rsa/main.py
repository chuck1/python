import math

import primes

def find_e(phi):
    e = 1
    while e < phi:
        if phi % e != 0:
            return e
        e += 1
    raise RuntimeError()

def find_d(phi, e):
    print('finding d')
    d = 1
    while True:
        if (d * e) % phi == 1:
            return d
        d += 1

def encode(s):
    bs = s.encode()
    m = 0
    for b in bs:
        m *= 2**8
        m += b
    return m

def decode(m):
    bl = []
    while m:
        bl.append(m % 2**8)
        m = m >> 8
    return bytes(reversed(bl)).decode()

def encrypt(k, n, m):
    
    c = (m ** k) % n

    return c

def decrypt(k, n, c):
    return (c ** k) % n

def divide_encode_encrypt(k, n, l, s):
    print('encrypting')

    sl = []
    while s:
        sl.append(s[:l])
        s = s[l:]
    
    ml = [encode(s) for s in sl]

    cl = [encrypt(k, n, m) for m in ml]

    return cl

def decrypt_decode_combine(k, n, l, cl):

    ml = [decrypt(k, n, c) for c in cl]

    sl = [decode(m) for m in ml]

    s = ''.join(sl)

    return s


l = 2

n_min = 2 ** (l * 8)

print('n_min =', n_min)
p_min = math.ceil(math.sqrt(n_min))
print('p_min =', p_min)


p, q = primes.pair(p_min)

n = p * q

phi = (p - 1) * (q - 1)

print('p   =', p)
print('q   =', q)
print('n   =', n)
print('phi =', phi)

e = find_e(phi)

print()
print('public key')
print('  e =', e)
print('  n =', n)
print()

d = find_d(phi, e)

print('d   =', d)



s = 'hi'

m = encode(s)

c = encrypt(e, n, m)

print('s   =', repr(s))
print('m   =', m)
print('c   =', c)

m = decrypt(d, n, c)

print('m   =', m)

s = decode(m)

print('s   =', repr(s))


s = 'by'

m = encode(s)

c = encrypt(d, n, m)

print('s   =', repr(s))
print('m   =', m)
print('c   =', c)

m = decrypt(e, n, c)

print('m   =', m)

s = decode(m)

print('s   =', repr(s))

s = 'a long message'

print('s   =', repr(s))

cl = divide_encode_encrypt(e, n, l, s)

print(cl)

s = decrypt_decode_combine(d, n, l, cl)

print('s   =', repr(s))




