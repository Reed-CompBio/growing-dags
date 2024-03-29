"""
WILL RETURN FILENOTFOUNDERROR in getPositives if the input file name is not
    PATHWAYNAME-anythingelse.txt
"""

import sys
import matplotlib.pyplot as plt
import datetime


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
                elif type(item) is tuple:
                    if (item[1], item[0]) in pos:
                        print("Here with {0} and {1}".format(item, (item[1], item[0])))
                        positives_so_far += 1
        try:
            prec.append(positives_so_far/len(already_seen))
        except ZeroDivisionError:
            prec.append(0)
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
            elif type(item) is tuple:
                if (item[1], item[0]) in pos:
                    if (item[1], item[0]) not in already_pos:
                        print("Here with {0} and {1}".format(item, (item[1], item[0])))
                        positives_so_far += 1
                        already_pos.add((item[1], item[0]))
        rec.append(positives_so_far/total_positives)
    return rec


def getItems(row, already_seen):
    line = ""
    if len(row) == 0:
        return "empty\t"
    if type(row[0]) is tuple:
        for item in row:
            if item not in already_seen:
                line += "({},{}), ".format(item[0], item[1])
                already_seen.add(item)
    else:
        for item in row:
            if item not in already_seen:
                line += "{}, ".format(item)
                already_seen.add(item)
    line = line[:-2] + "\t"
    return line

def pr(dic, pos):
    prec = precision(dic, pos)
    rec = recall(dic, pos)
    """
    outfile_name = "pr_out_" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + ".txt"
    counter = 0
    already_seen = set()

    with open(outfile_name, "w") as f:
        if len(dic[1][0]) == 1:
            f.write("#j\tnode\tprecision\trecall\n")
        else:
            f.write("#j\ttail\thead\tprecision\trecall\n")

        for row in dic.values():
            line = "{}\t".format(counter+1) + getItems(row, already_seen)
            line += "{}\t{}\n".format(prec[counter], rec[counter])
            counter += 1
            f.write(line)
    """
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


def getOutputNodes(output_file, G_0_file):
    """
    Iterates over the output file to create a dic that
    has j as key and a list of nodes as values.
    IMPORTANT: nodes are NOT guaranteed to be unique and will repeat
    """
    dic = {0: []}
    with open(G_0_file) as gf:
        for line in gf:
            if line == "\n" or line[0] == "#":
                continue
            items = line.rstrip().split("\t")
            dic[0].append(items[0])
        dic[0].append(items[1])

    with open(output_file) as of:
        for line in of:
            if line == "\n" or line[0] == "#":
                continue
            items = line.rstrip().split("\t")
            path = items[2]
            nodes = path.split("|")
            dic[int(items[0])] = nodes
    return dic


def getOutputEdges(output_file, G_0_file):
    """
    Iterates over the output file to create a dic that
    has j as key and a list of newly added edges as values.
    """
    dic = {0: []}

    with open(G_0_file) as gf:
        for line in gf:
            if line == "\n" or line[0] == "#":
                continue
            items = line.rstrip().split("\t")
            dic[0].append((items[0], items[1]))

    with open(output_file) as of:
        for line in of:
            if line == "\n" or line[0] == "#":
                continue
            items = line.rstrip().split("\t")
            path = items[2]
            nodes = path.split("|")
            edges = []
            for i in range(len(nodes)-1):
                edges.append((nodes[i], nodes[i+1]))
            dic[int(items[0])] = edges
    return dic


def getOutput(output_file, mode, G_0_file):
    """
    Wrapper function that calls correct getOutput based on mode
    """
    if mode == "nodes":
        return getOutputNodes(output_file, G_0_file)
    return getOutputEdges(output_file, G_0_file)


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

    pos = getPositives(pathway, mode)
    # pos is a set containing nodes/edges of the pathway from NetPath
    dic = getOutput(output_file, mode)
    # dic is a dictionary with j as keys and nodes/paths added at j as values
    precision, recall = pr(dic, pos)
    # pr is the main precision-recall function

    # Doing the above but for PathLinker output
    if pl_flag:
        p_dic = getOutput(pl_output, mode)
        p_precision, p_recall = pr(p_dic, pos)
        # pos is pathway dependant so will be the same for PathLinker

    plt.plot(recall, precision, color = "blue", label = "DAG")
    if pl_flag:
        plt.plot(p_recall, p_precision, color = "red", label = "PathLinker")
    plt.legend()
    plt.ylabel("Precision")
    plt.xlabel("Recall")
    plt.suptitle(pathway + " " + mode)
    name = pathway+"-pldag-" + mode +save_format
    print("Saving with filename ", name)
    plt.savefig(name)
    plt.show()


if __name__ == "__main__":
    main(sys.argv)
