"""
EPI 9.14 Compute the exterior of a binary tree

Given tree, the root of a binary tree, return the list of the nodes on its
exterior, each node once, in this order: the root, then the left
boundary from top to bottom, then the leaves from left to right, then the
right boundary from bottom to top. The left boundary starts at the left
child of the root and steps to the left child, or to the right child when
there is no left child, until it reaches a leaf. The leaf itself is not
part of the left boundary. The right boundary is the mirror of the left
boundary: it starts at the right child of the root and prefers the right
child. An empty tree gives an empty list.

Example 1:

Input: tree = [1, 2, 3, 4, 5, None, 6, None, None, 7, 8, 9]
Output: the nodes [1, 2, 4, 7, 8, 9, 6, 3]
Explanation: the left boundary is 2, the leaves are 4, 7, 8, 9, and the
right boundary from top to bottom is 3, 6.

            1
          /   \\
         2     3
        / \\     \\
       4   5     6
          / \\   /
         7   8 9

Example 2:

Input: tree = [1, None, 2, 3, 4]
Output: the nodes [1, 3, 4, 2]
Explanation: the root has no left child, so the left boundary is empty.

Example 3:

Input: tree = [1, 2, 3, None, 4, None, None, 5]
Output: the nodes [1, 2, 4, 5, 3]
Explanation: 2 has no left child, so the left boundary steps right to 4.
The right child 3 is a leaf, so the right boundary is empty.

Constraints:

    0 <= number of nodes <= 10^4
    Node values are distinct.

    REQUIRED: O(n) time for n nodes, O(h) extra space for a tree of
    height h, not counting the output.
"""


class Solution:
    def exterior_binary_tree(self, tree: TreeNode | None) -> list[TreeNode]:
        pass


sol = Solution()

t = build_tree([1, 2, 3, 4, 5, None, 6, None, None, 7, 8, 9])
draw_tree(t)
print([n.val for n in sol.exterior_binary_tree(t)])  # [1, 2, 4, 7, 8, 9, 6, 3]

# assert [n.val for n in sol.exterior_binary_tree(t)] == [1, 2, 4, 7, 8, 9, 6, 3]
# assert sol.exterior_binary_tree(t)[-1] is find_node(t, 3)
# assert [n.val for n in sol.exterior_binary_tree(build_tree([1, None, 2, 3, 4]))] == [1, 3, 4, 2]
# assert [n.val for n in sol.exterior_binary_tree(build_tree([1, 2, 3, None, 4, None, None, 5]))] == [1, 2, 4, 5, 3]
# assert sol.exterior_binary_tree(None) == []
# assert [n.val for n in sol.exterior_binary_tree(build_tree([1]))] == [1]
# assert [n.val for n in sol.exterior_binary_tree(build_tree([1, 2]))] == [1, 2]
# assert [n.val for n in sol.exterior_binary_tree(build_tree([1, None, 2]))] == [1, 2]
# assert [n.val for n in sol.exterior_binary_tree(build_tree([1, 2, 3]))] == [1, 2, 3]
# assert [n.val for n in sol.exterior_binary_tree(build_tree([1, 2, None, 3, None, 4]))] == [1, 2, 3, 4]
# assert [n.val for n in sol.exterior_binary_tree(build_tree([1, 2, 3, 4, 5, 6, 7, None, None, 8, 9, 10, 11]))] == [1, 2, 4, 8, 9, 10, 11, 7, 3]
# assert [n.val for n in sol.exterior_binary_tree(build_tree([1, 2, 3, 4, None, None, 5, None, 6, 7]))] == [1, 2, 4, 6, 7, 5, 3]
# chain = build_tree([498] + [v for k in range(497, -1, -1) for v in (k, None)])
# assert [n.val for n in sol.exterior_binary_tree(TreeNode(-1, chain, TreeNode(-2)))] == [-1] + list(range(498, -1, -1)) + [-2]
# full = build_tree(list(range(2 ** 12 - 1)))
# assert [n.val for n in sol.exterior_binary_tree(full)] == [0] + [2 ** d - 1 for d in range(1, 11)] + list(range(2 ** 11 - 1, 2 ** 12 - 1)) + [2 ** (d + 1) - 2 for d in range(10, 0, -1)]
