### DAG.py 
This is the main algorithm that you might want to use. Keep in mind that its outputs do NOT include the G_0 (because G_0 is not guaranteed to be a single path), and if you want to add a new cost function, you will have to update COST_FUNCTIONS variable and the argument parser. 
#### Usage
```python DAG.py interactome(G).txt G_0.txt node_file.txt k```
or
```python DAG.py -h```
for more options.
#### Dependencies
* NetworkX 

### OutputStats.py
Takes in a DAG output and prints some information as total cost/number of all paths and edges.
#### Usage
```python OutputStats.py G.txt G_0.txt node_file.txt output.txt```

### pr.py
Contains functions to make a precision recall graph. Can be modified so that you can call the script but for customizability, I have been just importing pr to use getOutput, getPositives and pr methods.
#### Usage
In a python environment, import pr. Use getPositives("Directory_to_NetPath_files/pathway", "edges/nodes") function to get a set of positive edges/nodes. Then for every line you want to plot, use getOutput("outputfile.txt", "edges/nodes", "G_0file.txt") to obtain a dictionary of step to nodes/edges. Finally, use pr(dictionary, set) to obtain 2 lists, precision and recall. These two lists can be plotted using matplotlib.pyplot.

### post.py & post_pathway.py
These two are used to put the output of DAG.py into graphspace. post.py puts the output while post_pathway puts the whole pathway, colouring the lines in the output. In the past, the output included G_0, but currently it doesn't so they might use a little modification. They both have my GraphSpace account hardcoded into them so you might want to change that in order to use it. They also automatically share the graphs to a group that has me(Tunc), Jiarong and Anna in it, so you might want to add yourself to the group if you are using it. 
