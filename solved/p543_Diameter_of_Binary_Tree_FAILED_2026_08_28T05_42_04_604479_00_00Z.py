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

Pretty sure i solved this question solo in oct 2025 yet i stubled multiple times since.

self.diam takes the max of self.diam and max_left + max_right.

And what we return is the max of what's on the left, or the right, + 1, which we can think of as routing.

yeah it makes sense in hindsight. Just hard on the spot. And to add insult to injury, this question is marked
as an easy.


The first comment in discussions is:

"Easy"

with 700+ votes.
"""


class Solution:
    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        def dfs(node):
            if not node:
                return 0
            max_left = dfs(node.left)
            max_right = dfs(node.right)
            self.diam = max(self.diam, max_left + max_right)
            _max = max(max_left, max_right) + 1
            node.val = _max
            return _max

        self.diam = 0
        dfs(root)
        return self.diam


sol = Solution()

tree = build_tree([1, 2, None, 3, 4, 5, 6, 7, 8])
res = sol.diameterOfBinaryTree(tree)
draw_tree(tree)
print(res)
assert res == 4

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
assert sol.diameterOfBinaryTree(build_tree([1, None, 2])) == 1


# FAILED: walked away after 16m 58s; no working solution.
# Judge the moves actually attempted as struggled, not clean.
