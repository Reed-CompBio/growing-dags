#tuncjksta.py
import heapq as hq
import math


def pop(heap, finished):
    """
    A helper function that pops the next element in the priority queue,
    while also adding it to the discarded pile
    """
    dist, node, path = hq.heappop(heap)
    finished[node] = (dist, path)
    return node, dist, path, finished

"""
def heap_update(heap, node, dist, current_node, current_path):
    # Determine node index in the heap
    index = 0
    # Previously popped nodes will not be seen
    not_seen = True
    for i in heap:
        if i[1] == node:
            not_seen = False
            break
        index += 1

    # If node has been previously popped, nothing to update
    if not_seen:
        return heap

    # Update only if new distance is shorter
    if heap[index][0] > dist:
        heap[index][0] = dist
        new_path = current_path.copy()
        new_path.append(node)
        heap[index][2] = new_path
        # Re-heapify to restore priority queue
        hq.heapify(heap)

    return heap
"""

def heap_update(heap, G, indeces, current_node, current_dist, current_path):
    for node in G.successors(current_node):
        try:
            index = indeces[node]
        except KeyError:
            continue

        dist = current_dist + G[current_node][node]["weight"]
        if heap[index][0] > dist:
            heap[index][0] = dist
            new_path = current_path.copy()
            new_path.append(node)
            heap[index][2] = new_path
    hq.heapify(heap)
    return heap


def multi_target_dijkstra(G, u, vset):
    heap = []   # contains lists of distance, node, path
    finished = {} # node -> (dist, path)


    # Create priority queue entries for each node
    for item in G.nodes():
        path = None
        dist = 9999999999999999999999999999999999999999999999999999999999999
        if item == u:
            path = [u]
            dist = 0
        hq.heappush(heap, [dist, item, path])


    # Iterate over vset so function will quit when all significant nodes are found
    while len(vset) > 0:
        current_node, current_dist, current_path, finished = pop(heap, finished)
        indeces = {}
        for i in range(len(heap)):
            indeces[heap[i][1]] = i
        # A node popping from the priority queue means shortest path to it is found
        if current_node in vset:
            vset.remove(current_node)
        heap = heap_update(heap, G, indeces, current_node, current_dist, current_path)
        """
        for node in G.successors(current_node):
            dist = current_dist + G[current_node][node]["weight"]
            heap = heap_update(heap, node, dist, current_node, current_path)
        """
    return finished
