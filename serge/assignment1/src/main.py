import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

SEED = 51187
REDS = [
    "#F3B4B4",
    "#E23232",
    "#7F1515",
]

BLUES = [
    "#B1B9FB",
    "#4254F5",
    "#061279",
]

GREENS = [
    "#C5FCBA",
    "#5AF73B",
    "#135D04",
]


def plot_degree_bars() -> None:
    """
    Plot varying minimum degree distributions
    """
    num_nodes = 1000
    max_degree = 75

    rng = np.random.default_rng(SEED)
    num_bins = np.linspace(0, 75, 26)

    # pareto distributions with varying alphas
    mdegree_0 = rng.pareto(2, num_nodes) + 0
    mdegree_10 = rng.pareto(2, num_nodes) + 10
    mdegree_20 = rng.pareto(2, num_nodes) + 20

    mdegree_0 = min_max_normalize(mdegree_0, 0, max_degree)
    mdegree_10 = min_max_normalize(mdegree_10, 10, max_degree)
    mdegree_20 = min_max_normalize(mdegree_20, 20, max_degree)

    mdegree_0, bins = np.histogram(mdegree_0, bins=num_bins, range=(0, max_degree))
    mdegree_10, _ = np.histogram(mdegree_10, bins=num_bins, range=(0, max_degree))
    mdegree_20, _ = np.histogram(mdegree_20, bins=num_bins, range=(0, max_degree))

    fig, ax = plt.subplots(1, 3, figsize=(9, 4), sharey=True)

    # define bar width
    bar_width = bins[1] - bins[0]

    # define x positions for the bars
    bin_centers = 0.5 * (bins[1:] + bins[:-1])
    index = np.arange(len(bin_centers)) * 3

    # plotting the histograms as grouped bars
    ax[0].bar(
        index,
        width=bar_width,
        height=mdegree_0,
        label="min degree 0",
        color=GREENS[0],
        edgecolor="white",
    )
    ax[1].bar(
        index,
        width=bar_width,
        height=mdegree_10,
        label="min degree 10",
        color=GREENS[1],
        edgecolor="white",
    )
    ax[2].bar(
        index,
        width=bar_width,
        height=mdegree_20,
        label="min degree 20",
        color=GREENS[2],
        edgecolor="white",
    )

    for axis in ax:
        axis.set_xlabel("node degrees")
        axis.set_ylabel("node count")
        axis.legend()
        axis.grid(True)

    # set Y-axis formatter to use scalar values
    plt.gca().yaxis.set_major_formatter(plt.ScalarFormatter())

    fig.suptitle("Synthetic Network Degree Distribution")
    plt.tight_layout()
    plt.show()


def plot_shape_bars() -> None:
    """
    Plot varying shape distributions
    """
    num_nodes = 1000
    min_degree = 0
    max_degree = 75

    rng = np.random.default_rng(SEED)
    num_bins = np.linspace(0, 75, 26)

    # pareto distributions with varying alphas
    shape_3 = rng.pareto(2, num_nodes) * 3 + min_degree
    shape_5 = rng.pareto(2, num_nodes) * 5 + min_degree
    shape_8 = rng.pareto(2, num_nodes) * 8 + min_degree

    shape_3 = min_max_normalize(shape_3, min_degree, max_degree)
    shape_5 = min_max_normalize(shape_5, min_degree, max_degree)
    shape_8 = min_max_normalize(shape_8, min_degree, max_degree)

    shape_3, bins = np.histogram(shape_3, bins=num_bins, range=(min_degree, max_degree))
    shape_5, _ = np.histogram(shape_5, bins=num_bins, range=(min_degree, max_degree))
    shape_8, _ = np.histogram(shape_8, bins=num_bins, range=(min_degree, max_degree))

    # Creating a figure and a set of subplots
    fig, ax = plt.subplots(1, 3, figsize=(9, 4), sharey=True)

    # define bar width
    bar_width = bins[1] - bins[0]

    # define x positions for the bars
    bin_centers = 0.5 * (bins[1:] + bins[:-1])
    index = np.arange(len(bin_centers)) * 3 + min_degree

    ax[0].bar(
        index,
        width=bar_width,
        height=shape_3,
        label="mode 3",
        color=BLUES[0],
        edgecolor="white",
    )
    ax[1].bar(
        index,
        width=bar_width,
        height=shape_5,
        label="mode 5",
        color=BLUES[1],
        edgecolor="white",
    )
    ax[2].bar(
        index,
        width=bar_width,
        height=shape_8,
        label="mode 8",
        color=BLUES[2],
        edgecolor="white",
    )

    for axis in ax:
        axis.set_yscale("log", base=2)
        axis.set_xlabel("node degrees")
        axis.set_ylabel("node count")
        axis.legend()
        axis.grid(True)

    # set Y-axis formatter to use scalar values
    plt.gca().yaxis.set_major_formatter(plt.ScalarFormatter())

    fig.suptitle("Synthetic Network Degree Distribution")
    plt.tight_layout()
    plt.show()


def plot_alpha_bars() -> None:
    """
    Plot varying alpha distributions
    """
    num_nodes = 1000
    min_degree = 0
    max_degree = 75

    rng = np.random.default_rng(SEED)
    num_bins = np.linspace(0, 75, 26)

    # pareto distributions with varying alphas
    alpha_2 = rng.pareto(2, num_nodes) + min_degree
    alpha_5 = rng.pareto(5, num_nodes) + min_degree
    alpha_8 = rng.pareto(8, num_nodes) + min_degree

    alpha_2 = min_max_normalize(alpha_2, min_degree, max_degree)
    alpha_5 = min_max_normalize(alpha_5, min_degree, max_degree)
    alpha_8 = min_max_normalize(alpha_8, min_degree, max_degree)

    alpha_2, bins = np.histogram(alpha_2, bins=num_bins, range=(min_degree, max_degree))
    alpha_5, _ = np.histogram(alpha_5, bins=num_bins, range=(min_degree, max_degree))
    alpha_8, _ = np.histogram(alpha_8, bins=num_bins, range=(min_degree, max_degree))

    fig, ax = plt.subplots(1, 3, figsize=(9, 4), sharey=True)

    # define bar width
    bar_width = bins[1] - bins[0]

    # define x positions for the bars
    bin_centers = 0.5 * (bins[1:] + bins[:-1])
    index = np.arange(len(bin_centers)) * 3 + min_degree

    # Plotting the histograms as grouped bars
    ax[0].bar(
        index,
        width=bar_width,
        height=alpha_2,
        label="Alpha 2",
        color=REDS[0],
        edgecolor="white",
    )
    ax[0].set_yscale("log", base=2)
    ax[1].bar(
        index,
        width=bar_width,
        height=alpha_5,
        label="Alpha 5",
        color=REDS[1],
        edgecolor="white",
    )
    ax[1].set_yscale("log", base=5)
    ax[2].bar(
        index,
        width=bar_width,
        height=alpha_8,
        label="Alpha 8",
        color=REDS[2],
        edgecolor="white",
    )
    ax[2].set_yscale("log", base=8)

    for axis in ax:
        axis.set_xlabel("node degrees")
        axis.set_ylabel("node count")
        axis.legend()
        axis.grid(True)

    # set Y-axis formatter to use scalar values
    plt.gca().yaxis.set_major_formatter(plt.ScalarFormatter())

    fig.suptitle("Synthetic Network Degree Distribution")
    plt.tight_layout()
    plt.show()


def generate_pdf_figures() -> None:
    """
    Generates base probability density function distributions
    """
    x = np.linspace(0, 3, 50)
    pdf_shape = lambda alpha: alpha / (x + 1) ** (alpha + 1)  # noqa: E731
    pdf_scale = lambda mode: 3 * mode / (x + mode) ** 4  # noqa: E731
    pdf_degree = lambda mdegree: (3 / (x + 1) ** 4) + mdegree  # noqa: E731

    fig, axs = plt.subplots(1, 3, figsize=(9, 4))

    axs[0].set_title("shape variations (alpha)")
    axs[0].plot(x, pdf_shape(1), linewidth=2, color=REDS[0], label="alpha 1")
    axs[0].plot(x, pdf_shape(3), linewidth=2, color=REDS[1], label="alpha 3")
    axs[0].plot(x, pdf_shape(5), linewidth=2, color=REDS[2], label="alphe 5")
    # axs[0].set_yscale("log")

    axs[1].set_title("scale variations (x_m)")
    axs[1].plot(x, pdf_scale(3), linewidth=2, color=BLUES[0], label="mode 3")
    axs[1].plot(x, pdf_scale(5), linewidth=2, color=BLUES[1], label="mode 5")
    axs[1].plot(x, pdf_scale(8), linewidth=2, color=BLUES[2], label="mode 8")
    # axs[1].set_yscale("log")

    axs[2].set_title("min-degree variations")
    axs[2].plot(x, pdf_degree(1), linewidth=2, color=GREENS[0], label="min 1")
    axs[2].plot(x, pdf_degree(2), linewidth=2, color=GREENS[1], label="min 2")
    axs[2].plot(x, pdf_degree(3), linewidth=2, color=GREENS[2], label="min 3")

    for ax in axs:
        ax.set_xlim(x.min(), x.max())
        ax.grid(True)
        ax.legend()
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: "{:.2f}".format(y)))

    plt.tight_layout()
    plt.show()


def min_max_normalize(
    pareto_distribution: list[float], new_min: int, new_max: int
) -> list[int]:
    """
    Helper function that normalizes a given distribution using provided
    new minimum and maximum values

    Params:
        pareto_distribution: a type of power distribution
        new_min: desired new minimum value the distribution will have
        new_max: desired new maximum value the distribution will have

    Returns:
        A min-max normalized pareto distribution of int values
    """

    old_min = min(pareto_distribution)
    old_max = max(pareto_distribution)
    old_range = old_max - old_min
    new_range = new_max - new_min

    feature_scale = lambda i: int(new_min + (i - old_min) * new_range / old_range)  # noqa: E731

    return [feature_scale(i) for i in pareto_distribution]


def draw_graph(degree_sequence: list[int]) -> None:
    """
    Draws graph object, saves data to 'output' directory

    Params:
        degree_sequence: a list of degrees, one per node in the graph
    """
    G = nx.configuration_model(degree_sequence)
    G = nx.Graph(G)  # Converts to simple graph
    G.remove_edges_from(nx.selfloop_edges(G))

    nx.write_graphml(G, "./output/graph1.graphml")
    nx.write_edgelist(G, "./output/graph1.csv")
    write_metis(G, "./output/graph1.metis")

    # print some basic information about the graph
    print(f"Graph has {G.number_of_nodes()} nodes and {G.number_of_edges()} edges.")

    plt.figure(figsize=(8, 8))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, node_size=10, with_labels=False)
    plt.show()


def synthetic_data(alpha: float, mode: float, min_degree) -> list[int] | int:
    """
    Use to source synthetic, normalized data

    Params:
        alpha: the shape of the probability density function
        mode: the scale of the probability density function
        min_degree: a scaler to shift the probability density function up
    """
    num_nodes = 1000

    rng = np.random.default_rng()

    # it's super likely that we succeed in generating a figure
    # within 10 attempts, if this doesn't work I'd recommend
    # you try again, we use the '-1' for basic error handling

    for _ in range(10):
        data = rng.pareto(alpha, num_nodes) * mode + min_degree
        data = min_max_normalize(data, min_degree, min_degree + 100)

        # aggregate degree list must be even
        if sum(data) % 2 == 0:
            return data

    return -1


def write_metis(G: nx.Graph, path: str) -> None:
    """
    Write the NetworkX graph G to a file in METIS format

    Params:
        G: The input graph
        path: The output file path
    """
    with open(path, "w") as f:
        # Write the number of nodes and edges
        f.write(f"{G.number_of_nodes()} {G.number_of_edges()}\n")

        # Write each node's neighbors
        for node in sorted(G.nodes()):
            neighbors = " ".join(map(str, sorted(G.neighbors(node))))
            f.write(f"{neighbors}\n")


def main():
    # handle visualizations for basic shape, scale, and min degree variations
    plot_alpha_bars()
    plot_shape_bars()
    plot_degree_bars()

    # handle visualizations for probability density function
    generate_pdf_figures()

    # throw together some data
    # data = synthetic_data(alpha=3.0, mode=3.0, min=0)
    data = synthetic_data(alpha=2.0, mode=3.0, min=2)

    # basic error handling
    if data == -1:
        return

    draw_graph(data)

    # finally a default, simple random graph
    num_nodes = 1000
    num_edges = 10000

    # Generate a random graph
    G = nx.gnm_random_graph(num_nodes, num_edges, SEED)

    # Optionally, draw the graph (for a large graph like this, visualization might be cluttered)
    plt.figure(figsize=(8, 8))
    pos = nx.spring_layout(G, SEED=42)
    nx.draw(G, pos, node_size=10, with_labels=False, alpha=0.6)
    plt.show()

    # Save the graph to a METIS file
    nx.write_metis(G, "graph.metis")


if __name__ == "__main__":
    main()
