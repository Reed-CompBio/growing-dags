# Assumes that there is a NetPath_Pathways folder in the current directory that contains edges/nodes files.
import sys


def pr_best_paths(args):
    # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #                      Usage Example                  #
    #   python pr_best_paths Wnt_k_50000-paths.txt Wnt .7 #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    pl_file = args[1]  # PathLinker paths file
    pathway_name = args[2]  # Name of the pathway
    min_precision = float(args[3])  # Minimum precision for paths

    all_pos_edges = set()  # Set to contain all positive edges for recall calculation
    all_pos_nodes = set()  # Set to contain all positive nodes for recall calculation
    all_seen_edges = set()  # Set to contain all seen edges for precision calculation
    all_seen_nodes = set()  # Set to contain all seen nodes for precision calculation
    accepted_edges = set()  # Set to contain edges from paths above minimum precision
    accepted_nodes = set()  # Set to contain nodes from paths above minimum precision

    # # # # # # # # # # # # # #
    # Determine positive nodes #
    # # # # # # # # # # # # # #
    with open("NetPath_Pathways/{}-nodes.txt".format(pathway_name)) as nf:
        for line in nf:
            if line == "\n" or line == "#":
                continue
            node = line.rstrip().split("\t")[0]
            all_pos_nodes.add(node)

    # # # # # # # # # # # # # #
    # Determine positive edges #
    # # # # # # # # # # # # # #
    with open("NetPath_Pathways/{}-edges.txt".format(pathway_name)) as ef:
        for line in ef:
            if line == "\n" or line == "#":
                continue
            items = line.rstrip().split("\t")
            all_pos_edges.add((items[0], items[1]))

    # # # # # # # # # # # # # # # # # # # # #
    # Collect paths above minimum precision #
    # # # # # # # # # # # # # # # # # # # # #
    with open(pl_file) as f:
        for line in f:
            if line == "\n" or line == "#":
                continue

            path = line.rstrip().split("\t")[2].split("|")
            pos_count = 0
            for i in range(len(path) - 1):
                edge = (path[i], path[i + 1])
                if edge in all_pos_edges:
                    pos_count += 1

            if pos_count / len(path) >= min_precision:
                for i in range(len(path) - 1):
                    # Add edges to seen and accepted sets
                    edge = (path[i], path[i + 1])
                    all_seen_edges.add(edge)
                    if edge in all_pos_edges:
                        accepted_edges.add(edge)
                    # Add nodes to seen and accepted sets
                    all_seen_nodes.add(path[i])
                    if path[i] in all_pos_nodes:
                        accepted_nodes.add(path[i])
                all_seen_nodes.add(path[-1])
                if path[-1] in all_pos_nodes:   # Last node is not included in the for-loop above
                    accepted_nodes.add(path[-1])

    # # # # # # # # # # # # # #
    # Calculation and Results #
    # # # # # # # # # # # # # #
    precision_edge = len(accepted_edges) / len(all_seen_edges)
    precision_node = len(accepted_nodes) / len(all_seen_nodes)
    recall_edge = len(accepted_edges) / len(all_pos_edges)
    recall_node = len(accepted_nodes) / len(all_pos_nodes)
    print("Nodes:")
    print("\tPrecision: ", precision_node)
    print("\tRecall: ", recall_node)
    print("Edges:")
    print("\tPrecision: ", precision_edge)
    print("\tRecall: ", recall_edge)


if __name__ == '__main__':
    pr_best_paths(sys.argv)
