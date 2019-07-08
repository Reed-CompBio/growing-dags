import sys
import subprocess
import glob
import time

NODE_FILE_GLOB = "/*-nodes.txt"
EDGE_FILE_GLOB = "/*-edges.txt"

PL_OUTPUT_NAME = "out_k_100-paths.txt"
G_0_FILE_NAME = "-G_0.txt"

def extractPathwayName(filename, folder):
    """
    Input node/edge file containing name of pathway and name of the folder they are contained
    expected format for filename: 
        folder/pathway_name-edges.txt OR 
        folder/pathway_name-nodes.txt
        
    """
    name = filename[len(folder):filename.find("-")]
    return name

def main(args):
    folder = args[1]
    node_files = sorted(glob.glob(folder + NODE_FILE_GLOB))
    edge_files = sorted(glob.glob(folder + EDGE_FILE_GLOB))
    for i in range(len(node_files)):
        args = "python PathLinker.py " + "--write-paths " + "--no-log-transform " + edge_files[i] + " " + node_files[i]
        subprocess.call(args, shell=True)
        with open(PL_OUTPUT_NAME) as f1:
            for line in f1:
                if line[0] == "#":
                    continue
                ls = line.rstrip().split("\t")
                path = ls[2].split("|")
                if len(path) > 2:
                    print("Breaking with path {}".format(path))
                    break
        if len(path) <= 2:
            continue
        pathway_name = extractPathwayName(node_files[i], folder)
        print("PATHWAY NAME: {}".format(pathway_name))
        with open(pathway_name+G_0_FILE_NAME, "w") as f2:
            f2.write("#{0}\n".format(pathway_name))
            f2.write("#tail\thead\n")
            for i in range(len(path)-1):
                f2.write(path[i]+"\t"+path[i+1]+"\n")

if __name__ == "__main__":
    main(sys.argv)