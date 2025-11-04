"""
1448. Count Good Nodes in Binary Tree
Medium
Given a binary tree root, a node X in the tree is named good if in the path from root to X there are no nodes with a value greater than X.

Return the number of good nodes in the binary tree.

Example 1:

Input: root = [3,1,4,3,null,1,5]
Output: 4
Explanation: Nodes in blue are good.
Root Node (3) is always a good node.
Node 4 -> (3,4) is the maximum value in the path starting from the root.
Node 5 -> (3,4,5) is the maximum value in the path
Node 3 -> (3,1,3) is the maximum value in the path.
Example 2:

Input: root = [3,3,null,4,2]
Output: 3

Explanation: Node 2 -> (3, 3, 2) is not good, because "3" is higher than it.
Example 3:

Input: root = [1]
Output: 1
Explanation: Root is considered as good.
"""


class Solution:
    def goodNodes(self, root: Optional[TreeNode]) -> int:

        def helper(node, max_val):
            if not node:
                return 0
            count = 0
            if node.val >= max_val:
                node.color = "blue"
                count = 1
            _max = max(node.val, max_val)
            return count + helper(node.left, _max) + helper(node.right, _max)

        return helper(root, root.val) if root else 0


sol = Solution()

tree1 = build_tree([3, 1, 4, 3, None, 1, 5])
res = sol.goodNodes(tree1)
assert res == 4
draw_tree(tree1)

tree1 = build_tree([3, 3, None, 4, 2])
res = sol.goodNodes(tree1)
assert res == 3
draw_tree(tree1)

tree1 = build_tree([1])
res = sol.goodNodes(tree1)
assert res == 1
draw_tree(tree1)

tree1 = build_tree([3, 1, 5])
res = sol.goodNodes(tree1)
assert res == 2
draw_tree(tree1)

tree1 = build_tree([-1, 5, -2, 4, 7, 3, -8])
res = sol.goodNodes(tree1)
assert res == 4
draw_tree(tree1)

tree1 = build_tree([1, None, 2, None, 3])
res = sol.goodNodes(tree1)
assert res == 3
draw_tree(tree1)

tree1 = build_tree([4, 4, 4, 4, 4, 4, 4])
res = sol.goodNodes(tree1)
assert res == 7
draw_tree(tree1)

tree1 = build_tree([5, 4, 3])
res = sol.goodNodes(tree1)
assert res == 1
draw_tree(tree1)

tree1 = build_tree([])
res = sol.goodNodes(tree1)
assert res == 0
draw_tree(tree1)
