import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import statistics as stat
from pandas.plotting import table

# Using pandas to create a dataframe to create a network.
doi_df = pd.read_csv('brianjy2_network.csv')

doi_graph = nx.Graph()

# Adding the nodes of the graph
doi_graph.add_nodes_from(doi_df['citing_iid'])
doi_graph.add_nodes_from(doi_df['cited_iid'])

edges = [(row['citing_iid'], row['cited_iid']) for index, 
         row in doi_df.iterrows()]

# Adding the edges created above into the graph
doi_graph.add_edges_from(edges)

# Creating a log-log scale graph image of the degree frequency in the network
degree_freq = nx.degree_histogram(doi_graph)
degrees = range(len(degree_freq))
plt.figure(figsize=(12, 8)) 
plt.loglog(degrees, degree_freq, 'go-') 
plt.title("Degree Distribution of Pubmed DOI Results")
plt.xlabel('Degree')
plt.ylabel('Frequency of Each Degree')
plt.savefig('doi_degree_distribution.png')

# Setting up the figure for the image of the network
plt.figure(figsize=(20, 20))  # Increase figure size

# Using a layout suitable for large networks
pos = nx.spring_layout(doi_graph, k=0.1, iterations=50)

# Creating an image of the network.
nx.draw(
    doi_graph, 
    pos,
    node_size=10, 
    node_color='blue', 
    edge_color='gray',
    alpha=0.5,  
    linewidths=0.1,
    with_labels=False  
)

# Saving the network as an image file
plt.savefig("doi_network.png", dpi=300, bbox_inches='tight')
plt.show()

# Getting the number of isolated nodes
isolated_nodes = list(nx.isolates(doi_graph))
isolated_nodes_num = len(isolated_nodes)

# Getting the number of connected components
connected_components_num = nx.number_connected_components(doi_graph)

# Geting the degrees of each node
doi_degrees = [d for n, d in doi_graph.degree()]

# Finding the minimum degree
min_doi_degree = np.min(doi_degrees)

# Finding the maximum degree
max_doi_degree = np.max(doi_degrees)

# Calculating the mean of the degrees in the network
mean_doi_degree = np.mean(doi_degrees)

# Calculating the median of the degrees in the network
median_doi_degree = np.median(doi_degrees)

# Calculating the mode of the degrees in the network
mode_doi_degree = stat.mode(doi_degrees)

# Creating a pandas table for the characteristics of the network
doi_data = {
    'Stats of DOI Network': ['Nodes', 'Edges', 'Minimum Degree', 
                        'Maximum Degree', 'Mean Degree', 'Mode Degree',
                        'Median Degree', 'Isolated Nodes',
                         'Connected Components'],
    'Values': [doi_graph.number_of_nodes(), doi_graph.number_of_edges(),
               min_doi_degree, max_doi_degree, mean_doi_degree, 
               mode_doi_degree, median_doi_degree, isolated_nodes_num,
               connected_components_num]                     
            } 

doi_stats_df = pd.DataFrame(doi_data)

# Plotting the table to use later
fig, ax = plt.subplots(figsize=(6, 2)) 
ax.axis('tight')
ax.axis('off')

# Creating the table from the stats of the network
tbl = table(ax, doi_stats_df, loc='center', cellLoc='center', 
            colWidths=[0.2, 0.2])
tbl.auto_set_font_size(False)
tbl.set_fontsize(8)
tbl.scale(1.0, 1.0) 

# Saving the table result as an image
plt.savefig("degree_statistics.png", bbox_inches='tight', dpi=300)
plt.show()
