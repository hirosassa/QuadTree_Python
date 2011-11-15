#/usr/bin/env python

class QuadTree:
    def __init__(self, x=0, y=0):
        self.point = (x, y)
        self.NW = None
        self.NE = None
        self.SW = None
        self.SE = None


    def makeQT(self)
