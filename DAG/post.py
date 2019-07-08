from graphspace_python.api.client import GraphSpace
from graphspace_python.graphs.classes.gsgraph import GSGraph
import sys

USERNAME ='koset@reed.edu'
PASSWORD = "nfbnke4Iifdc5D99Ee9V9@FA!8NFZie4"


colors = {True: "yellow", False: "green"}
shapes = {"tf" : "rectangle", "receptor" : "triangle", "none" : "ellipse"}
edge_styles = {True : "solid", False : "dashed", "G_0": "solid"}
edge_width = {True: 1, False: 0.5, "G_0": 1}
edge_color = {True: "red", False: "black", "G_0": "blue"}
INTERACTOME = '/Users/Tunc/Desktop/Reed/PathLinker/DAG/2015pathlinker-weighted.txt'


def createGSGraph(pathway):
    G = GSGraph()
    #interactome_nodes = set()
    #interactome_edges = {} # key = (u, v), value = weight
    pathway_nodes = {} # key = node id, value = (type, name)
    pathway_edges = set()
    output_nodes = set()
    output_edges = set()
    G_0_edges = set()
    
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
    with open(pathway+"-G_0.txt") as G_0_file:
        for line in G_0_file:
            if line == "\n" or line[0] == "#":
                continue
            items = line.rstrip().split("\t")
            G_0_edges.add((items[0], items[1]))
    
    with open(pathway+"-nodes.txt") as nodes_file:
        for line in nodes_file:
            if line == "\n" or line[0] == "#":
                continue
            items = line.rstrip().split("\t")
            pathway_nodes[items[0]] = items[1]
        
    with open(pathway+"-edges.txt") as edges_file:
        for line in edges_file:
            if line == "\n" or line[0] == "#":
                continue
            items = line.rstrip().split("\t")
            pathway_edges.add((items[0], items[1]))
            
    with open(pathway+"-output.txt") as output_file:
        for line in output_file:
            if line == "\n" or line[0] == "#":
                continue
            items = line.rstrip().split("\t")
            path = items[3]
            nodes = path.split("|")
            for i in range(len(nodes)-1):
                output_nodes.add(nodes[i])
                output_nodes.add(nodes[i+1])
                output_edges.add((nodes[i], nodes[i+1]))
    
    for i in output_nodes:
        t = "none"
        inPathway = False
        if i in pathway_nodes:
            t = pathway_nodes[i]
            inPathway = True
        G.add_node(i, label = i)
        G.add_node_style(i, shape = shapes[t], color = colors[inPathway])
        
    for i in output_edges:
        inPathway = False
        if (i[0], i[1]) in pathway_edges:
            inPathway = True
            if (i[0], i[1]) in G_0_edges:
                inPathway = "G_0"
        G.add_edge(i[0], i[1], directed = True)
        G.add_edge_style(i[0], i[1], directed = True, width = edge_width[inPathway], color = edge_color[inPathway], edge_style = edge_styles[inPathway])
    return G
    
def post(G, gs):
    try:
        graph = gs.update_graph(G)
    except:
        graph = gs.post_graph(G)
        gs.share_graph(graph = G, group_name = "GrowingDags")
    return graph

def main(args):
    pathway = args[1]
    G = createGSGraph(pathway)
    gs = GraphSpace(USERNAME, PASSWORD)
    G.set_name("DAG for {0}".format(pathway))
    G.set_tags(["DAG", pathway])
    post(G, gs)
    return

if __name__ == "__main__":
    main(sys.argv)
        
        
        
        