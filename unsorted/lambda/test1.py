
def lam():
	x = 0
	return lambda x=x,y=1: x

l = lam()

x = 1

print l()


