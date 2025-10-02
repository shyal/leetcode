"""
URL: https://leetcode.com/problems/sum-root-to-leaf-numbers/description/

129. Sum Root to Leaf Numbers

You are given the root of a binary tree containing digits from 0 to 9 only.

Each root-to-leaf path in the tree represents a number.

    For example, the root-to-leaf path 1 -> 2 -> 3 represents the number 123.

Return the total sum of all root-to-leaf numbers. Test cases are generated so that the answer will fit in a 32-bit integer.

A leaf node is a node with no children.


Example 1:

Input: root = [1,2,3]
Output: 25
Explanation:
The root-to-leaf path 1->2 represents the number 12.
The root-to-leaf path 1->3 represents the number 13.
Therefore, sum = 12 + 13 = 25.

Example 2:

Input: root = [4,9,0,5,1]
Output: 1026
Explanation:
The root-to-leaf path 4->9->5 represents the number 495.
The root-to-leaf path 4->9->1 represents the number 491.
The root-to-leaf path 4->0 represents the number 40.
Therefore, sum = 495 + 491 + 40 = 1026.


Constraints:

    The number of nodes in the tree is in the range [1, 1000].
    0 <= Node.val <= 9
    The depth of the tree will not exceed 10.
"""


class Solution:
    def sumNumbers(self, root: Optional[TreeNode]) -> int:
        def dfs(node, val=0):
            if not node:
                return 0
            left = dfs(node.left, val * 10 + node.val)
            right = dfs(node.right, val * 10 + node.val)
            if node.left is None and node.right is None:
                return val * 10 + node.val
            return left + right

        res = dfs(root)
        return res


sol = Solution()
tree = build_tree([1, 2, 3])
assert sol.sumNumbers(tree) == 25
tree = build_tree([4, 9, 0, 5, 1])
assert sol.sumNumbers(tree) == 1026
tree = build_tree([1])
assert sol.sumNumbers(tree) == 1
tree = build_tree([0])
assert sol.sumNumbers(tree) == 0
tree = build_tree([1, 2])
draw_tree(tree)
assert sol.sumNumbers(tree) == 12
tree = build_tree([1, 0])
assert sol.sumNumbers(tree) == 10
tree = build_tree([1, None, 2])
assert sol.sumNumbers(tree) == 12
tree = build_tree([1, 2, 3, 4])
assert sol.sumNumbers(tree) == 137
tree = build_tree([0, 0, 0])
assert sol.sumNumbers(tree) == 0
tree = build_tree([1, 2, None, 3])
assert sol.sumNumbers(tree) == 123
tree = build_tree([1, None, 2, None, 3])
assert sol.sumNumbers(tree) == 123
