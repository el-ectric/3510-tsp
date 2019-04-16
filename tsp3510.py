# Ryan Soedjak
import sys
import time
from helperFunctions import *


#def solve(bound):
startTime = time.time()

#I/O
_, inFileName, outFileName, timeLimit = sys.argv

####### testing
#inFileName = "china.txt"
#outFileName = "out1.txt"
#timeLimit = 180
#######

timeLimit = float(timeLimit)
timeLimit -= 0.015 #taking into account the time needed to write to out file
maxTime = startTime + timeLimit

#Computing distances
nodes, distances = setup(inFileName)

#Holds final answer
ans = {"path": None, "cost": float("inf")}

#The algorithm itself
annealing(nodes, distances, maxTime, ans)

#Writes to out file
finish(outFileName, startTime, ans)

#return ans["cost"]