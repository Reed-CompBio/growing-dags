#tuncjksta.py
import heapq as hq
import math


def pop(heap, finished):
    dist, node, path = hq.heappop(heap)
    finished[node] = (dist, path)
    return node, dist, path, finished


def heap_update(heap, node, dist, current_node, current_path):
    index = 0
    not_seen = True
    for i in heap:
        if i[1] == node:
            not_seen = False
            break
        index += 1
    
    if not_seen:
        return heap

    if heap[index][0] > dist:
        heap[index][0] = dist
        new_path = current_path.copy()
        new_path.append(node)
        heap[index][2] = new_path
        hq.heapify(heap)
        
    return heap


def multi_target_dijkstra(G, u, vset):
    heap = []   # contains tuples of distance, node, path
    finished = {} # node -> (dist, path)
    
    
    for item in G.nodes():
        path = None
        dist = math.inf
        if item == u:
            path = [u]
            dist = 0
        hq.heappush(heap, [dist, item, path])
    
    while len(vset) > 0:
        current_node, current_dist, current_path, finished = pop(heap, finished)
        if current_node in vset:
            vset.remove(current_node)
        for node in G.successors(current_node):
            dist = current_dist + G[current_node][node]["weight"]
            heap = heap_update(heap, node, dist, current_node, current_path)
    
    return finished   
