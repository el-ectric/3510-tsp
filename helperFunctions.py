from util import *
import random
import time

BestPathHolder = {"path":None, "cost":float("inf")}

def setup(inFileName):
    coords = []
    nodes = []
    in_ = open(inFileName, "r")
    for line in in_:
        nodeID, xCoord, yCoord = line.split()
        coords.append((int(nodeID), (float(xCoord), float(yCoord))))
        nodes.append(int(nodeID))
    in_.close()

    distances = NodeContainer()
    for i in range(len(coords) - 1):
        for j in range(i + 1, len(coords)):
            distances.add(coords[i], coords[j])
    return (nodes, distances)

def finish(outFileName):
    out_ = open(outFileName, "w")
    s = ""
    for n in BestPathHolder["path"]:
        s += str(n) + " -> "
    s += str(BestPathHolder["path"][0])
    out_.write(s)
    out_.write("Cost: " + str(BestPathHolder["cost"]))
    out_.close()
    print(BestPathHolder["cost"])
    print("Finish")

def solve(nodes, distances, timelimit):
    currPath = []
    currCost = 0
    for i in range(len(nodes)):
        currPath.append(nodes[i])
    random.shuffle(currPath)
    currPath = tuple(currPath)
    currCost = totalDist(currPath, distances)
    maxTemperature = timelimit
    startTime = time.time()
    avgInfo = [0, 0]
    while True:
        if currCost < BestPathHolder["cost"]:
            BestPathHolder["path"] = currPath
            BestPathHolder["cost"] = currCost
            print(BestPathHolder["cost"])
        newPath, newCost = randomNeighbor(currPath, currCost, distances)
        temperature = maxTemperature + (startTime - time.time())
        avgInfo[0] = (avgInfo[0] * avgInfo[1]+abs(currCost-newCost))/(avgInfo[1] + 1)
        avgInfo[1] += 1
        if random.random() < chance(currCost, newCost, temperature / maxTemperature, avgInfo[0]):
            currPath = newPath
            currCost = newCost

def randomNeighbor(currPath, currCost, distances):
    if random.random() > 2.0/len(currPath):
        i = random.randint(0, len(currPath) - 1)
        j = (i + 1)%len(currPath)
        newPath = list(currPath)
        newCost = currCost
        temp = newPath[i]
        newPath[i] = newPath[j]
        newPath[j] = temp
        newCost -= distances.get(currPath[(i - 1)%len(currPath)], currPath[i])
        newCost += distances.get(currPath[(i - 1)%len(currPath)], currPath[j])
        newCost -= distances.get(currPath[j], currPath[(j + 1)%len(currPath)])
        newCost += distances.get(currPath[i], currPath[(j + 1)%len(currPath)])
        return (tuple(newPath), newCost)
    else:
        i = random.randint(0, len(currPath) - 1)
        j = random.randint(0, len(currPath) - 1)
        newPath = list(currPath)
        newCost = currCost
        if i != j and (i+1)%len(currPath)!=j and (j+1)%len(currPath)!=i:
            newCost -= distances.get(currPath[(i - 1)%len(currPath)], currPath[i])
            newCost += distances.get(currPath[(i - 1)%len(currPath)], currPath[j])
            newCost -= distances.get(currPath[j], currPath[(j + 1)%len(currPath)])
            newCost += distances.get(currPath[i], currPath[(j + 1)%len(currPath)])
            iP = i
            jP = j
            if (i < j):
                maxx=(j-i+1)//2
            else:
                maxx=(j+1+len(currPath)-i)//2
            for _ in range(maxx):
                temp = newPath[iP]
                newPath[iP] = newPath[jP]
                newPath[jP] = temp
                iP = (iP + 1)%len(currPath)
                jP = (jP - 1)%len(currPath)

        return (tuple(newPath), newCost)

##def randomNeighborSwapRandom(currPath, currCost, distances):
##    i = random.randint(1, len(currPath) - 1)
##    j = random.randint(1, len(currPath) - 1)
##    newPath = list(currPath)
##    newCost = currCost
##    if i != j:
##        temp = newPath[i]
##        newPath[i] = newPath[j]
##        newPath[j] = temp
##        minI = min(i, j)
##        maxI = max(i, j)
##        newCost -= distances.get(currPath[minI - 1], currPath[minI])
##        newCost += distances.get(currPath[minI - 1], currPath[maxI])
##        newCost -= distances.get(currPath[maxI], currPath[(maxI + 1)%len(currPath)])
##        newCost += distances.get(currPath[minI], currPath[(maxI + 1)%len(currPath)])
##        if (maxI - minI != 1):
##            newCost -= distances.get(currPath[minI], currPath[minI + 1])
##            newCost += distances.get(currPath[maxI], currPath[minI + 1])
##            newCost -= distances.get(currPath[maxI - 1], currPath[maxI])
##            newCost += distances.get(currPath[maxI - 1], currPath[minI])
##
##    return (tuple(newPath), newCost)

def chance(currCost, newCost, temps, avg):
    if newCost < currCost:
        return 1
    else:
        return math.exp(-(float(newCost)-currCost)/(temps*avg))

def totalDist(currPath, distances):
    currCost = 0
    for i in range(len(currPath)):
        if i > 0:
            currCost += distances.get(currPath[i], currPath[i - 1])
    currCost += distances.get(currPath[0], currPath[-1])
    return currCost

def change():
    BestPathHolder["path"] = "ASDF"

def get():
    return BestPathHolder["path"]