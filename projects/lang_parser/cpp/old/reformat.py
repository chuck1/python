


def reformat():
	import vim
	
	cb = vim.current.buffer

	for i in range(0, len(cb)):
		line = cb[i]
		cb[i] = line + ':-)'
		print line

