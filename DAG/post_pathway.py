from graphspace_python.api.client import GraphSpace
from graphspace_python.graphs.classes.gsgraph import GSGraph
import sys

USERNAME ='koset@reed.edu'
PASSWORD = "nfbnke4Iifdc5D99Ee9V9@FA!8NFZie4"


node_colors = {"both" : "#FFF861", "pl" : "#F5B7EC", "dag" : "#F8B46C", None : "#CAE6EE"}
#                       yellow              pink         orange             blue
node_shapes = {"tf" : "rectangle", "receptor" : "triangle", "none" : "ellipse"}

edge_attr = {"both" : ("red", 1, "solid"),\
             "pl" : ("#F5B7EC", 1, "solid"),\
             "dag" : ("#F8B46C", 1, "solid"),\
             None : ("black", 0.5, "dashed")}

def post(G, gs):
    try:
        graph = gs.update_graph(G)
    except:
        graph = gs.post_graph(G)
        gs.share_graph(graph = G, group_name = "GrowingDags")
    return graph


def readDAG(dag_output):
    all_nodes = set()
    all_edges = set()
    with open(dag_output) as df:
        for line in df:
            if line == "\n" or line[0] == "#":
                continue
            items = line.rstrip().split("\t")
            nodes = items[3].split("|")
            for i in range(len(nodes)-1):
                if i == 0:
                    all_nodes.add(nodes[i])
                all_nodes.add(nodes[i+1])
                all_edges.add((nodes[i], nodes[i+1]))
    
    return all_nodes, all_edges


def readPL(pl_output):
    all_nodes = set()
    all_edges = set()
    with open(pl_output) as pf:
        for line in pf:
            if line == "\n" or line[0] == "#":
                continue
            items = line.rstrip().split("\t")
            nodes = items[2].split("|")
            for i in range(len(nodes)-1):
                if i == 0:
                    all_nodes.add(nodes[i])
                all_nodes.add(nodes[i+1])
                all_edges.add((nodes[i], nodes[i+1]))
    
    return all_nodes, all_edges


def readPathwayEdges(edges_file):
    edges = set()
    with open(edges_file) as ef:
        for line in ef:
            if line == "\n" or line[0] == "#":
                continue
            items = line.rstrip().split("\t")
            edges.add((items[0], items[1]))
            
    return edges


def readPathwayNodes(nodes_file):
    # Set of (node, type)
    node_items = set()
    with open(nodes_file) as nf:
        for line in nf:
            if line == "\n" or line[0] == "#":
                continue
            items = line.rstrip().split("\t")
            node_items.add((items[0], items[1]))
    
    return node_items
    

def findNodeAttributes(inDAG, inPL, node_type):
    color_key = None
    if inDAG and inPL:
        color_key = "both"
    elif inDAG:
        color_key = "dag"
    elif inPL:
        color_key = "pl"
        
    color = node_colors[color_key]
    shape = node_shapes[node_type]
    
    return color, shape
    

def findEdgeAttributes(inDAG, inPL):
    attr_key = None
    if inDAG and inPL:
        attr_key = "both"
    elif inDAG:
        attr_key = "dag"
    elif inPL:
        attr_key = "pl"
    
    color, width, style = edge_attr[attr_key]
    
    return width, color, style

def createPathwayGraph(edges_file, nodes_file, dag_output, pl_output):
    dag_nodes, dag_edges = readDAG(dag_output)
    pl_nodes, pl_edges = readPL(pl_output)
    pathway_edges = readPathwayEdges(edges_file)
    pathway_nodes = readPathwayNodes(nodes_file) #Set of tuples (node, type)
    G = GSGraph()
    
    for node_item in pathway_nodes:
        inDAG = False
        inPL = False
        node = node_item[0]
        node_type = node_item[1]
        
        if node in pl_nodes:
            inPL = True
        if node in dag_nodes:
            inDAG = True
        
        node_color, node_shape = findNodeAttributes(inDAG, inPL, node_type)
        
        G.add_node(node, label = node)
        G.add_node_style(node, shape = node_shape, color = node_color, width = 50, height = 40)
    
    for edge in pathway_edges:
        inDAG = False
        inPL = False
        
        if edge in pl_edges:
            inPL = True
        if edge in dag_edges:
            inDAG = True
            
        edge_width, edge_color, style = findEdgeAttributes(inDAG, inPL)
        
        G.add_edge(edge[0], edge[1], directed = True)
        G.add_edge_style(edge[0], edge[1], directed = True, width = edge_width, color = edge_color, edge_style = style)

    return G


def main(args):
    pathway_edges_file = args[1]
    pathway_nodes_file = args[2]
    dag_output = args[3]
    pl_output = args[4]
    
    pathway = pathway_edges_file[:pathway_edges_file.find("-")]
    print("Creating a graph for {}.".format(pathway))
    G = createPathwayGraph(pathway_edges_file, pathway_nodes_file, dag_output, pl_output)
    
    gs = GraphSpace(USERNAME, PASSWORD)
    G.set_name("{0} Pathway".format(pathway))
    G.set_tags([pathway, "DAG", "PathLinker"])
    print("Posting graph to GraphSpace with name '{} Pathway'.".format(pathway))
    post(G, gs)
    return

if __name__ == "__main__":
    main(sys.argv)