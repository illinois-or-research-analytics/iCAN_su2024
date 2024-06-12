import pandas as pd
import networkit as nk
import networkx as nx
import matplotlib.pyplot as plt


def main():
    """Here we generate some descriptive statistics about our network"""
    EDGE_COLOR = "tomato"

    # Load the results of the sqp query
    df = pd.read_csv(
        "/Users/serge/Code/cs597/iCAN_su2024/serge/assignment2/output/network_table.csv"
    )

    G = nk.graph.Graph(directed=True)

    # Add nodes to the graph
    nodes = set(df["citing_iid"]).union(set(df["cited_iid"]))
    for node in nodes:
        G.addNode()

    # Map node IDs to graph node indices
    node_map = {node: index for index, node in enumerate(nodes)}

    # Add edges to the graph
    for _, row in df.iterrows():
        G.addEdge(node_map[row["citing_iid"]], node_map[row["cited_iid"]])

    # Descriptive statistics
    num_nodes = G.numberOfNodes()
    num_edges = G.numberOfEdges()
    density = nk.graphtools.density(G)
    degree_dist = nk.centrality.DegreeCentrality(G)
    degree_dist.run()

    print(f"Number of nodes: {num_nodes}")
    print(f"Number of edges: {num_edges}")
    print(f"Density: {density:.4f}")

    # Degree distribution
    degrees = degree_dist.scores()
    plt.figure(figsize=(7, 5))
    plt.hist(degrees, range=(0, 200), bins=50, edgecolor=EDGE_COLOR)
    plt.title("Degree Distribution")
    plt.xlabel("Degree")
    plt.ylabel("Frequency")
    plt.show()

    # Compute and visualize the degree centrality
    centrality = nk.centrality.DegreeCentrality(G)
    centrality.run()
    scores = centrality.scores()

    plt.figure(figsize=(7, 5))
    plt.hist(scores, range=(0, 200), bins=50, edgecolor=EDGE_COLOR)
    plt.title("Degree Centrality Distribution")
    plt.xlabel("Degree Centrality")
    plt.ylabel("Frequency")
    plt.show()

    # Compute connected components (if the graph is undirected)
    if not G.isDirected():
        cc = nk.components.ConnectedComponents(G)
    else:
        cc = nk.components.StronglyConnectedComponents(G)

    cc.run()
    component_sizes = cc.getComponentSizes()
    largest_component = max(component_sizes.values())

    print(f"Number of connected components: {len(component_sizes)}")
    print(f"Largest component size: {largest_component}")

    # Compute and visualize the betweenness centrality
    betweenness = nk.centrality.Betweenness(G)
    betweenness.run()
    betweenness_scores = betweenness.scores()

    plt.figure(figsize=(7, 5))
    plt.hist(betweenness_scores, range=(0, 200), bins=50, edgecolor=EDGE_COLOR)
    plt.title("Betweenness Centrality Distribution")
    plt.xlabel("Betweenness Centrality")
    plt.ylabel("Frequency")
    plt.show()

    # Create a directed graph using NetworkX
    G = nx.DiGraph()

    # Add edges to the graph
    for _, row in df.iterrows():
        G.add_edge(row["citing_iid"], row["cited_iid"])

    subgraph = G.subgraph(list(G.nodes)[:100])

    # Compute layout for visualization
    pos = nx.spring_layout(subgraph, k=0.1)

    # Draw the network
    plt.figure(figsize=(12, 12))
    nx.draw_networkx_nodes(G, pos, node_size=10, node_color="blue", alpha=0.6)
    nx.draw_networkx_edges(G, pos, edge_color="gray", alpha=0.6)
    plt.title("Citation Network")
    plt.show()


if __name__ == "__main__":
    main()
