import random

def drawHand():
    deck = ['T']*4 + ['L']*55 + ['Z']*1
    random.shuffle(deck)
    return deck[:7]

n = 100000
t = 0
tandr = 0

for i in range(n):
    foundt = False
    for j in range(7):
        h = drawHand()
        if 'T' in h:
            if not foundt:
                t+=1
                foundt = True
                break

print(t, t/float(n))