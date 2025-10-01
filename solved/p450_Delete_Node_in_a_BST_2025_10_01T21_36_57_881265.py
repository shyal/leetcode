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

import random


class Solution:

    def deleteNode(self, root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
        def find_rightmost_leaf(root):
            if root and root.right:
                return find_rightmost_leaf(root.right)
            return root

        def helper(parent, node, key):
            if node:
                if node.val == key:
                    if rightmost := find_rightmost_leaf(node.left) or node.left:
                        rightmost.right = node.right
                    if node == parent.left:
                        parent.left = node.left or node.right
                    else:
                        parent.right = node.left or node.right
                elif key < node.val:
                    helper(node, node.left, key)
                elif key > node.val:
                    helper(node, node.right, key)

        dummy = TreeNode(-1e10, right=root)
        helper(dummy, root, key)
        return dummy.right


sol = Solution()

tree = build_tree([0])
tree = sol.deleteNode(tree, 0)
assert tree == None

tree = build_tree([5, 3, 6, 2, 4, None, 7])
tree = sol.deleteNode(tree, 3)

tree = build_tree([1, None, 2])
tree = sol.deleteNode(tree, 1)


for i in range(10):
    tree = generate_and_print_random_bst(20, seed=i + 1, verbose=False)
    delete = [*range(15)]
    random.shuffle(delete)
    for d in delete:
        verbose = False
        if verbose:
            print("about to delete node", d)
        tree = sol.deleteNode(tree, d)
        if verbose:
            draw_tree(tree)
            print(tree_to_list(tree))
            print("done")
        assert is_valid_bst(tree)
