
string1 = "open('a.txt','w').write('hello')"

string2 = "h.func.__globals__['p']"


def analysis(string):
    code = compile(string, 'string', 'eval')

    print()

    for k in dir(code):
        print("{:32}{:32}".format(k, repr(getattr(code,k))))

    print()

if __name__ == '__main__':
    
    analysis(string1)
    analysis(string2)




