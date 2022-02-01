import networkx as nx
import matplotlib.pyplot as plt

# H = nx.hexagonal_lattice_graph(2, 2, False, True)
# nx.draw(H)

G = nx.complete_graph(5)
nx.draw(G)
# G = nx.petersen_graph()
# subax1 = plt.subplot(121)
# nx.draw(G, with_labels=True, font_weight='bold')
# # subax2 = plt.subplot(122)
# # nx.draw_shell(G, nlist=[range(5, 10), range(5)], with_labels=True, font_weight='bold')


