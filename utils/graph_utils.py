from typing import Dict, Any
from collections import defaultdict
from colorama import Fore, Style

try:
    from tabulate import tabulate
except ImportError:
    pass  # Will handle in function

try:
    from graphviz import Digraph
except ImportError:
    pass  # Will handle in function

try:
    import networkx as nx
    from phart import ASCIIRenderer

    PHART_AVAILABLE = True
except ImportError:
    PHART_AVAILABLE = False


def draw_graph(G: Dict[Any, Dict[Any, Any]]) -> None:
    """
    Utility function to draw a graph (stored as dict of dicts) in the terminal as a colored adjacency matrix.
    Requires 'tabulate' library: pip install tabulate
    For colors, requires 'colorama': pip install colorama
    Colors edges based on values (e.g., 1 in red, 0 in blue).
    Assumes nodes are comparable for sorting.
    """
    try:
        from tabulate import tabulate
    except ImportError:
        print("Please install tabulate: pip install tabulate")
        return

    if not G:
        print("Empty graph")
        return

    print("\n")

    # Get all nodes
    all_nodes = set(G.keys())
    for neighbors in G.values():
        all_nodes.update(neighbors.keys())
    nodes = sorted(all_nodes)

    # Create table data
    headers = [str(node) for node in nodes]
    table = []

    for src in nodes:
        row = []
        for dst in nodes:
            if src in G and dst in G[src]:
                val = G[src][dst]
                val_str = str(val)
                # Example coloring based on value
                if val == 1:
                    val_str = Fore.RED + val_str + Style.RESET_ALL
                elif val == 0:
                    val_str = Fore.BLUE + val_str + Style.RESET_ALL
                # Add more colors as needed
                row.append(val_str)
            else:
                row.append("")
        table.append(row)

    # Use tabulate to print the table with headers
    print(
        tabulate(
            table,
            headers=headers,
            tablefmt="grid",
            showindex=range(len(nodes)),
            numalign="center",
            stralign="center",
        )
    )


def draw_graphviz(G: Dict[Any, Dict[Any, Any]]) -> None:
    """
    Utility function to draw a graph (stored as dict of dicts) using Graphviz.
    Outputs ASCII art if supported, otherwise saves a PNG file.
    Requires 'graphviz' library: pip install graphviz
    And the Graphviz executable installed on the system.
    For ASCII output, Graphviz must be built with AAlib support (not always default).
    """
    try:
        from graphviz import Digraph
    except ImportError:
        print("Please install graphviz: pip install graphviz")
        return

    if not G:
        print("Empty graph")
        return

    print("\n")

    # Collect all nodes
    all_nodes = set(G.keys())
    for neighbors in G.values():
        all_nodes.update(neighbors.keys())
    nodes = sorted(all_nodes, key=str)  # Sort for consistent order

    # Create directed graph (since dict of dicts implies direction)
    dot = Digraph(comment="The Graph")
    dot.attr(rankdir="LR")  # Horizontal layout for wider terminal view

    # Add nodes
    for node in nodes:
        dot.node(str(node))

    # Add edges
    for src in G:
        for dst, weight in G[src].items():
            label = str(weight) if weight not in (0, 1) else None
            edge_attr = (
                {"color": "red" if weight == 1 else "blue"} if weight in (0, 1) else {}
            )
            if label:
                edge_attr["label"] = label
            dot.edge(str(src), str(dst), **edge_attr)

    try:
        # Try to get ASCII output
        ascii_output = dot.pipe(format="ascii", encoding="utf-8")
        print(ascii_output.decode("utf-8"))
    except Exception:
        print(
            "ASCII output not supported (requires Graphviz with AAlib). Saving PNG instead."
        )
        try:
            dot.render("graph", format="png", cleanup=True, view=False)
            print("Graph visualization saved as 'graph.png'")
        except Exception as e:
            print(f"Failed to render PNG: {e}")
            # Fallback: print DOT source
            print("\nDOT source:\n")
            print(dot.source)


def draw_ascii_graph(G: Dict[Any, Dict[Any, Any]]) -> None:
    """
    Utility function to draw a graph (stored as dict of dicts) in the terminal using PHART for ASCII rendering.
    Requires 'networkx' and 'phart' libraries: pip install networkx phart
    Supports directed graphs. Edge weights (like 0/1) are ignored in rendering but structure is shown.
    """
    global PHART_AVAILABLE
    if not PHART_AVAILABLE:
        print("Please install networkx and phart: pip install networkx phart")
        return

    if not G:
        print("Empty graph")
        return

    print("\n")

    # Create NetworkX DiGraph from the dict of dicts
    nx_graph = nx.DiGraph()
    all_nodes = set(G.keys())
    for neighbors in G.values():
        all_nodes.update(neighbors.keys())
    nx_graph.add_nodes_from(all_nodes)

    # Add edges, ignoring weights for now (PHART doesn't support labels)
    for src in G:
        for dst in G[src]:
            nx_graph.add_edge(src, dst)

    # Render with PHART
    try:
        renderer = ASCIIRenderer(nx_graph)
        print(renderer.render())
    except Exception as e:
        print(f"Failed to render with PHART: {e}")
        # Fallback to adjacency list
        print("Fallback: Adjacency list")
        for src in sorted(G):
            neighbors = [f"{dst}({G[src][dst]})" for dst in sorted(G[src])]
            print(f"{src}: {', '.join(neighbors)}")
