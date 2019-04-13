# Ryan Soedjak
import sys
import time
from helperFunctions import *

starttime = time.time()
_, inFileName, outFileName, timelimit = sys.argv
timelimit = float(timelimit)
timelimit -= 0.005 #taking into account the time needed to write to out file
nodes, distances = setup(inFileName)

ans = {"path": None, "cost": float("inf")}

newTimeLimit = timelimit-(time.time()-starttime)
annealing(nodes, distances, newTimeLimit, ans)

finish(outFileName, starttime, ans)