import sys
import glob
import DAG as d

from multiprocessing.dummy import Pool as ThreadPool 
import itertools

"""
Usage:
    python folder_into_DAG.py k folder_containing_edges/nodes/G_0_files
Eg: 
    python folder_into_DAG.py 5 NetPath_Pathways
    
Assumptions:
    the folder containing pathways is only composed of 
        1 edge, 1 node and 1 G_0 file for each pathway
    folder name doesn't contain '-'
"""




NODE_FILE_GLOB = "/*-nodes.txt"
INTERACTOME = '/Users/Tunc/Desktop/Reed/PathLinker/DAG/2015pathlinker-weighted.txt'
"""
The G_0_FILE_GLOB is temporary until I know how we are going to obtain G_0s.
"""
G_0_FILE_GLOB = "/*-G_0.txt"


def extractPathwayName(filename, folder):
    """
    Input node/edge file containing name of pathway and name of the folder they are contained
    expected format for filename: 
        folder/pathway_name-edges.txt OR 
        folder/pathway_name-nodes.txt
        
    """
    name = filename[len(folder)+1:filename.find("-")]
    return name

"""
def main(args):
    k = int(args[1])
    folder = args[2]
    node_files = sorted(glob.glob(folder + NODE_FILE_GLOB))
    G_0_files = sorted(glob.glob(folder + G_0_FILE_GLOB))
    """
'''
    We might want to change DAG writing an output file.
    Temporarily, I will supply the name of the NetPath file being run as the
    output file name, but we might want to change it so that this main function
    creates an output with everything in one file.
'''
"""
    for i in range(len(node_files)):
        pathway_name = extractPathwayName(node_files[i], folder)
        output_name = pathway_name + "-output.txt"
        print("Currently DAGing {0}".format(pathway_name))
        d.apply(INTERACTOME, G_0_files[i], node_files[i], k, output_name)
"""

def main(args):
    k = int(args[1])
    folder = args[2]
    threads = 1
    if len(args) > 3:
        threads = int(args[3])
    node_files = sorted(glob.glob(folder + NODE_FILE_GLOB))
    G_0_files = sorted(glob.glob(folder + G_0_FILE_GLOB))
    output_names = []
    for i in range(len(node_files)):
        pathway_name = extractPathwayName(node_files[i], folder)
        output_names.append(pathway_name + "-output.txt")
    pool = ThreadPool(threads)
    pool.starmap(d.apply, zip(itertools.repeat(INTERACTOME), G_0_files, node_files, itertools.repeat(k), output_names))
    
       
if __name__ == "__main__":
    main(sys.argv)
        
    