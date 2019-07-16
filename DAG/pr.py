"""
WILL RETURN FILENOTFOUNDERROR in getPositives if the input file name is not
    PATHWAYNAME-anythingelse.txt
"""

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
    """
    Iterates over the NetPath nodes file to add every edge to a set 'pos'.
    """
    pos = set()
    with open(pathway + "-nodes.txt") as node_file:
        for line in node_file:
            if line == "\n" or line[0] == "#":
                continue
            items = line.rstrip().split("\t")
            pos.add(items[0])
    return pos


def getPositiveEdges(pathway):
    """
    Iterates over the NetPath edges file to add every edge to a set 'pos'.
    """
    pos = set()
    with open(pathway + "-edges.txt") as edge_file:
        for line in edge_file:
            if line == "\n" or line[0] == "#":
                continue
            items = line.rstrip().split("\t")
            pos.add((items[0], items[1]))
    return pos


def getPositives(pathway, mode):
    """
    Wrapper function that calls correct getPositives based on mode
    """
    assert mode in ('nodes', 'edges'), "Mode can only be 'nodes' or 'edges'."
    if mode == "nodes":
        return getPositiveNodes(pathway)
    return getPositiveEdges(pathway)


def getOutputNodes(output_file):
    """
    Iterates over the output file to create a dic that
    has j as key and a list of nodes as values.
    IMPORTANT: nodes are NOT guaranteed to be unique and will repeat
    """
    dic = {}
    with open(output_file) as of:
        for line in of:
            if line == "\n" or line[0] == "#":
                continue
            items = line.rstrip().split("\t")
            path = items[3]
            nodes = path.split("|")
            dic[int(items[0])] = nodes
    return dic


def getOutputEdges(output_file):
    """
    Iterates over the output file to create a dic that
    has j as key and a list of newly added edges as values.
    """
    dic = {}
    with open(output_file) as of:
        for line in of:
            if line == "\n" or line[0] == "#":
                continue
            items = line.rstrip().split("\t")
            path = items[3]
            nodes = path.split("|")
            edges = []
            for i in range(len(nodes)-1):
                edges.append((nodes[i], nodes[i+1]))
            dic[int(items[0])] = edges
    return dic


def getOutput(output_file, mode):
    """
    Wrapper function that calls correct getOutput based on mode
    """
    if mode == "nodes":
        return getOutputNodes(output_file)
    return getOutputEdges(output_file)


def p_getOutputNodes():
    """
    Iterates over the output file to create a dic that
    has j as key and a list of nodes as values.
    IMPORTANT: nodes are NOT guaranteed to be unique and will repeat
    """
    dic = {}
    with open("out_k_100-paths.txt") as output_file:    #for PathLinker
        for line in output_file:
            if line == "\n" or line[0] == "#":
                continue
            items = line.rstrip().split("\t")
            path = items[2] #2 for PathLinker output
            nodes = path.split("|")
            dic[int(items[0])] = nodes
    return dic


def p_getOutputEdges():
    """
    Iterates over the output file to create a dic that
    has j as key and a list of newly added edges as values.
    """
    dic = {}
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

def p_getOutput(mode):
    """
    Wrapper function that calls correct getOutput based on mode
    """
    if mode == "nodes":
        return p_getOutputNodes()
    return p_getOutputEdges()


def main(args):
    """
    Usage:
        python pr.py OUTPUT_FILE MODE(optional) SAVE_FORMAT(optional) PATHLINKER_OUTPUT(optional)

    Example:
        python pr.py BCR-output.txt nodes .png out_k_100-paths.txt
        python pr.py Wnt-output.txt
    
    Run this in the NetPath folder with the associated nodes/edges/output files.
    """
    output_file = args[1]
    pathway = output_file[:output_file.index("-")]
    
    # Default values
    mode = "nodes" 
    save_format = ".png"
    pl_flag = False
    
    # Parsing over arguments
    n_args = len(args)
    if n_args > 2:
        mode = args[2]
        if n_args > 3:
            save_format = args[3]
            if n_args > 4:
                pl_flag = True
                pl_output = args[4]
        
    pos = getPositives(output_file, mode)
    # pos is a set containing nodes/edges of the pathway from NetPath
    dic = getOutput(output_file, mode)
    # dic is a dictionary with j as keys and nodes/paths added at j as values
    precision, recall = pr(dic, pos)
    # pr is the main precision-recall function
    
    # Doing the above but for PathLinker output
    if pl_flag:
        p_dic = p_getOutput(pl_output, mode)
        p_precision, p_recall = pr(p_dic, pos)
        # pos is pathway dependant so will be the same for PathLinker
    
    plt.plot(recall, precision, color = "blue", label = "DAG")
    if pl_flag:
        plt.plot(p_recall, p_precision, color = "red", label = "PathLinker")
    plt.legend()
    plt.ylabel("Precision")
    plt.xlabel("Recall")
    plt.suptitle(pathway + " " + mode)
    plt.savefig(pathway+"-" + mode +save_format)
    plt.show()
    


if __name__ == "__main__":
    main(sys.argv)