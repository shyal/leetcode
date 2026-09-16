"""
URL: https://leetcode.com/problems/diameter-of-binary-tree/description/?envType=problem-list-v2&envId=vn57k9wr

543. Diameter of Binary Tree

Given the root of a binary tree, return the length of the diameter of the tree.

The diameter of a binary tree is the length of the longest path between any two nodes in a tree. This path may or may not pass through the root.

The length of a path between two nodes is represented by the number of edges between them.

Example 1:

Input: root = [1,2,3,4,5]
Output: 3
Explanation: 3 is the length of the path [4,2,1,3] or [5,2,1,3].

Example 2:

Input: root = [1,2]
Output: 1

Constraints:

    The number of nodes in the tree is in the range [1, 10^4].
    -100 <= Node.val <= 100

---


Again i forgot that:

self.best = max(self.best, max_left + max_right)

hinted.

LEETCODE: Accepted (7 ms, 22.3 MB)
"""


class Solution:
    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        def helper(n):
            if not n:
                return 0
            is_leaf = n.left == n.right == None
            if is_leaf:
                n.val = 1
                return 1

            max_left, max_right = 0, 0

            if n.left:
                max_left = helper(n.left)
            if n.right:
                max_right = helper(n.right)

            diam = max(max_left, max_right) + 1

            n.val = diam

            self.best = max(self.best, max_left + max_right)

            return diam

        self.best = 0
        helper(root)
        return self.best


sol = Solution()

root = build_tree([1, 2, 3, 4, 5, 6, 7, 8])

print(sol.diameterOfBinaryTree(root))  # 3
print(root)

assert sol.diameterOfBinaryTree(build_tree([1, 2, 3, 4, 5])) == 3
assert sol.diameterOfBinaryTree(build_tree([1, 2])) == 1

assert sol.diameterOfBinaryTree(build_tree([1])) == 0
assert sol.diameterOfBinaryTree(build_tree([1, -2, -3, -4, -5])) == 3
assert sol.diameterOfBinaryTree(build_tree([1, 1, 1, 1, 1, 1, 1])) == 4
assert (
    sol.diameterOfBinaryTree(build_tree([1, None, 2, None, 3, None, 4, None, 5])) == 4
)
assert sol.diameterOfBinaryTree(build_tree([1, 2, None, 3, None, 4, None, 5])) == 4
assert sol.diameterOfBinaryTree(build_tree([i for i in range(1, 10001)])) == 25
assert sol.diameterOfBinaryTree(build_tree([0] * 10000)) == 25
assert sol.diameterOfBinaryTree(build_tree([100] * 5000 + [-100] * 5000)) == 25
assert sol.diameterOfBinaryTree(build_tree([1, None, 2, 3, None, 4, None, 5])) == 4
assert (
    sol.diameterOfBinaryTree(build_tree([1, 2, 3, None, 4, None, 5, None, None, 6]))
    == 5
)
assert (
    sol.diameterOfBinaryTree(
        build_tree([1, None, 2, None, 3, None, 4, None, 5, None, 6])
    )
    == 5
)
assert sol.diameterOfBinaryTree(build_tree([1, -1, 2, -2, 3, -3, 4, -4, 5, -5])) == 5
