# graph_utils.py

import os
import json
import hashlib

from Types import GraphNode
from typing import List
from typing import Dict, Any, Optional, Union

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


def draw_graph(G: Dict[Any, Union[Dict[Any, Any], Any]]) -> None:
    """
    Utility function to draw a graph (stored as dict of dicts or dict with (row, col) tuples as keys) in the terminal as a colored adjacency matrix.
    Requires 'tabulate' library: pip install tabulate
    For colors, requires 'colorama': pip install colorama
    Colors edges based on values (e.g., 1 in red, 0 in blue).
    Assumes nodes are comparable for sorting.
    """

    # duck typing, auto convert edge list to graph
    if is_edge_list(G):
        G = build_graph_from_edge_list(G)

    try:
        from tabulate import tabulate
    except ImportError:
        print("Please install tabulate: pip install tabulate")
        return

    try:
        from colorama import Fore, Style
    except ImportError:
        print("Please install colorama: pip install colorama")
        return

    if not G:
        print("Empty graph")
        return

    print("\n")

    # Determine the graph format
    is_tuple_key = False
    if G:
        first_key = next(iter(G))
        if isinstance(first_key, tuple) and len(first_key) == 2:
            is_tuple_key = True

    # Get all nodes
    all_nodes = set()
    if is_tuple_key:
        for src, dst in G:
            all_nodes.add(src)
            all_nodes.add(dst)
    else:
        all_nodes.update(G.keys())
        for neighbors in G.values():
            all_nodes.update(neighbors.keys())
    nodes = sorted(all_nodes)

    # Create table data
    headers = [str(node) for node in nodes]
    table = []

    for src in nodes:
        row = []
        for dst in nodes:
            val = None
            if is_tuple_key:
                key = (src, dst)
                if key in G:
                    val = G[key]
            else:
                if src in G and dst in G[src]:
                    val = G[src][dst]

            if val is not None:
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

    # Use tabulate to print the table with headers and row labels
    print(
        tabulate(
            table,
            headers=headers,
            tablefmt="grid",
            showindex=headers,  # Use node labels for rows as well
            numalign="center",
            stralign="center",
        )
    )


def build_graph_from_edge_list(edges):
    G = defaultdict(dict)
    for u, v in edges:
        G[u][v] = 0
        G[v][u] = 0
    return G


def is_edge_list(edges):
    if type(edges) is list:
        if all(len(x) == 2 and type(x) is list for x in edges):
            return True
    return False


def draw_graphviz(
    G: Dict[Any, Dict[Any, Any]], png_filename: str = None, n=None
) -> None:

    if os.environ.get("RUNNING_TESTS") == "True":
        return

    # duck typing, auto convert edge list to graph
    if is_edge_list(G):
        G = build_graph_from_edge_list(G)

    if png_filename is None:
        # Compute deterministic hash for caching
        sorted_G = {
            str(k): {
                str(kk): vv for kk, vv in sorted(v.items(), key=lambda x: str(x[0]))
            }
            for k, v in sorted(G.items(), key=lambda x: str(x[0]))
        }
        data = {"G": sorted_G, "n": n}
        serialized = json.dumps(data, sort_keys=True)
        graph_hash = hashlib.sha256(serialized.encode()).hexdigest()[
            :16
        ]  # Shorten hash for filename
        png_filename = f"/tmp/graph_{graph_hash}.png"

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

    if n is not None:
        all_nodes.update(range(n))

    nodes = sorted(all_nodes, key=str)  # Sort for consistent order

    dot = Digraph(comment="The Graph")
    dot.attr(rankdir="TB")
    dot.attr(bgcolor="transparent")
    dot.node_attr.update(
        style="filled", fillcolor="transparent", color="white", fontcolor="white"
    )

    for node in nodes:
        dot.node(str(node))

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
        print(ascii_output)
    except Exception:
        try:
            base_name = png_filename[:-4]
            if os.path.exists(png_filename):
                pass
            else:
                dot.render(base_name, format="png", cleanup=True, view=False)
            result = os.system(f"timg {png_filename}")
            if result != 0:
                raise RuntimeError("timg failed to run (is it installed?)")
        except Exception as e:
            print(f"Failed to render/display PNG: {e}")
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


def build_graph(adj: List[List[int]]) -> Optional[GraphNode]:
    if not adj:
        return None
    n = len(adj)
    nodes = [GraphNode(i + 1) for i in range(n)]
    for i in range(n):
        for nb in adj[i]:
            nodes[i].neighbors.append(nodes[nb - 1])
    return nodes[0]


def get_adj_list(node: Optional[GraphNode]) -> List[List[int]]:
    if not node:
        return []
    node_map = {}
    queue = deque([node])
    visited = set([node])
    max_val = 0
    while queue:
        cur = queue.popleft()
        node_map[cur.val] = cur
        max_val = max(max_val, cur.val)
        for nb in cur.neighbors:
            if nb not in visited:
                visited.add(nb)
                queue.append(nb)
    adj = []
    for i in range(1, max_val + 1):
        cur = node_map.get(i)
        if cur:
            neighbors = sorted([nb.val for nb in cur.neighbors])
            adj.append(neighbors)
    return adj
