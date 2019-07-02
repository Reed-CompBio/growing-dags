import networkx as nx
import math
import matplotlib.pyplot as plt

def ReadGraph(fileName, pagerank=False):
    """
    This function takes in a string of the name of a text file containing the
    information of a graph. And returns a graph according to these information.
    """
    net = nx.DiGraph()
    infile = open(fileName, 'r')
    # Read the network file
    # infile = open(network_file, 'r')
    for line in infile:
        items = [x.strip() for x in line.rstrip().split('\t')]
        # Skip empty lines or those beginning with '#' comments
        if line=='\n':
            continue
        if line[0]=='#':
            continue
        id1 = items[0]
        id2 = items[1]
        # Ignore self-edges
        if id1==id2:
            continue
        # Possibly use an edge weight
        eWeight = 1

        if (not pagerank):
            if(len(items) > 2):
                eWeight = float(items[2])
            else:
                raise Exception(
                    "ERROR: All edges must have a weight "
                    "unless --PageRank is used. Edge (%s --> %s) does "
                    "not have a weight entry." % (id1, id2))   
        # Assign the weight. Note in the PageRank case, "weight" is
        # interpreted as running PageRank and edgeflux on a weighted
        # graph. 
        net.add_edge(id1, id2, weight=eWeight)

    return net


def Creat_s_t(stfileName, G):
    """
    Takes in a text file including the information of node types and a graph 
    object G. Creates a node 's' and a node 't'. Connecting all souce nodes in 
    G with 's' and all target nodes with 't'. Eg: 's'->source, target->'t'.
    """
    infile = open(stfileName, 'r')
    result = G.copy()
    for line in infile:
        items = [x.strip() for x in line.rstrip().split('\t')]
        if line=='\n':
            continue
        if line[0]=='#':
            continue
        if items[1] == 'source':
            source = items[0]
            if source in G.nodes():
                result.add_edge('s', source, weight = 0)
        if items[1] == 'target':
            target = items[0]
            if target in G.nodes():
                result.add_edge(target, 't', weight = 0)
    return result
    

def Get_G_0(G_0_name, G):
    """
    Takes in a text file of G_0 and a graph object G.
    Returns a graph object G_0.
    """
    edges = []
    infile = open(G_0_name, 'r')
    for line in infile:
        items = [x.strip() for x in line.rstrip().split('\t')]
        if line=='\n':
            continue
        if line[0]=='#':
            continue
        id1 = items[0]
        id2 = items[1]
        edge = (id1, id2)
        if edge in G.edges():
            edges.append(edge)
    G_0 = nx.edge_subgraph(G, edges)
    return G_0
    
    
def CountUpstream(G, s, t):
    """
    Takes in a graph object, a starting node, and a ending node.
    In the DAG from s to t, this function returns the number of paths from t to
    each node in the graph. Eg: {s: 5, b: 3}, which means that there are 5 
    paths from t to s, and 3 paths from t to b. 
    """
    nodes = list(nx.topological_sort(G))
    nodes.reverse()
    upstream = dict()
    upstream[t] = 1 
    for node in nodes:
        if node not in upstream:
            number = 0
            for n in G.successors(node):
                number += upstream[n]
            upstream[node] = number
    return upstream


def CountDownstream(G, s, t):
    """
    Takes in a graph object, a starting node, and a ending node.
    In the DAG from s to t, this function returns the number of paths from s to 
    each node in the graph. Eg: {t: 5, b: 1}, which means that there are 5 
    paths from s to t, and 1 path from s to b.
    """
    nodes = nx.topological_sort(G)
    upstream = dict()
    upstream[s] = 1
    for node in nodes:
        if node not in upstream:
            number = 0
            for n in G.predecessors(node):
                number += upstream[n]
            upstream[node] = number
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
    for edge in G.edges():
        paths[edge] = upstream[edge[1]] * downstream[edge[0]]
    return paths


def GraphCosts(G):
    """
    Takes in a graph object, a starting node, and a ending node.
    Returns the total weights of edges in the graph G from s to t.
    """
    return G.size('weight')


def TotalPathsCosts(G, s, t): 
    """
    Takes in a graph object, a starting node, and a ending node.
    Returns the total weights of all paths in the graph G from s to t.
    """
    result = 0
    pc = PathCounter(G, s, t)
    for edge in G.edges():
        if edge in pc:
            cost = G[edge[0]][edge[1]]['weight'] * pc[edge]
            result += cost
    return result


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
        for neighbor in G_0.successors(x):
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
        for neighbor in G_0.predecessors(x):
                number += down[neighbor]
        down[x] = number
        i += 1
    return down
    

def FindNextSubPath(G, G_0, s, t):
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
    nodes = list(nx.topological_sort(G_0))
    for i in range(1,len(nodes)-2):
        for j in range(i+1,len(nodes)-1):
            u = nodes[i]
            v = nodes[j]
            # Make sure the path starts and ends in G_0.
            if u in newGraph.nodes() and v in newGraph.nodes() and nx.has_path(newGraph, u, v):
                distance = nx.dijkstra_path_length(newGraph, u, v)
                path = nx.dijkstra_path(newGraph, u, v)
                # If there is no shortest path, skip.
                if distance == 0 and path == None:
                    continue
                # Check if there exist nodes in the path that are in G_0 other 
                # than the start and end nodes.
                existInG_0 = False
                for node in path:
                    if node == u or node == v:
                        continue
                    elif node in G_0.nodes():
                        existInG_0 = True
                # Skip if there exists any node between the start and end that is in G_0.
                if existInG_0 == True:
                    continue
                up = UpdateUpstream(G_0, u, v, upstream, nodes)
                down = UpdateDownstream(G_0, u, v, downstream, nodes)
                newTotalCost = up[v] * down[u] * distance
                oldTotalCost = 0
                for edge in G_0.edges():
                    oldTotalCost += up[edge[1]] * down[edge[0]] * G[edge[0]][edge[1]]['weight']
                score = newTotalCost + oldTotalCost
                if score < bestscore:
                    bestscore = score
                    bestpath = path
    return bestscore, bestpath


def getNewGraph(G, G_0):
    """
    Takes in Two Graphs G and G_0, returns a new graph G/G_0.
    """
    '''
    newGraph = nx.DiGraph()
    for edge in G.edges():
        if edge not in G_0.edges():
            newGraph.add_edge(edge[0], edge[1], weight=G[edge[0]][edge[1]]['weight'])
    '''
    edges = []
    for edge in G.edges():
        if edge not in G_0.edges():
            edges.append(edge)
    newGraph = nx.edge_subgraph(G, edges)
    return newGraph    
    
    
    
def apply(G_name, G_0_name, stfileName, k, out):
    """
    Takes in two graphs G and G_0. returns a out.txt file containg k paths to 
    be added to graph G_0 based on G by applying the DAG algorithm. 
    """
    out = open(out, 'w')
    out.write('#k\tpath_length\tpath\n')
    G_original = ReadGraph(G_name)
    G_0_original = Get_G_0(G_0_name, G_original)
    G = Creat_s_t(stfileName, G_original)
    G_0 = Creat_s_t(stfileName, G_0_original)
    # keeps track of the sum of all paths in the graph.
    for i in range(1,k+1):
        bestscore, bestpath = FindNextSubPath(G, G_0, 's', 't')
        if bestpath == None:
            path = 'None'
            bestscore = -1
        else:
            path = bestpath[0]
            for node in bestpath:
                if node == bestpath[0]:
                    continue
                path += '|' + node
            for m in range(0, len(bestpath)-1):
                G_0.add_edge(bestpath[m], bestpath[m+1], weight = G[bestpath[m]][bestpath[m+1]])
            #G_0.add_edges_from(newGraph.edges())
            #G_0.add_nodes_from(newGraph.nodes())
        out.write(str(i)+'\t'+str(bestscore)+'\t'+path + '\n')
        print(bestpath)
        # Stop if there is no path to be added.
        if bestpath == None:
            break
    out.close()
    return 


if __name__ == "__main__":
    #G = ReadGraph('G.txt')
    #G_0 = ReadGraph('demo_G_0.txt')
    #G_1 = ReadGraph('demo_G_1.txt')
    #nodes = nx.topological_sort(G_0)
    #upstream = CountUpstream(G_0, 's', 't')
    #downstream = CountDownstream(G_0, 's', 't')
    #print(UpdateUpstream(G_0, 'u', 'v', upstream, nodes))
    #print(CountUpstream(G_1, 's', 't'))
    #print(UpdateDownstream(G_0, 'u', 'v', downstream, nodes))
    #print(CountDownstream(G_1, 's', 't'))
    #print(TotalPathsCosts(G_0, 's', 't'))
    #newGraph = getNewGraph(G, G_0)
    #print(newGraph.edges())
    #print(nx.dijkstra_path_length(G, 's', 't'))
    #path = (nx.dijkstra_path(G, 's', 't'))
    #print(path.edges())
    #print(G.get_edge_data('s', 'b'))
    #G_0.add_edges_from(newGraph.edges())
    #G_0.add_nodes_from(newGraph.nodes())
    #print(G_0.nodes())
    #print(G_0.edges())
    #G_0_original = Get_G_0('G_0.txt', G)
    apply('G.txt', 'G_0.txt','nodetypes.txt', 5, 'output.txt')
    #print(newGraph.edges())
    #print(nx.dijkstra_path(newGraph, 'a', 't'))
    
    