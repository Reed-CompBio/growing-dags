### `precrec.py`

To calculate precision and recall for Wnt c1 k200:
```
python precrec.py ../../output/pathlinker-stitched/Wnt_c1_k200.txt ../../data/prepare-G0/pathlinker/Wnt-G0.txt ../../data/netpath/Wnt-edges.txt ../../output/pathlinker-stitched/precrec/Wnt_c1_k200-pr
```

To calculate subsampled precision and recall for Wnt c1 k200:
```
python precrec-subsample.py ../../output/pathlinker-stitched/Wnt_c1_k200.txt ../../data/prepare-G0/pathlinker/Wnt-G0.txt ../../data/netpath/Wnt-edges.txt ../../data/interactome-weights.txt ../../output/pathlinker-stitched/precrec/Wnt_c1_k200-pr
```

# Old Code

### pr.py
Contains functions to make a precision recall graph. Can be modified so that you can call the script but for customizability, I have been just importing pr to use getOutput, getPositives and pr methods.

#### Usage
In a python environment, import pr. Use getPositives("Directory_to_NetPath_files/pathway", "edges/nodes") function to get a set of positive edges/nodes. Then for every line you want to plot, use getOutput("outputfile.txt", "edges/nodes", "G_0file.txt") to obtain a dictionary of step to nodes/edges. Finally, use pr(dictionary, set) to obtain 2 lists, precision and recall. These two lists can be plotted using matplotlib.pyplot.
