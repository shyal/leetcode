"""
URL: https://leetcode.com/problems/delete-node-in-a-bst/description/?envType=study-plan-v2&envId=leetcode-75

450. Delete Node in a BST

Given a root node reference of a BST and a key, delete the node with the given key in the BST. Return the root node reference (possibly updated) of the BST.

Basically, the deletion can be divided into two stages:

        Search for a node to remove.
        If the node is found, delete the node.


Example 1:

Input: root = [5,3,6,2,4,null,7], key = 3
Output: [5,4,6,2,null,null,7]
Explanation: Given key to delete is 3. So we find the node with value 3 and delete it.
One valid answer is [5,4,6,2,null,null,7], shown in the above BST.
Please notice that another valid answer is [5,2,6,null,4,null,7] and it's also accepted.

Example 2:

Input: root = [5,3,6,2,4,null,7], key = 0
Output: [5,3,6,2,4,null,7]
Explanation: The tree does not contain a node with value = 0.

Example 3:

Input: root = [], key = 0
Output: []


Constraints:

        The number of nodes in the tree is in the range [0, 104].
        -105 <= Node.val <= 105
        Each node has a unique value.
        root is a valid binary search tree.
        -105 <= key <= 105


Follow up: Could you solve it with time complexity O(height of tree)?
"""

from bst_utils import generate_and_print_random_bst
from tree_utils import build_tree, draw_tree, TreeNode
from typing import Optional, List


class Solution:

    def deleteNode(self, root: Optional[TreeNode], key: int) -> Optional[TreeNode]:

        def find_leftmost_leaf(root):
            if not root:
                return
            if root.left:
                return find_leftmost_leaf(root.left)
            elif root.right:
                return find_leftmost_leaf(root.right)
            return root

        def helper(parent, root, key):
            if not root:
                return
            if root.val == key:
                print("FOUND", key)
                left_most = find_leftmost_leaf(root.right)
                if parent.val > root.val:
                    parent.left = root.right
                left_most.left = root.left
                return
            if key < root.val and root.left:
                helper(root, root.left, key)
            elif key > root.val and root.right:
                helper(root, root.right, key)

        helper(None, root, key)
        return root


sol = Solution()
tree = build_tree(
    [
        22,
        12,
        30,
        6,
        18,
        27,
        None,
        2,
        7,
        13,
        19,
        26,
        29,
        1,
        3,
        None,
        10,
        None,
        17,
        None,
        20,
        25,
        None,
        28,
        None,
        None,
        None,
        None,
        5,
        8,
        11,
        15,
        None,
        None,
        21,
        24,
        None,
        None,
        None,
        4,
        None,
        None,
        9,
        None,
        None,
        14,
        16,
        None,
        None,
        23,
    ]
)
draw_tree(tree)
res = sol.deleteNode(tree, 12)
draw_tree(tree)
sol.deleteNode(tree, 15)
draw_tree(tree)
sol.deleteNode(tree, 6)
draw_tree(tree)

# generate_and_print_random_bst(30)
