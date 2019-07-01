# Usage:
    python produce_stats.py path_to_folder_containing_all_edges/nodes_files
    
# Assumptions: 
* node_file and edge_file are tab-separated.
* node_file only contains none, receptor or tf as node_symbol
* all non-entry lines in the files start with #
* the folder containing pathways is only composed of 1 edges and 1 nodes file for each pathway

# Dependencies
* glob
