from typing import List, Optional, Dict, Any
from PrettyPrint import PrettyPrintTree
from colorama import Fore, Style
import TreeFormatter
from PrettyPrint import PrintTree
from Types import TreeNode
import sys

PrintTree.TreePrinter.TreeFormatter = TreeFormatter.TreeFormatter


class Node:
    def __init__(self, val: Any, children: Dict[Any, "Node"] = {}):
        self.val = val
        self.children = children


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

    pt = PrettyPrintTree(
        lambda x: [c for c in (x.left, x.right) if c], get_value, border=True
    )
    pt(root)


def draw_general_tree(root: Optional[Node]) -> None:
    """
    Utility function to draw a general tree (with dictionary children) in the terminal using PrettyPrintTree.
    Requires 'PrettyPrintTree' library: pip install PrettyPrintTree
    For colors, requires 'colorama': pip install colorama
    Supports node.color attribute for coloring the node value (e.g., 'blue', 'red', etc.).
    Displays edge labels based on the keys in the children dictionary.
    Uses horizontal orientation for a wider (bigger) print.
    """
    if not root:
        print("Empty tree")
        return

    print("\n")

    class _Wrapper:
        def __init__(self, node: Node, label: Any = None):
            self.node = node
            self.label = None

    def get_children(w: _Wrapper) -> List[_Wrapper]:
        return [
            _Wrapper(child, key) for key, child in sorted(w.node.children.items())
        ]  # Sorted for consistent order if keys comparable

    def get_value(w: _Wrapper) -> str:
        val_str = str(w.node.val)
        if hasattr(w.node, "color"):
            color = w.node.color.lower()
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

    def get_label(w: _Wrapper) -> Optional[str]:
        if w.label is not None:
            return str(w.label)
        return None

    pt = PrettyPrintTree(get_children, get_value, get_label=get_label, border=True)
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
    arr = list(range(1, num_nodes + 1))
    # Use the provided build_tree utility to construct the tree
    return build_tree(arr)


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
