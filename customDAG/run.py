import sys
import customDAG as cd

"""
When running customDAG in terminal, users need to input the file name of 
graph G, the file name of graph G_0, the number of paths needed to be added, 
and the name of the output file. Then, the user can get a output file of results.
Eg: CLee$ python3 run.py demo_G.txt demo_G_0.txt 5 output.txt
"""
def main(args):
    G_name = args[1]
    G_0_name = args[2]
    k = int(args[3])
    output = args[4]
    cd.apply(G_name, G_0_name, k, output)
    
if __name__ == '__main__':
    main(sys.argv)