from tsp3510 import *
d = {}
vals = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
for i in vals:
    d[i] = (0,0)

index = 0
while True:
    newVal = solve(vals[index])
    newPair = ((d[vals[index]][0]*d[vals[index]][1]+newVal)/(d[vals[index]][1]+1), d[vals[index]][1]+1)
    d[vals[index]] = newPair
    print(d)
    index+=1
    index%=len(vals)