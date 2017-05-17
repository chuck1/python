

class MyErr(Exception):
	pass


def throw():
	if True:
		raise MyErr
		raise

	return 1


try:
	a = throw()
except MyErr as e:
	print type(e)
except Exception as e:
	print "exception"
	print type(e)

else:
	print "no error"






