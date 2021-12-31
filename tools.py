
import networkx as nx
import numpy as np
import math
import json
import matplotlib.pyplot as plt
import gmplot




"""
Graph construction from coordinates
"""


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
            - Attributes:  Information about the given intersection; index, name, gps, etc.
            - Methods:  Finding nearest neighbors given a list of intersection objects
        """
        ## General information
        self.n = n
        self.name = streets
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





"""
Read/Write tools
"""

def load_coords(fname, alleys=False):
    """
    Given json file of intesection coordinates returns
    list of intersection objects
    """
    ## Load GPS data
    with open(fname) as f:
        store = json.load(f)

    ## Exclude alleys if desired
    if alleys == False:
        store = {key:val for key,val in store.items() if 'Aly' not in key}

    ## Add all nodes to list
    intersections = []
    for n, streets in enumerate(store):
        intersections.append(XS(n, streets, store[streets]))






"""
gmplot Mapping Tools
"""


def map_intersections(f_bounds, f_coords, map_fname):
    """
    Extract and plot GPS coordinates for intersections
    """
    ## Load GPS boundaries
    with open(f_bounds) as f:
        bounds = [[float(n) for n in line.split(', ')] for line in f.read().splitlines()]
        bounds.append(bounds[0])

    ## Load Intersection GPS data
    with open(f_coords) as f:
        store = json.load(f)

    ## Extract GPS coordinates from files
    gps_store = []
    for key in store:
        gps_store.append(store[key])


    ## Draw map of intersections and boundaries
    lat, lon = gps_store[0]
    gmap = gmplot.GoogleMapPlotter(lat, lon, 15)
    gmap.plot(*zip(*bounds), edge_width=6, color='blue')
    gmap.scatter(*zip(*gps_store), color='red')
    gmap.draw('maps/%s.html' % map_fname)









