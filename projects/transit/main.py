import math

def rad_to_deg(r):
    return r / math.pi * 180

d_earth = 150E9

r_e = 6.371E6

r_sun = 695700E3

d_i = 404E3

r_i = 50

a_s = math.atan(r_sun / d_earth)

a_i = math.atan(r_i / d_i)

print(a_s)
print(a_i)
print(rad_to_deg(a_s))
print(rad_to_deg(a_i))

f = 1.0

s_s = f * math.tan(a_s)
s_i = f * math.tan(a_i)

print('s_s:       {:8.3f} mm'.format(s_s * 1000))
print('s_i:       {:8.3f} mm'.format(s_i * 1000))
print('s_i / s_s: {:8.3f}'.format(s_i / s_s))

