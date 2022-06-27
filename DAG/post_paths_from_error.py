from graphspace_python.api.client import GraphSpace
from graphspace_python.graphs.classes.gsgraph import GSGraph
import sys
import ast

USERNAME = input('GS Username:')
PASSWORD = input('GS Password:')


colors = {True: "#FEFCA0", False: "#8AECFE"}
shapes = {"tf" : "rectangle", "receptor" : "triangle", "none" : "ellipse", "None": 'ellipse','source':'triangle','target':'rectangle'}
edge_styles = {True : "solid", False : "solid", "G_0": "solid"}
edge_width = {True: 1, False: 1, "G_0": 1}
edge_color = {True: "red", False: "black", "G_0": "#EA1BED"}#pink

# mapper
id2name = {}
with open('mapped-nodes.txt') as fin:
    for line in fin:
        if 'From' in line: # skip header
            continue
        row = line.strip().split()
        id2name[row[0]] = row[1]

def createGSGraph(interactome,pathsfile,logfile,nodesfile):
    G = GSGraph()
    k=0
    node_types = {}
    with open(nodesfile) as nf:
        for line in nf:
            if line == "\n" or line[0] == "#":
                continue
            items = line.rstrip().split()
            node_types[items[0]]= items[1]

    nodes = set()
    edges = set()
    with open(interactome) as edges_file:
        for line in edges_file:
            if line == "\n" or line[0] == "#":
                continue
            items = line.rstrip().split()
            edges.add((items[0], items[1],0))
            nodes.add((items[0],0))
            nodes.add((items[1],0))

    with open(pathsfile) as paths_file:
        for line in paths_file:
            if line == "\n" or line[0] == "#":
                continue
            row = line.strip().split()
            k = row[0]
            path = row[2].split('|')
            for i in range(len(path)):
                if path[i] not in [n[0] for n in nodes]:
                    nodes.add((path[i],k))
                if i != 0:
                    edges.add((path[i-1],path[i],k))

    with open(logfile) as log_file:
        for line in log_file:
            if line == 'ERROR: internal node is in G_0!\n':
                error_path = log_file.readline()
                break
    print(error_path,'error path')
    error_list = ast.literal_eval(error_path)
    print(error_list)
    error_k = int(k)+1
    for i in range(len(error_list)):
        if error_list[i] not in [n[0] for n in nodes]:
            nodes.add((error_list[i],error_k))
        if i != 0:
            edges.add((error_list[i-1],error_list[i],error_k))

    for node,k in nodes:
        if node not in node_types:
            t = "none"
        else:
            t = node_types[node]
        if node in id2name:
            G.add_node(node, label = id2name[node],k=k)
        else:
            G.add_node(node, label = node,k=k)
        G.add_node_style(node, shape = shapes[t], color = colors[False], width = 50, height = 40)

    for u,v,k in edges:
        G.add_edge(u,v, directed = True,k=k)
        if int(k) == error_k:
            G.add_edge_style(u,v, directed = True, width = edge_width[False], color = edge_color[True], edge_style = edge_styles[False])
        else:
            G.add_edge_style(u,v, directed = True, width = edge_width[False], color = edge_color[False], edge_style = edge_styles[False])


    return G

def post(G, gs):
    try:
        graph = gs.update_graph(G)
    except:
        graph = gs.post_graph(G)
        gs.share_graph(graph = G, group_name = "GrowingDags")
    print('Posted graph.')
    return graph

def main(args):
    label = args[1]
    G_0 = '../data/prepare-G0/ground_truth/%s-G0.txt' % (label)
    pathsfile = '../output/ground_truth-G0/%s_c1_k25.txt' % (label)
    logfile = '../output/ground_truth-G0/%s_c1_k25.log' % (label)
    nodesfile = '../data/netpath/%s-nodes.txt' % (label)

    G = createGSGraph(G_0,pathsfile,logfile,nodesfile)
    gs = GraphSpace(USERNAME, PASSWORD)
    G.set_name("ERROR DEBUG DAG paths for {0}".format(label))
    post(G, gs)
    return

if __name__ == "__main__":
    main(sys.argv)
