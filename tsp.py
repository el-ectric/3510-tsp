# Ryan Soedjak
import sys
import time
from helperFunctions import *

starttime = time.time()
_, inFileName, outFileName, timelimit = sys.argv
timelimit = float(timelimit)
nodes, distances = setup(inFileName)

ans = {"path": None, "cost": float("inf")}
newTimeLimit = timelimit-(time.time()-starttime)
annealing(nodes, distances, newTimeLimit, ans)
finish(outFileName, starttime, ans)