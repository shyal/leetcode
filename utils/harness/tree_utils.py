# tree_utils.py

import random
from collections import deque
from typing import Any, Iterable, List, Optional

from colorama import Fore, Style
from Types import TreeNode


def _pretty_print_tree():
    """PrettyPrintTree with our TreeFormatter patched in. Imported on first
    draw: PrettyPrint pulls in cmd2 (~75ms), and every interpreter start
    pays for sitecustomize's imports."""
    import TreeFormatter
    from PrettyPrint import PrettyPrintTree, PrintTree

    PrintTree.TreePrinter.TreeFormatter = TreeFormatter.TreeFormatter
    return PrettyPrintTree


class Node:
    # children is a dict for draw_general_tree and a list for build_nary_tree
    def __init__(self, val: Any, children: Any = None):
        self.val = val
        self.children: Any = children if children is not None else {}


def find_node(root, val):
    if not root:
        return
    if root.val == val:
        return root
    return find_node(root.left, val) or find_node(root.right, val)


def build_tree(arr: List[Optional[int]]) -> Optional[TreeNode]:
    """
    Utility function to build a binary tree from a level-order list representation.
    Null/None values are skipped for node creation.
    """
    if not arr or arr[0] is None:
        # should this be [] ?
        return None

    root = TreeNode(arr[0])
    queue = [root]
    i = 1

    while queue and i < len(arr):
        current = queue.pop(0)

        # Left child
        if i < len(arr) and arr[i] is not None:
            current.left = TreeNode(arr[i])
            queue.append(current.left)
        i += 1

        # Right child
        if i < len(arr) and arr[i] is not None:
            current.right = TreeNode(arr[i])
            queue.append(current.right)
        i += 1

    return root


def draw_tree(root: Optional[TreeNode]) -> None:
    """
    Utility function to draw a binary tree in the terminal using PrettyPrintTree.
    Requires 'PrettyPrintTree' library: pip install PrettyPrintTree
    For colors, requires 'colorama': pip install colorama
    Supports node.color attribute for coloring the node value (e.g., 'blue', 'red', etc.).
    Uses horizontal orientation for a wider (bigger) print.
    """
    if not root:
        print("Empty tree")
        return

    print("\n")

    def get_value(node: TreeNode) -> str:
        val_str = str(node.val)
        if hasattr(node, "color"):
            color = node.color.lower()
            color_map = {
                "black": Fore.BLACK,
                "red": Fore.RED,
                "green": Fore.GREEN,
                "yellow": Fore.YELLOW,
                "blue": Fore.BLUE,
                "magenta": Fore.MAGENTA,
                "cyan": Fore.CYAN,
                "white": Fore.WHITE,
            }
            if color in color_map:
                val_str = color_map[color] + val_str + Style.RESET_ALL
        return val_str

    pt = _pretty_print_tree()(
        lambda x: [c for c in (x.left, x.right) if c],
        get_value,
        border=True,
        color="\x1b[30;43m",
    )
    pt(root)


def draw_general_tree(root: Optional[Node]) -> None:
    """
    Draws a general tree (each node may have multiple children).
    Each node has:
        - .label: str
        - .children: List[Node]
    """
    if not root:
        print("Empty tree")
        return

    print("\n")

    class _Wrapper:
        def __init__(self, node: Node):
            self.node = node

    def get_children(w: _Wrapper):
        children: Any = w.node.children
        if isinstance(children, dict):
            children = children.values()
        return [_Wrapper(child) for child in children]

    def get_value(w: _Wrapper):
        return str(w.node.label) if hasattr(w.node, "label") else str(w.node.val)

    pt = _pretty_print_tree()(get_children, get_value, border=True, color="\x1b[30;43m")
    pt(_Wrapper(root))


def generate_full_binary_tree(height: int) -> Optional[TreeNode]:
    """
    Generates a full (perfect) binary tree of the given height.
    Height 0 returns a single node.
    Node values are assigned sequentially from 1 in level-order.
    """
    if height < 0:
        return None

    # Calculate the total number of nodes in a perfect binary tree of height h: 2^(h+1) - 1
    num_nodes = (1 << (height + 1)) - 1
    # Create a level-order list of node values
    arr: List[Optional[int]] = list(range(1, num_nodes + 1))
    # Use the provided build_tree utility to construct the tree
    return build_tree(arr)


def generate_random_tree(
    size: int,
    seed: Optional[int] = None,
    sparsity: float = 0.0,
    skew: float = 0.0,
    values: Optional[Iterable[int]] = None,
    bst: bool = False,
) -> Optional[TreeNode]:
    """A random binary tree with `size` nodes.

    The tree grows one node at a time. Each new node fills one of the empty
    child slots of the tree so far. Which slot is chosen is controlled by:

    sparsity in [0, 1]: 0 fills the shallowest slots first, so the tree is
        as bushy as a complete tree; 1 fills the deepest slots, so the tree
        is a long chain. In between, each node picks deep with probability
        `sparsity` and shallow otherwise.
    skew in [-1, 1]: -1 always takes a left slot when one is available at
        the chosen depth, 1 always takes a right one, 0 is even.
    values: the node values, in level order; default is 1..size shuffled.
        With bst=True the values are sorted and assigned in inorder, so the
        tree is a valid BST with the same shape.
    seed: fixes the tree; the global random state is untouched.
    """
    if size <= 0:
        return None
    rng = random.Random(seed)
    vals = list(values) if values is not None else list(range(1, size + 1))
    if len(vals) != size:
        raise ValueError(f"need {size} values, got {len(vals)}")
    if values is None:
        rng.shuffle(vals)

    root = TreeNode(0)
    nodes = [root]
    # (depth, parent, side): every empty child slot in the tree so far
    slots = [(1, root, "left"), (1, root, "right")]
    for _ in range(size - 1):
        deep = rng.random() < sparsity
        depth = max(d for d, _, _ in slots) if deep else min(d for d, _, _ in slots)
        at = [s for s in slots if s[0] == depth]
        right = rng.random() < (1 + skew) / 2
        side = [s for s in at if s[2] == ("right" if right else "left")] or at
        depth, parent, name = rng.choice(side)
        slots.remove((depth, parent, name))
        child = TreeNode(0)
        setattr(parent, name, child)
        nodes.append(child)
        slots += [(depth + 1, child, "left"), (depth + 1, child, "right")]

    if bst:
        order: List[TreeNode] = []
        stack: List[TreeNode] = []
        cur: Optional[TreeNode] = root
        while stack or cur:
            while cur:
                stack.append(cur)
                cur = cur.left
            cur = stack.pop()
            order.append(cur)
            cur = cur.right
        for node, v in zip(order, sorted(vals)):
            node.val = v
    else:
        for node, v in zip(nodes, vals):
            node.val = v
    return root


def get_inorder(root: Optional[TreeNode]) -> List[int]:
    def inorder(node: Optional[TreeNode]) -> List[int]:
        if not node:
            return []
        return inorder(node.left) + [node.val] + inorder(node.right)

    return inorder(root)


def is_balanced(root: Optional[TreeNode]) -> bool:
    def check_height(node: Optional[TreeNode]) -> int:
        if not node:
            return 0
        left = check_height(node.left)
        if left == -1:
            return -1
        right = check_height(node.right)
        if right == -1:
            return -1
        if abs(left - right) > 1:
            return -1
        return max(left, right) + 1

    return check_height(root) != -1


def get_level_order(root: Optional[TreeNode]) -> List[Optional[int]]:
    if not root:
        return []
    result = []
    queue = deque([root])
    while queue:
        node = queue.popleft()
        result.append(node.val if node else None)
        if node:
            queue.append(node.left)
            queue.append(node.right)
    # Trim trailing Nones
    while result and result[-1] is None:
        result.pop()
    return result


def build_nary_tree(arr: List[Optional[int]]) -> Optional[Node]:
    if not arr or arr[0] is None:
        return None
    root = Node(arr[0], children=[])
    queue = deque([root])
    i = 2  # skip the first null at index 1
    while queue and i < len(arr):
        node = queue.popleft()
        while i < len(arr) and arr[i] is not None:
            child = Node(arr[i], children=[])
            node.children.append(child)
            queue.append(child)
            i += 1
        i += 1  # skip the null
    return root
