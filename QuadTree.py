#!/usr/bin/env python
# -*- coding: utf-8 -*-
class Rect:
    def __init__(self, pt1, pt2): 
        self.topright   = (max(pt1[0], pt2[0]), max(pt1[1], pt2[1]))
        self.bottomleft = (min(pt1[0], pt2[0]), min(pt1[1], pt2[1]))
         
class QTNode:
    def __init__(self, point, label):
         self.label  = label
         self.x      = point[0]
         self.y      = point[1]
         self.NW     = None
         self.NE     = None
         self.SW     = None
         self.SE     = None
         self.Parent = None
             
class QuadTree:
    """
    Simple point quad tree implementaion.
    This quad tree supports insert, and searchNode operations.
    """
    def __init__(self):
        self.root = None
        self.nodeNum = 0
            
    def insertNode(self, newPoint):
        """Insert point into this quad tree."""
        new_node = QTNode(newPoint, self.nodeNum)
        if self.root is None :
            self.root = new_node            
        else :
            node = self.root
            while True :
                if newPoint[0] >= node.x and newPoint[1] >= node.y :  # NE region
                    if node.NE is None :
                        node.NE = new_node
                        new_node.Parent = node
                        break
                    node = node.NE
                elif newPoint[0] >= node.x and newPoint[1] < node.y : # SE region
                    if node.SE is None :
                        node.SE = new_node
                        new_node.Parent = node
                        break
                    node = node.SE
                elif newPoint[0] < node.x and newPoint[1] >= node.y : # NW region
                    if node.NW is None :
                        node.NW = new_node
                        new_node.Parent = node
                        break
                    node = node.NW
                else :                                                # SW region
                    if node.SW is None :
                        node.SW = new_node
                        new_node.Parent = node
                        break
                    node = node.SW
        self.nodeNum += 1
        return new_node
                    
    
    def searchNode(self, point):
        """
        Return the node for coordinates if the node is in the quad tree,
        or None otherwise.
        """
        node = self.root
        while node is not None :
            if point[0] == node.x and point[1] == node.y :   # Find!!
                return node
            elif point[0] >= node.x and point[1] >= node.y : # Go to NE region
                node = node.NE
            elif point[0] >= node.x and point[1] < node.y :  # Go to SE region
                node = node.SE
            elif point[0] < node.x and point[1] >= node.y :  # Go to NW region
                node = node.NW                                    
            else :                                           # Go to SW region
                node = node.SW
        return None

    def searchRegion(self, region):
        """Return the nodes which is in the region or None otherwise."""
        hits =
        return hits
        

    def makeOptQT(self, lst):
        """Generate a balanced quad tree from the point list."""
        
        def median(x):
            if x % 2 == 0 : # x is even
                return (x/2 + x/2 + 1)/2
            else :          # x is odd 
                return (x + 1)/2

        points = lst[:]     # copy the list of points 
        if len(points) == 0 : return
        points.sort()
        point = points[median(len(points))-1]  # Extract median point 
        self.insertNode(point)
        points.remove(points[median(len(points))-1])

        # Make sub region's point list and recursive call
        NE_points = [x for x in points if x[0] >= point[0] and x[1] >= point[1]] 
        SE_points = [x for x in points if x[0] >= point[0] and x[1] < point[1]]  
        NW_points = [x for x in points if x[0] < point[0] and x[1] >= point[1]]  
        SW_points = [x for x in points if x[0] < point[0] and x[1] < point[1]]  
        self.makeOptQT(NE_points)
        self.makeOptQT(SE_points)      
        self.makeOptQT(NW_points)
        self.makeOptQT(SW_points)


    def deleteNode(self, point):
        """Delete point in the quad tree."""
        
        node = searchNode(self, point)
        if  node is None:
            print "There is no such a node (", point[0], ", ", point[1], ")."
            return None

        def conj(direction):
            """Calculate opposite direction of input."""
            return (direction + 1) % 4 + 1
        
        def adjRegion(direction):
            """Calculate adjacent regions of input. Return value format is (previous, next)"""
            return ((direction + 2) % 4 + 1, direction % 4 + 1)
        
        def isinCrosshatched(point, center, region_point):
            ru = (max(center.x, region_point.x), max(center.y, region_point.y))
            ld = (min(center.x, region_point.x), min(center.y, region_point.y))
            return (ld[0] < point.x and point.x < ru[0]) \
                   or (ld[1] < point.y and point.y < ru[1])

        def findCandidate(self, point):
            node = self.searchNode(point)          
            cand_list = [] 
            for i in [NE, NW, SW, SE]: # Select candidates in the each region.
                candidate = node.i
                while candidate:
                    candidate = candidate.conj(i)
                cand_list.append(candidate)
            
            accept = []
            for i in range(1,5):    # Filter candidates whether other candidate is in crosshatched region or not
                (prev, next) = adjRegion(i)
                if not isinCrosshatched(next, node, cand_list[i]) \
                       and not isinCrosshatched(prev, node, cand_list[i]) :
                    accept.append(result[i])

            if len(accept) == 0 : accept = cand_list[:]
            minimum = float("inf")
            for i in accept:           # Filter candidates by L1 distance from delete node
                l1 = abs(node.x - i.x) + abs(node.y - i.y)
                if minimum > l1 :
                    minimum = l1
                    replace = (i.x, i.y)
                    
            return replace

        def ADJ(self, node, delete, replace, re_insert):
            if node is None : return
            if isinCrosshatched(node, delete, replace) :
                re_insert.append(node)
                return
            else:
                if node.y >= delete.y and replace.y >= delete.y:
                    # Both "node" and "replace" are in the positive side of x-axis of delete node
                    ADJ(node.SW, delete, replace, re_insert)
                    ADJ(node.SE, delete, replace, re_insert)
                elif node.y < delete.y and replace.y < delete.y :
                    # Both "node" and "replace" are in the nogative side of x-axis of delete node                    
                    ADJ(node.NW, delete, replace, re_insert)
                    ADJ(node.NE, delete, replace, re_insert)
                elif node.x >= delete.x and replace.x >= delete.x :
                    # Both "node" and "replace" are in the positive side of y-axis of delete node                    
                    ADJ(node.NW, delete, replace, re_insert)
                    ADJ(node.SW, delete, replace, re_insert)
                else :
                    # Both "node" and "replace" are in the negative side of y-axis of delete node                    
                    ADJ(node.NE, delete, replace, re_insert)
                    ADJ(node.SE, delete, replace, re_insert)

        def newRoot(self,):
            
            
        
    #def showTree(self):

    
if __name__ == '__main__':
    
    qtree = QuadTree()
    lst = [(0,0), (-1,-2), (-3,4), (2,-5), (1,4), (-4,-6), (3,5), (2,2), (-4,1), (1, -10)]
    qtree.makeOptQT(lst)
    qtree.insertNode((-1, 6))
    qtree.insertNode((1, 2))
