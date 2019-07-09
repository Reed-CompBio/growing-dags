import sys
import matplotlib.pyplot as plt


def precision(dic, pos):
    prec = []
    already_seen = set()
    positives_so_far = 0
    for step in dic.values():
        for item in step:
            if item not in already_seen:
                already_seen.add(item)
                if item in pos:
                    positives_so_far += 1
        prec.append(positives_so_far/len(already_seen))
    return prec
    

def recall(dic, pos):
    total_positives = len(pos)
    rec = []
    already_pos = set()
    positives_so_far = 0
    for step in dic.values():
        for item in step:
            if item in pos:
                if item not in already_pos:
                    positives_so_far += 1
                    already_pos.add(item)
        rec.append(positives_so_far/total_positives)
    return rec


def pr(dic, pos):
    prec = precision(dic, pos)
    rec = recall(dic, pos)
    return prec, rec


def getPositiveNodes(pathway):
    pos = set()
    with open(pathway + "-nodes.txt") as node_file:
        for line in node_file:
            if line == "\n" or line[0] == "#":
                continue
            items = line.rstrip().split("\t")
            pos.add(items[0])
    return pos


def getPositiveEdges(pathway):
    pos = set()
    with open(pathway + "-edges.txt") as edge_file:
        for line in edge_file:
            if line == "\n" or line[0] == "#":
                continue
            items = line.rstrip().split("\t")
            pos.add((items[0], items[1]))
    return pos


def getPositives(pathway, mode):
    assert mode in ('nodes', 'edges'), "Mode can only be 'nodes' or 'edges'."
    if mode == "nodes":
        return getPositiveNodes(pathway)
    return getPositiveEdges(pathway)


def getOutputNodes(pathway):
    """
    Iterates over the output file to create a dic that
    has j as key and a list of nodes as values.
    IMPORTANT: nodes are NOT guaranteed to be unique and will repeat
    """
    dic = {}
    with open(pathway + "-output.txt") as output_file: #for DAG
    #with open("out_k_100-paths.txt") as output_file:    #for PathLinker
        for line in output_file:
            if line == "\n" or line[0] == "#":
                continue
            items = line.rstrip().split("\t")
            path = items[3] #2 for PathLinker output, 3 for DAG output
            nodes = path.split("|")
            dic[int(items[0])] = nodes
    return dic


def getOutputEdges(pathway):
    """
    Iterates over the output file to create a dic that
    has j as key and a list of newly added edges as values.
    """
    dic = {}
    with open(pathway + "-output.txt") as output_file: #for DAG
    #with open("out_k_100-paths.txt") as output_file:    #for PathLinker
        for line in output_file:
            if line == "\n" or line[0] == "#":
                continue
            items = line.rstrip().split("\t")
            path = items[3]#2 for PathLinker output, 3 for DAG output
            nodes = path.split("|")
            edges = []
            for i in range(len(nodes)-1):
                edges.append((nodes[i], nodes[i+1]))
            dic[int(items[0])] = edges
    return dic


def getOutput(pathway, mode):
    """
    Wrapper function that calls correct getOutput based on mode
    """
    if mode == "nodes":
        return getOutputNodes(pathway)
    return getOutputEdges(pathway)


def p_getOutputNodes(pathway):
    """
    Iterates over the output file to create a dic that
    has j as key and a list of nodes as values.
    IMPORTANT: nodes are NOT guaranteed to be unique and will repeat
    """
    dic = {}
    #with open(pathway + "-output.txt") as output_file: #for DAG
    with open("out_k_100-paths.txt") as output_file:    #for PathLinker
        for line in output_file:
            if line == "\n" or line[0] == "#":
                continue
            items = line.rstrip().split("\t")
            path = items[2] #2 for PathLinker output, 3 for DAG output
            nodes = path.split("|")
            dic[int(items[0])] = nodes
    return dic


def p_getOutputEdges(pathway):
    """
    Iterates over the output file to create a dic that
    has j as key and a list of newly added edges as values.
    """
    dic = {}
    #with open(pathway + "-output.txt") as output_file: #for DAG
    with open("out_k_100-paths.txt") as output_file:    #for PathLinker
        for line in output_file:
            if line == "\n" or line[0] == "#":
                continue
            items = line.rstrip().split("\t")
            path = items[2]#2 for PathLinker output, 3 for DAG output
            nodes = path.split("|")
            edges = []
            for i in range(len(nodes)-1):
                edges.append((nodes[i], nodes[i+1]))
            dic[int(items[0])] = edges
    return dic

def p_getOutput(pathway, mode):
    """
    Wrapper function that calls correct getOutput based on mode
    """
    if mode == "nodes":
        return p_getOutputNodes(pathway)
    return p_getOutputEdges(pathway)


def main(args):
    """
    Usage:
        python pr.py PATHWAY_NAME MODE(optional) SAVE_FORMAT(optional)
    Example:
        python pr.py BCR nodes .png
        python pr.py Wnt edges .pdf
    
    Run this in the NetPath folder with the associated nodes/edges/output files.
    """
    pathway = args[1]
    mode = "nodes"
    if len(args) > 2:
        mode = args[2]
    save_format = ".png"
    if len(args) > 3:
        save_format = args[3]
        
    pos = getPositives(pathway, mode)
    # pos is a set containing nodes/edges of the pathway from NetPath
    dic = getOutput(pathway, mode)
    # dic is a dictionary with j as keys and nodes/paths added at j as values
    precision, recall = pr(dic, pos)
    # pr is the main precision-recall function
    
    p_dic = p_getOutput(pathway, mode)
    p_pos = getPositives(pathway, mode)
    p_precision, p_recall = pr(p_dic, p_pos)
    
    plt.plot(recall, precision, color = "blue", label = "DAG")
    plt.plot(p_recall, p_precision, color = "red", label = "PathLinker")
    plt.legend()
    plt.ylabel("Precision")
    plt.xlabel("Recall")
    plt.suptitle(pathway + " " + mode)
    plt.savefig(pathway+"-" + mode +save_format)
    plt.show()
    


if __name__ == "__main__":
    main(sys.argv)