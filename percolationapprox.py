import networkx as nx
from math import log, floor, ceil
from random import sample, choice
import operator
import collections

###########################################################################################
def R(x: float): return max(x, 0)
###########################################################################################



###########################################################################################
def get_diameter_approx(G: nx.classes.graph.Graph, directed: int):
	"""
	Vertex-diameter approximation function

	Parameters:
	-------------
	G: nx.classes.graph.Graph
		Networkx graph built from the given input data
	directed: int
		Binary flag indicating that G is directed (if 1) or not (if 0)


	Returns
	-------------
	max_d: int
		value for the vertex-diameter estimation

	"""


    max_d = 0
    if directed:
        H = G.to_undirected()
    else:
        H = G
    for c in nx.connected_components(H):
        v = sample(list(c), 1)[0]
        paths = nx.shortest_path(H, source=v)
        max1 = max2 = 0
        for t in paths:
            if len(paths[t]) > max1:
                max1 = len(paths[t])
                key1 = t

        del paths[key1]


        for t in paths:
            if len(paths[t]) > max2:
                max2 = len(paths[t])
      

        if(max1 + max2 - 2 > max_d):
            max_d = max1 + max2 - 2
    return max_d
###########################################################################################



###########################################################################################
def get_percolation_difference(G: nx.classes.graph.Graph, A: collections.OrderedDict):
	"""
	Implementation of Algorithm 1 as described in http://www.inf.ufpr.br/amlima/percolation.pdf.


	Parameters:
	-------------
	G: nx.classes.graph.Graph
		NetworkX Graph

	A: collections.OrderedDict
		Dictionary sorted by its float values


	Returns
	-------------
	minus_sum: dictionary
		For each key i, minus_sum[i] contains the accumulated sum of the values in A minus the value in A[i]


	"""

    n = len(A)
    sum = 0
    minus_sum = {}
    for v in G.nodes:
        minus_sum[v] = 0.0
    svp = [0] * (n+1)

    j = 0
    for i in A:
        if(j > 0):
            svp[j] = svp[j-1] + k
            sum = sum + j*A[i] - svp[j]
        k = A[i]
        j += 1
    svp[n] = svp[n-1] + k

    j = 0
    for i in A:
        minus_sum[i] = sum - A[i]*(2*j-n) - svp[n] + 2*svp[j]
        j += 1
    return minus_sum
###########################################################################################



###########################################################################################
def percolation_centrality_approximation(G: nx.classes.graph.Graph, x: dict, directed: int, epsilon: float, delta: float, universalConstant=0.5):
    """
    Implementation of Algorithm 2 as described in http://www.inf.ufpr.br/amlima/percolation.pdf.


    Parameters
    -------------
	G: nx.classes.graph.Graph
		NetworkX graph

	x: dictionary
		Dictionary where the keys are the vertices of G and the values are the percolation states

	directed: int
		Binary flag indicating that G is directed (if 1) or not (if 0)

	epsilon: float
		Quality parameter

	delta: float
		Confidence parameter

	universalConstant: float
		Constant of the upper bound to the minimum sample size. Default value=0.5.
	


	Returns
	-------------
	p_tilde: dictionary
		Dictionary where the keys are the vertices of G and the values are the percolation estimations

    """

    n = G.number_of_nodes()
    p_tilde = {}
    for v in G.nodes:
        p_tilde[v] = 0

    diam_G = get_diameter_approx(G,directed)
    r = ceil((universalConstant / (epsilon * epsilon)) * (floor(log(diam_G, 2.0) - 2.0) + 1.0 - log(delta)))
    print("Number of samples r = " + str(r))

    sorted_d = sorted(x.items(), key=lambda kv: kv[1])
    sorted_dict = collections.OrderedDict(sorted_d)
    minus_s = get_percolation_difference(G,sorted_dict)

    for i in range(r):
        u, w = sample(list(G.nodes), 2)  
        try:
            paths = [p for p in nx.all_shortest_paths(G, u, w)]
        except nx.NetworkXNoPath:
            paths = []
        if len(paths) != 0:
            t = w
            while t != u:
                z = choice([p[-2] for p in paths])  
                paths = [p[:-1] for p in paths if p[-2] == z]
                if z != u:
                    p_tilde[z] = p_tilde[z] + (1/r) * (R(x[u] - x[w])/minus_s[z])
                t = z

    return p_tilde
###########################################################################################