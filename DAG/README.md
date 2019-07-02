When running customDAG in terminal, users need use run.py with inputting argumenta of a file name of graph G, a file name of graph G_0, a file name of node types, a number of paths needed to be added, and a name of the output file. Then, the user can get a output file of results. 
Example of input: CLee$ python3 run.py G.txt G_0.txt nodetypes.txt 5 output.txt


### folder_into_dag
#### Usage:
    python folder_into_DAG.py k folder_containing_edges/nodes/G_0_files
#### Eg: 
    python folder_into_DAG.py 5 NetPath_Pathways   
#### Assumptions:
* the folder containing pathways is only composed of 1 edge, 1 node and 1 G_0 file for each pathway
* folder name doesn't contain '-'
#### Dependencies:
* glob
* DAG.py
