# Algorithms

## DAG.py

This is the main algorithm that you might want to use. Keep in mind that its outputs do NOT include the G_0 (because G_0 is not guaranteed to be a single path).

#### Usage

```
usage: DAG.py [-h] [-k K] [-o OUT_FILE] [--no-log-transform] [-c {1,2,3}] [-a A]
              interactome_file G0_file node_file

DAG

positional arguments:
  interactome_file      All interactions in G (three tab-delim columns: nodeA, nodeB, weight).
  G0_file               Initial DAG (G_0) (two tab-delim columns: nodeA, nodeB)
  node_file             File that contains node ids and their types. Should not contain nodes named 's' or 't'.

optional arguments:
  -h, --help            show this help message and exit
  -k K                  Number of paths the algorithm will try to add to G_0 (default 10). The algorithm might end earlier if it cannot find more paths.
  -o OUT_FILE, --out_file OUT_FILE
                        Output file name. (default='dag-out-{k}.txt')
  --no-log-transform    If interactome contains interaction costs (lower is better) instead of probabilities(higher is better), this option should be used.
  -c {1,2,3}, --cost-function {1,2,3}
                        Choice of cost function. (default=2)
                        	1-Minimize the total cost of all edges.
                        	2-Minimize the total cost of all paths.
                        	3-Mixture of 1 and 2 where total score is a*c1 + (1-a)*c2.
  -a A                  Tradeoff param for c3 (between 0 and 1 , default 0.5): a*c1 + (1-a)*c2.
```

#### Dependencies
* NetworkX

### OutputStats.py
Takes in a DAG output and prints some information as total cost/number of all paths and edges.

#### Usage
```
python OutputStats.py <interactome> <G0> <nodes> <output>
```

### Test Code

Find & visualize first 10 paths from toy (functions 1-2):

```
python ../viz/post_simple.py ../../data/toy/toy_G.txt ../../data/toy/toy_nodes.txt toy

python3 DAG.py ../../data/toy/toy_G.txt ../../data/toy/toy_G_0.txt ../../data/toy/toy_nodes.txt --no-log-transform -k 10 -c 1 -o ../../output/toy/toy_paths_c1_k10.txt
python ../viz/post_simple_paths.py ../../data/toy/toy_G_0.txt ../../output/toy/toy_paths_c1_k10.txt ../../data/toy/toy_nodes.txt toy_c1

python3 DAG.py ../../data/toy/toy_G.txt ../../data/toy/toy_G_0.txt ../../data/toy/toy_nodes.txt --no-log-transform -k 10 -c 1 -o ../../output/toy/toy_paths_c1_k10.txt
python ../viz/post_simple_paths.py ../../data/toy/toy_G_0.txt ../../output/toy/toy_paths_c1_k10.txt ../../data/toy/toy_nodes.txt toy_c1
```

## CODE:

To run small Wnt pathlinker datasets:

```
python3 DAG.py ../../data/interactome-weights.txt ../../data/prepare-G0/pathlinker/Wnt-G0.txt ../../data/netpath/Wnt-nodes.txt -k 20 -c 1 -o ../../output/pathlinker-G0/Wnt_c1_k20.txt > ../../output/pathlinker-G0/Wnt_c1.log
python ../viz/post_simple_paths.py ../../data/prepare-G0/pathlinker/Wnt-G0.txt ../../output/pathlinker-G0/Wnt_c1_k20.txt ../../data/netpath/Wnt-nodes.txt Wnt_c1_20paths
python3 DAG.py ../../data/interactome-weights.txt ../../data/prepare-G0/pathlinker/Wnt-G0.txt ../../data/netpath/Wnt-nodes.txt -k 20 -c 2 -o ../../output/pathlinker-G0/Wnt_c2_k20.txt > ../../output/pathlinker-G0/Wnt_c2.log
python ../viz/post_simple_paths.py ../../data/prepare-G0/pathlinker/Wnt-G0.txt ../../output/pathlinker-G0/Wnt_c2_k20.txt ../../data/netpath/Wnt-nodes.txt Wnt_c2_20paths
```
