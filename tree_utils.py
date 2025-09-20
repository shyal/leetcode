from typing import List, Optional
from PrettyPrint import PrettyPrintTree
from colorama import Fore, Style


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


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
