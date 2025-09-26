import random
from typing import List, Optional
from collections import deque
from tree_utils import draw_tree


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def insert(root: Optional[TreeNode], val: int) -> TreeNode:
    """Insert a value into the BST and return the root."""
    if not root:
        return TreeNode(val)
    if val < root.val:
        root.left = insert(root.left, val)
    elif val > root.val:
        root.right = insert(root.right, val)
    # If val == root.val, ignore (no duplicates in this BST)
    return root


def generate_random_bst(n: int, seed: int = None) -> Optional[TreeNode]:
    """Generate a random BST with values 1..n inserted in random order."""
    if n <= 0:
        return None
    if seed:
        random.seed(seed)
    values = list(range(1, n + 1))
    random.shuffle(values)
    root = None
    for val in values:
        root = insert(root, val)
    return root


def tree_to_list(root: Optional[TreeNode]) -> List[Optional[int]]:
    """Convert BST to list using level-order traversal."""
    if not root:
        return []
    result: List[Optional[int]] = []
    queue = deque([root])
    while queue:
        node = queue.popleft()
        if node is not None:
            result.append(node.val)
            queue.append(node.left)
            queue.append(node.right)
        else:
            result.append(None)
    # Trim trailing Nones
    while result and result[-1] is None:
        result.pop()
    return result


def is_valid_bst(root: Optional[TreeNode]) -> bool:
    """Check if the tree is a valid BST using inorder traversal."""

    def inorder(node):
        if not node:
            return []
        return inorder(node.left) + [node.val] + inorder(node.right)

    vals = inorder(root)
    return all(vals[i] < vals[i + 1] for i in range(len(vals) - 1))


def generate_and_print_random_bst(n: int, seed=None, verbose=True) -> None:
    root = generate_random_bst(n, seed)
    valid = is_valid_bst(root)
    assert valid
    if verbose:
        draw_tree(root)
        lst = tree_to_list(root)
        print(lst)
        print("Valid BST:", valid)
    return root
