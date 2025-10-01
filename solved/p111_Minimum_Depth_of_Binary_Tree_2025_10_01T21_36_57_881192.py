"""
URL: https://leetcode.com/problems/minimum-depth-of-binary-tree/description/

111. Minimum Depth of Binary Tree

Given a binary tree, find its minimum depth.

The minimum depth is the number of nodes along the shortest path from the root node down to the nearest leaf node.

Note: A leaf is a node with no children.


Example 1:

Input: root = [3,9,20,null,null,15,7]
Output: 2

Example 2:

Input: root = [2,null,3,null,4,null,5,null,6]
Output: 5


Constraints:

        The number of nodes in the tree is in the range [0, 105].
        -1000 <= Node.val <= 1000
"""


class Solution:
    def minDepth(self, root: Optional[TreeNode]) -> int:
        def dfs(node, depth):
            if not node:
                return float("inf")

            is_leaf = node.left is None and node.right is None

            if is_leaf:
                return depth

            return min(dfs(node.left, depth + 1), dfs(node.right, depth + 1))

        return dfs(root, 1) if root else 0


sol = Solution()
tree = build_tree([3, 9, 20, None, None, 15, 7])
res = sol.minDepth(tree)
assert res == 2

sol = Solution()
tree = build_tree([])
res = sol.minDepth(tree)
assert res == 0

sol = Solution()
tree = build_tree([1])
res = sol.minDepth(tree)
assert res == 1
