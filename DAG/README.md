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

### Test Code

Find first 10 paths from toy (functions 1-2):

```
python post_simple.py toy_G.txt toy_nodes.txt toy

python3 DAG.py toy_G.txt toy_G_0.txt toy_nodes.txt --no-log-transform -k 10 -c 1 -o toy_paths_c1_k10.txt
python post_simple_paths.py toy_G_0.txt toy_paths_c1_k10.txt toy_nodes.txt toy_c1

python3 DAG.py toy_G.txt toy_G_0.txt toy_nodes.txt --no-log-transform -k 10 -c 2 -o toy_paths_c2_k10.txt
python post_simple_paths.py toy_G_0.txt toy_paths_c2_k10.txt toy_nodes.txt toy_c2

python3 DAG.py toy_G.txt toy_G_0.txt toy_nodes.txt --no-log-transform -k 10 -c 3 -o toy_paths_c3_k10.txt
python post_simple_paths.py toy_G_0.txt toy_paths_c3_k10.txt toy_nodes.txt toy_c3

```

Find first 25 paths from Wnt NetPath pathway (functions 1-3):
```
python3 DAG.py interactome.txt ../G_0\'s\ from\ PathLinker/Wnt-G_0.txt ../NetPath/Wnt-nodes.txt -k 25 -c 1 -o wnt_paths_c1_k25.txt
python post_simple_paths.py ../G_0\'s\ from\ PathLinker/Wnt-G_0.txt wnt_paths_c1_k25.txt ../NetPath/Wnt-nodes.txt wnt_c1

python3 DAG.py interactome.txt ../G_0\'s\ from\ PathLinker/Wnt-G_0.txt ../NetPath/Wnt-nodes.txt -k 25 -c 2 -o wnt_paths_c2_k25.txt
python post_simple_paths.py ../G_0\'s\ from\ PathLinker/Wnt-G_0.txt wnt_paths_c2_k25.txt ../NetPath/Wnt-nodes.txt wnt_c2

python3 DAG.py interactome.txt ../G_0\'s\ from\ PathLinker/Wnt-G_0.txt ../NetPath/Wnt-nodes.txt -k 25 -c 3 -o wnt_paths_c3_k25.txt
python post_simple_paths.py ../G_0\'s\ from\ PathLinker/Wnt-G_0.txt wnt_paths_c3_k25.txt ../NetPath/Wnt-nodes.txt wnt_c3
```

## CODE:

To run small Wnt pathlinker datasets:

```
python3 DAG.py ../data/interactome-weights.txt ../data/prepare-G0/pathlinker/Wnt-G0.txt ../NetPath/Wnt-nodes.txt -k 20 -c 1 -o ../output/pathlinker-G0/Wnt_c1_k20.txt > ../output/pathlinker-G0/Wnt_c1.log
python post_simple_paths.py ../data/prepare-G0/pathlinker/Wnt-G0.txt ../output/pathlinker-G0/Wnt_c1_k20.txt ../NetPath/Wnt-nodes.txt Wnt_c1_20paths
python3 DAG.py ../data/interactome-weights.txt ../data/prepare-G0/pathlinker/Wnt-G0.txt ../NetPath/Wnt-nodes.txt -k 20 -c 2 -o ../output/pathlinker-G0/Wnt_c2_k20.txt > ../output/pathlinker-G0/Wnt_c2.log
python post_simple_paths.py ../data/prepare-G0/pathlinker/Wnt-G0.txt ../output/pathlinker-G0/Wnt_c2_k20.txt ../NetPath/Wnt-nodes.txt Wnt_c2_20paths
```

To post paths for all results:

```
python post_simple_paths.py ../data/prepare-G0/pathlinker/Wnt-G0.txt ../output/pathlinker-G0/Wnt_c1_k25.txt ../NetPath/Wnt-nodes.txt Wnt_c1
python post_simple_paths.py ../data/prepare-G0/pathlinker/IL1-G0.txt ../output/pathlinker-G0/IL1_c1_k25.txt ../NetPath/IL1-nodes.txt IL1_c1
python post_simple_paths.py ../data/prepare-G0/pathlinker/EGFR1-G0.txt ../output/pathlinker-G0/EGFR1_c1_k25.txt ../NetPath/EGFR1-nodes.txt EGFR1_c1
python post_simple_paths.py ../data/prepare-G0/pathlinker/TCR-G0.txt ../output/pathlinker-G0/TCR_c1_k25.txt ../NetPath/TCR-nodes.txt TCR_c1
python post_simple_paths.py ../data/prepare-G0/pathlinker/TGFbetaReceptor-G0.txt ../output/pathlinker-G0/TGFbetaReceptor_c1_k25.txt ../NetPath/TGF_beta_Receptor-nodes.txt TGFbetaReceptor_c1
python post_simple_paths.py ../data/prepare-G0/pathlinker/BCR-G0.txt ../output/pathlinker-G0/BCR_c1_k25.txt ../NetPath/BCR-nodes.txt BCR_c1

python post_simple_paths.py ../data/prepare-G0/pathlinker/Wnt-G0.txt ../output/pathlinker-G0/Wnt_c2_k25.txt ../NetPath/Wnt-nodes.txt Wnt_c2
python post_simple_paths.py ../data/prepare-G0/pathlinker/IL1-G0.txt ../output/pathlinker-G0/IL1_c2_k25.txt ../NetPath/IL1-nodes.txt IL1_c2
python post_simple_paths.py ../data/prepare-G0/pathlinker/EGFR1-G0.txt ../output/pathlinker-G0/EGFR1_c2_k25.txt ../NetPath/EGFR1-nodes.txt EGFR1_c2
python post_simple_paths.py ../data/prepare-G0/pathlinker/TCR-G0.txt ../output/pathlinker-G0/TCR_c2_k25.txt ../NetPath/TCR-nodes.txt TCR_c2
python post_simple_paths.py ../data/prepare-G0/pathlinker/TGFbetaReceptor-G0.txt ../output/pathlinker-G0/TGFbetaReceptor_c2_k25.txt ../NetPath/TGF_beta_Receptor-nodes.txt TGFbetaReceptor_c2
python post_simple_paths.py ../data/prepare-G0/pathlinker/BCR-G0.txt ../output/pathlinker-G0/BCR_c2_k25.txt ../NetPath/BCR-nodes.txt BCR_c2


python post_simple_paths_gt.py ../data/prepare-G0/ground_truth/Wnt-G0.txt ../output/ground_truth-G0/Wnt_c1_k25.txt ../NetPath/Wnt-nodes.txt Wnt_c1_ground_truth
python post_simple_paths_gt.py ../data/prepare-G0/ground_truth/IL1-G0.txt ../output/ground_truth-G0/IL1_c1_k25.txt ../NetPath/IL1-nodes.txt IL1_c1_ground_truth
python post_simple_paths_gt.py ../data/prepare-G0/ground_truth/EGFR1-G0.txt ../output/ground_truth-G0/EGFR1_c1_k25.txt ../NetPath/EGFR1-nodes.txt EGFR1_c1_ground_truth
python post_simple_paths_gt.py ../data/prepare-G0/ground_truth/TCR-G0.txt ../output/ground_truth-G0/TCR_c1_k25.txt ../NetPath/TCR-nodes.txt TCR_c1_ground_truth
python post_simple_paths_gt.py ../data/prepare-G0/ground_truth/TGFbetaReceptor-G0.txt ../output/ground_truth-G0/TGFbetaReceptor_c1_k25.txt ../NetPath/TGF_beta_Receptor-nodes.txt TGFbetaReceptor_c1_ground_truth
python post_simple_paths_gt.py ../data/prepare-G0/ground_truth/BCR-G0.txt ../output/ground_truth-G0/BCR_c1_k25.txt ../NetPath/BCR-nodes.txt BCR_c1_ground_truth

python post_simple_paths_gt.py ../data/prepare-G0/ground_truth/Wnt-G0.txt ../output/ground_truth-G0/Wnt_c2_k25.txt ../NetPath/Wnt-nodes.txt Wnt_c2_ground_truth
python post_simple_paths_gt.py ../data/prepare-G0/ground_truth/IL1-G0.txt ../output/ground_truth-G0/IL1_c2_k25.txt ../NetPath/IL1-nodes.txt IL1_c2_ground_truth
python post_simple_paths_gt.py ../data/prepare-G0/ground_truth/EGFR1-G0.txt ../output/ground_truth-G0/EGFR1_c2_k25.txt ../NetPath/EGFR1-nodes.txt EGFR1_c2_ground_truth
python post_simple_paths_gt.py ../data/prepare-G0/ground_truth/TCR-G0.txt ../output/ground_truth-G0/TCR_c2_k25.txt ../NetPath/TCR-nodes.txt TCR_c2_ground_truth
python post_simple_paths_gt.py ../data/prepare-G0/ground_truth/TGFbetaReceptor-G0.txt ../output/ground_truth-G0/TGFbetaReceptor_c2_k25.txt ../NetPath/TGF_beta_Receptor-nodes.txt TGFbetaReceptor_c2_ground_truth
python post_simple_paths_gt.py ../data/prepare-G0/ground_truth/BCR-G0.txt ../output/ground_truth-G0/BCR_c2_k25.txt ../NetPath/BCR-nodes.txt BCR_c2_ground_truth
```
