# Ryan Soedjak, Nick Fratto
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

def finish(outFileName, startTime, ans):
    """Writing final answer to out file"""
    out_ = open(outFileName, "w")
    out_.write("%d\n" %ans["cost"])
    if len(ans["path"]) > 0:
        s = ""
        for n in ans["path"]:
            s += str(n) + " "
        s += str(ans["path"][0])
        out_.write(s)
    out_.close()
    print("Cost: %d" %ans["cost"])
    print("Finished in %f seconds" %(time.time()-startTime))

def annealing(nodes, distances, maxTime, ans):
    """TSP algorithm based on simulated annealing"""

    #edge cases
    if len(nodes) == 0:
        ans["path"] = []
        ans["cost"] = 0
        return
    if len(nodes) == 1:
        ans["path"] = nodes
        ans["cost"] = 0
        return
    if len(nodes) == 2:
        ans["path"] = nodes
        ans["cost"] = totalDist(nodes, distances)
        return

    #Picking a starting tour
    currPath = generateStartingTour(nodes, distances)
    currCost = totalDist(currPath, distances)

    startingAnnealingTime = time.time()
    maxTemperature = maxTime - startingAnnealingTime + 0.05
    avg = 0
    while True:
        #check if time is up
        t = time.time()
        if t > maxTime:
            break
        
        #check if current path is best path
        if currCost < ans["cost"]:
            ans["path"] = currPath
            ans["cost"] = currCost
            #print(ans["cost"])

        #try a neighbor
        skel = randomNeighborSkeleton(currPath, currCost, distances)
        if skel[0] == 1:
            i = skel[1]
            j = skel[2]
            newCost = skel[3]
        else:
            i = skel[1]
            newCost = skel[2]

        currTemperature = maxTemperature - (t - startingAnnealingTime)

        avg = (avg * 1000 + abs(currCost-newCost)) / 1001

        #move to neighbor with some probability
        if random.random() < chance(currCost, newCost, currTemperature, maxTemperature, avg):
            if skel[0] == 1:
                contiguousFlip(currPath, i, j)
            else:
                consecutiveFlip(currPath, i)
            currCost = newCost

def randomNeighborSkeleton(currPath, currCost, distances):
    """Picks a neighbor and computes its cost. Doesn't actually return the neighbor"""
    r = random.random()
    if 0 <= r < 0.3:
        # flip a contiguous chunk of the path
        i = random.randint(0, len(currPath) - 1)
        j = random.randint(0, len(currPath) - 1)
        newCost = currCost
        if i != j and (i+1)%len(currPath)!=j and (j+1)%len(currPath)!=i:
            newCost -= distances.get(currPath[(i - 1)%len(currPath)], currPath[i])
            newCost += distances.get(currPath[(i - 1)%len(currPath)], currPath[j])
            newCost -= distances.get(currPath[j], currPath[(j + 1)%len(currPath)])
            newCost += distances.get(currPath[i], currPath[(j + 1)%len(currPath)])
            return (1, i, j, newCost)
        return (1, 0, 0, newCost)
    else:
        #swap 2 consecutive elements of a path
        i = random.randint(0, len(currPath) - 1)
        j = (i + 1)%len(currPath)
        newCost = currCost
        newCost -= distances.get(currPath[(i - 1)%len(currPath)], currPath[i])
        newCost += distances.get(currPath[(i - 1)%len(currPath)], currPath[j])
        newCost -= distances.get(currPath[j], currPath[(j + 1)%len(currPath)])
        newCost += distances.get(currPath[i], currPath[(j + 1)%len(currPath)])
        return (2, i, newCost)

def contiguousFlip(currPath, i, j):
    """Flips indices i to j in currPath"""
    if i != j and (i+1)%len(currPath)!=j and (j+1)%len(currPath)!=i:
        iP = i
        jP = j
        if (i < j):
            maxx=(j-i+1)//2
        else:
            maxx=(j+1+len(currPath)-i)//2
        for _ in range(maxx):
            temp = currPath[iP]
            currPath[iP] = currPath[jP]
            currPath[jP] = temp
            iP = (iP + 1)%len(currPath)
            jP = (jP - 1)%len(currPath)

def consecutiveFlip(currPath, i):
    """Flips elements at indices i and i+1 in currPath"""
    j = (i + 1)%len(currPath)
    temp = currPath[i]
    currPath[i] = currPath[j]
    currPath[j] = temp
    
def chance(currCost, newCost, currTemperature, maxTemperature, avg):
    """Helper function for annealing"""
    temps = currTemperature / maxTemperature
    if newCost <= currCost:
        return 1
    try:
        p = math.exp(-8*(newCost-currCost)/(temps * avg))
    except: #catching divide by 0 errors lol
        p = 0
    return p

def totalDist(currPath, distances):
    """Computes total cost of a path"""
    currCost = 0
    for i in range(1, len(currPath)):
        currCost += distances.get(currPath[i], currPath[i - 1])
    currCost += distances.get(currPath[0], currPath[-1])
    return currCost

def generateStartingTour(nodes, distances):
    start = random.choice(nodes)
    tour = [start]
    remaining = set(nodes)
    remaining.remove(start)
    while remaining:
        minDist = float("inf")
        minNode = None
        #check min dist from end of tour
        for n in remaining:
            dist = distances.get(tour[-1], n)
            if dist < minDist:
                minDist = dist
                minNode = n
        tour.append(minNode)
        remaining.remove(minNode)
    return tour


"""def randomNeighbor(currPath, currCost, distances):
    Helper function for annealing
        Finds a random neighbor along with its cost
    r = random.random()
    if 0 <= r < 0.3:
        # flip a contiguous chunk of the path
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
    else:
        #swap 2 consecutive elements of a path
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
        #swap 2 random elements
        i = random.randint(1, len(currPath) - 1)
        j = random.randint(1, len(currPath) - 1)
        newPath = list(currPath)
        newCost = currCost
        if i != j:
            temp = newPath[i]
            newPath[i] = newPath[j]
            newPath[j] = temp
            minI = min(i, j)
            maxI = max(i, j)
            newCost -= distances.get(currPath[minI - 1], currPath[minI])
            newCost += distances.get(currPath[minI - 1], currPath[maxI])
            newCost -= distances.get(currPath[maxI], currPath[(maxI + 1)%len(currPath)])
            newCost += distances.get(currPath[minI], currPath[(maxI + 1)%len(currPath)])
            if (maxI - minI != 1):
                newCost -= distances.get(currPath[minI], currPath[minI + 1])
                newCost += distances.get(currPath[maxI], currPath[minI + 1])
                newCost -= distances.get(currPath[maxI - 1], currPath[maxI])
                newCost += distances.get(currPath[maxI - 1], currPath[minI])

        return (tuple(newPath), newCost)"""