import networkx as nx
import math
import argparse
import heapq as hq
import sys
import time

NUM_RERUNS = 0
POSS_RERUNS = 0

"""
This is the main file that script for our signaling pathway reconstruction
using Directed Acyclic Graphs (DAGs) method. This script takes in text files
that contain an interactome,

Usage:
    You can use this script with::

        $ python DAG.py interactome.txt G_0.txt nodes.txt 100

    or for more details::

        $ python DAG.py -h

Dependencies:
    * NetworkX

Notes:
    * If the interactome contains edge costs (lower is better) instead of
    edge weights, use --no-log-transform option.
    * When implementing new cost functions, COST_FUNCTIONS variable and
    the argparse option should be updated.
"""

def main(args):
    """
    Helper function to define the argument parser for usage from terminal.
    """
    parser = argparse.ArgumentParser(description='DAG')
    parser.add_argument("G_file",
                        help="File that contains all the interactions that makes up G, usually the interactome. Must be weighted.")

    parser.add_argument("G_0_file",
                        help="File that contains the initial DAG.")

    parser.add_argument("node_file",
                        help="File that contains node ids and their types. Should not contain nodes named 's' or 't'.")

    parser.add_argument("-k", type=int,default=10,help="Number of paths the algorithm will try to add to G_0 (default 10). The algorithm might end earlier if it cannot find more paths.")

    parser.add_argument('-o',"--out_file", default=False, help="Output file name. (default='dag-out-{k}.txt')")

    parser.add_argument("--no-log-transform", action="store_true", default=False,
                        help="If G_file contains interaction costs (lower is better) instead of probabilities"
                             "(higher is better), this option should be used.")

    parser.add_argument('-c',"--cost-function", type=int, choices=[1,2,3,4,5], default=2,
                        help="Choice of cost function. (default=2)\n"
                             "1-Minimize the total cost of all edges(Dijkstra)."
                             "2-Minimize the total cost of all paths(Dijkstra)."
                             "3-Maximize the number of paths using shortest paths(Dijkstra)."
                             "4-Mixture of 1 and 2 where total score is a*score1 + (1-a)*score2 (default a=0.5)"
                             "5-Minimize the total cost of all paths(Floyd-Warshall).")

    parser.add_argument("-a", type=float, default=0.5,
                        help="When cost function 4 is being used, the total score is "
                             "a*score of cost function 1 + (1-a)*score of cost function 2."
                             "By default a = 0.5.")

    args = parser.parse_args()

    # If there is no output file name, create one
    if not args.out_file:
        args.out_file = "dag-out-{}.txt".format(args.k)

    # Run the main algorithm
    apply(args.G_file, args.G_0_file, args.node_file, args.k, args.out_file, args.cost_function, args.no_log_transform,
          args.a)
    return

def readGraph(G_file):
    """
    This function takes in a string of the name of a text file containing the
    information of a graph. And returns a graph according to these information.
    The graph must contain edge weights.

    :param G_file: A tab delimited .txt file that contains a tail and head
                    proteins of a directed interaction for the whole interactome
                    and their weights/costs.
    :return: A NetworkX DiGraph object that represents the interactome where nodes
            are proteins, edges are interactions. Each edge contains a "weight" attribute
            containing the weights included in the input file.
    """
    # Initialize empty Directed Graph
    G = nx.DiGraph()

    with open(G_file) as f:
        for line in f:
            # Skip empty lines or comments
            if line == "\n" or line[0] == "#":
                continue

            items = [x.strip() for x in line.rstrip().split()]
            node1 = items[0]
            node2 = items[1]
            # Skip self-edges
            if node1 == node2:
                continue
            # Get edge weight, otherwise raise Exception
            try:
                edge_weight = float(items[2])
            except IndexError:
                raise Exception(
                    "ERROR: All edges must have a weight. "
                    "Edge {} --> {} does not have a weight entry.".format(node1, node2))
            # Add the edge to graph
            G.add_edge(node1, node2, weight=edge_weight)
    return G

def logTransformEdgeWeights(G):
    """
    Modifies G so that each edge has an attribute "cost" that contains
    lower-is-better edge costs, used to determine shortest paths.
    This function should only be used when "weight" attribute created in
    ```readGraph``` contains edge weights that are bigger-is-better.

    :param G: The graph created using ```readGraph``` function.
    """
    for u, v in G.edges():
        w = -math.log(max([0.000000001, G[u][v]['weight']])) / math.log(10)
        G[u][v]['cost'] = w
    return

def turnWeightsIntoCosts(G):
    """
    Modifies G so that each edge has an attribute "cost" that contains
    lower-is-better edge costs, used to determine shortest paths.
    This function should only be used when "weight" attribute created in
    ```readGraph``` contains edge weights that are lower-is-better.

    :param G: The graph created using ```readGraph``` function.
    """
    for u, v in G.edges():
        G[u][v]["cost"] = G[u][v]["weight"]
    return

def addSourceSink(node_file, G):
    """
    Modifies G to connect all the receptors into a super-source 's' and
    a super-sink 't', according to the information in node_file.

    :param node_file: A tab delimited file that contains each protein in the pathway
            and whether it is a receptor, tf, or None.
    :param G: The graph created using ```readGraph``` function.
    :return: * receptors (set): contains the receptors in the pathway
             * tfs (set): contains the transcription factors in the pathway
    """
    # Empty sets to contain receptors and tfs
    receptors = set()
    tfs = set()

    # Find receptors and tfs
    with open(node_file) as f:
        for line in f:
            if line == "\n" or line[0] == "#":
                continue
            items = [x.strip() for x in line.rstrip().split()]
            if items[1] == "source" or items[1] == "receptor":
                receptors.add(items[0])
            elif items[1] == "target" or items[1] == "tf":
                tfs.add(items[0])

    # Remove incoming edges to receptors and outgoing edges from tfs.
    # NEW 2022
    to_remove = []
    for u,v in G.edges():
        if v in receptors or u in tfs:
            to_remove.append([u,v])
    print('removing %d edges into receptors or out of tfs' % (len(to_remove)))
    G.remove_edges_from(to_remove)

    # Connect receptors to s
    for receptor in receptors:
        if receptor not in G.nodes():
            raise Exception("Node {} not in G. It is listed as a receptor.".format(receptor))
        G.add_edge("s", receptor, weight=1, cost=0)
        #print('adding edge: s ->',receptor)

    # Connect tfs to t
    for tf in tfs:
        if tf not in G.nodes():
            raise Exception("Node {} not in G. It is listed as a tf.".format(tf))
        G.add_edge(tf, "t", weight=1, cost=0)
        #print('adding edge:',tf,'-> t')

    # For creation of G_0
    return receptors, tfs

def createG_0(G_0_file, G, receptors, tfs):
    """
    Creates an edge subgraph of G from G_0 file, including s and t.
    Also returns ancestors dictionary based on G_0

    :param G_0_file: A tab delimited file that contains the ground-truth information about a pathway
            to which our script will add new paths.
    :param G: The graph created using ```readGraph``` function.
    :param receptors: The list created using ```addSourceSink``` function.
    :param tfs: The list created using ```addSourceSink``` function.
    :return: G_0: A NetworkX DiGraph representing the information in G_0_file.
    """
    edges = set()

    # Collect G_0 edges from G_0 file
    with open(G_0_file) as f:
        for line in f:
            if line == "\n" or line[0] == "#":
                continue

            items = [x.strip() for x in line.rstrip().split()]
            node1 = items[0]
            # If receptor, connect to s
            if node1 in receptors:
                edges.add(("s", node1))

            node2 = items[1]
            # If tf, connect to t
            if node2 in tfs:
                edges.add((node2, "t"))

            # NEW 2022: ignore edges out of tfs or into receptors:
            if node1 in tfs or node2 in receptors:
                continue

            edge = (node1, node2)
            if edge not in G.edges():
                raise Exception(
                    "G_0 edge {} --> {} not found in G.".format(node1, node2))
            edges.add(edge)

    # edge_subgraph creates a Read-only view
    # The outer DiGraph function turns it into a mutable graph
    G_0 = nx.DiGraph(G.edge_subgraph(edges))
    assert nx.is_directed_acyclic_graph(G_0)
    return G_0, None

def CountPathsToSink(G_0):
    """
    Returns a dictionary with nodes as keys and values for
    how many paths there are from node to t (super-sink).
    Eg: {s: 5, b: 3}, which means that there are 5
    paths from s to t, and 3 paths from b to t.

    :param G_0: The graph created using ```createG_0``` function.
    :return: dictionary where keys are nodes and values are the
            number of paths from the node to super-sink.
    """
    nodes = list(nx.topological_sort(G_0))
    nodes.reverse()
    n_paths_to_sink = dict()
    n_paths_to_sink["t"] = 1
    for node in nodes:
        if node not in n_paths_to_sink:
            number = 0
            for n in G_0.successors(node):
                number += n_paths_to_sink[n]
            n_paths_to_sink[node] = number
    return n_paths_to_sink

def CountPathsFromSource(G_0):
    """
    Returns a dictionary with nodes as keys and values for
    how many paths there are from s (super-source) to node.
    Eg: {t: 5, b: 1}, which means that there are 5
    paths from s to t, and 1 path from s to b.

    :param G_0: The graph created using ```createG_0``` function.
    :return: dictionary where keys are nodes and values are the
            number of paths from the super-source to the node.
    """
    nodes = nx.topological_sort(G_0)
    n_paths_from_source = dict()
    n_paths_from_source["s"] = 1
    for node in nodes:
        if node not in n_paths_from_source:
            number = 0
            for n in G_0.predecessors(node):
                number += n_paths_from_source[n]
            n_paths_from_source[node] = number
    return n_paths_from_source

def getG_delta(G, G_0):
    """
    Used as the graph where new paths are found.

    :param G: The graph created using ```readGraph``` function.
    :param G_0: The graph created using ```createG_0``` function.
    :return: A read-only G_delta that is G - G_0. (* with some extra edges removed)
    """
    '''
    induced = nx.induced_subgraph(G,G_0.nodes()).copy()
    print('G_0 has %d edges; induced G_0 has %d edges' %(len(G_0.edges()),len(induced.edges())))
    to_remove = []
    for edge in induced.edges():
        if edge in G_0.edges(): # definitely keep G_0 to remove.
            continue
        ancestors = nx.ancestors(G_0,edge[1])
        if edge[0] in ancestors:
            to_remove.append(edge)
    induced.remove_edges_from(to_remove)
    print('Removing %d edges after retaining edges that follow topological order' %(len(induced.edges())))
    # NEW 2022: it's possible that (u,v) is in G but v < u in G_0's nodes.
    # This should NEVER be selected because it violates the DAG; remove these.
    # fixed this by using induced subgraph rather than G_0 and ignoring edges that are OK.
    '''
    edges = []
    for edge in G.edges():

        if edge not in G_0.edges():
            edges.append(edge)

    G_delta = nx.edge_subgraph(G, edges)
    #print('removed %d edges from G (%d edges) to get G_delta (%d edges)' % (len(G.edges())-len(edges),len(G.edges()),len(G_delta.edges())))
    return G_delta

def UpdatePathsToSink(G_0, u, v, n_paths_to_sink, nodes):
    """
    Used within cost functions to enumerate the usage of each edge if
    a path between u and v were added.

    :param G_0: The graph created using ```createG_0``` function.
    :param u: The starting node of a path.
    :param v: The ending node of a path.
    :param n_paths_to_sink: The dictionary created using ```CountPathsToSink``` function.
    :param nodes: The list created within cost functions.
    :return: A modified version of n_paths_to_sink for a graph if a path between
            u and v were added to G_0.
    """
    new = n_paths_to_sink.copy()
    new[u] = n_paths_to_sink[u] + n_paths_to_sink[v]
    i = nodes.index(u) - 1
    while i >= 0:
        x = nodes[i]
        number = 0
        for neighbor in G_0.successors(x):
            number += new[neighbor]
        new[x] = number
        i -= 1
    return new

def UpdatePathsFromSource(G_0, u, v, n_paths_from_source, nodes):
    """
    Used within cost functions to enumerate the usage of each edge if
    a path between u and v were added

    :param G_0: The graph created using ```createG_0``` function.
    :param u: The starting node of a path
    :param v: The ending node of a path
    :param n_paths_from_source: The dictionary created using ```CountPathsFromSource``` function.
    :param nodes: The list created withing cost functions.
    :return: A modified version of n_paths_from_source for a graph if a path between
    u and v were added to G_0.
    """
    new = n_paths_from_source.copy()
    new[v] = n_paths_from_source[u] + n_paths_from_source[v]
    i = nodes.index(v) + 1
    while i < len(new):
        x = nodes[i]
        number = 0
        for neighbor in G_0.predecessors(x):
            number += new[neighbor]
        new[x] = number
        i += 1
    return new

def multi_target_dijkstra(G, u, vset, all_vs):
    """
    Finds the shortest paths from u to every node in vset.

    :param G: The graph where shortest paths are found. Intended to be G_delta.
    :param u: The starting node for the paths.
    :param vset: The set of nodes to find shortest paths.
    :param all_vs: All downstream and incomparable nodes that should not be internal on any path.
    :return: A dictionary where keys are nodes in vset and values are a tuple of distance and path.
    """
    """
    Takes in a networkx graph, a starting node u and a set of target nodes vset.
    Returns a dictionary that has nodes as keys and a tuple of distance, path as values.
    """
    #print('MULTI_TARGET_DIJKSTRA',u,vset,all_vs)

    heap = []  # contains lists of distance, node, path
    finished = {}  # node -> (dist, path)
    seen = {}  # node -> dist
    orig_vset = vset.copy()

    # In case old math module
    try:
        inf = math.inf
    except AttributeError:
        inf = 99999999999999

    # Create priority queue entries for each node
    for item in G.nodes():
        path = None
        dist = inf
        # Starting node
        if item == u:
            path = [u]
            dist = 0
        hq.heappush(heap, (dist, item, path))
        seen[item] = dist

    # Iterate over vset so function will quit when all target nodes are found
    found_vset = set()
    while len(vset) > len(found_vset) and len(heap) > 0:
        current_dist, current_node, current_path = hq.heappop(heap)

        # if current_node already has a smaller distance or equal, skip it.
        if current_node in finished and current_dist >= finished[current_node][0]:
            continue

        # otherwise, update finished dictionary & explore.
        finished[current_node] = (current_dist, current_path)

        # A node popping from the priority queue means shortest path to it is found
        # new 2022: if you find a node in vset, DO NOT continue. It would otherwise be considered an internal node.
        #print('\n')
        #print(current_node,finished[current_node])
        if current_node in all_vs:
            if current_node in vset:
                found_vset.add(current_node)
        else:
            #print(current_node,'continues!')
            for node in G.successors(current_node):
                dist = current_dist + G[current_node][node]["cost"]
                if dist < seen[node]:
                    seen[node] = dist
                    hq.heappush(heap, (dist, node, current_path + [node]))

    # new 2022: prune finished to just be vset.
    finished_vset = {v:finished[v] for v in finished if v in vset}
    finished_vset.update({v:(inf,None) for v in vset if v not in finished})

    #print(len(finished_vset),finished_vset)
    #if len(finished_vset)>0:
    #    sys.exit()
    return finished_vset

def costFunction2(G,G_0,u,v,u_v_cost,u_v_path, n_paths_to_sink,n_paths_from_source,nodes):

    # Get how many paths there are from each node to s and t if edge u->v is added to G_0
    new_n_paths_to_sink = UpdatePathsToSink(G_0, u, v, n_paths_to_sink, nodes)
    new_n_paths_from_source = UpdatePathsFromSource(G_0, u, v, n_paths_from_source, nodes)

    # addedCost is the cost of the path * how many times it appears in all paths from s to t
    # We can treat the path from u to v as a single edge because all the nodes in between are not in G_0
    # hence cannot branch into other paths.
    totalCostOfNewPath = new_n_paths_to_sink[v] * new_n_paths_from_source[u] * u_v_cost

    # TotalCostOfRest is the total cost of G_0 if u->v was added, excluding the cost of u->v.
    # They are calculated separately because u->v is not actually added to G_0
    totalCostOfRest = 0
    for edge in G_0.edges():
        totalCostOfRest += new_n_paths_to_sink[edge[1]] * new_n_paths_from_source[edge[0]] * \
                           G[edge[0]][edge[1]]['cost']
    score = totalCostOfNewPath + totalCostOfRest
    return score

def update_distances(G_0,G_delta,dist={},added_path=[]):
    global NUM_RERUNS,POSS_RERUNS
    ## if just G_0 is passed, initialize distances.
    ## otherwise update.

    #generations = [set(g) for g in nx.topological_generations(G_0)]
    #print('GENERATIONS:',generations)
    '''
    print('*'*10)
    print('G DELTA EDGES')
    for edge in G_delta.edges():
        print(edge)
    print('*'*10)
    '''
    #print('\nSTARTING UPDATE')

    if dist == {}:
        print('Initializing Distances...')
        num = 0
        for u in G_0.nodes():
            num+=1
            print('running for %s (%d/%d)' % (u,num,G_0.number_of_nodes()))
            upstream = set(nx.ancestors(G_0,u))
            downstream = set(nx.descendants(G_0,u))
            incomparable = set(G_0.nodes()) - upstream - downstream - set([u])
            G_delta_copy = G_delta.copy()
            G_delta_copy.remove_nodes_from(upstream)
            start = time.time()
            dist[u] = multi_target_dijkstra(G_delta_copy, u, downstream.union(incomparable),downstream.union(incomparable))
            end = time.time()
            for v in dist[u].keys():
                if dist[u][v][1] != None:
                    internal_nodes = dist[u][v][1][1:-1]
                    if any([x in G_0.nodes() for x in internal_nodes]):
                        print('ERROR: internal node is in G_0!')
                        print(u,v,dist[u][v])
                        print(internal_nodes,'internal nodes')
                        print(G_0.nodes(),'G_0s nodes')
                        print('!!!')
                        print(dist)
                        print('!!!')
                        for u in dist:
                            print(' ',u,':',dist[u])
                        print('!!!')
                        sys.exit()

            #print("Init Dijkstra took {} seconds".format(end - start))
        print('done init. distances')
        #sys.exit()
    else:
        #print('Updating Distances...')

        ## get source/receptors (could be passed in)
        source_nodes = [u for u in G_0.nodes() if G_0.has_edge('s',u)]
        #print('source nodes:',source_nodes)

        # internal nodes from added_path (will be empty if added_path is edge)
        internal_nodes = set(added_path[1:-1])

        # for every node in G_0...
        for u in G_0.nodes():
            if G_0.has_edge(u,'t'): # target/tf; skip
                dist[u] = {'t':(math.inf,None)}
                continue

            upstream = set(nx.ancestors(G_0,u))
            if u != 's': # don't check source nodes as downstream.
                upstream.update(source_nodes)

            downstream = set(nx.descendants(G_0,u))
            incomparable = set(G_0.nodes()) - upstream - downstream - set([u])

            # 1. delete any u -> upstream distances (were previously incomparable)
            for up in upstream:
                if u in dist and up in dist[u]:
                    del dist[u][up]

            # 2. add any targets that (a) are not in dist dict or (b) have paths that contain
            # internal nodes from the added_path.
            if u in internal_nodes: # calculate all downstream & incomparable.
                #print(u,'is an internal node!')
                assert u not in dist
                rerun = downstream.union(incomparable)
                dist[u] = {}
            else:
                rerun = set()
                for v in downstream.union(incomparable):
                    if v not in dist[u] or (dist[u][v][1] != None and len(set(dist[u][v][1]).intersection(internal_nodes))>0) or [u,v] == added_path:
                        rerun.add(v)

            #print('  Rerun Dijkstra for {} ({}/{})'.format(u,len(rerun),len(downstream.union(incomparable))))
            NUM_RERUNS += len(rerun)
            POSS_RERUNS += len(downstream.union(incomparable))

            start = time.time()
            if len(rerun)>0:
                G_delta_copy = G_delta.copy()
                G_delta_copy.remove_nodes_from(upstream)
                res = multi_target_dijkstra(G_delta_copy, u, rerun, downstream.union(incomparable))
                #print(res)
                dist[u].update(res)
            end = time.time()
            #print("Took {} seconds".format(end - start))
    #print('ENDING UPDATE\n')
    return dist

def get_best_path(G, G_0, dist, cost_function):
    """
    Finds shortest paths in G - G_0 and returns the path that minimizes the total cost of all paths.

    :param G: The graph created using ```readGraph``` function.
    :param G_0: The graph created using ```createG_0``` function.
    :param ancestors: The dictionary created using ```createG_0``` function.
    :return: * bestscore (float): The score of the bestpath according to the cost function.
             * bestpath (list): The list of nodes that make up the path to be added to G_0.
    """

    # pre-computed variables depends on the cost function.
    if cost_function == 1:
        # get sum of all edges in G_0
        all_edge_costs = sum([c for c in nx.get_edge_attributes(G_0, "cost").values()])
    if cost_function == 2 or cost_function == 3:
        # Obtain the number of paths from node to s/t in G_0
        n_paths_to_sink = CountPathsToSink(G_0)
        n_paths_from_source = CountPathsFromSource(G_0)
        # get list of nodes
        nodes = list(nx.topological_sort(G_0))

    # Initialize best score as a big number
    try:
        bestscore = math.inf
    # In case old math module
    except AttributeError:
        bestscore = 99999999999999999999
    bestpath = None

    # G_delta = G - G_0
    G_delta = getG_delta(G, G_0)

    print('\nGETTING BEST PATH')
    for u in G_0.nodes():
        # If all the edges connected to a node is in G_0, node will not be in G_delta
        if u not in G_delta.nodes():
            continue

        for v in dist[u].keys():
            if dist[u][v][1] == None:
                continue

            u_v_cost, u_v_path = dist[u][v]
            internal_nodes = u_v_path[1:-1]
            if len(set(internal_nodes).intersection(set(G_0.nodes()))) > 0:
                print('ERROR: internal node is in G_0!')
                print(u_v_path)
                print(internal_nodes,'internal nodes')
                print(G_0.nodes(),'G_0s nodes')
                print('!!!')
                print(dist)
                print('!!!')
                for u in dist:
                    print(' ',u,':',dist[u])
                print('!!!')
                sys.exit()


            if cost_function == 1:
                # This is the total cost of all edges if u->v path was added to G_0
                score = all_edge_costs + u_v_cost

            elif cost_function == 2:
                score = costFunction2(G,G_0,u,v,u_v_cost,u_v_path, n_paths_to_sink,n_paths_from_source,nodes)

            elif cost_function == 3:
                score = costFunction3(G,G_0,u,v,u_v_cost,u_v_path, n_paths_to_sink,n_paths_from_source,nodes)

            elif cost_function == 4:
                bestscore, bestpath = cost_function(G, G_0, ancestors, a)


            if score < bestscore:
                bestscore = score
                bestpath = u_v_path
                #print('**BEST SCORE SO FAR!',bestscore,bestpath)

    return bestscore, bestpath

def apply(G_file, G_0_file, node_file, k, out_file, cost_function, no_log_transform, a):
    """
    The main function for the script.

    :param G_file: A tab delimited file name containing the interactome information.
    :param G_0_file: A tab delimited file name containing the ground-truth information.
    :param node_file: A tab delimited file name containing node information.
    :param k: The number of paths to be added to G_0. The function can end before k if no paths can be found.
    :param out_file: The name of the output file.
    :param cost_function: The cost function to be used when evaluating paths.
    :param no_log_transform: Boolean to indicate whether the edge weights in G_file should be transformed to costs.
    """

    G = readGraph(G_file)

    # Create cost attributes for cost functions
    # At the end of this, each edge should have a "cost" attribute where a lower value means a more likely interaction
    if no_log_transform:
        turnWeightsIntoCosts(G)
    else:
        logTransformEdgeWeights(G)

    # Add s and t nodes to G, receptors and tfs will be used for G_0 creation
    receptors, tfs = addSourceSink(node_file, G)

    # Create G_0 and ancestors
    G_0, ignore = createG_0(G_0_file, G, receptors, tfs)

    # initialize distances dictionary
    G_delta = getG_delta(G, G_0)
    dist = update_distances(G_0,G_delta)

    # Open the output file
    of = open(out_file, "w")
    of.write('#j\tscore of cost function\tpath\n')

    # Main loop
    for i in range(1, k + 1):

        # Get the next best path
        start = time.time()
        bestscore, bestpath = get_best_path(G, G_0, dist, cost_function)
        end = time.time()
        # If no more paths, break
        if bestpath is None:
            break

        print("#" + str(i), bestpath, 'time:',(end - start),'\n')

        # Add edges of the new path to G_0
        for m in range(len(bestpath) - 1):
            G_0.add_edge(bestpath[m], bestpath[m + 1],
                         weight=G[bestpath[m]][bestpath[m + 1]]['weight'],
                         cost=G[bestpath[m]][bestpath[m + 1]]['cost'])

        # update distances dictionary
        G_delta = getG_delta(G, G_0)
        dist = update_distances(G_0,G_delta,dist,bestpath)

        # Get rid of super-source and sink
        if bestpath[0] == "s":
            bestpath = bestpath[1:]
        if bestpath[-1] == "t":
            bestpath = bestpath[:-1]
        path = "|".join(bestpath)

        # Write path to output file
        of.write(str(i) + '\t' + str(bestscore) + '\t' + path + '\n')

    print("DAG done")
    return


if __name__ == "__main__":
    total_start = time.time()
    main(sys.argv)
    total_end = time.time()
    print()
    print('%d Dijksta reruns out of %d total' % (NUM_RERUNS,POSS_RERUNS))
    print("Function call took {} seconds in total.".format(total_end - total_start))
