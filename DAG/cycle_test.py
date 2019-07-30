import networkx as nx
G = nx.DiGraph()

with open("BCR_k_50000-paths.txt") as f:
    for line in f:
        if line =="\n" or line[0]=="#":
            continue
        items = line.rstrip().split("\t")
        nodes = items[2].split("|")
        for i in range(len(nodes)-1):
            G.add_edge(nodes[i], nodes[i+1])
        if items[0] == "800":
            break
print(len(G.edges()))
print(len(list(nx.simple_cycles(G))))
