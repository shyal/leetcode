"""
URL: https://leetcode.com/problems/count-complete-tree-nodes/description/?envType=problem-list-v2&envId=vn57k9wr

222. Count Complete Tree Nodes

Given the root of a complete binary tree, return the number of the nodes in the tree.

According to Wikipedia, every level, except possibly the last, is completely filled in a complete binary tree, and all nodes in the last level are as far left as possible. It can have between 1 and 2h nodes inclusive at the last level h.

Design an algorithm that runs in less than O(n) time complexity.


Example 1:

Input: root = [1,2,3,4,5,6]

Output: 6

Example 2:

Input: root = []

Output: 0

Example 3:

Input: root = [1]

Output: 1


Constraints:

        The number of nodes in the tree is in the range [0, 5 * 104].
        0 <= Node.val <= 5 * 104
        The tree is guaranteed to be complete.
"""


class Solution:
    def countNodes(self, root: Optional[TreeNode]) -> int:
        def dfs(node, height=0, direction=None):
            if not node:
                if direction is None:
                    return 0
                return height - 1
            if direction is None:
                left_height = dfs(node.left, height + 1, 0)
                right_height = dfs(node.right, height + 1, 1)
                if left_height == right_height:
                    return 2 ** (left_height + 1) - 1
                else:
                    left_count = dfs(node.left, 0, None)
                    right_count = dfs(node.right, 0, None)
                    node.val = left_count + right_count + 1
                    return left_count + right_count + 1
            elif direction == 0:
                return dfs(node.left, height + 1, direction)
            elif direction == 1:
                return dfs(node.right, height + 1, direction)

        res = dfs(root) if root else 0
        return res


sol = Solution()
tree = build_tree([1, 2, 3, 4, 5, 6])
assert sol.countNodes(tree) == 6

sol = Solution()
tree = build_tree([])
assert sol.countNodes(tree) == 0

sol = Solution()
tree = build_tree([1])
assert sol.countNodes(tree) == 1

sol = Solution()
tree = build_tree([0, 0, 0, 0, 0])
sol.countNodes(tree)
assert sol.countNodes(tree) == 5
