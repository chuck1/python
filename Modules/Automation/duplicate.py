import os
import re
import argparse
import shutil

import Automation
import Automation.Case

root = '/nfs/mohr/sva/work/rymalc/bin'

def ensure_dir(f):
	d = os.path.dirname(f)
	if not os.path.exists(d):
		os.makedirs(d)

def process_conf(parent, child):
	rel = os.path.relpath(child.path, root)
	#print "root",root
	#print "path",child.path
	#print "rel ",rel
	
	# first dir
	h,t = os.path.split(rel)
	h,t = os.path.split(h)
	#print "h,t",h,t
	
	src_ind = int(t[1:])
	
	dst_ind = Automation.next_id(os.path.join(root,h))
	
	# destination of copy
	dst = os.path.join(h, "x{0:04d}".format(dst_ind))
	
	src_abs = os.path.dirname(child.path)
	dst_abs = os.path.join(root,dst)
	
	print "copy {0} to {1}".format(repr(src_abs),repr(dst_abs))

	# copy child directory
	if not args.dryrun:
		ignore = shutil.ignore_patterns("build")
		shutil.copytree(src_abs, dst_abs, ignore=ignore)
	
	# change parent xmltree
	
	child.path = os.path.join(dst_abs,'config.xml')
	
	if parent:
		#print parent.root
		for inc in parent.root.findall('include'):
			dir = inc.attrib['dir']
			#print 'dir,h',repr(dir),repr(h)
			if dir == h:
				ind = int(inc.attrib['index'])
				if ind == src_ind:
					
					# change index
					inc.set('index', "{0}".format(dst_ind))
					
					#print 'index',ind
		
		print "save",repr(parent.path)
		if not args.dryrun:
			ensure_dir(parent.path)
			parent.tree.write(parent.path)
		
def walk_conf(parent, child, stop):
	
	process_conf(parent, child)
	
	for c in child.config:
		rel = os.path.relpath(c.path, root)
		if stop:
			if stop in rel:
				#print "stopping!"
				continue
		
		walk_conf(child, c, stop)

if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('src')
	parser.add_argument('--stop')
	parser.add_argument('--dryrun',action='store_true')
	args = parser.parse_args()
	
	if args.stop:
		stop = args.stop
	else:
		stop = 'Master'

	#print repr(args.src)
	
	abs = os.path.abspath(args.src)
	dir = os.path.dirname(abs)
	
	#print repr(dir)
	
	case = Automation.Case.Case(os.path.join(args.src, 'config.xml'))

	walk_conf(None, case, stop)




