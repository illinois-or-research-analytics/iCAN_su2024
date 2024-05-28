import networkx as nx
import matplotlib.pyplot as plt

# Need to generate a random graph with 1000 nodes and at least 10,000 edges
nodes_num = 1000
edges_num = 10000

# Making sure there are enough edges in the graph
while True:
    graph_result = nx.gnm_random_graph(nodes_num, edges_num)
    if nx.number_of_edges(graph_result) >= edges_num:
        break

# Saving as an edge list (TSV) file
nx.write_edgelist(graph_result, "network.edgelist.tsv", delimiter="\t")

# Saving as a METIS file
with open("network.metis", "w") as graph_metis_file:
    graph_metis_file.write(f"{nodes_num} {edges_num}\n")
    for u, v in graph_result.edges():
        graph_metis_file.write(f"{u + 1} {v + 1}\n")

# Saving as a GraphML file
nx.write_graphml(graph_result, "network.graphml")

# Ploting the degree distribution of the generated graph
degree_sequence = sorted([degree for node, degree in \
                          graph_result.degree()], reverse=True)
plt.figure()
plt.hist(degree_sequence, bins=30)
plt.title("Degree Distribution")
plt.xlabel("Degree")
plt.ylabel("Frequency")
plt.savefig("degree_distribution.png")

# Getting the number of isolated nodes
isolated_nodes = list(nx.isolates(graph_result))
isolated_nodes_num = len(isolated_nodes)

# Getting the number of connected components
connected_components_num = nx.number_connected_components(graph_result)

# Printing the results
print(f"Number of isolated nodes in the graph: {isolated_nodes_num}")
print("Number of connected components in the graph: " \
      f"{connected_components_num}")