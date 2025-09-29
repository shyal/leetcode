"""
URL: https://leetcode.com/problems/invert-binary-tree/description/?envType=problem-list-v2&envId=vn57k9wr

226. Invert Binary Tree

Given the root of a binary tree, invert the tree, and return its root.


Example 1:

Input: root = [4,2,7,1,3,6,9]
Output: [4,7,2,9,6,3,1]

Example 2:

Input: root = [2,1,3]
Output: [2,3,1]

Example 3:

Input: root = []
Output: []


Constraints:

        The number of nodes in the tree is in the range [0, 100].
        -100 <= Node.val <= 100

"""


class Solution:
    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        def dfs(node):
            if not node:
                return
            dfs(node.left)
            dfs(node.right)
            node.right, node.left = node.left, node.right

        dfs(root)
        return root


sol = Solution()
tree = build_tree([4, 2, 7, 1, 3, 6, 9])
inverted = sol.invertTree(tree)
assert inverted is tree
assert inverted.val == 4
assert inverted.left.val == 7
assert inverted.right.val == 2
assert inverted.left.left.val == 9
assert inverted.left.right.val == 6
assert inverted.right.left.val == 3
assert inverted.right.right.val == 1
assert inverted.left.left.left is None
assert inverted.left.left.right is None
assert inverted.left.right.left is None
assert inverted.left.right.right is None
assert inverted.right.left.left is None
assert inverted.right.left.right is None
assert inverted.right.right.left is None
assert inverted.right.right.right is None

tree = build_tree([2, 1, 3])
inverted = sol.invertTree(tree)
assert inverted is tree
assert inverted.val == 2
assert inverted.left.val == 3
assert inverted.right.val == 1
assert inverted.left.left is None
assert inverted.left.right is None
assert inverted.right.left is None
assert inverted.right.right is None

tree = build_tree([])
inverted = sol.invertTree(tree)
assert inverted is None
