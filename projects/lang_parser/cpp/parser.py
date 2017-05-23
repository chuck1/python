import re
import logging

from Chunk import *
from Scope_Key import *

# TODO make Scope key start a tuple (like key end is) to determine if starting word should be reprocessed in new chunk
# TODO hide terminator in printout

## generators

def gen_namespace(c):
    for l in c.keep:
        if isinstance(l, Namespace):
            yield l
        elif isinstance(l, PreProc):
            for l2 in gen_namespace(l):
                yield l2

def gen_class(c):
    for l in c.keep:
        if isinstance(l, Class):
            yield l
        elif isinstance(l, PreProc):
            for l2 in gen_class(l):
                yield l2
        elif isinstance(l, NamespaceBody):
            for l2 in gen_class(l):
                yield l2

def gen_full(c):
    for cl in gen_class(c):
        yield [cl.name()]
    
    for ns in gen_namespace(c):
        for s in gen_full(ns):
            yield [ns.name()] + s


# main process function

def process(c):
	#term = terminator_dict[c.code]
	
	# if chunk has a starter, then it was created by another call to process and we should therefore scan for an initiator
	#c.scan_start()
	
	print c.words
	
	# do until all words are poped
	while c.words:
		# pop words until starter is found
		word = c.words.pop(0)
		logging.debug("%r" % word)
		

		key = classify(word)
		#print "key={0}".format(key)
		#print "end={0}".format(c.scope.list_key_end)

                        #print '    word =',repr(word)
		#print '    key =',repr(key)
		
		# child
		scope = key_in_scope_start(key, c.scope.list_scope_child)
		if scope:
                        #print "creating chunk",scope.name
			# create new chunk
                        if scope.name == 'ns':
                            new_chunk = Namespace(c, c.words, scope)
                        elif scope.name == 'ns body':
                            new_chunk = NamespaceBody(c, c.words, scope)
                        elif scope.name == 'class':
                            new_chunk = Class(c, c.words, scope)
                        elif scope.name == 'class body':
                            new_chunk = ClassBody(c, c.words, scope)
                        elif scope.name == 'preproc ifndef':
                            new_chunk = PreProc(c, c.words, scope)
                        elif scope.name == 'function':
                            new_chunk = Function(c, c.words, scope)
                        elif scope.name == 'function body':
                            new_chunk = FunctionBody(c, c.words, scope)
                        elif scope.name == 'function params':
                            new_chunk = FunctionParams(c, c.words, scope)
                        elif scope.name == 'object member':
                            new_chunk = ObjectMember(c, c.words, scope)
                        else:
                            new_chunk = Chunk(c, c.words, scope)
			
			
                        #new_chunk.keep.append(word)
                        new_chunk.words = [word] + new_chunk.words


			#print "word"
			#print word
			#print "words"
			#print c.words
			#print "keep"
			#print c.keep
			#print new_chunk.keep


			c.words = process(new_chunk)
										
			c.keep.append(new_chunk)
				
			continue
		
		# end
		for k,b in c.scope.list_key_end: #if term != 0:
                        #print "end",repr(k),repr(b),repr(key)
                        if key:
			    if key[1] == k:
				
				# immediate terminator
				#if term == 1:
				#	ret = c.words
				#	ret.insert(0,word)
				#	c.words = []
				#	return ret
				# return what was not used
				#if word == term:

				# keep or return the end word?
				if b:
					c.keep.append(word)
                                        #pass
				else:
					c.words.insert(0,word)
				
				# return all unused words
				ret = c.words
				c.words = []
				
				return ret
		
		# if word is neither a start nor an end, keep it
		c.keep.append(word)
		
	return []


def classify(word):
    logging.debug("classify")
    for k,v in sorted(list_key.items()):
        logging.debug(repr(k),repr(word))
	if v.test(word):
	    logging.debug("{0} is a '{1}' key".format(repr(word),v.name))
	    return k

    return None

def get_buffer():
	word_list = []

	cb = vim.current.buffer
	
	for i in range(0,len(cb)):
		line = cb[i]
		#print line
		word_list.append(line+'\n')
	
	return word_list

def fragment(list_word, string_pattern):
	pat = re.compile(string_pattern)
	
	list_word_frag = []
	
	for word in list_word:
		list_subword = pat.split(word)
		#for subword in list_subword:
		#	list_word_frag.append(subword)
		list_word_frag += list_subword
		
	return list_word_frag
	
def nullstring(x):
	if x == '':
		return False
	return True

def remove_white(words):
    nwords = []
    for w in words:
        #if w in ['','\n']:
        if w in ['']:
            pass
        else:
            nwords.append(w)
    
    return nwords


def reformat():
	list_word = get_buffer();
	#print list_word
	
	list_word = fragment(list_word, "[\t\ ]+")
	#print list_word
	
	list_word = fragment(list_word, "([\n{};])")
	#print list_word
	
	list_word = filter(nullstring,list_word)
	print list_word

	
	# global chunk
	gchunk = Chunk(list_word)
	gchunk.process()
	
	
	#print_chunk(gchunk,"",0)
	print '%%%'
	gchunk.cprint()
        print '%%%'
	print gchunk.keep


def preprocess(lines):
        lines = fragment(lines, "[\t\ ]+")
	
	lines = fragment(lines, "([\n{}\(\);,])")

        lines = fragment(lines, "(?<!:)(:)(?!:)")

        lines = remove_white(lines)

        return lines














