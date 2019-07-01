"""
USAGE:
    python produce_stats.py folder_containing_all_edges/nodes_files
    
Assumptions: 
    node_file and edge_file are tab-separated.
    node_file only contains none, receptor or tf as node_symbol
    all non-entry lines in the files start with #
    the folder containing pathways is only composed of 1 edges and 1 nodes file for each pathway
"""

import sys
import glob

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
     
    results = [len(nodes), n_edges, n_tf, n_receptor, avg_indegree, avg_outdegree]
    results = [str(i) for i in results]
    return results   
    
 
def main(args):
    folder = args[1]
    edge_files = sorted(glob.glob(folder+"/*-edges.txt"))
    node_files = sorted(glob.glob(folder+"/*-nodes.txt"))
    with open("pathway_stats_output.txt", "w") as f1:
        f1.write("#n_nodes\tn_edges\tn_tf\tn_receptors\tavg_indegree\tavg_outdegree\n")
        for i in range(len(node_files)):
            name = node_files[i][len(folder)+1:node_files[i].find("-")]
            #name = name[len(folder)+1:-10]
            f1.write("\n#"+name+"\n")
            results = produceStats(node_files[i], edge_files[i])
            f1.write("\t".join(results)+"\n")

if __name__ == "__main__":
    main(sys.argv)