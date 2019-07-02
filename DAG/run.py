import sys
import DAG as d

"""
When running DAG in terminal, users need to input the file name of 
graph G, the file name of graph G_0, the file name of node types, the number of
paths needed to be added, and the name of the output file. Then, the user can 
get a output file of results.
Eg: CLee$ python3 run.py G.txt G_0.txt nodetyes.txt 5 output.txt
"""
def main(args):
    G_name = args[1]
    G_0_name = args[2]
    stfileName = args[3]
    k = int(args[4])
    output = args[5]
    d.apply(G_name, G_0_name, stfileName, k, output)
    
if __name__ == '__main__':
    main(sys.argv)
