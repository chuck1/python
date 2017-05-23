

def f_circular(Re):
    if Re < 2E4:
        f = 0.316 * Re**(-1/4)
    elif Re >= 2E4:
        f = 0.184 * Re**(-1/5)
    return f


