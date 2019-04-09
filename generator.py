import random

outFileName = "coords2.txt"
numNodes = random.randint(600, 1000)
minX = 0
minY = 0
maxX = 1000000
maxY = 1000000
out_ = open(outFileName, "w")

for i in range(numNodes):
    print("%d %d %d\n"%(i + 1, random.randint(minX, maxX), random.randint(minY, maxY)))
    out_.write("%d %d %d\n"%(i + 1, random.randint(minX, maxX), random.randint(minY, maxY)))
out_.close()