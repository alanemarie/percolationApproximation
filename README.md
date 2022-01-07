# This folder contains the following files:

## SCRIPTS

    - percolationapprox.py: script having the main functions of our paper [https://dl.acm.org/doi/abs/10.1145/3394486.3403235](https://dl.acm.org/doi/abs/10.1145/3394486.3403235): 
        - get_diameter_approx: compute the vertex-diameter approximation of the given graph.
        - get_percolation_difference: implementation of Algorithm 1.
        - percolation_centrality_approximation: implementation of Algorithm 2.


    - test_percolation.py: script of our experiments
        Usage: python3.7 ./test_percolation <path_to_file> <directed>
        
        The file must be in .txt extension, and the corresponding graph must be in .mtx format.
        The value in <directed> must be a binary integer indicating if the graph is directed (value 1) or not (value 0).
        
