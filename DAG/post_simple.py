from graphspace_python.api.client import GraphSpace
from graphspace_python.graphs.classes.gsgraph import GSGraph
import sys

USERNAME = input('GS Username:')
PASSWORD = input('GS Password:')


colors = {True: "#FEFCA0", False: "#8AECFE"}
shapes = {"tf" : "rectangle", "receptor" : "triangle", "none" : "ellipse", "None": 'ellipse','source':'triangle','target':'rectangle'}
edge_styles = {True : "solid", False : "solid", "G_0": "solid"}
edge_width = {True: 1, False: 1, "G_0": 1}
edge_color = {True: "red", False: "black", "G_0": "#EA1BED"}#pink


def createGSGraph(interactome,nodesf):
    G = GSGraph()
    #interactome_nodes = set()
    #interactome_edges = {} # key = (u, v), value = weight
    pathway_nodes = {} # key = node id, value = (type, name)
    pathway_edges = set()
    output_nodes = set()
    output_edges = set()

    edge_count = 0
    inPathway_edge = 0

    """
    with open(INTERACTOME) as interactome:
        for line in interactome:
            if line == "\n" or line[0] == "#":
                continue
            items = line.split("\t")
            interactome_nodes.add(items[0])
            interactome_nodes.add(items[1])
            interactome_edges[(items[0], items[1])] = items[2]
     """
    node_types = {}
    with open(nodesf) as nf:
        for line in nf:
            if line == "\n" or line[0] == "#":
                continue
            items = line.rstrip().split()
            node_types[items[0]]= items[1]

    pathway_nodes = set()
    with open(interactome) as edges_file:
        for line in edges_file:
            if line == "\n" or line[0] == "#":
                continue
            items = line.rstrip().split()
            pathway_edges.add((items[0], items[1]))
            pathway_nodes.add(items[0])
            pathway_nodes.add(items[1])


    for node in pathway_nodes:
        if node not in node_types:
            t = "none"
        else:
            t = node_types[node]
        G.add_node(node, label = node)
        G.add_node_style(node, shape = shapes[t], color = colors[False], width = 50, height = 40)


    for u,v in pathway_edges:
        G.add_edge(u,v, directed = True)
        G.add_edge_style(u,v, directed = True, width = edge_width[False], color = edge_color[False], edge_style = edge_styles[False])


    return G

def post(G, gs):
    try:
        graph = gs.update_graph(G)
    except:
        graph = gs.post_graph(G)
        gs.share_graph(graph = G, group_name = "GrowingDags")
    return graph

def main(args):
    G = args[1]
    nodes = args[2]
    name = args[3]
    G = createGSGraph(G,nodes)
    gs = GraphSpace(USERNAME, PASSWORD)
    G.set_name("DAG for {0}".format(name))
    G.set_tags(["DAG", name])
    post(G, gs)
    return

if __name__ == "__main__":
    main(sys.argv)
