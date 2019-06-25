# File: dijkstra.py

"""
This module implements Dijkstra's algorithm for solving the single-source
shortest-path problem.
"""

from pqueue import PriorityQueue
import math


def applyDijkstra(g, start, finish):
    """
    Applies Dijkstra's algorithm to the graph g, updating the
    distance from start to each node in g.
    """
    #initialize the start node.
    start.distance = 0
    start.predecessor = None
    finalized = set()
    
    pq = PriorityQueue()
    pq.enqueue(start)
    
    while not pq.isEmpty():
        node = pq.dequeue()        
        finalized.add(node)
        # Stop searching when we find the finish node. 
        if node == finish:
            dis = finish.distance
            path = getPath(finish)
            return dis, path
        for arc in node.getArcsFrom():
            n1 = arc.getStart()
            n2 = arc.getFinish()
            if n2 not in finalized:
                # Initialize n2 if we haven't visitd it.
                if n2 not in pq:
                    initializeNode(n1, n2, arc)
                    pq.enqueue(n2, n2.distance)
                else:
                    oldDistance = n2.distance
                    relax(n1, n2, arc.getCost())
                    if n2.distance < oldDistance:
                        pq.raisePriority(n2, n2.distance)

    return 0, None

                   
def initializeNode(n1, n2, arc):
    """ Initialize node n2 with arc connecting n1 and n2."""
    n2.distance = n1.distance + arc.getCost()
    n2.predecessor = n1
    
def initializeSingleSource(g, start):
    """Initialize the distance and predecessor attributes."""
    for node in g.getNodes():
        node.distance = math.inf
        node.predecessor = None
    start.distance = 0

def relax(n1, n2, cost):
    """Update the fields of n2 using the path n1 -> n2."""
    if n2.distance > n1.distance + cost:
        n2.distance = n1.distance + cost
        n2.predecessor = n1
            
def getDistance(node):
    return node.distance

def getPath(node):
    curr = node
    path = []
    while curr.predecessor is not None:
        for arc in curr.getArcsTo():
            if arc.getStart() is curr.predecessor:
                path.append(arc)
        curr = curr.predecessor    
    path.reverse()
    return path
