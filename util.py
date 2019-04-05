import math

class NodeContainer:
    def __init__(self):
        self.distances = {}
    def add(self, aData, bData):
        self.distances[(aData[0], bData[0])] = self.approxDist(aData[1], bData[1])
    def get(self, a, b):
        if (a, b) in self.distances:
            return self.distances[(a, b)]
        if (b, a) in self.distances:
            return self.distances[(b, a)]
        return None
    def approxDist(self, aCoord, bCoord):
        return int(round(math.sqrt((aCoord[0] - bCoord[0]) ** 2 + (aCoord[1] - bCoord[1]) ** 2)))
    def __str__(self):
        return str(self.distances)