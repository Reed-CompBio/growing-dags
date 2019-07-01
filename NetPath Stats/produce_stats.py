"""
USAGE:
    python produce_stats.py node_file edge_file
    
Assumptions: 
    node_file and edge_file are tab-separated.
    node_file only contains none, receptor or tf as node_symbol
    all non-entry lines in the files start with #
"""

import sys

def readNodes(node_file):
    nodes = {}
    n_tf = 0
    n_receptor = 0
    with open(node_file) as f1:
        for line in f1:
            if line[0] == "#":  # Skip comments
                continue
            
            first_tab = line.find("\t")
            node_id = line[:first_tab]
            nodes[node_id] = [0, 0] # Indegree and outdegree
            
            
            # This part assumes that node_symbol can only be tf, none or receptor
            if line[first_tab+1] == "t":
                n_tf += 1
            elif line[first_tab+1] == "r":
                n_receptor += 1
            
    return nodes, n_tf, n_receptor


def produceStats(node_file, edge_file):
    nodes, n_tf, n_receptor = readNodes(node_file)
    n_edges = 0
    with open(edge_file) as f1:
        for line in f1:
            if line[0] == "#":  # Skip comments
                continue
            first_tab = line.find("\t")
            second_tab = line.find("\t", first_tab+1)
            tail = line[:first_tab]
            head = line[first_tab+1: second_tab]
            nodes[head][0] += 1
            nodes[tail][1] += 1
            n_edges += 1
            
    total_indegree = 0
    total_outdegree = 0
    for i in nodes.values():
        total_indegree += i[0]
        total_outdegree += i[1]
    avg_indegree = total_indegree/len(nodes)
    avg_outdegree = total_outdegree/len(nodes)
            
    sep = node_file.find("-")
    if sep != -1:
        output_name = node_file[:sep]+"-stats_output.txt"
    else:
        output_name = "output_stats.txt"
    with open(output_name, "w") as f1:
        f1.write("#n_nodes\tn_edges\tn_tf\tn_receptors\tavg_indegree\tavg_outdegree\n")
        f1.write("{0}\t{1}\t{2}\t{3}\t{4}\t{5}".format(len(nodes), n_edges, n_tf, n_receptor, avg_indegree, avg_outdegree))
 

if __name__ == "__main__":
    produceStats(sys.argv[1], sys.argv[2])