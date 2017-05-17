

def list2tree(lsts):
    
    d = dict()

    for lst in lsts:
        target = d
        for l in lst:
            try:
                target = target[l]
            except:
                target[l] = dict()
                target = target[l]

    return d

def printtree(d, spaces=''):
    for k,v in d.items():
        print spaces+str(k)
        printtree(v, spaces+'  ')

if __name__ == '__main__':
    
    l = [
            [1,1,1],
            [1,2,1],
            [2,1,1],
            [2,2,1]
            ]

    t = list2tree(l)

    printtree(t)

