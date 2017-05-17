import re

head = ''

def scan1(t,ch):
	pat = '^.*?' + ch
	m = re.search(pat,t)
	
	if m:
		h = t[:m.end(0)]
		t = t[m.end(0):]
	else:
		h = ''

	return h,t

def scan(t,o,c):
	pat = '^[^' + o + ']*?' + c
	m = re.search(pat,t)
	
	if m:
		h = t[:m.end(0)]
		t = t[m.end(0):]
		return h,t
	
	m = re.search('^.*?' + o,t)
	
	if m:
		h = t[:m.end(0)]
		t = t[m.end(0):]
		h2,t = scan(t,o,c)
		h3,t = scan(t,o,c)
		h += h2 + h3
		return h,t
	
	print pat
	print t
	
def block(t,o,c):
	m = re.search(o,t)
	
	if m:
		h = t[:m.end(0)]
		t = t[m.end(0):]
		
		b,t = scan(t,o,c)	
	else:
		h = ''
		b = ''

	def debug():
		print repr(h)
		print repr(b)
		print repr(t)

	debug()

	return h,b,t

def prep(filename):
	with open(filename,'r') as f:
		lines = f.readlines()

	lines = [l for l in lines if l[0] != '#']

	t = ''.join(lines)

	t = t.replace('\n','')
	t = t.replace('\t','')

	return t

def next_word(t):
	m = re.search('[^ ]+',t)
	
	if m:
		h = t[:m.start(0)]
		b = t[m.start(0):m.end(0)]
		t = t[m.end(0):]
	else:
		h = ''
		b = ''
	
	
	def debug():
		print repr(h)
		print repr(b)
		print repr(t)

	debug()

	return h,b,t

####################################

classes = []
namespaces = []

####################################

tail = prep('test.h')

head,body,tail = next_word(tail)

while body:
	if body == 'class':
		h,b,t = block(tail,'{','}')
		
		name = h[:-1]
		name = name.strip()
		print 'name',repr(name)
		
		e,tail = scan1(t,';')
		print 'end',repr(e)
		print 'tail',repr(tail)
		
		classes.append(body + h + b + e)
	elif body == 'namespace':
		h,b,tail = block(tail,'{','}')
		
		namespaces.append(body + h + b)
	
	head,body,tail = next_word(tail)
	

print classes
print namespaces

