# File: graph.py

"""
This module defines the classes Graph, Node, and Arc, which are
used for working with graphs.
"""

class Graph:
    """Defines a graph as a set of nodes and a set of arcs."""

    def __init__(self):
        """Creates an empty graph."""
        self.clear()

    def clear(self):
        """Removes all the nodes and arcs from the graph."""
        self._nodes = { }
        self._arcs = set()

    def addNode(self, arg):
        """
        Adds a node to the graph.  The parameter to addNode is
        either an existing Node object or a string.  If a node is
        specified as a string, addNode looks up that string in the
        dictionary of nodes.  If it exists, the existing node is
        returned; if not, addNode creates a new node with that name.
        The addNode method returns the Node object.
        """
        if type(arg) is str:
            node = self.findNode(arg)
            if node is None:
                node = self.createNode(arg)
        elif isinstance(arg, Node):
            node = arg
        else:
            raise ValueError("Illegal node specification")
        self._nodes[node.getName()] = node
        return node
    
    def removeNode(self, arg):
        # If the input is a string 
        if type(arg) is str:
            node = self.findNode(arg)
            if node is None:
                raise ValueError("Could not find this node in the graph.")
        elif isinstance(arg, Node):
            node = arg     
        else:
            raise ValueError("Illegal node specification")
        # Delete all arcs of the node we want to delete.
        for n in sorted(self._nodes.values()):
            for arcFrom in n.getArcsFrom():
                if arcFrom.getFinish() == node:
                    n._arcsFrom.remove(arcFrom)
            for arcTo in n.getArcsTo():
                if arcTo.getStart() == node:
                    n._arcsTo.remove(arcTo)
        newset = set()
        # Renew the arcs of the graph.
        for arc in self._arcs:
            if arc.getStart() != node and arc.getFinish() != node:
                newset.add(arc)
        self._arcs = newset
        del self._nodes[node.getName()]
    
    def addArc(self, a1, a2=None):
        """
        Adds an arc to the graph.  The parameters to addArc are
        either a single Arc object or a pair of nodes, each of
        which can be an existing Node object or a string.  If a
        node is specified as a string, addArc looks up that name
        in the dictionary of nodes.  If it exists, the existing
        node is returned; if not, addArc creates a new node with
        that name.  The addArc method returns the Arc object.
        """
        if isinstance(a1, Arc) and a2 is None:
            arc = a1
        else:
            start = self.addNode(a1)
            finish = self.addNode(a2)
            arc = self.createArc(start, finish)
        self._arcs.add(arc)
        arc.getStart()._addArcFrom(arc)
        arc.getFinish()._addArcTo(arc)
        return arc
    
    def removeArc(self, a1, a2=None):
        if isinstance(a1, Arc) and a2 is None:
            arc = a1
        elif type(a1) is str and type(a2) is str:
            arc = None
            n1 = self.addNode(a1)
            n2 = self.addNode(a2)
            # Find if the arc exists.
            for a in n2.getArcsFrom():
                if a.getFinish() == n1:
                    arc = a
            for a in n2.getArcsTo():
                if a.getStart() == n1:
                    arc = a
            if arc == None:
                raise ValueError("Could not find this arc in the graph.")
        elif isinstance(a1, Node) and isinstance(a2, Node):
            arc = None
            n1 = a1
            n2 = a2
            # Find if the arc exists.
            for a in n2.getArcsFrom():
                if a.getFinish() == n1:
                    arc = a
            for a in n2.getArcsTo():
                if a.getStart() == n1:
                    arc = a
            if arc == None:
                raise ValueError("Could not find this arc in the graph.")
        else:
            raise ValueError("Illegal node specification")
        # Remove the target arc from its start and finish node.
        start = arc.getStart()
        start._arcsFrom.remove(arc)
        finish = arc.getFinish()
        finish._arcsTo.remove(arc) 
        # Renew arcs of the graph.
        self._arcs.remove(arc)
        
    
    def findNode(self, name):
        """Returns the node with the specified name, or None."""
        return self._nodes.get(name)

    def getNodes(self):
        """Returns a sorted list of all the nodes in the graph."""
        return [ node for node in sorted(self._nodes.values()) ]

    def getArcs(self):
        """Returns a sorted list of all the arcs in the graph."""
        return [ arc for arc in sorted(self._arcs) ]

    def createNode(self, name):
        """Returns a Node with the specified name."""
        return Node(name)

    def createArc(self, start, finish):
        """Returns a Arc between the specified nodes."""
        return Arc(start, finish)
    
# Overload standard methods

    def __str__(self):
        s = ""
        for arc in self.getArcs():
            if len(s) > 0:
                s += ", "
            s += str(arc)
        return "<" + s + ">"

    def __len__(self):
        return len(self._nodes)


class Node:

    def __init__(self, name):
        """Creates a graph node with the given name."""
        self._name = name
        self._arcsFrom = set()
        self._arcsTo = set()
                
    def getName(self):
        """Returns the name of this node."""
        return self._name

    def getArcs(self):
        """Equivalent to getArcsFrom (included for backward compatibility)."""
        return self.getArcsFrom()

    def getArcsFrom(self):
        """Returns a list of all the arcs leaving this node."""
        return [ arc for arc in sorted(self._arcsFrom) ]

    def getArcsTo(self):
        """Returns a list of all the arcs ending at this node."""
        return [ arc for arc in sorted(self._arcsTo) ]

    def getNeighbors(self):
        """Returns a list of the nodes to which arcs exist."""
        targets = set()
        for arc in self._arcsFrom:
            targets.add(arc.getFinish())
        return [ node for node in sorted(targets) ]
    
    def getComingNeighbors(self):
        """Returns a list of the nodes to which arcs exist."""
        targets = set()
        for arc in self._arcsTo:
            targets.add(arc.getStart())
        return [ node for node in sorted(targets) ]

    def isConnectedTo(self, node):
        """Returns True if any arcs connects to node."""
        for arc in self._arcsFrom:
            if arc.getFinish() is node:
                return True
        return False
    

# Package methods called only by the Graph class

    def _addArcFrom(self, arc):
        """Adds an arc that starts at this node."""
        if arc.getStart() is not self:
            raise ValueError("Arc must start at the specified node")
        self._arcsFrom.add(arc)

    def _addArcTo(self, arc):
        """Adds an arc that finishes at this node."""
        if arc.getFinish() is not self:
            raise ValueError("Arc must end at the specified node")
        self._arcsTo.add(arc)
    
    def scanOptions(self, options):
        """Scans the options string on a node definition line."""

# Overload standard methods

    def __str__(self):
        return self._name

    def __lt__(self, other):
        if not isinstance(other, Node):
            return NotImplemented
        elif self is other:
            return False
        elif self._name < other._name:
            return True
        elif self._name > other._name:
            return False
        else:
            raise KeyError("Duplicate names in a graph")

    def __le__(self, other):
        return self is other or self < other


class Arc:
    """This class defines a directed arc from one node to another."""

    def __init__(self, start, finish):
        """Creates an arc from start to finish."""
        self._start = start
        self._finish = finish
        self._cost = 0

    def getStart(self):
        """Returns the node at the start of the arc. Eg: node-> """
        return self._start
    
    def getTail(self):
        """Returns the node at the start of the arc. Eg: node-> """
        return self._start
        
    def getFinish(self):
        """Returns the node at the end of the arc. Eg: ->node """
        return self._finish
    
    def getHead(self):
        """Returns the node at the end of the arc. Eg: ->node """
        return self._finish

    def setCost(self, cost):
        """Sets the cost attribute for the arc."""
        self._cost = cost

    def getCost(self):
        """Returns the cost attribute for the arc."""
        return self._cost


    def scanOptions(self, options):
        """Scans the options string on an arc definition line."""
        cost = float(options)
        if cost == int(cost):
            cost = int(cost)
        self._cost = cost

# Overload standard methods

    def __str__(self):
        suffix = ""
        cost = self._cost
        if cost != 0:
            if cost == int(cost):
                cost = int(cost)
            suffix = " (" + str(cost) + ")"
        return str(self._start) + " -> " + str(self._finish) + suffix

    def __lt__(self, other):
        if not isinstance(other, Arc):
            return NotImplemented
        elif self is other:
            return False
        elif self._start < other._start:
            return True
        elif self._start > other._start:
            return False
        elif self._finish < other._finish:
            return True
        elif self._finish > other._finish:
            return False
        else:
            return id(self) < id(other)

    def __le__(self, other):
        return self is other or self < other
