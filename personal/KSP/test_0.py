import ksp

print ksp.circle_to_ellipse(ksp.sun,
		ksp.kerbin.obt.apoapsis,
		ksp.duna.obt.periapsis)

h = ksp.PlanetTransfer(ksp.kerbin, ksp.duna)
h.calc()
print h

