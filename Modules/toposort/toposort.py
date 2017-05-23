N = [1,2,3]
E = [[2,1],[3,1]]
L = []
S = []


for n in N:
	no_incoming = 1
	for e in E:
		#print "e",e
		if e[1] == n:
			no_incoming = 0
			break
	if no_incoming == 1:
		S.append(n)




#print N
#print S

while len(S) > 0:
	n = S.pop(0)
	L.append(n)
	for e in E:
		if e[0] == n:
			E.pop(E.index(e))
			m = e[1]
			no_other_incoming = 1
			for f in E:
				if f[0] != n and f[1] == m:
					no_other_incoming = 0
					break
			if no_other_incoming == 1:
				S.append(m)
				


print "L",L


