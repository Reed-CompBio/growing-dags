import sys


def precision(dic, pos):
    prec = []
    already_pos = set()
    positives_so_far = 0
    n = 0
    for step in dic.values():
        n += 1
        for item in step:
            if item in pos:
                if item not in already_pos:
                    positives_so_far += 1
                    already_pos.add(item)
        prec.append(positives_so_far/n)
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
    dic = {}
    with open(pathway + "-output.txt") as output_file:
        for line in output_file:
            if line == "\n" or line[0] == "#":
                continue
            items = line.rstrip().split("\t")
            path = items[3]
            nodes = path.split("|")
            dic[int(items[0])] = nodes
    return dic


def getOutputEdges(pathway):
    dic = {}
    with open(pathway + "-output.txt") as output_file:
        for line in output_file:
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


def getOutput(pathway, mode):
    if mode == "nodes":
        return getOutputNodes(pathway)
    return getOutputEdges(pathway)


def main(args):
    """
    Usage:
        python pr.py PATHWAY_NAME MODE(optional)
    Example:
        python pr.py BCR nodes
        python pr.py Wnt edges
    
    Run this in the NetPath folder with the associated nodes/edges/output files.
    """
    pathway = args[1]
    mode = "nodes"
    if len(args) > 2:
        mode = args[2]
    pos = getPositives(pathway, mode)
    dic = getOutput(pathway, mode)
    precision, recall = pr(dic, pos)
    print("Precision: {}".format(precision))
    print("Recall: {}".format(recall))
    return


if __name__ == "__main__":
    main(sys.argv)