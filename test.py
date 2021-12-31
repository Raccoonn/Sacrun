import matplotlib.pyplot as plt
import networkx as nx


G = nx.Graph()

G.add_node(5, nbrs=[1,2,3,4])

print(type(G.nodes[5]['nbrs']))