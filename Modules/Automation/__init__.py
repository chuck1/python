import os
import re


def next_id(dir):
	imax = 0
	for root, dirs, files in os.walk(dir):
		for d in dirs:
			m = re.search('^x(\d{4})$', d)
			if m:
				#print m.group(1)
				i = int(m.group(1))
				imax = max(imax,i)

	#print "next = {0:04d}".format(imax+1)

	return imax + 1


