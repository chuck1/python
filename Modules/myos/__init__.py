import os
import re



def glob(patstr, search = "."):
	
	pat = re.compile(patstr)

	for root, dirs, files in os.walk(search):
		#print root, files, dirs
		for f in files:
			f = os.path.join(root, f)
			#print f
			if pat.match(f):
				yield os.path.abspath(f)
				#yield f




if __name__=="__main__":
	print(list(glob(".*")))

