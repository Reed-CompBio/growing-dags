#pldag existing output
import networkx as nx
import datetime
import sys


def hasCycles(G_0, bestpath):
    test = G_0.copy()
    for i in range(len(bestpath) - 1):
        test.add_edge(bestpath[i], bestpath[i+1])
    try:
        nx.find_cycle(test)
        return True
    except nx.NetworkXNoCycle:
        return False


def validPath(G_0, path, minNofEdges, stats):
    
    stats[1] += 1
    if hasCycles(G_0, path):
        stats[2] += 1
        print("Has a cycle")
        
        return False

    newEdge = 0
    
    try:
        G_0[path[0]]
    except KeyError:
        newEdge += 1
        
    try:
        G_0[path[-1]]
    except KeyError:
        newEdge += 1
    
    for i in range(len(path)-1):
        u = path[i]
        v = path[i+1]
        try:
            G_0[u][v]
            continue
        except KeyError:
            newEdge += 1

    if newEdge >= minNofEdges or newEdge == len(path)-1:
        return True
    stats[3] += 1
    return False


def apply(args):
    
    
    path_file = args[1]
    k = int(args[2])
    minNofEdges = 1
    if len(args) > 3:
        minNofEdges = int(args[3])
     
    print("PL-DAG called with k = {}, min_edges = {} on {}".format(k, minNofEdges, path_file))
    G_0 = nx.DiGraph()
    added_path_counter = 0
    outfile_name = "pldag_out_j_{}_x_{}-".format(k, minNofEdges) + datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + ".txt"
    file_done_flag = True #Keeps track of whether all the paths in the file has been evaluated


    #number_of_evaluated_paths = 0            1 in stats
    #number_of_rejected_paths_cycle = 0       2 in stats
    #number_of_rejected_paths_minNofEdges = 0 3 in stats
    stats = {1:0, 2:0, 3:0}


    with open(path_file) as rf, open(outfile_name, "w") as wf:
        wf.write("#j\tpath_weight\tpath\n")
                 
        for line in rf:
            if line == "\n" or line[0] == "#":
                continue
            items = line.rstrip().split("\t")
            path = items[2].split("|")

            if validPath(G_0, path, minNofEdges, stats):
                added_path_counter += 1
                print("#{}: ".format(added_path_counter), path)
                print("\n")
                for i in range(len(path)-1):
                    n1 = path[i]
                    n2 = path[i+1]
                    G_0.add_edge(n1, n2)
                wf.write("{0}\t{1}\t{2}\n".format(added_path_counter, items[1], "|".join(path)))
                if added_path_counter == k:
                    print("{} paths has been added, results are in {}".format(k, outfile_name))
                    file_done_flag = False
                    break
    
    if file_done_flag:
        print("After iterating over all the paths in {}, only {} has been added.".format(path_file, added_path_counter))
        print("Results are in {}.".format(outfile_name))
        
    print("{} paths were evaluated.".format(stats[1]))
    print("{} of them were rejected due to cycles.".format(stats[2]))
    print("{} of them didn't have enough number of new edges".format(stats[3]))
    
    return

if __name__ == "__main__":
    apply(sys.argv)