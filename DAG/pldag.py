import networkx as nx
import ksp_Astar as ksp
from math import log


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


def Get_G_0(G_0_name, G):
    """
    Takes in a text file of G_0 and a graph object G.
    Returns a graph object G_0.
    """
    edges = []
    infile = open(G_0_name, 'r')
    path = []
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
    pathstring = '|'.join(path)
    return G_0, pathstring


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
    result.add_edges_from(addedges, weight = 0, ksp_weight = 0)
    return result


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


def logTransformEdgeWeights(net):
    """
    Apply a negative logarithmic transformation to edge weights,
    converting multiplicative values (where higher is better) to
    additive costs (where lower is better).

    Before the transformation, weights are normalized to sum to one,
    supporting an interpretation as probabilities.

    If the weights in the input graph correspond to probabilities,
    shortest paths in the output graph are maximum-probability paths
    in the input graph.

    :param net: NetworkX graph

    """

    for u,v in net.edges():
        w = -log(max([0.000000001, net.adj[u][v]['weight']]))/log(10)
        net.adj[u][v]['ksp_weight'] = w
    return


def undoLogTransformPathLengths(node):
    """
    Undoes the logarithmic transform to path lengths, converting the
    path lengths back into terms of the original edge weights

    :param node: node to apply the transform to (tuple)

    """

    return (10 ** (-1 * node[1]))


def hasCycles(G_0, bestpath):
    test = G_0.copy()
    for i in range(len(bestpath) - 1):
        test.add_edge(bestpath[i][0], bestpath[i+1][1])
    try:
        nx.find_cycle(test)
        return True
    except nx.NetworkXNoCycle:
        return False


def validPath(G_0, path, minNofEdges):
    if hasCycles(G_0, path):
        print("Has a cycle")
        return False

    newEdge = 0
    for i in range(len(path)-1):
        u = path[i][0]
        v = path[i+1][0]
        try:
            G_0[u][v]
            continue
        except KeyError:
            newEdge += 1

    if newEdge >= minNofEdges or newEdge == len(path)-1:
        return True
    return False


def apply(G_name, stfileName, k, out, minNofEdges = 1):
    """
    Takes in two graphs G and G_0. returns a out.txt file containg k paths to
    be added to graph G_0 based on G by applying the DAG algorithm.
    """

    G_original = ReadGraph(G_name)
    logTransformEdgeWeights(G_original)
    G = Creat_s_t(stfileName, G_original)
    G_0 = nx.DiGraph()
    
    added_path_counter = 0
    paths = []
    pointer_to_next_path = 0
    k_multiplier = 1
    added_paths = {}

    while added_path_counter < k:

        if len(paths) == 0:
            print("Getting initial {} paths".format(k))
            paths = ksp.k_shortest_paths_yen(G, "s", "t", k, weight = 'ksp_weight', clip = False)
            print("Computation complete")
        elif pointer_to_next_path == len(paths) - 1:
            k_multiplier += 1
            print("Refreshing path list with k_m = {}".format(k_multiplier))
            paths = ksp.k_shortest_paths_yen(G, "s", "t", k*k_multiplier, weight = 'ksp_weight', clip = False)
            print("Computation complete")

        path = paths[pointer_to_next_path]
        pointer_to_next_path += 1

        if validPath(G_0, path, minNofEdges):
            added_path_counter += 1
            print("#{}: ".format(added_path_counter), path)
            print("\n")
            added_paths[added_path_counter] = path  # This is below so that it will start from 1 instead of 0
            for i in range(len(path)-1):
                n1 = path[i][0]
                n2 = path[i+1][0]
                log_weight = path[i+1][1] - path[i][1]
                G_0.add_edge(n1, n2, ksp_weight = log_weight)


    with open(out, "w") as of:
        of.write('#j\tpath_weight\tpath\n')
        for i in range(1, added_path_counter +1):
            path = added_paths[i]
            formatted_path = ""
            for node in path[1:-1]:
                formatted_path += (node[0]+"|")
            formatted_path = formatted_path[:-1]
            weight = undoLogTransformPathLengths(node)      # Only un-log the last node because it's cumulative
            of.write(str(i)+"\t"+str(weight)+"\t"+formatted_path+"\n")


    return

if __name__ == "__main__":
    apply("2015pathlinker-weighted.txt", 'NetPath_Pathways/BCR-nodes.txt', 200, "BCR-pldag-output.txt", 5)
