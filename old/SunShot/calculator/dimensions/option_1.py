import sys
import math

if len(sys.argv) != 6:
	print "usage: %r <D> <PL> <Z> <Z in> <Z out>" % sys.argv[0]
	sys.exit(0)

D = float( sys.argv[1] )
PL = float( sys.argv[2] )
Z = float( sys.argv[3] )
Z_in = float( sys.argv[4] )
Z_out = float( sys.argv[5] )

Z_mid = Z - Z_in - Z_out

PT = math.sqrt( 3 ) / 2 * PL

Z_mid2 = Z_mid - PL / 2

N = math.floor( Z_mid2 / PL )

Z_rem = Z_mid - PL * ( N + 0.5 )

R = D / 2

H = PL - D

print "PL    %e" % PL
print "PT    %e" % PT
print "R     %e" % R
print "D     %e" % D
print "H     %e" % H
print "Z_mid %e" % Z_mid
print "Z_rem %e" % Z_rem
print "N     %i" % N


