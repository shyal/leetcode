"""
URL: https://leetcode.com/problems/maximum-depth-of-binary-tree/description/?envType=problem-list-v2&envId=vn57k9wr

104. Maximum Depth of Binary Tree

Given the root of a binary tree, return its maximum depth.

A binary tree's maximum depth is the number of nodes along the longest path from the root node down to the farthest leaf node.

Example 1:

Input: root = [3,9,20,null,null,15,7]
Output: 3

Example 2:

Input: root = [1,null,2]
Output: 2

Constraints:

    The number of nodes in the tree is in the range [0, 10^4].
    -100 <= Node.val <= 100
"""


class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        def dfs(n, i):
            if not n:
                return i
            return max([dfs(n.left, i + 1), dfs(n.right, i + 1)])

        return dfs(root, 0)


sol = Solution()

tree = build_tree([3, 9, 20, None, None, 15, 7])
draw_tree(tree)

print(sol.maxDepth(tree))  # 3

assert sol.maxDepth(build_tree([3, 9, 20, None, None, 15, 7])) == 3
assert sol.maxDepth(build_tree([1, None, 2])) == 2
assert sol.maxDepth(build_tree([])) == 0
assert sol.maxDepth(build_tree([0])) == 1

assert (
    sol.maxDepth(
        build_tree(
            [
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
            ]
        )
    )
    == 6
)
assert (
    sol.maxDepth(
        build_tree([1, -1, 2, -2, -1, None, 3, None, None, -3, None, None, None, 4])
    )
    == 5
)
assert sol.maxDepth(build_tree([None])) == 0
assert sol.maxDepth(build_tree([1] * 10000)) == 14
assert sol.maxDepth(build_tree([1, None, 2, None, 3, None, 4, None, 5])) == 5
assert sol.maxDepth(build_tree([5, 5, 5, 5, None, None, 5, None, None, None, 5])) == 4
assert sol.maxDepth(build_tree([-100] * 10)) == 4
assert sol.maxDepth(build_tree([1, 2, 3, 4, None, None, 5, 6, None, None, 7])) == 4
assert (
    sol.maxDepth(
        build_tree(
            [
                1,
                None,
                2,
                None,
                3,
                None,
                4,
                None,
                5,
                None,
                6,
                None,
                7,
                None,
                8,
                None,
                9,
                None,
                10,
            ]
        )
    )
    == 10
)
assert sol.maxDepth(build_tree([1])) == 1
assert sol.maxDepth(build_tree([1, 2, None, 3, None, 4, None, 5])) == 5
assert sol.maxDepth(build_tree([1, None, 2, 3, None, 4, None, None, 5])) == 5
