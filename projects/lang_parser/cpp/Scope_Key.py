import re
import logging

def displaysearch(search):
	if search is None:
		return None
	return '<Search: %r, groups=%r>' % (search.group(), search.groups())

class Scope:
	def __init__(self, name, list_key_start, list_scope_child, list_key_end):
                #print 'scope __init__'
		self.name = name
		self.list_key_start = list_key_start

                # possible child scopes
                self.list_scope_child = list_scope_child

		self.list_key_end = list_key_end


class Key:
	def __init__(self, name, string_pattern, ):
                #print 'Key __init__'
		self.name = name
		self.string_pattern = string_pattern
		self.pattern = re.compile(string_pattern)
		
	def test(self, word):
		if self.pattern.match(word):
			return True

		return False

scope_none = Scope(
	'none',
	[],
	['preproc if','preproc ifndef','preproc include','function'],
	[]);

# class
scope_class = Scope(
	'class',
	['class'],
	['class body'],
	[('semicolon',True)])

scope_class_body = Scope(
	'class body',
	['curly open'],
	['class public','function'],
	[('curly close',True)])

scope_class_public = Scope(
		'class public',
		['public'],
		['function'],
		[('curly close',False)])

# ns
scope_ns = Scope(
	'ns',
	['ns'],
	['ns body'],
	[('curly close',True)])

# list_key_end:
#     pass curly close back to 'ns' to close 'ns'
scope_ns_body = Scope(
	'ns body',
	['curly open'],
	['ns','class'],
	[('curly close',False)])


# preproc

scope_preproc_if = Scope(
	'preproc if',	
	['preproc if'],
	['class','ns'],
	[('preproc endif',True)])


scope_preproc_ifndef = Scope(
	'preproc ifndef',
	['preproc ifndef'],
	['class','ns','preproc define'],
	[('preproc endif',True)])

scope_preproc_define = Scope(
	'preproc define',
	['preproc define'],
	[],
	[('newline',True)])

# function
scope_function = Scope(
	'function',
	['word','dtor','ns name'],
	['function body','function params'],
	[('curly close',True),('semicolon',True)])

scope_function_body = Scope(
	'function body',
	['curly open'],
	['function line'],
	[('curly close',False)])

scope_function_params = Scope(
	'function params',
	['paren open'],
	[],
	[('paren close',True)])

scope_function_line = Scope(
		'function_line',
		['word','object member'],
		['object member'],
		[('semicolon',True)])

# function line

scope_object_member = Scope(
		'object member',
		['object member'],
		[],
		[])

list_scope = {
	'class':		scope_class,
	'class body':		scope_class_body,
	'class public':		scope_class_public,
	'ns':	        	scope_ns,
	'ns body':		scope_ns_body,
	'preproc define':	scope_preproc_define,
	'preproc if':		scope_preproc_if,
	'preproc ifndef':	scope_preproc_ifndef,
	'preproc include':	Scope('preproc include',['preproc include'],[],[('newline',True)]),
	'preproc else':		Scope('preproc else',[],[],[]),
	'preproc elif':		Scope('preproc elif',[],[],[]),
	'preproc endif':	Scope('preproc endif',[],[],[]),
        'function':             scope_function,
        'function body':        scope_function_body,
        'function params':      scope_function_params,
        'function line':	scope_function_line,
	'object member':	scope_object_member,
        }




key_class = Key(
	'class',
	'class$')

key_ns = Key(
	'namespace',
	'namespace$')

key_semicolon = Key(
	'semicolon',
	';')

key_preproc_if = Key(
	'preproc if',	
	'#if$')

key_preproc_ifndef = Key(
	'preproc ifndef',
	'#ifndef$')

key_preproc_include = Key(
	'preproc include',
	'#include$')

list_key = {
        (0,'newline'):              Key('newline','^\n$'),
        (1,'class'):		key_class,
        (2,'ns'):                   key_ns,
	(3,'curly open'):		Key('curly open','{$'),
	(4,'curly close'):		Key('curly close','}$'),
	(5,'paren open'):		Key('paren open','\($'),
	(6,'paren close'):		Key('paren close','\)$'),
	(7,'semicolon'):		key_semicolon,
	(8,'preproc define'):	Key('preproc define','#define$'),
	(9,'preproc if'):		key_preproc_if,
	(10,'preproc ifndef'):	key_preproc_ifndef,
	(11,'preproc include'):	key_preproc_include,
	(12,'preproc else'):	Key('preproc else','#else$'),
	(13,'preproc elif'):	Key('preproc elif','#elif$'),
	(14,'preproc endif'):	Key('preproc endif','#endif$'),
	(15,'public'):		Key('public', 'public$'),
        (16,'word'):		Key('word','\w+$'),
        (17,'dtor'):		Key('dtor','~\w+'),
	(18,'object member'):	Key('object member','\w+\.\w+'),
	(19,'ns name'):		Key('ns name','\w+::\w+[::\w+]*$'),
        }
	

def key_in_scope_start(key, list_scope_):
        logging.debug('key_in_scope_start')
        logging.debug('    key =',repr(key))
        logging.debug('    list_scope_ =',list_scope_)

	for scope_name in list_scope_:
		scope = list_scope[scope_name]
		if key:
			if key[1] in scope.list_key_start:
				#print 'returning',scope
				return scope
	
	return None




