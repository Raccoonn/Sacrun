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




class XS:
    def __init__(self, n, streets, gps):
        """
        Intersection object
        """
        ## General information
        self.n = n
        self.streets = streets.split(' & ')
        self.gps = gps
        self.lat, self.lon = gps


    def find_neighbors(self, intersections, max_n=4):
        """
        Find all nearest neighbors
            - Maximum = 4
            - Minimum = 2
        """
        ## Initialize neighbors
        self.neighbors = [None]*max_n

        ## Adjacency to other nodes, intersections perserves node index
        self.adj = [dist(xs.gps, self.gps) for xs in intersections]

        ## Maximum check twenty closest nodes (Skipping self node)
        for idx in np.argsort(self.adj)[:10]:
            xs = intersections[idx]
            if xs.n != self.n:
                for n, i in zip(range(2), range(0,4,2)):
                    ## Check matching street name
                    if self.streets[n] == xs.streets[n]:
                        ## Add closest
                        if self.neighbors[i] == None:
                            self.neighbors[i] = xs

                        ## Next neighbor check distances
                        elif self.neighbors[i+1] == None:
                            d_ax = dist(self.neighbors[i].gps, self.gps)
                            d_bx = dist(xs.gps, self.gps)
                            d_ab = dist(xs.gps, self.neighbors[i].gps)
                            if d_ax <= d_ab and d_bx <= d_ab:
                                self.neighbors[i+1] = xs

                    ## Break if four neighbors found, otherise continue search
                    if None not in self.neighbors:
                        return








## Load GPS data
fname = 'xs_gps/1220_004707_final_xs_gps_store.json'
with open(fname) as f:
    store = json.load(f)


##
## No alleys
##
store = {key:val for key,val in store.items() if 'Aly' not in key}


## Add all nodes to list
intersections = []
for n, streets in enumerate(store):
    intersections.append(XS(n, streets, store[streets]))

## Find all neighbors for each node
for xs in intersections:
    xs.find_neighbors(intersections)





# xs = intersections[99]
# print(xs.streets)
# for n in xs.neighbors:
#     if n != None:
#         print(n.streets)
#     else:
#         print("no neighbor")


xs_0 = intersections[0]
gmap = gmplot.GoogleMapPlotter(xs_0.lat, xs_0.lon, 15)

## Build graph
G = nx.Graph()
for xs in intersections:
    for nbr in xs.neighbors:
        if nbr != None:
            G.add_edge(xs.n, nbr.n, weight=xs.adj[nbr.n])
            gmap.plot(*zip(*[xs.gps, nbr.gps]), edge_width=13, color='black')



gmap.draw('new neighbor mapping_no alleys.html')


print(len(G.nodes))
print(len(G.edges))

for node in G:
    print(G.edges(node))


nx.draw(G, with_labels=True)

# nx.draw_networkx_edges(G, pos=nx.spring_layout(G))

plt.show()