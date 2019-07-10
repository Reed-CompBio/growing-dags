import sys
import subprocess
import glob
import time

NODE_FILE_GLOB = "/*-nodes.txt"
EDGE_FILE_GLOB = "/*-edges.txt"

PL_OUTPUT_NAME = "out_k_100-paths.txt"
G_0_FILE_NAME = "-G_0.txt"

def getReAndTf(filename):
    receptor = []
    tf = []
    with open(filename) as f:
        for line in f:
            if line[0] == "#":
                continue
            if line=='\n':
                continue
            items = [x.strip() for x in line.rstrip().split('\t')]
            node = items[0]
            tp = items[1]
            if tp == 'source' or tp == 'receptor':
                receptor.append(node)
            if tp == 'target' or tp == 'tf':
                tf.append(node)
    return receptor, tf

def extractPathwayName(filename, folder):
    """
    Input node/edge file containing name of pathway and name of the folder they are contained
    expected format for filename: 
        folder/pathway_name-edges.txt OR 
        folder/pathway_name-nodes.txt
        
    """
    name = filename[len(folder)+1:filename.find("-")]
    return name

def main(args):
    folder = args[1]
    node_files = sorted(glob.glob(folder + NODE_FILE_GLOB))
    edge_files = sorted(glob.glob(folder + EDGE_FILE_GLOB))
    for i in range(len(node_files)):
        receptor, tf = getReAndTf(node_files[i])
        if len(receptor) == 0 or len(tf) == 0:
            continue
        args = "python PathLinker.py " + "--write-paths " + edge_files[i] + " " + node_files[i]
        subprocess.call(args, shell=True)
        time.sleep(3)
        with open(PL_OUTPUT_NAME) as f1:
            for line in f1:
                if line[0] == "#":
                    continue
                if line=='\n':
                    continue
                ls = line.rstrip().split("\t")
                nodes = ls[2].split("|")
                print("Nodes: {}".format(nodes))
                if len(nodes) > 2 and nodes[0] in receptor and nodes[-1] in tf:
                    break
        pathway_name = extractPathwayName(node_files[i], folder)
        with open(pathway_name+G_0_FILE_NAME, "w") as f2:
            f2.write("#{0}\n".format(pathway_name))
            f2.write("#tail\thead\n")
            for i in range(len(nodes)-1):
                f2.write(nodes[i]+"\t"+nodes[i+1]+"\n")

if __name__ == "__main__":
    main(sys.argv)