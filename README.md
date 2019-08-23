# growing-dags

Hello! The DAG folder contains the main files related to this work. G_0's from PathLinker contain G_0 files that were obtained by taking the first path longer than a single edge from the output of PathLinker for the respective pathways.

## Future/unexplored work

* The current model of the network doesn't explicitly take into account some biological processes such as negative feedback. How can we improve the base model to take them into account?
* Cost functions: we haven't really ran anything over 100 paths, we need to observe how our cost functions perform beyond that in terms of precision and recall, and even devise new cost functions that model biological networks better.
* We haven't tested how does changing the ground truth G_0's affect the output. This is not only to change the path in G_0 but even make G_0 bigger.
* Does the fact that edge weights in the interactome were calculated using their inclusion in NetPath make our results meaningless?
