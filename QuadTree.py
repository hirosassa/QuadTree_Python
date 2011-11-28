#!/usr/bin/env python
# -*- coding: utf-8 -*-

class QTNode:
    def __init__(self, point, label):
         self.label  = label
         self.x      = point[0]
         self.y      = point[1]
         self.region = [None, None, None, None, None]
         self.Parent = None

    def coordinates(self):
        return (self.x, self.y)

    def nodeDirection(self, from_node):
        """Calculate direction to node from from_node"""
        if self.x >= from_node.x and self.y >= from_node.y:
            return 1
        elif self.x >= from_node.x and self.y < from_node.y:
            return 4
        elif self.x < from_node.x and self.y >= from_node.y:
            return 2
        else:
            return 3

    
class QuadTree:
    """
    Simple point quad tree implementaion.
    This quad tree supports insert, and searchNode, deleteNode operations.
    """
    def __init__(self):
        self.root = None
        self.nodeNum = 0
        
    def insertNode(self, newPoint):
        """Insert point into this quad tree."""
        if isinstance(newPoint, tuple):
            new_node = QTNode(newPoint, self.nodeNum)
            self.nodeNum += 1
        else:
            new_node = newPoint  # newPoint is already existing node (re-insertion).
        
        if self.root is None:
            self.root = new_node            
        else:
            node = self.root
            while True:
                if newPoint[0] >= node.x and newPoint[1] >= node.y:   # NE region
                    if node.region[1] is None:
                        node.region[1]= new_node
                        new_node.Parent = node
                        break
                    node = node.region[1]
                elif newPoint[0] >= node.x and newPoint[1] < node.y:  # SE region
                    if node.region[4] is None:
                        node.region[4]= new_node
                        new_node.Parent = node
                        break
                    node = node.region[4]
                elif newPoint[0] < node.x and newPoint[1] >= node.y:  # NW region
                    if node.region[2] is None:
                        node.region[2] = new_node
                        new_node.Parent = node
                        break
                    node = node.region[2]
                else:                                                 # SW region
                    if node.region[3] is None:
                        node.region[3] = new_node
                        new_node.Parent = node
                        break
                    node = node.region[3]
        return new_node

    def reinsertSubtree(self,subroot):
        """Reinsert entire subtree into the quadtree."""
        stack = []
        stack.append(subroot)
        while len(stack) != 0:
            node = stack.pop()
            for i in range(1,5):
                if node.region[i] is None: pass
                else:
                    stack.append(node.region[i])
                    node.region[i] = None       # delete reference
            self.insertNode(node)
        
    def searchNode(self, point):
        """
        Return the node for coordinates if the node is in the quad tree,
        or None otherwise.
        """
        node = self.root
        while node is not None :
            if point[0] == node.x and point[1] == node.y:   # Find!!
                return node
            elif point[0] >= node.x and point[1] >= node.y: # Go to NE region
                node = node.region[1]
            elif point[0] >= node.x and point[1] < node.y:  # Go to SE region
                node = node.region[4]
            elif point[0] < node.x and point[1] >= node.y:  # Go to NW region
                node = node.region[2]
            else :                                          # Go to SW region
                node = node.region[3]
        return None

    # def searchRegion(self, region):
    #     """Return the nodes which is in the region or None otherwise."""
    #     hits =
    #     return hits
        
    def makeOptQT(self, lst):
        """Generate a balanced quad tree from the point list."""
        
        def median(x):
            if x % 2 == 0: # x is even
                return (x/2 + x/2 + 1)/2
            else:          # x is odd 
                return (x + 1)/2

        points = lst[:]
        if len(points) == 0: return
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
        
        delete = self.searchNode(point)
        if  delete is None:
            print "There is no such a node" , (point[0], point[1]), "."
            return None

        if (delete.region[1] is None) and (delete.region[2] is None)\
           and (delete.region[3] is None) and (delete.region[4] is None):   # delete node is a leaf.
               direction = delete.nodeDirection(delete.Parent)
               delete.Parent.region[direction] = None
               return 
    
        def conj(region):
            """Calculate opposite region of input."""
            return (region + 1) % 4 + 1
    
        def adjRegion(region):
            """Calculate adjacent regions of input. Return value format is (previous, next)"""
            return ((region + 2) % 4 + 1, region % 4 + 1)

        def isinCrosshatched(point, center, region_point):
            if point is None: return False
            ru = (max(center.x, region_point.x), max(center.y, region_point.y))
            ld = (min(center.x, region_point.x), min(center.y, region_point.y))
            return (ld[0] < point.x and point.x < ru[0]) \
                   or (ld[1] < point.y and point.y < ru[1])

        def findCandidate(delete):
            cand_list = [] 
            for i in range(1, 5): # Select candidates in the each region.
                candidate = delete.region[i]
                while candidate:
                    if candidate.region[conj(i)] is None: break
                    candidate = candidate.region[conj(i)]
                cand_list.append(candidate)
            accept = []
            for i in range(1,5):    # Filter candidates whether other candidate is in crosshatched region or not
                if cand_list[i-1] is None: pass #error routine
                else:
                    (prev, next) = adjRegion(cand_list[i-1].nodeDirection(delete))
                    if not isinCrosshatched(cand_list[next-1], delete, cand_list[i-1]) \
                           and not isinCrosshatched(cand_list[prev-1], delete, cand_list[i-1]):
                        accept.append(cand_list[i-1])
            if len(accept) == 0: accept = cand_list[:]
            minimum = float("inf")
            for i in accept:           # Filter candidates by L1 distance from delete node
                l1 = abs(delete.x - i.x) + abs(delete.y - i.y)
                if minimum > l1 :
                    minimum = l1
                    replace = i
            return replace

        def ADJ(node, delete, replace, re_insert):
            if node is None : return
            if isinCrosshatched(node, delete, replace):
                direction = node.Parent.nodeDirection(node)
                node.Parent.region[direction] = None  # delete parent's reference
                re_insert.append(node)
                return
            else:
                if node.y >= delete.y and replace.y >= delete.y:
                    # Both "node" and "replace" are in the positive side of x-axis of delete node
                    ADJ(node.region[3], delete, replace, re_insert)
                    ADJ(node.region[4], delete, replace, re_insert)
                elif node.y < delete.y and replace.y < delete.y:
                    # Both "node" and "replace" are in the nogative side of x-axis of delete node
                    ADJ(node.region[2], delete, replace, re_insert)
                    ADJ(node.region[1], delete, replace, re_insert)
                elif node.x >= delete.x and replace.x >= delete.x:
                    # Both "node" and "replace" are in the positive side of y-axis of delete node
                    ADJ(node.region[2], delete, replace, re_insert)
                    ADJ(node.region[3], delete, replace, re_insert)
                else:
                    # Both "node" and "replace" are in the negative side of y-axis of delete node
                    ADJ(node.region[1], delete, replace, re_insert)
                    ADJ(node.region[4], delete, replace, re_insert)

        def newRoot(subroot, delete, replace, rep_region, re_insert):
            (prev, next) = adjRegion(rep_region)
            ADJ(subroot.region[prev], delete, replace, re_insert)
            ADJ(subroot.region[next], delete, replace, re_insert)
            if subroot.region[conj(rep_region)] == None:
                subroot.Parent.region[conj(rep_region)] = subroot.region[rep_region]
                subroot.region[rep_region] = None
                return
            newRoot(subroot.region[conj(rep_region)], delete,
                    replace, rep_region, re_insert)

                        
        candidate = findCandidate(delete)
        if candidate is None:
            print "can't delete the node"
            return self.root
        
        (prev, next) = adjRegion(candidate.nodeDirection(delete))
        re_insert = []
        ADJ(delete.region[prev], delete, candidate, re_insert)
        ADJ(delete.region[next], delete, candidate, re_insert)
        newRoot(delete.region[candidate.nodeDirection(delete)], delete,
                candidate, candidate.nodeDirection(delete), re_insert)

        for i in range(1,5):      # Replace delete node with candidate node
            candidate.region[i] = delete.region[i]
        candidate.Parent = delete.Parent

        for node in re_insert:    # Reinsertion sub-tree
            self.reinsertSubtree(node)
    
if __name__ == '__main__':
    import numpy as np                            
                                                  
    nodeNum = 10                                  
    x = np.random.randint(-10, 10, nodeNum)       
    y = np.random.randint(-10, 10, nodeNum)       
    lst = [(x[i], y[i]) for i in range(nodeNum)]  
                                                  
    qtree = QuadTree()                            
    qtree.makeOptQT(lst)                          
    qtree.insertNode((-1, 6))
    qtree.insertNode((1, 2))
    

