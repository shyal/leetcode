"""
URL: https://leetcode.com/problems/diameter-of-binary-tree/description/

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

    The number of nodes in the tree is in the range [1, 104].

    -100 <= Node.val <= 100

---

I think the diameter is essentially the max of the depth on the left subtree
and and the right subtree. This definition works recursively.

"""


class Solution:
    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        # not my solution
        self.diam = 0

        def dfs(node):
            if not node:
                return 0
            left = dfs(node.left)
            right = dfs(node.right)
            self.diam = max(self.diam, left + right)
            return max(left, right) + 1

        dfs(root)
        return self.diam


sol = Solution()
assert sol.diameterOfBinaryTree(build_tree([1, 2, 3, 4, 5])) == 3
assert sol.diameterOfBinaryTree(build_tree([1, 2])) == 1
assert (
    sol.diameterOfBinaryTree(
        build_tree(
            [
                7,
                6,
                9,
                4,
                None,
                8,
                10,
                1,
                5,
                None,
                None,
                None,
                None,
                None,
                2,
                None,
                None,
                None,
                3,
            ]
        )
    )
    == 7
)
assert sol.diameterOfBinaryTree(build_tree([1])) == 0
assert sol.diameterOfBinaryTree(build_tree([1, 2, 3])) == 2
assert sol.diameterOfBinaryTree(build_tree([1, 2, 3, 4])) == 3
tree = build_tree([1, 2, None, 3, 4, 5, 6, 7, 8])
res = sol.diameterOfBinaryTree(tree)
draw_tree(tree)
assert res == 4
assert sol.diameterOfBinaryTree(build_tree([1, None, 2])) == 1
