import networkx as nx
import DAG as d
import sys


def TotalCostOfAllPaths(G_0):

    total_cost_of_all_paths = 0
    n_paths_to_sink = d.CountPathsToSink(G_0)
    n_paths_from_source = d.CountPathsFromSource(G_0)
    costs = nx.get_edge_attributes(G_0, "cost")
    for edge in G_0.edges():
        total_cost_of_all_paths += (n_paths_to_sink[edge[1]] * n_paths_from_source[edge[0]] * costs[edge])

    return total_cost_of_all_paths


def TotalCostOfAllEdges(G_0):

    total_cost_of_all_edges = 0
    costs = nx.get_edge_attributes(G_0, "cost")
    for cost in costs.values():
        total_cost_of_all_edges += cost

    return total_cost_of_all_edges


def getEdgesAndPaths(G_0):

    n_paths_from_source = d.CountPathsFromSource(G_0)
    n_paths = n_paths_from_source["t"]
    n_edges = len(list(G_0.edges()))

    return n_edges, n_paths


def apply(G_file, G_0_file, node_file, output_file):
    G = d.readGraph(G_file)
    d.logTransformEdgeWeights(G)
    recep, tf = d.addSourceSink(node_file, G)
    G_0, _ = d.createG_0(G_0_file, G, recep, tf)

    with open(output_file) as f:
        for line in f:
            if line == "\n" or line[0] == "#":
                continue

            items = [x.strip() for x in line.rstrip().split('\t')]
            path = items[2].split("|")
            for i in range(len(path)-1):
                G_0.add_edge(path[i], path[i+1], cost=G[path[i]][path[i+1]]["cost"])
            if path[0] in recep:
                G_0.add_edge("s", path[0], weight=1, cost=0)
            if path[-1] in tf:
                G_0.add_edge(path[-1], "t", weight=1, cost=0)

    total_cost_of_all_paths = TotalCostOfAllPaths(G_0)
    total_cost_of_all_edges = TotalCostOfAllEdges(G_0)
    n_edges, n_paths = getEdgesAndPaths(G_0)

    print("Total cost of all paths: {}".format(total_cost_of_all_paths))
    print("Total cost of all edges: {}".format(total_cost_of_all_edges))
    print("There are {} edges and {} paths in the network.".format(n_edges, n_paths))
    print("Edges to paths ratio: {}".format(n_edges/n_paths))
    return


def main(args):
    G_file = args[1]
    G_0_file = args[2]
    node_file = args[3]
    output_file = args[4]
    return apply(G_file, G_0_file, node_file, output_file)


if __name__ == "__main__":
    main(sys.argv)
