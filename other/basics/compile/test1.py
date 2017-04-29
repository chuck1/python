#!/usr/bin/env python3


def f(s):
	print(repr(s))
	try:
		c=compile(s,'<string>','eval')
	except Exception as e:
		print(e)
		return
	

	try:
		print(eval(c))
	except Exception as e:
		print(e)
	try:
		print(eval(c,{'__builtins__':{}}))
	except Exception as e:
		print(e)

f('import math')
f('__import__(\'math\')')
f('list([1,2,3])')
f('eval(\'2+2\')')

