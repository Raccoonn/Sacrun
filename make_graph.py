import networkx as nx
import numpy as np
import math
import json



def dist(p1, p2):
    """
    Returns distance between two GPS points
    """
    R = 6372800
    lat1, lon1 = p1
    lat2, lon2 = p2

    phi1, phi2 = math.radians(lat1), math.radians(lat2) 
    dphi       = math.radians(lat2 - lat1)
    dlambda    = math.radians(lon2 - lon1)
    
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    
    return 2*R*math.atan2(math.sqrt(a), math.sqrt(1 - a))







## Load GPS data
fname = 'store.json'
with open(fname) as f:
    store = json.load(f)




## Create fully connected graph from adjacency matrix
adj = np.zeros((len(store), len(store)))

for i, ix1 in enumerate(store):
    for j, ix2 in enumerate(store):
        p1 = store[ix1]
        p2 = store[ix2]
        adj[i,j] = dist(p1, p2)


G = nx.from_numpy_matrix(adj)

attrs = {0 : store}
nx.set_node_attributes(G, attrs)

m = nx.minimum_edge_cut(G)

ixs = list(store)




"""
Method for connecting intersections:

    - Select a node
    - Check for the closest node
    - If street is shared take node
        - If street is also shared with a previous found node
          check distance between the nodes is > distance from current node

    - Repeat until maximum (4) nodes is reached or distance is outside "average" radius

"""










