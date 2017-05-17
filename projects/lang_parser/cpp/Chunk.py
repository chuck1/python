from Scope_Key import *

import colors

class Chunk:
	def __init__(self, parent, words, scope=scope_none):

                #print 'words:'
                #for w in words:
                #    print '   ',repr(w)

                self.parent = parent
                self.words = words
		self.keep = []
		self.scope = scope

	def __str__(self):
		return colors.draw(self.__class__.__name__+" "+self.scope.name, fg_blue=True)

        def printvar(self,prefix=''):
            #print 'words:'
            #print self.words

            #if self.scope:
            #    print prefix+'scope:', self.scope.name
            #else:
            #    print prefix+'scope:', self.scope

            #print prefix+'keep:'

            temp = []

            for k in self.keep:
                if isinstance(k,Chunk):

                    if temp:
                        print prefix + repr(" ".join(temp))
                        temp = []

                    print prefix+str(k)
                    k.printvar(prefix+'\t')
                else:
                    if k != '\n':
	                    #print prefix + repr(k)
                            temp.append(k)

            if temp:
                print prefix + repr(" ".join(temp))

#	def scan_start(self):
#		ret = []
#		if self.scope.list_key_start:
#			while self.words:
#				w = self.words.pop(0)
#				
#				k = classify(w)
#				
#				# terminator
#				if k in self.scope.list_key_start:
#					self.keep.append(w)
#					return ret
#				
#				# discard
#				#if any(w == s for s in discard):
#				#	continue
#				# neutral
#				self.keep.append(w)


        def gen_chunks(self):
            for k in self.keep:
                if isinstance(k,Chunk):
                    yield k

	def cprint(self,prefix=''):
		#print self.keep

		keep = self.keep
		
		string = ''
		
		while keep:
			word = keep.pop(0)
			
			
			if isinstance(word,Chunk):
				if string != '':
					print prefix+string
					string = ''
				
				word.cprint(prefix+'\t')
			elif word == '\n':
				if string != '':
					print prefix+string
					string = ''

			else:
				string += word
		
		
		if string != '':
			print prefix+string
			string = ''
	
class Namespace(Chunk):
	def __init__(self, parent, words, scope=scope_none):
            Chunk.__init__(self, parent, words, scope)
	def __str__(self):
		return colors.draw(self.__class__.__name__, fg_blue=True)

        def name(self):
            return self.keep[1]

class NamespaceBody(Chunk):
	def __init__(self, parent, words, scope=scope_none):
            Chunk.__init__(self, parent, words, scope)
	def __str__(self):
		return colors.draw(self.__class__.__name__, fg_blue=True)

class Class(Chunk):
	def __init__(self, parent, words, scope=scope_none):
            Chunk.__init__(self, parent, words, scope)
	def __str__(self):
		return colors.draw(self.__class__.__name__, fg_blue=True)

        def name(self):
            return self.keep[1]

class ClassBody(Chunk):
	def __init__(self, parent, words, scope=scope_none):
            Chunk.__init__(self, parent, words, scope)
	def __str__(self):
		return colors.draw(self.__class__.__name__, fg_blue=True)

class PreProc(Chunk):
	def __init__(self, parent, words, scope=scope_none):
            Chunk.__init__(self, parent, words, scope)
	def __str__(self):
		return colors.draw(self.__class__.__name__, fg_blue=True)

class Function(Chunk):
	def __init__(self, parent, words, scope=scope_none):
            Chunk.__init__(self, parent, words, scope)
	def __str__(self):
		return colors.draw(self.__class__.__name__ + " " + self.name(), fg_blue=True)
	def name(self):
		# get everything before the FunctionParams
		temp = []
		for k in self.keep:
			if isinstance(k, FunctionParams):
				break
			temp.append(k)
		
		#s = re.split('::', self.keep[0])
		#return str(s)
		#return self.keep[0]

		return " ".join(temp)

class FunctionBody(Chunk):
	def __init__(self, parent, words, scope=scope_none):
            Chunk.__init__(self, parent, words, scope)
	def __str__(self):
		return colors.draw(self.__class__.__name__, fg_blue=True)

class FunctionParams(Chunk):
	def __init__(self, parent, words, scope=scope_none):
            Chunk.__init__(self, parent, words, scope)
	def __str__(self):
		return colors.draw(self.__class__.__name__, fg_blue=True)

class ObjectMember(Chunk):
	def __init__(self, parent, words, scope=scope_none):
            Chunk.__init__(self, parent, words, scope)
	def __str__(self):
		temp = self.__class__.__name__ + " obj=" + repr(self.obj()) + " member=" + repr(self.mbr())

		return colors.draw(temp, fg_blue=True)
	def obj(self):
		w = self.keep[0]
		s = w.split('.')
		return s[0]
	def mbr(self):
		w = self.keep[0]
		s = w.split('.')
		return s[1]



class ChunkNone(Chunk):
	def __init__(self, parent, words, scope=scope_none):
            Chunk.__init__(self, parent, words, scope)
	def __str__(self):
		return colors.draw(self.__class__.__name__, fg_blue=True)



