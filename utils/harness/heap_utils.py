# heap_utils.py

from typing import List
from tree_utils import build_tree, draw_tree


def draw_heap(heap_list: List[int]) -> None:
    """
    Utility function to draw a heap represented as a list in the terminal.
    The heap list is assumed to be in level-order (array representation of a complete binary tree).
    Leverages build_tree and draw_tree from tree_utils.py.
    """
    if not heap_list:
        print("Empty heap")
        return

    # Build the binary tree from the heap list (no Nones expected)
    root = build_tree(
        [val for val in heap_list]
    )  # Convert to List[Optional[int]] implicitly
    draw_tree(root)
