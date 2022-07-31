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

For time testing:

```
python3 DAG.py ../../data/interactome-weights.txt ../../data/prepare-G0/pathlinker/Wnt-G0.txt ../../data/netpath/Wnt-nodes.txt -k 10 -c 1 -o ../../output/pathlinker-G0/Wnt_c1_k10.txt
```

BEFORE:
```
DAG.py ../../data/interactome-weights.txt ../../data/prepare-G0/pathlinker/Wnt-G0.txt ../../data/netpath/Wnt-nodes.txt -k 10 -c 1 -o ../../output/pathlinker-G0/Wnt_c1_k10.txt
--> READING GRAPH: 1.680295 seconds (cumulative 1.681283 s)
--> Converting Costs: 1.302834 seconds (cumulative 2.984203 s)
removing 2506 edges into receptors or out of tfs
--> ADDING SOURCES/SINKS: 0.084316 seconds (cumulative 3.068548 s)
--> CREATING G_0: 0.002195 seconds (cumulative 3.070763 s)
--> GETTING G_Delta: 1.557519 seconds (cumulative 4.628302 s)
Initializing Distances...
running for P98082 (1/4)
running for t (2/4)
running for s (3/4)
running for O75581 (4/4)
done init. distances
--> UPDATING DISTANCES: 11.476761 seconds (cumulative 16.105103 s)

GETTING BEST PATH
#1 ['s', 'O00144', 'O14641', 'P98082'] time: 1.5957670211791992

--> 1 ADDING EDGES: 0.000044 seconds (cumulative 17.701730 s)
--> 1 GET G_DELTA: 1.584222 seconds (cumulative 19.285965 s)
--> 1 UPDATING DISTANCES: 11.233217 seconds (cumulative 30.519228 s)

GETTING BEST PATH
#2 ['s', 'O75084', 'O14641'] time: 1.6616311073303223

--> 2 ADDING EDGES: 0.000066 seconds (cumulative 32.181029 s)
--> 2 GET G_DELTA: 1.567670 seconds (cumulative 33.748729 s)
--> 2 UPDATING DISTANCES: 6.119701 seconds (cumulative 39.868472 s)

GETTING BEST PATH
#3 ['s', 'Q13467', 'O14641'] time: 1.5816776752471924

--> 3 ADDING EDGES: 0.000031 seconds (cumulative 41.450280 s)
--> 3 GET G_DELTA: 1.576694 seconds (cumulative 43.026982 s)
--> 3 UPDATING DISTANCES: 6.259244 seconds (cumulative 49.286259 s)

GETTING BEST PATH
#4 ['s', 'Q14332', 'O14641'] time: 1.6132681369781494

--> 4 ADDING EDGES: 0.000031 seconds (cumulative 50.899662 s)
--> 4 GET G_DELTA: 1.555014 seconds (cumulative 52.454683 s)
--> 4 UPDATING DISTANCES: 6.230363 seconds (cumulative 58.685089 s)

GETTING BEST PATH
#5 ['s', 'Q9H461', 'O14641'] time: 1.6696019172668457

--> 5 ADDING EDGES: 0.000062 seconds (cumulative 60.354877 s)
--> 5 GET G_DELTA: 1.719702 seconds (cumulative 62.074586 s)
--> 5 UPDATING DISTANCES: 6.487364 seconds (cumulative 68.561996 s)

GETTING BEST PATH
#6 ['s', 'Q9NPG1', 'O14641'] time: 1.6090738773345947

--> 6 ADDING EDGES: 0.000032 seconds (cumulative 70.171202 s)
--> 6 GET G_DELTA: 1.593169 seconds (cumulative 71.764378 s)
--> 6 UPDATING DISTANCES: 6.448025 seconds (cumulative 78.212445 s)

GETTING BEST PATH
#7 ['s', 'Q9ULW2', 'O14641'] time: 1.5946428775787354

--> 7 ADDING EDGES: 0.000033 seconds (cumulative 79.807285 s)
--> 7 GET G_DELTA: 1.599830 seconds (cumulative 81.407123 s)
--> 7 UPDATING DISTANCES: 6.314387 seconds (cumulative 87.721582 s)

GETTING BEST PATH
#8 ['s', 'Q9UP38', 'O14641'] time: 1.571134090423584

--> 8 ADDING EDGES: 0.000033 seconds (cumulative 89.292843 s)
--> 8 GET G_DELTA: 1.834102 seconds (cumulative 91.126952 s)
--> 8 UPDATING DISTANCES: 6.283071 seconds (cumulative 97.410064 s)

GETTING BEST PATH
#9 ['O14641', 'P25054', 't'] time: 1.6166181564331055

--> 9 ADDING EDGES: 0.000045 seconds (cumulative 99.026918 s)
--> 9 GET G_DELTA: 1.572750 seconds (cumulative 100.599681 s)
--> 9 UPDATING DISTANCES: 28.413704 seconds (cumulative 129.013428 s)

GETTING BEST PATH
#10 ['s', 'Q01974', 'O43318', 'P98082'] time: 1.5709202289581299

--> 10 ADDING EDGES: 0.000070 seconds (cumulative 130.584564 s)
--> 10 GET G_DELTA: 1.554730 seconds (cumulative 132.139301 s)
--> 10 UPDATING DISTANCES: 32.706774 seconds (cumulative 164.846119 s)
DAG done
--> TOTAL TIME: 164.846119

89 Dijksta reruns out of 341 total
Function call took 165.00309586524963 seconds in total.
```
