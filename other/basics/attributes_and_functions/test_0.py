

class Foo(object):

	def a(self):
		print 'a'
		
	def __setattr__(self, name, value):
		print 'setattr',name
		object.__setattr__(self, name, value)

		
f = Foo()

f.a()
f.b = 1

print f.b

f.a = 1
f.a

raw_input()

