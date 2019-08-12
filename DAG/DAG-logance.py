import networkx as nx
import math
import time
import multi_target_dijkstra as mt
import copy
import sys

total_time_in_dij = 0
lastpath = None

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
        # Skip empty lines or those beginning with '#' comments
        if line=='\n':
            continue
        if line[0]=='#':
            continue

        items = [x.strip() for x in line.rstrip().split('\t')]
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
    addedges = []
    removeedges = []
    for line in infile:
        if line=='\n':
            continue
        if line[0]=='#':
            continue
        items = [x.strip() for x in line.rstrip().split('\t')]

        if items[1] == 'source' or items[1] == 'receptor':
            source = items[0]
            if source in G.nodes():
                for neighbor in G.predecessors(source):
                    removeedges.append((neighbor, source))
                addedges.append(('s', source))

        if items[1] == 'target' or items[1] == 'tf':
            target = items[0]
            if target in G.nodes():
                for neighbor in G.successors(target):
                    removeedges.append((target, neighbor))
                addedges.append((target, 't'))
    result.remove_edges_from(removeedges)
    result.add_edges_from(addedges, weight = 0, log_weight = 0)
    return result


def Get_G_0(G_0_name, G):
    """
    Takes in a text file of G_0 and a graph object G.
    Returns a graph object G_0.
    """
    edges = []
    infile = open(G_0_name, 'r')
    path = []
    ancestors = {'s':set(), "t":set()}
    for line in infile:
        if line=='\n':
            continue
        if line[0]=='#':
            continue

        items = [x.strip() for x in line.rstrip().split('\t')]

        id1 = items[0]
        id2 = items[1]
        if id1 not in path:
            path.append(id1)
        path.append(id2)
        edge = (id1, id2)
        if edge in G.edges():
            edges.append(edge)
    G_0 = nx.edge_subgraph(G, edges)
    prevnodes = set("s")
    for node in list(nx.topological_sort(G_0)):
        ancestors[node] = prevnodes.copy()
        prevnodes.add(node)
    ancestors["t"] = prevnodes.copy()
    pathstring = '|'.join(path)
    return G_0, pathstring, ancestors


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
            cost = G.get_edge_data(edge[0],edge[1])['weight'] * pc[edge]
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

"""
def isConnectedsuc(u, lastpath):
    if not lastpath:
        return True
    suc = u.successors()
    while len(suc) > 0:
def isConnectedpre(v, lastpath):
    if not lastpath:
        return True
"""

def merge_two_dicts(x, y):
    z = x.copy()   # start with x's keys and values
    z.update(y)
    return z


def FindNextSubPath(G, G_0, s, t, checked,G_0_weight, ancestors):
    """
    Takes in a graph G, a DAG G_0, a starting node, a ending node, and a
    dictionary storing shortest paths between pairs of nodes that we've already
    checked. For example: {u:{v:(distance, path)}}.
    Returns the optimal path that minimizes the total costs of all paths of the
    new DAG G_1. Also returns the total costsof all paths after adding the
    optimal path in G_0.
    """
    global total_time_in_dij

    upstream  = CountUpstream(G_0, s, t)

    downstream = CountDownstream(G_0, s, t)

    bestscore = 99999999999999999999999999999999999999999999999
    bestpath = None
    # Find G/G_0.
    newGraph = getNewGraph(G, G_0)
    nodes  = list(nx.topological_sort(G_0))
    for u in G_0.nodes():
        
        if u not in newGraph.nodes():
            continue
        vset = set(G_0.nodes()) - ancestors[u]
        vset.remove(u)
        vset_copy = copy.deepcopy(vset)
        for v in vset_copy:
            if v not in newGraph.nodes() or not nx.has_path(newGraph, u, v):
                vset.remove(v)

        vset_copy = copy.deepcopy(vset)

        if u in checked.keys():
            for v in vset.copy():
                if v in checked[u].keys():
                    path = checked[u][v][1]
                    if len(path) > 2:
                        inG_0 = [node for node in path[1:-1] if node in G_0.nodes()]
                        if len(inG_0) == 0:
                            vset.remove(v)
        else:
            checked[u] = {}

        if len(vset) > 0:
            start = time.time()
            checked[u] = merge_two_dicts(checked[u], mt.multi_target_dijkstra(newGraph, u, vset.copy()))
            end = time.time()
            print("Dijkstra took {} seconds".format(end-start))
        for v in vset_copy:
            u_v_dist, u_v_path = checked[u][v]
            '''
            existsInG_0 = False
            for node in u_v_path:
                if node == u or node == v:
                    continue
                elif node in G_0.nodes():
                    print("Node {0} in path {1} exists in G_0".format(node, u_v_path))
                    existsInG_0 = True
            if existsInG_0:
                continue
            '''
            up = UpdateUpstream(G_0, u, v, upstream, nodes)
            down = UpdateDownstream(G_0, u, v, downstream, nodes)
            newTotalCost = up[v] * down[u] * u_v_dist
            oldTotalCost = 0
            for edge in G_0.edges():
                oldTotalCost += up[edge[1]] * down[edge[0]] * G[edge[0]][edge[1]]['log_weight']
            score = newTotalCost + oldTotalCost
            if score < bestscore:
                bestscore = score
                bestpath = u_v_path
    print("bestpath: {}".format(bestpath))
    print("bestscore: {}".format(bestscore))
    return bestscore, bestpath, checked, G_0_weight



def hasCycles(G_0, bestpath):
    test = G_0.copy()
    for i in range(len(bestpath) - 1):
        test.add_edge(bestpath[i], bestpath[i+1])
    try:
        nx.find_cycle(test)
        return True
    except nx.NetworkXNoCycle:
        return False


def MinTotalWeightofEdges(G, G_0, s, t, checked, G_0_weight, ancestors):
    bestscore = 99999999999999999999999999999999999999999999999
    bestpath = None
    # Find G/G_0.
    newGraph = getNewGraph(G, G_0)
    nodes = list(nx.topological_sort(G_0))

    for u in G_0.nodes():
        
        if u not in newGraph.nodes():
            continue
        vset = set(G_0.nodes()) - ancestors[u]
        vset.remove(u)
        vset_copy = copy.deepcopy(vset)
        for v in vset_copy:
            if v not in newGraph.nodes() or not nx.has_path(newGraph, u, v):
                vset.remove(v)

        vset_copy = copy.deepcopy(vset)

        if u in checked.keys():
            for v in vset.copy():
                if v in checked[u].keys():
                    path = checked[u][v][1]
                    if len(path) > 2:
                        inG_0 = [node for node in path[1:-1] if node in nodes]
                        if len(inG_0) == 0:
                            vset.remove(v)
        else:
            checked[u] = {}

        if len(vset) > 0:
            checked[u] = merge_two_dicts(checked[u], mt.multi_target_dijkstra(newGraph, u, vset.copy()))
            #print("Dijkstra took {} seconds".format(end-start))
        for v in vset_copy:
            u_v_dist, u_v_path = checked[u][v]
            newTotalCost = u_v_dist
            oldTotalCost = 0
            for edge in G_0.edges():
                oldTotalCost += G[edge[0]][edge[1]]['log_weight']
            score = newTotalCost + oldTotalCost
            
            if score < bestscore:
                if not hasCycles(G_0, u_v_path):
                    bestscore = score
                    bestpath = u_v_path
                else:
                    print("Continuing")
                    continue
    print("bestpath: {}".format(bestpath))
    print("bestscore: {}".format(bestscore))
    return bestscore, bestpath, checked,G_0_weight

def MinAverageWeightstoPaths(G, G_0, s, t, checked, G_0_weight, ancestors):
    
    upstream  = CountUpstream(G_0, s, t)

    downstream = CountDownstream(G_0, s, t)

    bestscore = 99999999999999999999999999999999999999999999999
    bestpath = None
    # Find G/G_0.
    newGraph = getNewGraph(G, G_0)
    nodes = list(nx.topological_sort(G_0))

    potential_G_weight = 0
    for i in range(len(nodes)-1):
        u = nodes[i]

        if u not in newGraph.nodes():
            continue

        vset = set(G_0.nodes()) - ancestors[u]
        vset.remove(u)
        vset_copy = copy.deepcopy(vset)
        for v in vset_copy:
            if v not in newGraph.nodes() or not nx.has_path(newGraph, u, v):
                vset.remove(v)
        vset_copy = copy.deepcopy(vset)
        if u in checked.keys():
            for v in vset.copy():
                if v in checked[u].keys():
                    path = checked[u][v][1]
                    if len(path) > 2:
                        inG_0 = [node for node in path[1:-1] if node in nodes]
                        if len(inG_0) == 0:
                            vset.remove(v)
        else:
            checked[u] = {}

        if len(vset) > 0:
            checked[u] = merge_two_dicts(checked[u], mt.multi_target_dijkstra(newGraph, u, vset.copy()))

        for v in vset_copy:
            u_v_dist, u_v_path = checked[u][v]
                
            up = UpdateUpstream(G_0, u, v, upstream, nodes)
            down = UpdateDownstream(G_0, u, v, downstream, nodes)
            newTotalCost = up[v] * down[u] * u_v_dist
            oldTotalCost = 0
            for edge in G_0.edges():
                oldTotalCost += up[edge[1]] * down[edge[0]] * G[edge[0]][edge[1]]['weight']
            new_G_0_weight = newTotalCost + oldTotalCost
            weight_diff = new_G_0_weight - G_0_weight
            path_num_diff = up['s'] - upstream['s']
            score = weight_diff/path_num_diff
            if score < bestscore:
                potential_G_weight = new_G_0_weight
                bestscore = score
                bestpath = u_v_path
                
    
    print("bestpath: {}".format(bestpath))
    print("bestscore: {}".format(bestscore))
    return bestscore, bestpath, checked, potential_G_weight


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

            
def updateAncestors(G_0, ancestors, start):
    for des in G_0.successors(start):
        ancestors[des] |= ancestors[start] 
        updateAncestors(G_0, ancestors, des)        


def logTransformEdgeWeights(net):
    """
    Apply a negative logarithmic transformation to edge weights,
    converting multiplicative values (where higher is better) to
    additive costs (where lower is better).
    Before the transformation, weights are costs of paths
    If the weights in the input graph correspond to probabilities,
    shortest paths in the output graph are maximum-probability paths
    in the input graph.
    """

    for u,v in net.edges():
        w = -math.log(max([0.000000001, net[u][v]['weight']]))/math.log(10)
        net[u][v]['log_weight'] = w
    return


def undoLogTransformPathLengths(paths):
    """
    Undoes the logarithmic transform to path lengths, converting the
    path lengths back into terms of the original edge weights
    :param paths: paths to apply the transform to
    """

    new_paths_list = []

    # Reconstructs the path list with each edge distance un-log transformed.
    # We build a new list because tuples are unmodifiable.
    for path in paths:
        new_path = [(x[0], 10 ** (-1 * x[1])) for x in path]
        new_paths_list.append(new_path)
    return new_paths_list

          

def apply(G_name, G_0_name, stfileName, k, out):
    """
    Takes in two graphs G and G_0. returns a out.txt file containg k paths to
    be added to graph G_0 based on G by applying the DAG algorithm.
    """
    global total_time_in_dij

    out = open(out, 'w')
    out.write('#j\tlog_weight\tpath\n')
    G_original = ReadGraph(G_name)
    
    # Set log_weights to edges of G
    logTransformEdgeWeights(G_original)

    G_0_original, G_0_path, ancestors = Get_G_0(G_0_name, G_original)
    G = Creat_s_t(stfileName, G_original)
    G_0 = Creat_s_t(stfileName, G_0_original)
    
    checked = {}
    total_time_in_func = 0
    G_0_weight = 0
    for edge in G_0.edges():
        G_0_weight += G_0[edge[0]][edge[1]]['log_weight']

    out.write(str(0)+'\t'+str(TotalPathsCosts(G_0, 's', 't')) +'\t'+G_0_path + '\n')

    # keeps track of the sum of all paths in the graph.
    for i in range(1,k+1):
        start = time.time()
        bestscore, bestpath, checked, G_0_weight = MinTotalWeightofEdges(G, G_0, 's', 't', checked, G_0_weight, ancestors)
        end = time.time()
        print('#'+str(i), end-start)
        if bestpath == None:
            path = 'None'
        else:
            print("bestpath:")
            print(bestpath)
            print("\n")
            for m in range(0, len(bestpath)-1):
                G_0.add_edge(bestpath[m], bestpath[m+1], 
                             weight = G[bestpath[m]][bestpath[m+1]]['weight'], 
                             log_weight = G[bestpath[m]][bestpath[m+1]]['log_weight'])
                prev_ancestors = ancestors[bestpath[m]]
                if bestpath[m+1] not in ancestors.keys():
                    ancestors[bestpath[m+1]] = set()
                ancestors[bestpath[m+1]].update(prev_ancestors)
                ancestors[bestpath[m+1]].add(bestpath[m])
            updateAncestors(G_0, ancestors, bestpath[-1])
            if bestpath[0] == "s":
                bestpath = bestpath[1:]
            if bestpath[-1] == "t":
                bestpath = bestpath[:-1]
            path = "|".join(bestpath)
            
        out.write(str(i)+'\t'+str(TotalPathsCosts(G_0, 's', 't')) + '\t'
                  +path + '\n')

        # Stop if there is no path to be added.
        if bestpath == None:
            break
    print("In MinTotalWeightofEdges: {0}".format(total_time_in_func))
    print("In dijkstra: {0}".format(total_time_in_dij))
    out.close()
    print(list(nx.topological_sort(G_0)))
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
    apply('2015pathlinker-weighted.txt', 'NetPath_Pathways/Wnt-G_0.txt','NetPath_Pathways/Wnt-nodes.txt', 100, 'NetPath_Pathways/Wnt-logance-cost1-output.txt')
    #apply('toy_G.txt', 'toy_G_0.txt','toy_nodes.txt', 15, 'toy_output.txt')
    #print(newGraph.edges())