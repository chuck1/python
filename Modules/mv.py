import markdown
import argparse
import re
import os
import sys
import shutil
import logging

logging.basicConfig(level=logging.DEBUG)

def change_ext(path):
	
	root,ext = os.path.splitext(path)

	if ext == '.html':
		ext = '.md'
	elif ext == '.md':
		ext = '.html'
	

	return root + ext

def fix_links(md_file, src, dst):
	count = 0
	
	with open(md_file, 'r') as f:
		tail = f.read()
	
	# links are relative, so we need the dir of this file
	md_dir = os.path.dirname(md_file)
	
	logging.debug("fixing: {0}".format(repr(md_file)))
	
	# store processed string
	head = ''
	
	src2 = change_ext(src)
	
	src2_esc = src2.replace('/','\/')
	
	
	
	# prepare the destination
	dst2 = change_ext(dst)
	dst2_rel = os.path.relpath(dst2, md_dir)
	
	#str = '\[.*?\]\((' + src2_esc + ').*?\)' # for markdown
	pat = '#include <(' + src2_esc + ').*?>' # for cpp
	
	logging.debug("search: {0}".format(pat))
	
	match = re.search(pat, tail)
	while match:
		count += 1
		# search for links

		print "match in",repr(md_file)
		#print match.group(1)
		#print match.start(1)
		#print match.end(1)
		
		head += tail[:match.start(1)]
		
		head += dst

		tail = tail[match.end(1):]
		
		match = re.search(pat, tail)

	if count > 0:
	
		head += tail
	
		#print head

		with open(md_file, 'w') as f:
			f.write(head)

#####################

parser = argparse.ArgumentParser()
parser.add_argument('src')
parser.add_argument('dst')
args = parser.parse_args()

for root, dirs, files in os.walk('.'):
	for file in files:
		roo,ext = os.path.splitext(file)
		#if ext == '.md':
		if 1:
			path = os.path.join(root,file)
			path = os.path.normpath(path)
			#print path
			fix_links(path, args.src, args.dst)

dst_dir = os.path.dirname(args.dst)
if dst_dir:
	if not os.path.exists(dst_dir):
		 os.makedirs(dst_dir)


shutil.move(args.src, args.dst)

print "move {0} to {1}".format(repr(args.src),repr(args.dst))

