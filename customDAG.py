import graph as g
import dijkstra as d
import math


def ReadGraph(fileName):
    
    """
    Takes in a string of the name of a text file containing the
    information of a graph. And returns a graph according to these information.
    """
    G = g.Graph()
    with open(fileName) as f:
        for line in f:
            # Ignores the titles in the text file.
            if not line.startswith("#"):
                nodeName, neighborName, cost = line.split(',')
                node = G.addNode(nodeName)
                neighbor = G.addNode(neighborName)
                edge = G.addArc(node, neighbor)
                edge.setCost(int(cost))
    return G
  
    
def sortNodes(G):
    
    """
    Takes in a graph object, and returns a list of sorted nodes in that graph.
    Topologically sort V and truncate so nodes[0]=s and nodes[len(nodes)-1]=t.
    """
    
    visited = dict((node, False) for node in G.getNodes())
    result = []
    # Depth first search.
    def dfs(G, startNode):
        for n in startNode.getNeighbors():
            if visited[n] == False:
                visited[n] = True
                dfs(G, n)
        result.append(startNode)
    for node in G.getNodes():
        if not visited[node]:
            visited[node] = True
            dfs(G, node)
    result.reverse()
    return result
    

def is_DAG(G):
    """
    Takes in a graph, and returns True if the input is a directed acyclic graph,
    False otherwise.
    """
    cycle = False
    stack = set()
    visited = set()
    for n in G.getNodes():
        if n not in visited and __is_DAG_helper__(n, visited, stack):
            cycle = True
    if cycle:
        return False
    else:
        return True
    
    
def __is_DAG_helper__(n, visited, stack):
    """
    Private function only used for is_DAG(G).
    Takes in a node and two sets of nodes.
    Returns True if the DFS traversal starting at n detects a cycle, False otherwise.
    """
    if n in stack:
        return True
    stack.add(n)
    for neighbor in n.getNeighbors():
        if neighbor not in visited and __is_DAG_helper__(neighbor, visited, stack):
            return True
    stack.remove(n)
    visited.add(n)
    return False
        


def CountUpstream(G, s, t):
    
    """
    Takes in a graph object, a starting node, and a ending node.
    In the DAG from s to t, this function returns the number of paths from t to
    each node in the graph. Eg: {s: 5, b: 3}, which means that there are 5 
    paths from t to s, and 3 paths from t to b. 
    """
    nodes = sortNodes(G)
    nodes.reverse()
    upstream = dict()
    upstream[t] = 1 # comeback
    for node in nodes:
        if node not in upstream:
            number = 0
            for n in node.getNeighbors():
                number += upstream[n]
            upstream[node] = number
        if node is s:
            break
    return upstream


def CountDownstream(G, s, t):
    """
    Takes in a graph object, a starting node, and a ending node.
    In the DAG from s to t, this function returns the number of paths from s to 
    each node in the graph. Eg: {t: 5, b: 1}, which means that there are 5 
    paths from s to t, and 1 path from s to b.
    """
    nodes = sortNodes(G)
    upstream = dict()
    upstream[s] = 1
    for node in nodes:
        if node not in upstream:
            number = 0
            for n in node.getComingNeighbors():
                number += upstream[n]
            upstream[node] = number
        if node is t:
            break
    return upstream


def PathCounter(G, s, t):
    """
    Takes in a graph object, a starting node, and a ending node.
    In the DAG from s to t, this functions returns the total number that each 
    edge is used in all the paths from s to t. Eg: {(a,c):2}, which means that 
    the edge between a and c is used twice in all the paths from s to t.
    """
    upstream = CountUpstream(G, s, t)
    downstream = CountDownstream(G, s, t)
    paths = dict() # edges with corresponding weights
    for arc in G.getArcs():
        paths[arc] = upstream[arc.getFinish()] * downstream[arc.getStart()]
    return paths


def UpdateUpstream(G_0, u, v, upstream, nodes):
    """
    Takes in a graph object, a pair of ndoes connected  by the imaginary edge, 
    the original upstream of G_0, and a list of topologically sorted nodes.
    Returns a dictionay of updated upstream with adding an imaginary between 
    u and v.
    """
    up = upstream.copy() 
    up[u] = upstream[u] + upstream[v]
    i = nodes.index(u) - 1
    while i >= 0:
        x = nodes[i]
        number = 0
        for neighbor in x.getNeighbors():
                number += up[neighbor]
        up[x] = number
        i -= 1
    return up
    

def UpdateDownstream(G_0, u, v, downstream, nodes):
    """
    Takes in a graph object, a pair of ndoes connected  by the imaginary edge, 
    the original downstream of G_0, and a list of topologically sorted nodes.
    Returns a dictionay of updated downstream with adding an imaginary between 
    u and v.
    """

    down = downstream.copy()
    down[v] = downstream[u] + downstream[v]
    i = nodes.index(v) + 1
    while i < len(down):
        x = nodes[i]
        number = 0
        for neighbor in x.getComingNeighbors():
                number += down[neighbor]
        down[x] = number
        i += 1
    return down

def FindNextSubPath2(G, G_0, s, t):
    """
    Takes in a graph G, a DAG G_0, a starting node, and a ending node.
    Returns the optimal path that minimizes the total costs of all paths of the
    new DAG G_1. Also returns the total costsof all paths after adding the
    optimal path in G_0.
    """
    upstream  = CountUpstream(G_0, s, t)
    downstream = CountDownstream(G_0, s, t)
    bestscore = math.inf
    bestpath = None
    # Find G/G_0.
    newGraph = getNewGraph(G, G_0)
    newnodes = sortNodes(newGraph)
    nodes = sortNodes(G_0)
    i = 0
    while i < len(newnodes)-1:
        j = i + 1
        while j < len(newnodes):
            G_0_u = G_0.findNode(newnodes[i].getName())
            G_0_v = G_0.findNode(newnodes[j].getName())
            # Make sure the path starts and ends in G_0.
            if G_0_u != None and G_0_v != None:
                u = newnodes[i]
                v = newnodes[j]
                distance, path = d.applyDijkstra(newGraph, u, v)
                # If there is no shortest path, skip.
                if distance == 0 and path == None:
                    if j == len(nodes):
                        i += 1
                        j = i + 1
                    else:
                        j += 1
                    continue
                up = UpdateUpstream(G_0, G_0_u, G_0_v, upstream, nodes)
                down = UpdateDownstream(G_0, G_0_u, G_0_v, downstream, nodes)
                newCost = 0
                for arc in path:
                    newCost += arc.getCost()
                newTotalCost = up[G_0_v] * down[G_0_u] * newCost
                oldTotalCost = 0
                for arc in G_0.getArcs():
                    oldTotalCost += up[arc.getFinish()] * down[arc.getStart()] * arc.getCost() 
                score = newTotalCost + oldTotalCost
                if score < bestscore:
                    bestscore = score
                    bestpath = path
            j += 1
        i+= 1
    return bestscore, bestpath
            
    
def __ExistedPaths__(G, arc):
    """
    Private function for FindNextSubPath(G, G_0, s, t).
    Takes in a graph and an arc object.
    Returns True if arc is in G, False otherwise.
    """
    exist = True
    G_start = G.findNode(arc.getStart().getName())
    G_finish = G.findNode(arc.getFinish().getName())
    G_arc = None
    if G_start != None:
        for a in G_start.getArcsFrom():
            if a.getFinish() is G_finish and a.getCost() == arc.getCost():
                G_arc = a
    if G_start is None:
        exist = False
    elif G_finish is None:
        exist = False
    elif G_arc == None:
        exist = False
    return exist
    
def getNewGraph(G, G_0):
    """
    Takes in Two Graphs G and G_0, returns a new graph G/G_0.
    """
    newGraph = g.Graph()
    for arc in G.getArcs():
        if __ExistedPaths__(G_0, arc) == False:
            node1 = newGraph.addNode(arc.getStart().getName())
            node2 = newGraph.addNode(arc.getFinish().getName())
            newarc = newGraph.addArc(node1, node2)
            newarc.setCost(arc.getCost())
    return newGraph
    
    
    
def GraphCosts(G):
    """
    Takes in a graph object, a starting node, and a ending node.
    Returns the total weights of edges in the graph G from s to t.
    """
    result = 0
    for arc in G.getArcs():
        result += arc.getCost()
    return result
    
    
def TotalPathsCosts(G, s, t): 
    """
    Takes in a graph object, a starting node, and a ending node.
    Returns the total weights of all paths in the graph G from s to t.
    """
    result = 0
    pc = PathCounter(G, s, t)
    for arc in G.getArcs():
        if arc in pc:
            cost = arc.getCost() * pc[arc]
            result += cost
    return result


def apply(G, G_0, k, out):
    """
    Takes in two graphs G and G_0. returns a out.txt file containg k paths to 
    be added to graph G_0 based on G by applying the DAG algorithm. 
    """
    out = open(out, 'w')
    out.write('#k\tpath_length\tpath\n')
    G = ReadGraph(G)
    G_0 = ReadGraph(G_0)
    s = G_0.findNode('s')
    t = G_0.findNode('t')
    currscore = 0
    for i in range(1,k+1):
        bestscore, bestpath = FindNextSubPath2(G, G_0, s, t)
        if bestpath == None:
            path = 'None'
            bestscore = currscore
        else:
            path = bestpath[0].getStart().getName()
            # Adds the new path to G_0.
            G_0_u = G_0.findNode(bestpath[0].getStart().getName())
            for arc in bestpath:
                path += "|" + arc.getFinish().getName()
                G_0_v = G_0.findNode(arc.getFinish().getName())
                if G_0_v == None:
                    G_0_v = G_0.addNode(arc.getFinish().getName())
                newarc = G_0.addArc(G_0_u, G_0_v)
                newarc.setCost(arc.getCost())
                G_0_u = G_0_v
            currscore = bestscore
        out.write(str(i)+'\t'+str(bestscore)+'\t'+path + '\n')
    out.close()
    return 
    
        
        
# Main
if __name__ == "__main__":
    # Test for apply(G, G_0, k, out).
    apply('demo_G.txt', 'demo_G_0.txt', 5, 'output.txt')
    
    
    
    
    #Graph after changed G_1. For testing apply(G, G_0, k, out).
    G_1 = ReadGraph('demo_G_1.txt')
    s_1 = G_1.findNode('s')
    t_1 =G_1.findNode('t')
    
    # Test for PathsCosts(G_1, s, t).
    print('The total costs of all paths in G_1 is: ')
    print(TotalPathsCosts(G_1, s_1, t_1))
    print('\n')
    
    
    '''
    G_0 = ReadGraph('demo_G_0.txt')
    s_0 = G_0.findNode('s')
    t_0 = G_0.findNode('t')
    u_0 = G_0.findNode('u')
    v_0 = G_0.findNode('v')
    
    G = ReadGraph('demo_G.txt')
    
    
    # Test for sortNodes(G).
    print("The topolocially sorted order of G_0: ")
    nodes = sortNodes(G_0)
    order = ''
    for node in nodes:
        order += node.getName() + " "
    print(order)
    print('\n')
        
    
    #Test for FindNextSubPath(G, G_0, s, t)
    bestscore, bestpath = FindNextSubPath2(G, G_0, s_0, t_0)
    print('The best score of G_1 is: ')
    print(bestscore)
    print('The optimal path is: ')
    for arc in bestpath:
        print(arc.getStart().getName()+ " -> " + arc.getFinish().getName())
        
    
    
    #Test for getNewGraph(G, G_0)
    newGraph = getNewGraph(G, G_0)
    newnode = sortNodes(newGraph)
    print('new:')
    for node in newnode:
        print(node.getName())
    
    
    
    # Test for CountUpstream(G, s, t).
    print('The result of upstream is: ')
    upstream = CountUpstream(G_0, s_0, t_0)
    for node in upstream:
        print(node.getName()+ " " + str(upstream[node]))
    print('\n')
        
    # Test for CountDownstream(G, s, t).
    print('The result of downstream is: ')
    downstream = CountDownstream(G_0, s_0, t_0)
    for node in downstream:
        print(node.getName()+ " " + str(downstream[node]))
    print('\n')
    
    # Test for PathCounter(G, s, t).
    print('The result of path counter is: ')
    paths = PathCounter(G_1, s_1, t_1)
    for p in paths:
        print(p.getStart().getName() + " -> " + p.getFinish().getName() + " : "
              + str(paths[p]))
    print('\n')
    
    # Test for GraphCosts(G, s, t).
    print('The total costs of this graph is: ')
    print(GraphCosts(G_1))
    print('\n')
    
    # Test for PathsCosts(G_1, s, t).
    print('The total costs of all paths in G_1 is: ')
    print(TotalPathsCosts(G_1, s_1, t_1))
    print('\n')
    
    
    # Test for UpdateUpstream(G_0, u, v, upstream, nodes)
    print("The updated upstream is: ")
    updateUp = UpdateUpstream(G_0, u_0, v_0, upstream, nodes)
    for node in updateUp:
        print(node.getName()+ " " + str(updateUp[node]))
    print('\n')
    
     # Test for UpdateDownstream(G_0, u, v, downstream,nodes)
    print("The updated downstream is: ")
    updateDown = UpdateDownstream(G_0, u_0, v_0, downstream, nodes)
    for node in updateDown:
        print(node.getName()+ " " + str(updateDown[node]))
    print('\n')
    '''
    