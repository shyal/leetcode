"""
URL: https://leetcode.com/problems/path-sum/description/

112. Path Sum

Given the root of a binary tree and an integer targetSum, return true if the tree has a root-to-leaf path such that adding up all the values along the path equals targetSum.

A leaf is a node with no children.


Example 1:

Input: root = [5,4,8,11,None,13,4,7,2,None,None,None,1], targetSum = 22
Output: true
Explanation: The root-to-leaf path with the target sum is shown.

Example 2:

Input: root = [1,2,3], targetSum = 5
Output: false
Explanation: There are two root-to-leaf paths in the tree:
(1 --> 2): The sum is 3.
(1 --> 3): The sum is 4.
There is no root-to-leaf path with sum = 5.

Example 3:

Input: root = [], targetSum = 0
Output: false
Explanation: Since the tree is empty, there are no root-to-leaf paths.


Constraints:

        The number of nodes in the tree is in the range [0, 5000].
        -1000 <= Node.val <= 1000
        -1000 <= targetSum <= 1000
"""


class Solution:
    def hasPathSum(self, root: Optional[TreeNode], targetSum: int) -> bool:
        def dfs(prefix, node):
            if not node:
                return False
            is_leaf = node.left is None and node.right is None
            return (
                prefix + node.val == targetSum
                if is_leaf
                else dfs(prefix + node.val, node.left)
                or dfs(prefix + node.val, node.right)
            )

        return dfs(0, root)


sol = Solution()

tree = build_tree([5, 4, 8, 11, None, 13, 4, 7, 2, None, None, None, 1])
# print(tree)
res = sol.hasPathSum(tree, 22)
assert res == True

tree = build_tree([1, 2, 3])
# print(tree)
res = sol.hasPathSum(tree, 5)
assert res == False

tree = build_tree([1, 2, 3])
# print(tree)
res = sol.hasPathSum(tree, 4)
assert res == True

tree = build_tree([1])
# print(tree)
res = sol.hasPathSum(tree, 1)
assert res == True

tree = build_tree([])
# print(tree)
res = sol.hasPathSum(tree, 0)
assert res == False
