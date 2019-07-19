"""
    WILL RETURN FILENOTFOUNDERROR in getPositives if the input file name is not
    PATHWAYNAME-anythingelse.txt
    """

import sys
import matplotlib.pyplot as plt


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
            dic[int(items[0])] = len(nodes)
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
            dic[int(items[0])] = len(nodes)//2 + 1
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
    with open("out_k_200-paths.txt") as output_file:    #for PathLinker
        for line in output_file:
            if line == "\n" or line[0] == "#":
                continue
            items = line.rstrip().split("\t")
            path = items[2] #2 for PathLinker output
            nodes = path.split("|")
            dic[int(items[0])] = len(nodes)
    return dic


def p_getOutputEdges():
    """
    Iterates over the output file to create a dic that
    has j as key and a list of newly added edges as values.
    """
    dic = {}
    with open("out_k_200-paths.txt") as output_file:    #for PathLinker
        for line in output_file:
            if line == "\n" or line[0] == "#":
                continue
            items = line.rstrip().split("\t")
            path = items[2]#2 for PathLinker output, 3 for DAG output
            nodes = path.split("|")
            dic[int(items[0])] = len(nodes)//2 + 1
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

    # pos is a set containing nodes/edges of the pathway from NetPath
    dic = getOutput(output_file, mode)
    # Doing the above but for PathLinker output
    if pl_flag:
        p_dic = p_getOutput(pl_output, mode)

    plt.plot(list(dic.key()), list(dic.values()), color = "blue", label = "DAG")
    if pl_flag:
        plt.plot(list(p_dic.key()), list(p_dic.value()), color = "red", label = "PathLinker")
    plt.legend()
    if mode == 'nodes':
        plt.ylabel("# of nodes")
    else:
        plt.ylabel("# of edges")
    plt.xlabel("k")
    plt.suptitle(pathway + " " + mode)
    plt.savefig(pathway+"-" + mode +save_format)
    plt.show()



if __name__ == "__main__":
    main(sys.argv)
