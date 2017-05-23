
# probability of getting h heads then a tails
def prob(h):
    return 0.5**(h+1)

def winnings(h):
    return 2**h

for h in range(0,10):
    print prob(h), winnings(h), prob(h) * winnings(h)
    
    

