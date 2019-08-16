import networkx as nx
import math
import argparse
import heapq as hq
import sys
import time

"""
DO NOT FORGET TO UPDATE COST FUNCTIONS DICTIONARY DEFINED JUST BEFORE MAIN
"""


def readGraph(G_file):
    """
    This function takes in a string of the name of a text file containing the
    information of a graph. And returns a graph according to these information.
    The graph must contain edge weights.
    """
    # Initialize empty Directed Graph
    G = nx.DiGraph()

    with open(G_file) as f:
        for line in f:
            # Skip empty lines or comments
            if line == "\n" or line[0] == "#":
                continue

            items = [x.strip() for x in line.rstrip().split('\t')]
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
    Apply a negative logarithmic transformation to edge weights,
    converting multiplicative values (where higher is better) to
    additive costs (where lower is better).
    """
    for u, v in G.edges():
        w = -math.log(max([0.000000001, G[u][v]['weight']])) / math.log(10)
        G[u][v]['cost'] = w
    return


def turnWeightsIntoCosts(G):
    """
    When the G file has costs (lower is better) instead of weights (higher is better), this function is used to
    copy weight attributes to cost
    """
    for u, v in G.edges():
        G[u][v]["cost"] = G[u][v]["weight"]
    return


def addSourceSink(node_file, G):
    """
    Takes in the name of a file that contains node information and a graph G.
    Connects all the receptor nodes in G to a super-source s
    and all the transcription factors to a super-sink t.
    Returns the set of receptors and tfs to assist creation of s and t
    in G_0.
    """
    # Empty sets to contain receptors and tfs
    receptors = set()
    tfs = set()

    # Find receptors and tfs
    with open(node_file) as f:
        for line in f:
            if line == "\n" or line[0] == "#":
                continue
            items = [x.strip() for x in line.rstrip().split('\t')]
            if items[1] == "source" or items[1] == "receptor":
                receptors.add(items[0])
            elif items[1] == "target" or items[1] == "tf":
                tfs.add(items[0])

    # Connect receptors to s
    for receptor in receptors:
        if receptor not in G.nodes():
            raise Exception("Node {} not in G. It is listed as a receptor.".format(receptor))
        G.add_edge("s", receptor, weight=1, cost=0)

    # Connect tfs to t
    for tf in tfs:
        if tf not in G.nodes():
            raise Exception("Node {} not in G. It is listed as a tf.".format(tf))
        G.add_edge(tf, "t", weight=1, cost=0)

    # For creation of G_0
    return receptors, tfs


def createAncestors(G_0, ancestors, starting_node="s", node_ancestors=None):
    """
    Fills in the ancestors dictionary as a part of createG_0 function.
    """
    if node_ancestors is None:
        node_ancestors = set()

    for node in G_0.successors(starting_node):
        # Initialize empty sets
        if node not in ancestors.keys():
            ancestors[node] = set()
        # Merge ancestors and add itself
        ancestors[node] |= node_ancestors
        ancestors[node].add(starting_node)
        createAncestors(G_0, ancestors, node, ancestors[node])


def createG_0(G_0_file, G, receptors, tfs):
    """
    Creates an edge subgraph of G from G_0 file, including s and t.
    Also return ancestors based on G_0.
    """
    edges = set()
    ancestors = {"s": set(), "t": set()}

    # Collect G_0 edges from G_0 file
    with open(G_0_file) as f:
        for line in f:
            if line == "\n" or line[0] == "#":
                continue

            items = [x.strip() for x in line.rstrip().split('\t')]
            node1 = items[0]
            # If receptor, connect to s
            if node1 in receptors:
                edges.add(("s", node1))

            node2 = items[1]
            # If tf, connect to t
            if node2 in tfs:
                edges.add((node2, "t"))

            edge = (node1, node2)
            if edge not in G.edges():
                raise Exception(
                    "G_0 edge {} --> {} not found in G.".format(node1, node2))
            edges.add(edge)

    # edge_subgraph creates a Read-only view
    # The outer DiGraph function turns it into a mutable graph
    G_0 = nx.DiGraph(G.edge_subgraph(edges))
    createAncestors(G_0, ancestors)
    return G_0, ancestors


def CountPathsToSink(G_0):
    """
    Takes in a graph object.
    Returns a dictionary with nodes as keys and values for
    how many paths there are from node to t (super-sink).
    Eg: {s: 5, b: 3}, which means that there are 5
    paths from s to t, and 3 paths from b to t.
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
    Takes in a graph object.
    Returns a dictionary with nodes as keys and values for
    how many paths there are from s (super-source) to node.
    Eg: {t: 5, b: 1}, which means that there are 5
    paths from s to t, and 1 path from s to b.
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
    Takes in Two Graphs G and G_0, returns a READ-ONLY new graph G/G_0.
    """
    edges = []
    for edge in G.edges():
        if edge not in G_0.edges():
            edges.append(edge)
    G_delta = nx.edge_subgraph(G, edges)
    return G_delta


def merge_two_dicts(x, y):
    """
    Merges two dictionaries with giving priority to values in y
    """
    z = x.copy()
    z.update(y)
    return z


def UpdatePathsToSink(G_0, u, v, n_paths_to_sink, nodes):
    """
    Takes in G_0, the nodes of the edges to be tested,
    n_paths_to_sink from CountPathsToSink and nodes from nx.topological_sort.
    Returns how n_paths_to_sink would be if edge u->v was added to G_0.
    DOES NOT ADD EDGE u->v TO G_0
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
    Takes in G_0, the nodes of the edges to be tested,
    n_paths_from_source from CountPathsFromSource and nodes from nx.topological_sort.
    Returns how n_paths_from_source would be if edge u->v was added to G_0.
    DOES NOT ADD EDGE u->v TO G_0
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


def multi_target_dijkstra(G, u, vset):
    """
    Takes in a networkx graph, a starting node u and a set of target nodes vset.
    Returns a dictionary that has nodes as keys and a tuple of distance, path as values.
    """
    heap = []  # contains lists of distance, node, path
    finished = {}  # node -> (dist, path)
    seen = {}  # node -> dist

    # Create priority queue entries for each node
    for item in G.nodes():
        path = None
        dist = math.inf
        # Starting node
        if item == u:
            path = [u]
            dist = 0
        hq.heappush(heap, (dist, item, path))
        seen[item] = dist

    # Iterate over vset so function will quit when all target nodes are found
    while len(vset) > 0:
        current_dist, current_node, current_path = hq.heappop(heap)
        if current_node in finished.keys():
            continue
        finished[current_node] = (current_dist, current_path)

        # A node popping from the priority queue means shortest path to it is found
        if current_node in vset:
            vset.remove(current_node)

        for node in G.successors(current_node):
            if node in finished.keys():
                continue
            dist = current_dist + G[current_node][node]["cost"]
            if dist < seen[node]:
                seen[node] = dist
                hq.heappush(heap, (dist, node, current_path + [node]))

    return finished


def costFunction2(G, G_0, ancestors):
    """
    Also known as FindNextSubPath
    """
    # Obtain the number of paths from node to s/t in G_0
    n_paths_to_sink = CountPathsToSink(G_0)
    n_paths_from_source = CountPathsFromSource(G_0)

    # This will be needed for UpdatePathsFromSource and UpdatePathsFromSink functions.
    # It is here otherwise it will be called twice for every v in vset for every u.
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

    for u in G_0.nodes():
        # If all the edges connected to a node is in G_0, node will not be in G_delta
        if u not in G_delta.nodes():
            continue

        # Vset is the set of nodes that doesn't have a path to u
        vset_original = set(G_0.nodes()) - ancestors[u]

        # Self is removed from target v's
        vset_original.remove(u)

        # Set size can't be changed during iteration so vset is copied.
        vset_modified = vset_original.copy()

        # Remove v's that cannot be reached in G_delta
        for v in vset_original:
            if v not in G_delta.nodes or not nx.has_path(G_delta, u, v):
                vset_modified.remove(v)

        if len(vset_modified) > 0:
            start = time.time()
            results = multi_target_dijkstra(G_delta, u,
                                               vset_modified.copy())  # This copy is only here when for loop below is over vset_modified
            end = time.time()
            print("Dijkstra took {} seconds".format(end - start))

        # In the working version of DAG, this happens over vset_original with checked, to take into account previously calculated stuff
        # Here I've changed it into vset_modified to get rid of checked and reimplement it later to make sure everything is working ok
        # Also, this for loop should be at the same level as if len(vset_modified) > 0 when checked is being used
        for v in vset_modified:
            u_v_cost, u_v_path = results[v]

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

            if score < bestscore:
                bestscore = score
                bestpath = u_v_path

    return bestscore, bestpath


def floydWarshall(G, G_0, ancestor):
    """
    This is the same cost function as costFunction2, but paths are obtained using Floyd-Warshall algorithm.
    ancestor argument is redundant. It is here to keep all the arguments for all cost functions consistent.
    """

    # Obtain the number of paths from node to s/t in G_0
    n_paths_to_sink = CountPathsToSink(G_0)
    n_paths_from_source = CountPathsFromSource(G_0)

    # This will be needed for UpdatePathsFromSource and UpdatePathsFromSink functions.
    # It is here otherwise it will be called twice for every edge.
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

    start = time.time()
    predecessors, distance = nx.floyd_warshall_predecessor_and_distance(G_delta, weight="cost")
    end = time.time()
    print("Floyd-Warshall took {} seconds.".format(end-start))

    for u in G_0.nodes():
        for v in G_0.nodes():

            if u == v:
                continue

            # Get how many paths there are from each node to s and t if edge u->v is added to G_0
            new_n_paths_to_sink = UpdatePathsToSink(G_0, u, v, n_paths_to_sink, nodes)
            new_n_paths_from_source = UpdatePathsFromSource(G_0, u, v, n_paths_from_source, nodes)

            # addedCost is the cost of the path * how many times it appears in all paths from s to t
            # We can treat the path from u to v as a single edge because all the nodes in between are not in G_0
            # hence cannot branch into other paths.
            totalCostOfNewPath = new_n_paths_to_sink[v] * new_n_paths_from_source[u] * distance[u][v]

            # TotalCostOfRest is the total cost of G_0 if u->v was added, excluding the cost of u->v.
            # They are calculated separately because u->v is not actually added to G_0
            totalCostOfRest = 0
            for edge in G_0.edges():
                totalCostOfRest += new_n_paths_to_sink[edge[1]] * new_n_paths_from_source[edge[0]] * \
                                   G[edge[0]][edge[1]]['cost']
            score = totalCostOfNewPath + totalCostOfRest

            if score < bestscore:
                bestscore = score
                bestpath = nx.reconstruct_path(u, v, predecessors)

    return bestscore, bestpath


def updateAncestors(G_0, ancestors, start):
    """
    This function takes in G_0, ancestors and the last node of a newly added path.
    This function merges ancestor sets of all the nodes downstream of this last node
    with the ancestor set of the last node.
    """
    for des in G_0.successors(start):
        ancestors[des] |= ancestors[start]
        updateAncestors(G_0, ancestors, des)


def apply(G_file, G_0_file, node_file, k, out_file, cost_function, no_log_transform):

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
    G_0, ancestors = createG_0(G_0_file, G, receptors, tfs)

    # Open the output file
    of = open(out_file, "w")
    of.write('#j\tscore of cost function\tpath\n')

    # Main loop
    for i in range(1, k + 1):

        # Get the next best path
        start = time.time()
        bestscore, bestpath = cost_function(G, G_0, ancestors)
        end = time.time()
        print("#" + str(i), end - start)

        # If no more paths, break
        if bestpath is None:
            break
        print("bestpath:")
        print(bestpath)
        print("\n")

        # Add edges of the new path to G_0
        for m in range(len(bestpath) - 1):
            G_0.add_edge(bestpath[m], bestpath[m + 1],
                         weight=G[bestpath[m]][bestpath[m + 1]]['weight'],
                         cost=G[bestpath[m]][bestpath[m + 1]]['cost'])

            # The first node in the newly added path doesn't have any new ancestors so no need for updating
            # The rest are updated with the previous nodes ancestors, then the previous node is added
            prev_ancestors = ancestors[bestpath[m]]
            if bestpath[m + 1] not in ancestors.keys():
                ancestors[bestpath[m + 1]] = set()

            ancestors[bestpath[m + 1]].update(prev_ancestors)
            ancestors[bestpath[m + 1]].add(bestpath[m])

        # Update the ancestors of all the nodes downstream of the path
        updateAncestors(G_0, ancestors, bestpath[-1])

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


COST_FUNCTIONS = {1: floydWarshall, 2: costFunction2}


def main(args):
    """ ADD BETTER DESCRIPTION HERE"""
    parser = argparse.ArgumentParser(description='DAG')
    parser.add_argument("G_file",
                        help="File that contains all the interactions that makes up G, usually the interactome. "
                             "Must be weighted.")

    parser.add_argument("G_0_file",
                        help="File that contains the ground-truth information that the algorithm starts with.")

    parser.add_argument("node_file",
                        help="File that contains node ids and their types. Should not contain nodes named 's' or 't'.")

    parser.add_argument("k", type=int, help="Number of paths the algorithm will try to add to G_0. "
                                            "The algorithm might end earlier if it cannot find more paths.")

    parser.add_argument("--out_file", default=False, help="Output file name. (default='dag-out-{k}.txt')")

    parser.add_argument("--no-log-transform", action="store_true", default=False,
                        help="If G_file contains interaction costs (lower is better) instead of probabilities"
                             "(higher is better), this option should be used.")

    parser.add_argument("--cost-function", type=int, choices=[1, 2], default=2,
                        help="Choice of cost function. (default=2)"
                             "1-Minimize the total weight of all paths(Floyd-Warshall)."
                             "2-Minimize the total weight of all paths(Djikstra).")

    args = parser.parse_args()

    # If there is no output file name, create one
    if not args.out_file:
        args.out_file = "dag-out-{}.txt".format(args.k)

    # Convert the cost function number to the actual function, dictionary is defined right before this function
    args.cost_function = COST_FUNCTIONS[args.cost_function]

    # Run the main algorithm
    apply(args.G_file, args.G_0_file, args.node_file, args.k, args.out_file, args.cost_function, args.no_log_transform)
    return


if __name__ == "__main__":
    start = time.time()
    main(sys.argv)
    end = time.time()
    print("Function call took {} seconds in total.".format(end-start))
