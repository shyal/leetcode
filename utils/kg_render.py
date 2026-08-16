# kg_render — shared graphviz styling + terminal display for the graph tools.
#
# kg_viz draws the whole taxonomy; kg_next draws one problem's input tree.
# Both get their look and their inline-terminal rendering from here.

import base64
import os
import random
import shutil
import struct
import subprocess
import sys
import graphviz

from kg_lib import GRAPH_DIR, SOLID, STALE, FRAGILE, MISSING

FILL = {SOLID: "#238636", STALE: "#bb8009", FRAGILE: "#da3633", MISSING: "#6e7681"}

# Random face per node, drawn from the status's vibe — never the move name.
STATUS_FACE = {
    SOLID:   ["😄", "💪", "😎", "✨", "💎", "🟢"],
    STALE:   ["😐", "🫤", "😑", "😴", "🥀", "⌛"],
    FRAGILE: ["😰", "🫠", "🥲", "😬", "💔", "😵"],
    MISSING: ["👻", "❔", "😶", "🫥", "🕳️"],
}


def make_digraph(name, title=None):
    graph_attr = {
        "rankdir": "TB",
        "bgcolor": "#0d1117",
        "fontname": "Helvetica",
        "compound": "true",
        "ranksep": "0.6",
        "nodesep": "0.25",
    }
    if title:
        graph_attr.update({"label": title, "labelloc": "t", "fontcolor": "#c9d1d9", "fontsize": "16"})
    return graphviz.Digraph(
        name,
        graph_attr=graph_attr,
        node_attr={
            "shape": "box",
            "style": "rounded,filled",
            "fontname": "Helvetica",
            "fontsize": "11",
            "fontcolor": "white",
            "color": "#30363d",
            "margin": "0.12,0.06",
        },
        edge_attr={"color": "#8b949e", "arrowsize": "0.6"},
    )


def status_node(g, node_id, node, status, when, highlight=False, labeled=True):
    tooltip = f"{node['name']} — {status}" + (f" ({when})" if when else "")
    attrs = {"fillcolor": FILL[status], "tooltip": tooltip}
    if highlight:
        attrs.update({"color": "#c9d1d9", "penwidth": "2"})
    if labeled:
        g.node(node_id, label=node_id.replace("-", "-\n", 1), **attrs)
        return
    face = random.choice(STATUS_FACE[status])
    g.node(node_id, label=f"{status} {face}", **attrs)


def add_legend(dot):
    with dot.subgraph(name="cluster_legend") as c:
        c.attr(label="legend", fontcolor="#8b949e", color="#30363d", style="rounded")
        for status in (SOLID, STALE, FRAGILE, MISSING):
            c.node(f"legend_{status}", label=status.lower(), fillcolor=FILL[status])


def _png_width(path):
    with open(path, "rb") as f:
        f.seek(16)  # IHDR width field
        return struct.unpack(">I", f.read(4))[0]


def render(dot, basename, min_width_px=2000):
    """Render svg + png into graph/, return the graph's logical width in px.

    The PNG carries at least min_width_px of pixels (re-rendered at higher
    DPI if needed) so it stays crisp on retina, but the LOGICAL width — the
    96-DPI layout size — is what the terminal should display it at.
    """
    for fmt in ("svg", "png"):
        dot.render(filename=basename, directory=GRAPH_DIR, format=fmt, cleanup=True)
    png = os.path.join(GRAPH_DIR, f"{basename}.png")
    logical_width = _png_width(png)
    if logical_width < min_width_px:
        dot.graph_attr["dpi"] = str(int(96 * min_width_px / logical_width) + 1)
        dot.render(filename=basename, directory=GRAPH_DIR, format="png", cleanup=True)
    return logical_width


def animate(text, effect=("decrypt", "--typing-speed", "20")):
    """Play text through a ttfx effect on a tty; plain write otherwise.

    Runs ttfx against the real terminal so it can't swallow anything written
    around it (the inline-image escape in particular).
    """
    exe = shutil.which("ttfx")
    if not exe or not sys.stdout.isatty():
        sys.stdout.write(text)
        sys.stdout.flush()
        return
    subprocess.run(
        [exe, "--frame-rate", "360", "--existing-color-handling", "always", *effect],
        input=text.encode(), check=False)


def show_inline(png_path, display_width_px=None):
    """Draw the PNG in-place via the iTerm2 inline-image protocol (OSC 1337).

    display_width_px is the graph's logical size — iTerm shows it at that
    size (scaling the hi-DPI pixels down, never up) and caps at pane width.
    """
    if not sys.stdout.isatty() or os.environ.get("LC_TERMINAL", os.environ.get("TERM_PROGRAM", "")) not in ("iTerm2", "iTerm.app"):
        return False
    width = f"{display_width_px}px" if display_width_px else "auto"
    payload = base64.b64encode(open(png_path, "rb").read()).decode()
    name = base64.b64encode(os.path.basename(png_path).encode()).decode()
    sys.stdout.write(f"\033]1337;File=name={name};size={len(payload)};inline=1;width={width};preserveAspectRatio=1:{payload}\a\n")
    sys.stdout.flush()
    return True


def display(basename, display_width_px=None):
    """Inline in the terminal when possible; open the SVG on a non-iTerm tty; do nothing when piped."""
    if show_inline(os.path.join(GRAPH_DIR, f"{basename}.png"), display_width_px):
        return
    if sys.stdout.isatty():
        subprocess.run(["open", os.path.join(GRAPH_DIR, f"{basename}.svg")], check=False)
