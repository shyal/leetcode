"""
URL: https://leetcode.com/problems/binary-tree-maximum-path-sum/description/?envType=problem-list-v2&envId=vn57k9wr

124. Binary Tree Maximum Path Sum

A path in a binary tree is a sequence of nodes where each pair of adjacent
nodes in the sequence has an edge connecting them. A node can only appear in
the sequence at most once. Note that the path does not need to pass through
the root.

The path sum of a path is the sum of the node's values in the path.

Given the root of a binary tree, return the maximum path sum of any non-empty
path.


Example 1:

Input: root = [1,2,3]
Output: 6
Explanation: The optimal path is 2 -> 1 -> 3 with a path sum of 2 + 1 + 3 = 6.

Example 2:

Input: root = [-10,9,20,null,null,15,7]
Output: 42
Explanation: The optimal path is 15 -> 20 -> 7 with a path sum of 15 + 20 + 7 = 42.


Constraints:

    The number of nodes in the tree is in the range [1, 3 * 10^4].
    -1000 <= Node.val <= 1000
"""


class Solution:
    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        def DP(n):
            if not n:
                return 0
            left_max = DP(n.left)
            right_max = DP(n.right)
            mem['max'] = max(mem['max'], left_max + right_max + n.val)
            if left_max > right_max:
                return left_max + n.val if left_max + n.val > 0 else 0
            else:
                return right_max + n.val if right_max + n.val > 0 else 0
        mem = {'max': float('-inf')}
        DP(root)
        return mem['max']


sol = Solution()

# draw_tree(build_tree([-1, -2, -3]))
# print(sol.maxPathSum(build_tree([-1, -2, -3])))  # -1

assert sol.maxPathSum(build_tree([1, 2, 3])) == 6
assert sol.maxPathSum(build_tree([-10, 9, 20, None, None, 15, 7])) == 42
assert sol.maxPathSum(build_tree([5])) == 5
assert sol.maxPathSum(build_tree([-3])) == -3
assert sol.maxPathSum(build_tree([0])) == 0
assert sol.maxPathSum(build_tree([-1000])) == -1000
assert sol.maxPathSum(build_tree([-1, -2, -3])) == -1
assert sol.maxPathSum(build_tree([-2, -1])) == -1
assert sol.maxPathSum(build_tree([2, -1])) == 2
assert sol.maxPathSum(build_tree([2, -1, -2])) == 2
assert sol.maxPathSum(build_tree([0, -1, -2])) == 0
assert sol.maxPathSum(build_tree([1, -2, 3])) == 4
assert sol.maxPathSum(build_tree([-3, 4])) == 4
assert sol.maxPathSum(build_tree([1, None, 2])) == 3
assert sol.maxPathSum(build_tree([1, 2, None, 3])) == 6
assert sol.maxPathSum(build_tree([1, 2, 3, 4, 5, 6, 7])) == 18
assert sol.maxPathSum(build_tree([5, 4, 8, 11, None, 13, 4, 7, 2, None, None, None, 1])) == 48
assert sol.maxPathSum(build_tree([1, -2, -3, 10])) == 10
assert sol.maxPathSum(build_tree([1, -10, -10, 5, 6, 5, 6])) == 6
assert sol.maxPathSum(build_tree([1000, 1000, 1000])) == 3000