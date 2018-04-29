import sys

def progress_bar(i, n):
    length = 100
    fill = u"\u25A0"
    blank = ' '
    
    fill_length = int(length * i / n)

    bar = fill * fill_length + blank * (length - fill_length)
    
    sys.stdout.write('\r[{:s}] {:4}/{:4}'.format(bar, i, n))
    sys.stdout.flush()

