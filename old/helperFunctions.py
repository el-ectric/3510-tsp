# Ryan Soedjak
from util import *
import random
import time

def setup(inFileName):
    """Reading input and setting up node distances"""
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

def finish(outFileName, starttime, ans):
    """Writing to out file"""
    t = time.time()
    out_ = open(outFileName, "w")
    s = ""
    for n in ans["path"]:
        s += str(n) + " -> "
    s += str(ans["path"][0])
    out_.write(s)
    out_.write("\nCost: %d\nFinished in %f seconds" %(ans["cost"], t-starttime))
    out_.close()
    print("Cost: %d" %ans["cost"])
    print("Finished in %f seconds" %(t-starttime))

def annealing(nodes, distances, timelimit, ans):
    """Based on the simulated annealing technique"""
    startTime = time.time()

    #The current tour we're considering and its cost
    currPath = []
    currCost = 0
    
    #Picking a random starting tour
    for i in range(len(nodes)):
        currPath.append(nodes[i])
    random.shuffle(currPath)
    currPath = tuple(currPath)
    currCost = totalDist(currPath, distances)

    maxTemperature = timelimit
    avgInfo = [0, 0]
    while True:
        if currCost < ans["cost"]:
            ans["path"] = currPath
            ans["cost"] = currCost
            print(ans["cost"])
        t = time.time()
        if t - startTime > timelimit:
            break
        newPath, newCost = randomNeighbor(currPath, currCost, distances)
        temperature = maxTemperature + (startTime - t)
        avgInfo[0] = (avgInfo[0] * avgInfo[1]+abs(currCost-newCost))/(avgInfo[1] + 1)
        avgInfo[1] += 1
        if random.random() < chance(currCost, newCost, temperature / maxTemperature, avgInfo[0]):
            currPath = newPath
            currCost = newCost

def randomNeighbor(currPath, currCost, distances):
    """Helper function for annealing
        Finds a random neighbor along with its cost"""
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

def chance(currCost, newCost, temps, avg):
    """Helper function for annealing"""
    if newCost < currCost:
        return 1
    else:
        return math.exp(-(float(newCost)-currCost)/(temps*avg))

def totalDist(currPath, distances):
    """Computes total cost of a path"""
    currCost = 0
    for i in range(len(currPath)):
        if i > 0:
            currCost += distances.get(currPath[i], currPath[i - 1])
    currCost += distances.get(currPath[0], currPath[-1])
    return currCost