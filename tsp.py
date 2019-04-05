import sys
import multiprocessing
from util import *
from helperFunctions import *

if __name__ == '__main__':
    starttime = time.time()
    _, inFileName, outFileName, timelimit = sys.argv
    timelimit = float(timelimit)
    nodes, distances = setup(inFileName)

    newTimeLimit = timelimit-(time.time()-starttime)
    p = multiprocessing.Process(target=solve, args=(nodes, distances, newTimeLimit))
    p.start()
    p.join(newTimeLimit)
    p.terminate()
    p.join()

    finish(outFileName)