"""
URL: https://leetcode.com/problems/deepest-leaves-sum/description/?envType=problem-list-v2&envId=vn57k9wr

1302. Deepest Leaves Sum

Given the root of a binary tree, return the sum of values of its deepest leaves.

Example 1:

Input: root = [1,2,3,4,5,null,6,7,null,null,null,null,8]
Output: 15

Example 2:

Input: root = [6,7,8,2,7,1,3,9,null,1,4,null,null,null,5]
Output: 19

Constraints:

    The number of nodes in the tree is in the range [1, 10^4].
    1 <= Node.val <= 100
"""


class Solution:
    def deepestLeavesSum(self, root: Optional[TreeNode]) -> int:
        def dfs(node, depth=0):
            if not node:
                return

            self.max_depth = max(self.max_depth, depth)

            dfs(node.left, depth + 1)
            dfs(node.right, depth + 1)

            if not node.left and not node.right:
                self.leaves[depth].append(node.val)

        self.max_depth = 0
        self.leaves = defaultdict(list)
        dfs(root)
        return sum(self.leaves[self.max_depth]) if self.leaves[self.max_depth] else 0


sol = Solution()

# print(
#     sol.deepestLeavesSum(
#         build_tree([1, 2, 3, 4, 5, None, 6, 7, None, None, None, None, 8])
#     )
# )  # 15

assert (
    sol.deepestLeavesSum(
        build_tree([1, 2, 3, 4, 5, None, 6, 7, None, None, None, None, 8])
    )
    == 15
)
assert (
    sol.deepestLeavesSum(
        build_tree([6, 7, 8, 2, 7, 1, 3, 9, None, 1, 4, None, None, None, 5])
    )
    == 19
)
assert sol.deepestLeavesSum(build_tree([1])) == 1
assert sol.deepestLeavesSum(build_tree([1, 2, 3])) == 5
assert sol.deepestLeavesSum(build_tree([1, 2, None, 3])) == 3
assert sol.deepestLeavesSum(build_tree([1, None, 2, None, 3])) == 3
assert sol.deepestLeavesSum(build_tree([1, 2, 3, 4, None, None, 5])) == 9
assert sol.deepestLeavesSum(build_tree([100])) == 100
assert sol.deepestLeavesSum(None) == 0
