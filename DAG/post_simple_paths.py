from graphspace_python.api.client import GraphSpace
from graphspace_python.graphs.classes.gsgraph import GSGraph
import sys

#USERNAME = input('GS Username:')
#PASSWORD = input('GS Password:')
USERNAME = 'aritz@reed.edu'
PASSWORD = 'platypus'


colors = {True: "#FEFCA0", False: "#D3EDF2"}
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

def createGSGraph(interactome,pathsfile,nodesf):
    G = GSGraph()

    node_types = {}
    with open(nodesf) as nf:
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
            edges.add((items[0], items[1],0,7))
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
                    edges.add((path[i-1],path[i],k,2))

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

    for u,v,k,width in edges:
        G.add_edge(u,v, directed = True,k=k)
        G.add_edge_style(u,v, directed = True, width = width, color = edge_color[False], edge_style = edge_styles[False])


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
    G_0 = args[1]
    paths = args[2]
    nodes = args[3]
    name = args[4]
    G = createGSGraph(G_0,paths,nodes)
    gs = GraphSpace(USERNAME, PASSWORD)
    G.set_name(name)
    G.set_tags(["DAG", name])
    post(G, gs)
    return

if __name__ == "__main__":
    main(sys.argv)
