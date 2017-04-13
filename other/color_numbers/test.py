
def clr(x):
    return "\033[{0}m".format(x)

class bcolors:
    MAGENTA = '\033[95m'
    BLUE    = '\033[94m'
    GREEN   = '\033[92m'
    YELLOW  = '\033[93m'
    RED     = '\033[91m'
    ENDC    = '\033[0m'
   
for x in range(0,100):
    print x, clr(40) + clr(1) + clr(x) + '0' + clr(0)




