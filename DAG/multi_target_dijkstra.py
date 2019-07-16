import heapq as hq
import math


def multi_target_dijkstra(G, u, vset):
    """
    Takes in a networkx graph, a starting node u and a set of target nodes vset.
    Returns a dictionary that has nodes as keys and a tuple of distance, path as values.
    """
    heap = []   # contains lists of distance, node, path
    finished = {} # node -> (dist, path)
    seen = {} # node -> dist

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
            dist = current_dist + G[current_node][node]["weight"]
            if dist < seen[node]:
                seen[node] = dist
                hq.heappush(heap, (dist, node, current_path + [node]))

    return finished