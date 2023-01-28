from pathlib import Path
from typing import Optional, Tuple, Union

import networkx as nx


def output_graph(
    graph: nx.DiGraph,
    file_name: Union[Path, str],
    sort: bool = True,
    file_format=None,
    dpi: Optional[int] = 800,
) -> None:
    """Output a graph to a file, either as image or as dot file.
    Args:
        graph: the DiGraph to write or plot
        file_name: the file name to write to.
        sort: create a copy of the graph with sorted keys
        file_format: graphviz output format, if None, the file_name extension is used as format
            https://graphviz.org/doc/info/output.html
        dpi: Output image resolution
    Returns:
        Nothing
    Raises:
        ValueError when the file_name does not end on .svg, .png or .dot
    """
    G = graph.copy()

    G.graph["node"] = {"shape": "box", "color": "red"}
    if dpi is not None:
        graph.graph["graph"] = {"dpi": dpi}

    if sort:
        # Create ordered graph for deterministic image outputs
        G_sorted = nx.DiGraph()
        G_sorted.graph["node"] = {"shape": "box", "color": "red"}
        G_sorted.add_nodes_from(sorted(G.nodes, key=lambda x: str(x)))

        style = nx.get_edge_attributes(G, "style")
        for edge in sorted(G.edges, key=lambda x: (str(x[0]), str(x[1]))):
            G_sorted.add_edge(*edge, style=style.get(edge))
        G = G_sorted

    p = nx.drawing.nx_pydot.to_pydot(G)
    if not isinstance(file_name, Path):
        file_name = Path(file_name)

    if file_format is None:
        file_format = file_name.suffix[1:].lower()

    try:
        p.write(file_name, format=file_format)
    except AssertionError:
        raise ValueError("Could not write file. Please make sure that the format is accepted by pydot.")


def plot_graph(
    graph: nx.DiGraph,
    dpi: int = 800,
    figsize: Optional[Tuple[int, int]] = None,
):
    """
    Args:
        graph: the DiGraph to write or plot
        dpi: dpi of the matplotlib figure.
        figsize: figure size
    Returns:
        Displays the image
    """
    import os
    import tempfile

    from matplotlib import image as mpimg
    from matplotlib import pyplot as plt

    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
        output_graph(graph, temp_file.name, dpi=dpi)
        img = mpimg.imread(temp_file.name)
        plt.figure(dpi=dpi, figsize=figsize)
        plt.axis("off")
        plt.imshow(img)
    os.unlink(temp_file.name)
