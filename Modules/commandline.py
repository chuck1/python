import re
import sys

def invalid(arg):
	print "invalid argument: {0}".format(arg)

class Arg:
	def __init__(self,short):
		self.short = short
		self.isset = False
		self.values = []
		self.id = -1
		
class commandline:
	def __init__(self, argv, args):
		self.argv = list(argv)	
		self.program = self.argv.pop(0)

		self.free = []

		self.args = args
		
		self.lastarg = None
		
		self.process()

	
	def process(self):
		while self.argv:
			string = self.argv.pop(0)
			
			#print string
			#print len(string)
			
			if len(string) > 1:
				print string[0:2]
				if string[0:2] == '--':
					if len(string) == 2:
						invalid(string)
						continue
					
					if self.process_long(string):
						continue
					else:
						continue
			
			if string[0] == '-':
				if len(string) == 1:
					invalid(string)
					sys.exit(0)
				
				
				if self.process_shorts(string):
					continue
				else:
					sys.exit(0)

			
			print "value: {0}".format(string)
			
			if self.lastarg:
				self.args[self.lastarg].values.append(string)
			else:
				self.free.append(string)

			

	def process_long(self, string):
		string = string[2:len(string)]

		#print string
	
		for long, arg in self.args.items():
			#print long
			
			if string == long:
				arg.isset = True
				
				self.lastarg = string
				print "long argument: {0}".format(string)

				return True

		print "invalid long argument: {0}".format(string)
		return False
	
	def process_shorts(self, string):
		r = True
		
		for i in range(1,len(string)):
			if not self.process_short(string[i]):
				r = False
				break
		
		return r
	
	
	def process_short(self, string):
		for long, arg in self.args.items():
			if string == arg.short:
				arg.isset = True
		
				self.lastarg = long
				print "short argument: {0}".format(string)
				
				return True
		
		print "invalid short argument: {0}".format(string)
		return False







