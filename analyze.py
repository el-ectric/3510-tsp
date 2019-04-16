from tsp3510 import *

def an1():
    d = {}
    vals = [32, 64, 128, 256]
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

def an2():
    for problem in range(3, 11):
        print("Problem %d: %d\n"%(problem, solve(problem)))
an1()