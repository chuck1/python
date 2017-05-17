import sys
import math
import scipy.optimize
import numpy as np

import lambert
import quaternion

TWO_PI = 2 * math.pi

HALF_PI = 0.5 * math.pi

def sign(x):
	if x:
		if x < 0:
			return -1
		else:
			return 1
	
	return None

def sinh(angle):
	p = math.exp(angle)
	return (p - (1 / p)) * 0.5

def cosh(angle):
	p = math.exp(angle)
	return (p + (1 / p)) * 0.5


def acosh(n):
	return math.log(n + math.sqrt(n * n - 1))


def normalize(v):
	return numeric.divVS(v, np.linalg.norm(v));


def projectToPlane(p, n):
	return numeric.subVV(p, numeric.mulSV(numeric.dotVV(p, n), n));


def angleInPlane(fr, to, normal):
	
	fr = normalize(projectToPlane(fr, normal));
	to = normalize(projectToPlane(to, normal));
	rot = quaternion.fromToRotation(normal, [0, 0, 1]);
	
	fr = quaternion.rotate(rot, fr);
	to = quaternion.rotate(rot, to);
	result = math.atan2(fr[1], fr[0]) - math.atan2(to[1], to[0]);
	
	if (result < 0):
		return result + TWO_PI;
	else:
		return result;
	


newtonsMethod = scipy.optimize.newton #roots.newtonsMethod;

#brentsMethod = roots.brentsMethod;

goldenSectionSearch = scipy.optimize.golden;

class Orbit:
	#(typeof exports !== "undefined" and exports !== None ? exports : this).Orbit = Orbit = (function():
	
	def __init__(self, referenceBody, semiMajorAxis, eccentricity, inclination, longitudeOfAscendingNode, argumentOfPeriapsis, meanAnomalyAtEpoch, timeOfPeriapsisPassage = 0):
		self.referenceBody = referenceBody;
		self.semiMajorAxis = semiMajorAxis;
		self.eccentricity = eccentricity;
		self.inclination = inclination
		self.longitudeOfAscendingNode = longitudeOfAscendingNode
		self.argumentOfPeriapsis = argumentOfPeriapsis
		
		self.meanAnomalyAtEpoch = meanAnomalyAtEpoch;
		self.timeOfPeriapsisPassage = timeOfPeriapsisPassage;
		
		if inclination:
			self.inclination = inclination * math.pi / 180;
		
		if longitudeOfAscendingNode:
			self.longitudeOfAscendingNode = longitudeOfAscendingNode * math.pi / 180
		
		if argumentOfPeriapsis:
			self.argumentOfPeriapsis = argumentOfPeriapsis * math.pi / 180

	def isHyperbolic(self):
		return self.eccentricity > 1
	

	def apoapsis(self):
		return self.semiMajorAxis * (1 + self.eccentricity)
	

	def periapsis(self):
		return self.semiMajorAxis * (1 - self.eccentricity)
	

	def apoapsisAltitude(self):
		return self.apoapsis() - self.referenceBody.radius
	

	def periapsisAltitude(self):
		return self.periapsis() - self.referenceBody.radius
	

	def semiMinorAxis(self):
		e = self.eccentricity;
		return self.semiMajorAxis * math.sqrt(1 - e * e);
	

	def semiLatusRectum(self):
		e = self.eccentricity;
		return self.semiMajorAxis * (1 - e * e);
	

	def meanMotion(self):
		a = math.fabs(self.semiMajorAxis)
		return math.sqrt(self.referenceBody.gravitationalParameter / (a * a * a))
	

	def period(self):
		if (self.isHyperbolic()):
			return Infinity
		else:
			return TWO_PI / self.meanMotion()
		
	

	def rotationToReferenceFrame(self):
		axisOfInclination = [math.cos(-self.argumentOfPeriapsis), math.sin(-self.argumentOfPeriapsis), 0];

		q = quaternion.fromAngleAxis(self.longitudeOfAscendingNode + self.argumentOfPeriapsis, [0, 0, 1])

		return q.concat(quaternion.fromAngleAxis(self.inclination, axisOfInclination))
	

	def normalVector(self):
		return self.rotationToReferenceFrame().rotate([0, 0, 1]);
	

	def phaseAngle(self, orbit, t):

		n = self.normalVector()
		p1 = self.positionAtTrueAnomaly(self.trueAnomalyAt(t))
		p2 = orbit.positionAtTrueAnomaly(orbit.trueAnomalyAt(t))
		p2 = numeric.subVV(p2, numeric.mulVS(n, numeric.dotVV(p2, n)))
		r1 = np.linalg.norm(p1)
		r2 = np.linalg.norm(p2)
		phaseAngle = math.acos(numeric.dotVV(p1, p2) / (r1 * r2));
		if (numeric.dotVV(crossProduct(p1, p2), n) < 0):
			phaseAngle = TWO_PI - phaseAngle
		
		if (orbit.semiMajorAxis < self.semiMajorAxis):
			phaseAngle = phaseAngle - TWO_PI
		
		return phaseAngle;
	

	def meanAnomalyAt(self, t):

		if (self.isHyperbolic()):
			return (t - self.timeOfPeriapsisPassage) * self.meanMotion()
		else:
			if self.timeOfPeriapsisPassage:
				M = ((t - self.timeOfPeriapsisPassage) % self.period()) * self.meanMotion()
				if (M < 0):
					return M + TWO_PI
				else:
					return M
			else:
				return (self.meanAnomalyAtEpoch + self.meanMotion() * (t % self.period())) % TWO_PI
				

	def eccentricAnomalyAt(self, t):

		e = self.eccentricity;
		M = self.meanAnomalyAt(t);
		if (self.isHyperbolic()):
			return newtonsMethod(lambda x: M - e * sinh(x) + x, M, lambda x: 1 - e * cosh(x))
		else:
			return newtonsMethod(lambda x: M + e * math.sin(x) - x, M, lambda x: e * math.cos(x) - 1)
		

	def trueAnomalyAt(self, t):
		e = self.eccentricity;
		if (self.isHyperbolic()):
			H = self.eccentricAnomalyAt(t);
			tA = math.acos((e - cosh(H)) / (cosh(H) * e - 1));
			if (H < 0):
				return -tA;
			else:
				return tA;
		
		else:
			E = self.eccentricAnomalyAt(t);
			tA = 2 * math.atan2(math.sqrt(1 + e) * math.sin(E / 2), math.sqrt(1 - e) * math.cos(E / 2));
			if (tA < 0):
				return tA + TWO_PI
			else:
				return tA
	

	def eccentricAnomalyAtTrueAnomaly(self, tA):

		e = self.eccentricity
		if self.isHyperbolic():
			cosTrueAnomaly = math.cos(tA)
			H = acosh((e + cosTrueAnomaly) / (1 + e * cosTrueAnomaly))
			if (tA < 0):
				return -H
			else:
				return H
		
		else:
			E = 2 * math.atan(math.tan(tA / 2) / math.sqrt((1 + e) / (1 - e)));
			if (E < 0):
				return E + TWO_PI
			else:
				return E
	

	def meanAnomalyAtTrueAnomaly(self, tA):
		e = self.eccentricity;
		if (self.isHyperbolic()):
			H = self.eccentricAnomalyAtTrueAnomaly(tA);
			return e * sinh(H) - H;
		else:
			E = self.eccentricAnomalyAtTrueAnomaly(tA);
			return E - e * math.sin(E);
		
	def timeAtTrueAnomaly(self, tA, t0):

		if (t0 == None):
			t0 = 0;
	
		M = self.meanAnomalyAtTrueAnomaly(tA);
		if self.isHyperbolic():
			return self.timeOfPeriapsisPassage + M / self.meanMotion();

		p = self.period();
	
		if self.timeOfPeriapsisPassage != None:
			t = self.timeOfPeriapsisPassage + p * math.floor((t0 - self.timeOfPeriapsisPassage) / p) + M / self.meanMotion();
		else:
			t = (t0 - (t0 % p)) + (M - self.meanAnomalyAtEpoch) / self.meanMotion();
		
	
		if (t < t0):
			return t + p
		else:
			return t

	def radiusAtTrueAnomaly(self, tA):
		e = self.eccentricity;
		return self.semiMajorAxis * (1 - e * e) / (1 + e * math.cos(tA))
	
	def altitudeAtTrueAnomaly(self, tA):
		return self.radiusAtTrueAnomaly(tA) - self.referenceBody.radius
	

	def speedAtTrueAnomaly(self, tA):
		return math.sqrt(self.referenceBody.gravitationalParameter * (2 / self.radiusAtTrueAnomaly(tA) - 1 / self.semiMajorAxis))
	

	def positionAtTrueAnomaly(self, tA):
		r = self.radiusAtTrueAnomaly(tA);
		q = self.rotationToReferenceFrame()
		print 'q',q
		v = q.rotate([r * math.cos(tA), r * math.sin(tA), 0])
		print 'v',v
		return v
	

	def velocityAtTrueAnomaly(self, tA):
		mu = self.referenceBody.gravitationalParameter;
		e = self.eccentricity;
		h = math.sqrt(mu * self.semiMajorAxis * (1 - e * e));
		r = self.radiusAtTrueAnomaly(tA);
		sin = math.sin(tA);
		cos = math.cos(tA);
		vr = mu * e * sin / h;
		vtA = h / r;
		return self.rotationToReferenceFrame().rotate([vr * cos - vtA * sin, vr * sin + vtA * cos, 0]);
	

	def trueAnomalyAtPosition(self, p):
		p = quaternion.rotate(quaternion.conjugate(self.rotationToReferenceFrame()), p)
		return math.atan2(p[1], p[0])
	
	
	def refineTransfer(transfer, transferType, originBody, destinationBody, t0, dt, initialOrbitalVelocity, finalOrbitalVelocity):

		if not initialOrbitalVelocity:
			return transfer;
		
		for i in range(10):
			if (isNaN(transfer.deltaV)):
				return transfer;
			
			if (transfer.ejectionAngle == None):
				transfer = Orbit.transferDetails(transfer, originBody, t0, initialOrbitalVelocity);
			
			mu = originBody.gravitationalParameter;
			rsoi = originBody.sphereOfInfluence;	
			vsoi = np.linalg.norm(transfer.ejectionDeltaVector);		
			v1 = math.sqrt(vsoi * vsoi + 2 * initialOrbitalVelocity * initialOrbitalVelocity - 2 * mu / rsoi);	
			initialOrbitRadius = mu / (initialOrbitalVelocity * initialOrbitalVelocity);	
			e = initialOrbitRadius * v1 * v1 / mu - 1;
			a = initialOrbitRadius / (1 - e);
			nu = math.acos((a * (1 - e * e) - rsoi) / (e * rsoi));
			originOrbit = originBody.orbit;
			prograde = originOrbit.velocityAtTrueAnomaly(originOrbit.trueAnomalyAt(t0));
			longitudeOfAscendingNode = math.atan2(prograde[1], prograde[0]) - transfer.ejectionAngle;
			argumentOfPeriapsis = 0;
		
			if (transfer.ejectionInclination < 0):
				longitudeOfAscendingNode -= math.PI;
				argumentOfPeriapsis = math.PI;

			while (longitudeOfAscendingNode < 0):
				longitudeOfAscendingNode += TWO_PI
			
			ejectionOrbit = Orbit(originBody, a, e, None, None, None, None, t0);
			ejectionOrbit.inclination = transfer.ejectionInclination;
			ejectionOrbit.longitudeOfAscendingNode = longitudeOfAscendingNode;
			ejectionOrbit.argumentOfPeriapsis = argumentOfPeriapsis;
			t1 = ejectionOrbit.timeAtTrueAnomaly(nu, t0);
			dtFromSOI = dt - (t1 - t0);
			originTrueAnomalyAtSOI = originOrbit.trueAnomalyAt(t1);
			p1 = numeric.addVV(ejectionOrbit.positionAtTrueAnomaly(nu), originOrbit.positionAtTrueAnomaly(originTrueAnomalyAtSOI));
			originVelocityAtSOI = originOrbit.velocityAtTrueAnomaly(originTrueAnomalyAtSOI);
			orbit = Orbit.fromPositionAndVelocity(originOrbit.referenceBody, p1, originVelocityAtSOI, t1);
			
			tempBody = CelestialBody(None, None, None, orbit);
			transfer = Orbit.transfer(transferType, tempBody, destinationBody, t1, dtFromSOI, 0, finalOrbitalVelocity, p1, originVelocityAtSOI);
			
			if (i & 1):
				lastEjectionDeltaVector = transfer.ejectionDeltaVector;
			else:
				transfer.ejectionDeltaVector = numeric.mulSV(0.5, numeric.addVV(lastEjectionDeltaVector, transfer.ejectionDeltaVector));
				transfer.ejectionDeltaV = np.linalg.norm(transfer.ejectionDeltaVector);
			
			transfer.orbit = Orbit.fromPositionAndVelocity(originOrbit.referenceBody, p1, transfer.ejectionVelocity, t1);
			transfer.ejectionDeltaV = circularToEscapeDeltaV(originBody, initialOrbitalVelocity, transfer.ejectionDeltaV, transfer.ejectionInclination);
			transfer.deltaV = transfer.ejectionDeltaV + transfer.planeChangeDeltaV + transfer.insertionDeltaV;
		
		return transfer;
	

	def courseCorrection(transferOrbit, destinationOrbit, burnTime, eta):

		mu = transferOrbit.referenceBody.gravitationalParameter;
		trueAnomaly = transferOrbit.trueAnomalyAt(burnTime);
		p0 = transferOrbit.positionAtTrueAnomaly(trueAnomaly);
		v0 = transferOrbit.velocityAtTrueAnomaly(trueAnomaly);
		n0 = transferOrbit.normalVector();
		n1 = destinationOrbit.normalVector();

		velocityForArrivalAt = lambda t1: lambert(mu, p0, destinationOrbit.positionAtTrueAnomaly(destinationOrbit.trueAnomalyAt(t1)), t1 - burnTime)[0][0]
	
		t1Min = math.max(0.5 * (eta - burnTime), 3600);
		t1Max = 1.5 * (eta - burnTime);
		
		t1 = goldenSectionSearch(
				lambda t1:np.linalg.normSquared(numeric.subVV(velocityForArrivalAt(burnTime + t1), v0)),
				brack = (t1Min, t1Max),
				tol = 1e-4
				)
		
		t1 = t1 + burnTime;
		correctedVelocity = velocityForArrivalAt(t1);
		deltaVector = numeric.subVV(correctedVelocity, v0);
		deltaV = np.linalg.norm(deltaVector);
		burnDirection = numeric.divVS(deltaVector, deltaV);
		positionDirection = numeric.divVS(p0, np.linalg.norm(p0));
		pitch = math.asin(numeric.dotVV(burnDirection, positionDirection));
		heading = angleInPlane([0, 0, 1], burnDirection, positionDirection);
		progradeDirection = numeric.divVS(v0, np.linalg.norm(v0));
		progradeDeltaV = numeric.dotVV(deltaVector, progradeDirection);
		normalDeltaV = numeric.dotVV(deltaVector, n0);
		radialDeltaV = math.sqrt(deltaV * deltaV - progradeDeltaV * progradeDeltaV - normalDeltaV * normalDeltaV);

		if (numeric.dotVV(crossProduct(burnDirection, progradeDirection), n0) < 0):
			radialDeltaV = -radialDeltaV;
		
		return {
			correctedVelocity: correctedVelocity,
			deltaVector: deltaVector,
			deltaV: deltaV,
			pitch: pitch,
			heading: heading,
			progradeDeltaV: progradeDeltaV,
			normalDeltaV: normalDeltaV,
			radialDeltaV: radialDeltaV,
			arrivalTime: t1
		}

def fromApoapsisAndPeriapsis(referenceBody, apoapsis, periapsis, inclination, longitudeOfAscendingNode, argumentOfPeriapsis, meanAnomalyAtEpoch, timeOfPeriapsisPassage):

	if (apoapsis < periapsis):
		periapsis, apoapsis = apoapsis, periapsis

	semiMajorAxis = (apoapsis + periapsis) / 2;
	eccentricity = apoapsis / semiMajorAxis - 1;
	return Orbit(referenceBody, semiMajorAxis, eccentricity, inclination, longitudeOfAscendingNode, argumentOfPeriapsis, meanAnomalyAtEpoch, timeOfPeriapsisPassage);
	

def fromPositionAndVelocity(referenceBody, position, velocity, t):

	mu = referenceBody.gravitationalParameter;
	r = np.linalg.norm(position);
	v = np.linalg.norm(velocity);
	specificAngularMomentum = crossProduct(position, velocity);
	
	if specificAngularMomentum[0] != 0 or specificAngularMomentum[1] != 0:
		nodeVector = normalize([-specificAngularMomentum[1], specificAngularMomentum[0], 0]);
	else:
		nodeVector = [1, 0, 0];
	
	eccentricityVector = numeric.mulSV(1 / mu, numeric.subVV(numeric.mulSV(v * v - mu / r, position), numeric.mulSV(numeric.dotVV(position, velocity), velocity)));
	semiMajorAxis = 1 / (2 / r - v * v / mu);
	eccentricity = np.linalg.norm(eccentricityVector);
	orbit = Orbit(referenceBody, semiMajorAxis, eccentricity);
	orbit.inclination = math.acos(specificAngularMomentum[2] / np.linalg.norm(specificAngularMomentum));
	
	if eccentricity == 0:
		orbit.argumentOfPeriapsis = 0;
		orbit.longitudeOfAscendingNode = 0;
	else:
		orbit.longitudeOfAscendingNode = math.acos(nodeVector[0])
	
		if (nodeVector[1] < 0):
			orbit.longitudeOfAscendingNode = TWO_PI - orbit.longitudeOfAscendingNode;
	
		orbit.argumentOfPeriapsis = math.acos(numeric.dotVV(nodeVector, eccentricityVector) / eccentricity);
		
		if (eccentricityVector[2] < 0):
			orbit.argumentOfPeriapsis = TWO_PI - orbit.argumentOfPeriapsis;
	
	trueAnomaly = math.acos(numeric.dotVV(eccentricityVector, position) / (eccentricity * r));
	
	if (numeric.dotVV(position, velocity) < 0):
		trueAnomaly = -trueAnomaly;
	
	meanAnomaly = orbit.meanAnomalyAtTrueAnomaly(trueAnomaly);
	orbit.timeOfPeriapsisPassage = t - meanAnomaly / orbit.meanMotion();
	return orbit;
	

def circularToEscapeDeltaV(body, v0, vsoi, relativeInclination):

	mu = body.gravitationalParameter;
	rsoi = body.sphereOfInfluence;
	v1 = math.sqrt(vsoi * vsoi + 2 * v0 * v0 - 2 * mu / rsoi);
	r0 = mu / (v0 * v0);
	e = r0 * v1 * v1 / mu - 1;
	ap = r0 * (1 + e) / (1 - e);
	
	if ap > 0 and ap <= rsoi:
		return math.nan
	
	if (relativeInclination):
		return math.sqrt(v0 * v0 + v1 * v1 - 2 * v0 * v1 * math.cos(relativeInclination));
	else:
		return v1 - v0
	
	

def insertionToCircularDeltaV(body, vsoi, v0):
	mu = body.gravitationalParameter
	rsoi = body.sphereOfInfluence
	return math.sqrt(vsoi * vsoi + 2 * v0 * v0 - 2 * mu / rsoi) - v0
	

def ejectionAngle(vsoi, theta, prograde):
	_ref = normalize(vsoi)
	ax = _ref[0], ay = _ref[1], az = _ref[2]

	cosTheta = math.cos(theta);
	g = -ax / ay;
	a = 1 + g * g;
	b = 2 * g * cosTheta / ay;
	c = cosTheta * cosTheta / (ay * ay) - 1;

	if (b < 0):
		q = -0.5 * (b - Math.sqrt(b * b - 4 * a * c));
	else:
		q = -0.5 * (b + Math.sqrt(b * b - 4 * a * c));

	vx = q / a;
	vy = g * vx + cosTheta / ay;
	
	if (sign(crossProduct([vx, vy, 0], [ax, ay, az])[2]) != sign(Math.PI - theta)):
		vx = c / q
		vy = g * vx + cosTheta / ay
	
	prograde = [prograde[0], prograde[1], 0];
	
	if crossProduct([vx, vy, 0], prograde)[2] < 0:
		return TWO_PI - math.acos(numeric.dotVV([vx, vy, 0], prograde))
	else:
		return math.acos(numeric.dotVV([vx, vy, 0], prograde))
	

## Create a transfer
# @param transferType string. "optimal",
# @dt something to do with time of flight
def transfer(transferType, originBody, destinationBody, t0, dt, initialOrbitalVelocity, finalOrbitalVelocity, p0 = None, v0 = None, n0 = None, p1 = None, v1 = None, planeChangeAngleToIntercept = None):
	planeChangeAngle = None
	
	referenceBody = originBody.orbit.referenceBody;
	t1 = t0 + dt;
	
	if not (p0 != None and v0 != None):
		nu0 = originBody.orbit.trueAnomalyAt(t0);
		if (p0 == None):
			p0 = originBody.orbit.positionAtTrueAnomaly(nu0);
			print 'p0',p0
		
		if (v0 == None):
			v0 = originBody.orbit.velocityAtTrueAnomaly(nu0);
	
	if not ((p1 != None) and (v1 != None)):
		nu1 = destinationBody.orbit.trueAnomalyAt(t1)
		if (p1 == None):
			p1 = destinationBody.orbit.positionAtTrueAnomaly(nu1)
		
		if (v1 == None):
			v1 = destinationBody.orbit.velocityAtTrueAnomaly(nu1)
	
	
	if (n0 == None):
		n0 = originBody.orbit.normalVector();
	
	if (transferType == "optimal"):
		ballisticTransfer = transfer("ballistic", originBody, destinationBody, t0, dt, initialOrbitalVelocity, finalOrbitalVelocity, p0, v0, n0, p1, v1);
		if (ballisticTransfer.angle <= HALF_PI):
			return ballisticTransfer;
		
		planeChangeTransfer = transfer("optimalPlaneChange", originBody, destinationBody, t0, dt, initialOrbitalVelocity, finalOrbitalVelocity, p0, v0, n0, p1, v1);
		
		if (ballisticTransfer.deltaV < planeChangeTransfer.deltaV):
			return ballisticTransfer;
		else:
			return planeChangeTransfer;
		
	elif (transferType == "optimalPlaneChange"):
		if (np.linalg.norm(p0) > np.linalg.norm(p1)):
			x1 = HALF_PI;
			x2 = math.PI;
		else:
			x1 = 0;
			x2 = HALF_PI;
	
		relativeInclination = math.asin(numeric.dotVV(p1, n0) / np.linalg.norm(p1));
		planeChangeRotation = quaternion.fromAngleAxis(-relativeInclination, crossProduct(p1, n0));
		p1InOriginPlane = quaternion.rotate(planeChangeRotation, p1);
		v1InOriginPlane = quaternion.rotate(planeChangeRotation, v1);
		ejectionVelocity = lambert(referenceBody.gravitationalParameter, p0, p1InOriginPlane, dt)[0][0];
		orbit = Orbit.fromPositionAndVelocity(referenceBody, p0, ejectionVelocity, t0);
		trueAnomalyAtIntercept = orbit.trueAnomalyAtPosition(p1InOriginPlane);
		

		x = goldenSectionSearch(x1, x2, 1e-2,
				lambda x: math.abs(2 * orbit.speedAtTrueAnomaly(trueAnomalyAtIntercept - x) * math.sin(0.5 * math.atan2(math.tan(relativeInclination), math.sin(x))))
				)

		planeChangeAngle = math.atan2(math.tan(relativeInclination), math.sin(x));
		planeChangeAxis = quaternion.rotate(quaternion.fromAngleAxis(-x, n0), projectToPlane(p1, n0));
		planeChangeRotation = quaternion.fromAngleAxis(planeChangeAngle, planeChangeAxis);
		p1InOriginPlane = quaternion.rotate(planeChangeRotation, p1);
		v1InOriginPlane = quaternion.rotate(planeChangeRotation, v1);
		ejectionVelocity = lambert(referenceBody.gravitationalParameter, p0, p1InOriginPlane, dt)[0][0];
		orbit = Orbit.fromPositionAndVelocity(referenceBody, p0, ejectionVelocity, t0);
		trueAnomalyAtIntercept = orbit.trueAnomalyAtPosition(p1InOriginPlane);
		
		x = goldenSectionSearch(x1, x2, 1e-2,
				lambda x: math.abs(2 * orbit.speedAtTrueAnomaly(trueAnomalyAtIntercept - x) * math.sin(0.5 * math.atan2(math.tan(relativeInclination), math.sin(x))))
				)

		return Orbit.transfer("planeChange", originBody, destinationBody, t0, dt, initialOrbitalVelocity, finalOrbitalVelocity, p0, v0, n0, p1, v1, x)

	elif transferType == "planeChange":
		if (planeChangeAngleToIntercept == None):
			planeChangeAngleToIntercept = HALF_PI
	
		relativeInclination = math.asin(numeric.dotVV(p1, n0) / np.linalg.norm(p1))
		planeChangeAngle = math.atan2(math.tan(relativeInclination), math.sin(planeChangeAngleToIntercept))
		
		if (planeChangeAngle != 0):
			planeChangeAxis = quaternion.rotate(quaternion.fromAngleAxis(-planeChangeAngleToIntercept, n0), projectToPlane(p1, n0))
			planeChangeRotation = quaternion.fromAngleAxis(planeChangeAngle, planeChangeAxis)
			p1InOriginPlane = quaternion.rotate(quaternion.conjugate(planeChangeRotation), p1)
	

	print p0, p1
	transferAngle = math.acos(np.dot(p0, p1) / (np.linalg.norm(p0) * np.linalg.norm(p1)));

	if (p0[0] * p1[1] - p0[1] * p1[0] < 0):
		transferAngle = TWO_PI - transferAngle
	

	if (not planeChangeAngle) or (transferAngle <= HALF_PI):
		solutions = lambert(referenceBody.gravitationalParameter, p0, p1, dt, 10);
		minDeltaV = Infinity;
		for _i in range(solutions.length):
			s = solutions[_i];
			dv = np.linalg.norm(numeric.subVV(s[0], v0));

			#if (typeof finalOrbitVelocity != "undefined" and finalOrbitVelocity != None):
			if finalOrbitVelocity:
				dv += np.linalg.norm(numeric.subVV(s[1], v1));
		
			if dv < minDeltaV:
				minDeltaV = dv;
				ejectionVelocity = s[0], insertionVelocity = s[1], transferAngle = s[2];
		
		
			planeChangeDeltaV = 0;
	else:
		_ref = lambert(referenceBody.gravitationalParameter, p0, p1InOriginPlane, dt)[0]
		ejectionVelocity = _ref[0]
		insertionVelocity = _ref[1]

		orbit = Orbit.fromPositionAndVelocity(referenceBody, p0, ejectionVelocity, t0);
		planeChangeTrueAnomaly = orbit.trueAnomalyAt(t1) - planeChangeAngleToIntercept;
		planeChangeDeltaV = math.abs(2 * orbit.speedAtTrueAnomaly(planeChangeTrueAnomaly) * math.sin(planeChangeAngle / 2));
		
		if (isNaN(planeChangeDeltaV)):
			planeChangeDeltaV = 0;
			
		planeChangeTime = orbit.timeAtTrueAnomaly(planeChangeTrueAnomaly, t0);
		insertionVelocity = quaternion.rotate(planeChangeRotation, insertionVelocity);
		
		
	ejectionDeltaVector = numeric.subVV(ejectionVelocity, v0);
	ejectionDeltaV = np.linalg.norm(ejectionDeltaVector);
	ejectionInclination = math.asin(ejectionDeltaVector[2] / ejectionDeltaV);

	if initialOrbitalVelocity:
		ejectionDeltaV = circularToEscapeDeltaV(originBody, initialOrbitalVelocity, ejectionDeltaV, ejectionInclination);
		
	if finalOrbitalVelocity:
		insertionDeltaVector = insertionVelocity - v1
		insertionDeltaV = np.linalg.norm(insertionDeltaVector);
		insertionInclination = math.asin(insertionDeltaVector[2] / insertionDeltaV);
		if finalOrbitalVelocity:
			insertionDeltaV = insertionToCircularDeltaV(destinationBody, insertionDeltaV, finalOrbitalVelocity)
	else:
		insertionDeltaV = 0;
		
	return {
		angle: transferAngle,
		orbit: orbit,
		ejectionVelocity: ejectionVelocity,
		ejectionDeltaVector: ejectionDeltaVector,
		ejectionInclination: ejectionInclination,
		ejectionDeltaV: ejectionDeltaV,
		planeChangeAngleToIntercept: planeChangeAngleToIntercept,
		planeChangeDeltaV: planeChangeDeltaV,
		planeChangeTime: planeChangeTime,
		planeChangeAngle: planeChangeAngle if planeChangeTime != None else 0,
		insertionVelocity: insertionVelocity,
		insertionInclination: insertionInclination,
		insertionDeltaV: insertionDeltaV,
		deltaV: ejectionDeltaV + planeChangeDeltaV + insertionDeltaV
		}
	

	

def transferDetails(trans, originBody, t0, initialOrbitalVelocity):

	referenceBody = originBody.orbit.referenceBody;
	nu0 = originBody.orbit.trueAnomalyAt(t0);
	p0 = originBody.orbit.positionAtTrueAnomaly(nu0);
	v0 = originBody.orbit.velocityAtTrueAnomaly(nu0);

	#_ref = transfer.orbit

	if (trans.orbit == None):
		trans.orbit = Orbit.fromPositionAndVelocity(referenceBody, p0, trans.ejectionVelocity, t0);
	
	ejectionDeltaVector = transfer.ejectionDeltaVector;
	ejectionInclination = transfer.ejectionInclination;
	
	if (initialOrbitalVelocity):
		mu = originBody.gravitationalParameter;
		rsoi = originBody.sphereOfInfluence;
		vsoi = np.linalg.norm(ejectionDeltaVector);
		v1 = math.sqrt(vsoi * vsoi + 2 * initialOrbitalVelocity * initialOrbitalVelocity - 2 * mu / rsoi);
		transfer.ejectionNormalDeltaV = v1 * math.sin(ejectionInclination);
		transfer.ejectionProgradeDeltaV = v1 * math.cos(ejectionInclination) - initialOrbitalVelocity;
		transfer.ejectionHeading = math.atan2(transfer.ejectionProgradeDeltaV, transfer.ejectionNormalDeltaV);
		initialOrbitRadius = mu / (initialOrbitalVelocity * initialOrbitalVelocity);
		e = initialOrbitRadius * v1 * v1 / mu - 1;
		a = initialOrbitRadius / (1 - e);
		theta = math.acos((a * (1 - e * e) - rsoi) / (e * rsoi));
		theta += math.asin(v1 * initialOrbitRadius / (vsoi * rsoi));
		transfer.ejectionAngle = ejectionAngle(ejectionDeltaVector, theta, normalize(v0));
	else:
		ejectionDeltaV = transfer.ejectionDeltaV

		positionDirection = p0 / np.linalg.norm(p0)
		progradeDirection = v0 / np.linalg.norm(v0)

		n0 = originBody.orbit.normalVector()

		burnDirection = numeric.divVS(ejectionDeltaVector, ejectionDeltaV);
		transfer.ejectionPitch = math.asin(numeric.dotVV(burnDirection, positionDirection));
		transfer.ejectionHeading = angleInPlane([0, 0, 1], burnDirection, positionDirection);
		progradeDeltaV = numeric.dotVV(ejectionDeltaVector, progradeDirection);
		normalDeltaV = numeric.dotVV(ejectionDeltaVector, n0);
		radialDeltaV = math.sqrt(ejectionDeltaV * ejectionDeltaV - progradeDeltaV * progradeDeltaV - normalDeltaV * normalDeltaV);
		if (numeric.dotVV(crossProduct(burnDirection, progradeDirection), n0) < 0):
			radialDeltaV = -radialDeltaV;
		
		transfer.ejectionProgradeDeltaV = progradeDeltaV;
		transfer.ejectionNormalDeltaV = normalDeltaV;
		transfer.ejectionRadialDeltaV = radialDeltaV;
	
	return transfer;



