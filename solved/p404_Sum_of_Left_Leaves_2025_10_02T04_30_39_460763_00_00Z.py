"""
URL: https://leetcode.com/problems/sum-of-left-leaves/description/

404. Sum of Left Leaves

Given the root of a binary tree, return the sum of all left leaves.

A leaf is a node with no children. A left leaf is a leaf that is the left child of another node.


Example 1:

Input: root = [3,9,20,null,null,15,7]

Output: 24

Explanation: There are two left leaves in the binary tree, with values 9 and 15 respectively.

Example 2:

Input: root = [1]

Output: 0


Constraints:

    The number of nodes in the tree is in the range [1, 1000].
    -1000 <= Node.val <= 1000

"""


class Solution:
    def sumOfLeftLeaves(self, root: Optional[TreeNode]) -> int:
        def dfs(node, dir=None):
            if not node:
                return 0
            if node.left is None and node.right is None and dir is False:
                return node.val
            return dfs(node.left, False) + dfs(node.right, True)

        res = dfs(root)
        return res


sol = Solution()
tree = build_tree([3, 9, 20, None, None, 15, 7])
assert sol.sumOfLeftLeaves(tree) == 24

sol = Solution()
tree = build_tree([1])
assert sol.sumOfLeftLeaves(tree) == 0

sol = Solution()
tree = build_tree([1, 2])
assert sol.sumOfLeftLeaves(tree) == 2

sol = Solution()
tree = build_tree([1, None, 2])
assert sol.sumOfLeftLeaves(tree) == 0

sol = Solution()
tree = build_tree([1, 2, 3])
assert sol.sumOfLeftLeaves(tree) == 2

sol = Solution()
tree = build_tree([1, 2, 3, 4])
assert sol.sumOfLeftLeaves(tree) == 4

sol = Solution()
tree = build_tree([1, -2, 3])
assert sol.sumOfLeftLeaves(tree) == -2

sol = Solution()
tree = build_tree([5, 4, 3, 2])
assert sol.sumOfLeftLeaves(tree) == 2

sol = Solution()
tree = build_tree([1, 2, 3, 4, 5])
assert sol.sumOfLeftLeaves(tree) == 4

sol = Solution()
tree = build_tree([0, -1000])
assert sol.sumOfLeftLeaves(tree) == -1000

sol = Solution()
tree = build_tree([1, None, 2, None, 3])
assert sol.sumOfLeftLeaves(tree) == 0
