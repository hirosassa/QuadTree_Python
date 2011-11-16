#!/usr/bin/env python
# -*- coding: utf-8 -*-

            
class QuadTree:
    class Node:
        def __init__(self, point, label):
            self.label = label
            self.x = point[0]
            self.y = point[1]
            self.NW = None
            self.NE = None
            self.SW = None
            self.SE = None

        def insert(self, newPoint, label):
                if self.x <= newPoint[0] and self.y <= newPoint[1] :  # NE
                    if self.NE is None:
                        self.NE = QuadTree.Node(newPoint, label)
                    else : self.NE = insert(newPoint, label)
                elif self.x <= newPoint[0] and self.y > newPoint[1] : # SE
                    if self.SE is None:
                        self.SE = QuadTree.Node(newPoint, label)
                    else : self.SE = insert(newPoint, label)
                elif self.x > newPoint[0] and self.y <= newPoint[1] : # NW
                    if self.NW is None:
                        self.NW = QuadTree.Node(newPoint, label)
                    else : self.NW = insert(newPoint, label)
                else :                                                # SW
                    if self.SW is None:
                        self.SW= QuadTree.Node(newPoint, label)
                    else : self.SW = insert(newPoint, label)


    def __init__(self):
        self.root = None
        self.nodeNum = 0
            
    def insertNode(self, newPoint):
        if self.root is None :
            self.root = QuadTree.Node(newPoint, self.nodeNum)
        else :
            self.root.insert(newPoint, self.nodeNum)
        self.nodeNum += 1


    #def searchNode(self, point):
    #def makeQT(self, points):
    #def deleteNode(self):
    #def balanceQT(self):
    #def getDepth():
    #def searchRegion():
    
    

if __name__ == '__main__':
    
    qtree = QuadTree()
    qtree.insertNode((0, 0))
    qtree.insertNode((1, 2))

    
