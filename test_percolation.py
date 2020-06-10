import random
from percolationapprox import percolation_centrality_approximation, get_diameter_approx
import networkx as nx
import time
import os
import collections
from random import sample, choice
from math import log, floor, ceil
import itertools
import sys
from statistics import stdev 

###########################################################################################
def read_snap_graph(file: str, directed: int):
    """
    Function that reads a graph from file


    Parameters
    -------------
    file: string
        Path to the input graph file
    
    directed: int
        Binary flag indicating that G is directed (if 1) or not (if 0)


    Returns
    -------------
    G: nx.classes.graph.Graph
        NetworkX graph

    """

    if directed:
        G = nx.DiGraph()
    else:
        G = nx.Graph()

    for line in file:
        tokens = line.split()
        if tokens[0] != '#':
            source = tokens[0]
            target = tokens[1]
            if len(tokens) > 2:
                G.add_edge(source,target, weight = tokens[2])
            else:
                weight = random.randrange(1,100)
                G.add_edge(source,target,weight = weight)

    return G
###########################################################################################



###########################################################################################
def main(file: str, directed: int):

    """
    Main function


    Parameters
    -------------
    file: string
        Path to the input graph file

    directed: int
        Binary flag indicating that G is directed (if 1) or not (if 0)
  
    """


    '''
    Barabasi-Albert graph generator
    n = 1000
    #G = nx.barabasi_albert_graph(n, 3)
    '''

    with open(file, 'r') as f:
        G = read_snap_graph(f,int(directed))
    f.close
    n = len(G)


    print("The graph has {} vertices and {} edges".format(G.number_of_nodes(), G.number_of_edges()))

 

    for node in G.nodes:
        G.nodes[node]['percolation'] = random.uniform(0.0,1.0)
    x = {node: G.nodes[node]['percolation'] for node in G.nodes}


    t1 = time.process_time()
    pc = nx.percolation_centrality(G)
    print("Total running time (exact algorithm): " + str(time.process_time() - t1))
    print("Exact percolation values: \n" + ', '.join('{:0.20f}'.format(pc[i]/(n*(n-1))) for i in pc) + "\n")


    epsilon = [0.04, 0.06, 0.08, 0.10]
    delta = 0.1

    i = 0
    for e in epsilon:
        times = []
        errors = []
        diffs_list = []
        deviations = []
        while i < 5:
            print("epsilon: "+str(e)+" ------------------------------------")
            t2 = time.process_time()
            pc_tilde = percolation_centrality_approximation(G, x, int(directed), float(e), float(delta))
            print("Total running time (approximation algorithm): " + str(time.process_time() - t2))
            times.append(time.process_time() - t2)
            print("Approximated percolation values: \n" + ', '.join('{:0.20f}'.format(pc_tilde[i]) for i in pc_tilde))
            print("Zeros = " + str(list(pc_tilde.values()).count(0)) + "\n")

            diffs = {}
            sum_diffs = 0.0
            for v in G.nodes:
                diffs[v] = abs(pc[v]/(n*(n-1)) - pc_tilde[v])
                sum_diffs += diffs[v]
                diffs_list.append(diffs[v])
            avg_error = sum_diffs/len(G.nodes)
            errors.append(avg_error)
            deviation = stdev(diffs_list)
            deviations.append(deviation)
    
            print("Absolute difference between the exact and the approximation algorithm:\n" + ', '.join('{:0.20f}'.format(diffs[i]) for i in diffs))
            sorted_diffs = sorted(diffs.items(), key=lambda kv: kv[1], reverse=True)
            diffs_d = collections.OrderedDict(sorted_diffs)
            print("Absolute difference between the exact and the approximation algorithm (sorted, non-increasing):\n" + ', '.join('{:0.20f}'.format(diffs_d[i]) for i in diffs_d))

            i += 1
        print("time: ")
        print(times)
        print("avg error: ")
        print(errors)
        print("std dev: ")
        print(deviations)
    
        i = 0

    del G
###########################################################################################



###########################################################################################
if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("Use: python3.7 ./test_percolation <path_to_file> <int: directed>.")

    main(sys.argv[1], sys.argv[2])
###########################################################################################
