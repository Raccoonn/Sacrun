import networkx as nx
import numpy as np
import math
import json
import matplotlib.pyplot as plt
import gmplot





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
fname = 'xs_gps/030316_final_xs_gps_store.json'
with open(fname) as f:
    store = json.load(f)

## Conversion dictionaries for easier xs <-> node number lookup
n_to_xs = {n : xs for n, xs in enumerate(store)}
xs_to_n = {v : k for (k, v) in n_to_xs.items()}

## Add each node in store with intersection/gps stored as attributes
G = nx.Graph()
for i, xs in enumerate(store):
    G.add_node(i, xs=xs, gps=store[xs])



## Create fully connected adjacency matrix
adj = np.zeros((len(store), len(store)))

for i, ix1 in enumerate(store):
    for j, ix2 in enumerate(store):
        p1 = store[ix1]
        p2 = store[ix2]
        adj[i,j] = dist(p1, p2)



lat, lon = store[n_to_xs[0]]
gmap = gmplot.GoogleMapPlotter(lat, lon, 15)




## Link intersections

for n, xs_1 in enumerate(store):
    neighbors = [None] * 4
    gps_1 = store[xs_1]
    streets = xs_1.split(' & ')

    for i in np.argsort(adj[n])[1:7]:
        xs_2 = n_to_xs[i]
        gps_2 = store[xs_2]

        if streets[0] in xs_2.split(' & '):
            if neighbors[0] == None:
                neighbors[0] = (i, xs_2, gps_2)

            else:
                gps_n = neighbors[0][2]
                if min((gps_2[0], gps_n[0])) < gps_1[0] < max((gps_2[0], gps_n[0])) and \
                   min((gps_2[1], gps_n[1])) < gps_1[1] < max((gps_2[1], gps_n[1])):

                   neighbors[1] = (i, xs_2, gps_2)



        if streets[1] in xs_2.split(' & '):
            if neighbors[2] == None:
                neighbors[2] = (i, xs_2, gps_2)

            else:
                gps_n = neighbors[2][2]
                if min((gps_2[0], gps_n[0])) < gps_1[0] < max((gps_2[0], gps_n[0])) and \
                   min((gps_2[1], gps_n[1])) < gps_1[1] < max((gps_2[1], gps_n[1])):
                   neighbors[3] = (i, xs_2, gps_2)


        if None not in neighbors:
            break

    
    for nei in neighbors:
        if nei != None:
            G.add_edge(n, nei[0], weight=adj[n, nei[0]])
            gmap.plot(*zip(*[gps_1, nei[2]]), edge_width=5, color='black')



gmap.draw('connected.html')

H = nx.algorithms.eulerize(G)
path = nx.algorithms.eulerian_circuit(H)

with open('path.txt', 'w') as f:
    for edge in path:
        xs_1 = n_to_xs[edge[0]]
        xs_2 = n_to_xs[edge[1]]
        f.write(xs_1 + '  to  ' + xs_2 + '\n')




