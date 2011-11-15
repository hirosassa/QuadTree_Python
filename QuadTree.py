#/usr/bin/env python

class QuadTree:
    def __init__(self, x=0, y=0):
        self.point = (x, y)
        self.NW = None
        self.NE = None
        self.SW = None
        self.SE = None
        self.depth = 0
        self.node_num = 1

    def makeQT(self, poitlist):

    def searchNode()


if __name__ == '__main__':
    points = [(1,2), (4,4), (2,5), (9,8)]
    quad_tree = QuadTree(0,0)
    
    quad_tree.makeQT(points)
    
