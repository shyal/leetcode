"""
URL: https://leetcode.com/problems/validate-binary-search-tree/description/

98. Validate Binary Search Tree

Given the root of a binary tree, determine if it is a valid binary search tree (BST).

A valid BST is defined as follows:

    The left subtree of a node contains only nodes with keys strictly less than the node's key.
    The right subtree of a node contains only nodes with keys strictly greater than the node's key.
    Both the left and right subtrees must also be binary search trees.


Example 1:

Input: root = [2,1,3]
Output: true

Example 2:

Input: root = [5,1,4,null,null,3,6]
Output: false
Explanation: The root node's value is 5 but its right child's value is 4.


Constraints:

    The number of nodes in the tree is in the range [1, 104].
    -231 <= Node.val <= 231 - 1
"""


class Solution:
    def isValidBST(self, root: TreeNode) -> bool:
        def dfs(node, max_bound, min_bound):
            if not node:
                return True
            node_is_valid = min_bound < node.val < max_bound
            left_is_valid = dfs(node.left, node.val, min_bound)
            right_is_valid = dfs(node.right, max_bound, node.val)
            return all([left_is_valid, right_is_valid, node_is_valid])

        return dfs(root, maxsize, -maxsize)


sol = Solution()


tree = build_tree([3, 1, 5, 0, 2, 4, 6])
valid = sol.isValidBST(tree)
# print(valid)
assert valid == True
# draw_tree(tree)

tree = build_tree([5, 4, 6, None, None, 3, 7])
# draw_tree(tree)
assert sol.isValidBST(tree) == False

tree = build_tree([2, 1, 3])
# draw_tree(tree)
assert sol.isValidBST(tree) == True

tree = build_tree([5, 1, 4, None, None, 3, 6])
# draw_tree(tree)
assert sol.isValidBST(tree) == False

tree = build_tree([])
# draw_tree(tree)
assert sol.isValidBST(tree) == True
