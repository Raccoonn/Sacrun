import matplotlib.pyplot as plt
import networkx as nx


G = nx.Graph()

G.add_node(1)
G.add_node(2)

G.add_edge(1, 2, weight=5)
G.add_edge(2, 1, weight=5)

print(list(G.edges))
nx.draw(G)

plt.show()