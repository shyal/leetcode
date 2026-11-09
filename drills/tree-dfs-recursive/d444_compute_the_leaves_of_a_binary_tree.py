"""
EPI 9.13 Compute the leaves of a binary tree

Given tree, the root of a binary tree, return the list of its leaf nodes
from left to right. A leaf is a node with no children. An empty tree
gives an empty list.

Example 1:

Input: tree = [1, 2, 3, 4, 5, None, 6, None, None, 7, 8]
Output: the nodes [4, 7, 8, 6]

          1
         / \\
        2   3
       / \\   \\
      4   5   6
         / \\
        7   8

Example 2:

Input: tree = [1, None, 2, 3]
Output: the nodes [3]

Example 3:

Input: tree = [1]
Output: the nodes [1]
Explanation: the root is a leaf when it has no children.

Constraints:

    0 <= number of nodes <= 10^4
    -10^9 <= node.val <= 10^9

    REQUIRED: O(n) time for n nodes, O(h) extra space for a tree of
    height h, not counting the output.
"""


class Solution:
    def create_list_of_leaves(self, tree: TreeNode | None) -> list[TreeNode]:
        pass


sol = Solution()

t = build_tree([1, 2, 3, 4, 5, None, 6, None, None, 7, 8])
draw_tree(t)
print([n.val for n in sol.create_list_of_leaves(t)])  # [4, 7, 8, 6]

# assert [n.val for n in sol.create_list_of_leaves(t)] == [4, 7, 8, 6]
# assert sol.create_list_of_leaves(t)[0] is find_node(t, 4)
# assert [n.val for n in sol.create_list_of_leaves(build_tree([1, None, 2, 3]))] == [3]
# assert [n.val for n in sol.create_list_of_leaves(build_tree([1]))] == [1]
# assert sol.create_list_of_leaves(None) == []
# assert [n.val for n in sol.create_list_of_leaves(build_tree([1, 2]))] == [2]
# assert [n.val for n in sol.create_list_of_leaves(build_tree([1, 2, 3]))] == [2, 3]
# assert [n.val for n in sol.create_list_of_leaves(build_tree([1, 2, 3, None, 4, 5]))] == [4, 5]
# assert [n.val for n in sol.create_list_of_leaves(build_tree([1, 1, 1, 1, 1, 1, 1]))] == [1, 1, 1, 1]
# assert [n.val for n in sol.create_list_of_leaves(build_tree([9, 8, 7, 6, None, None, 5, 4, None, None, 3]))] == [4, 3]
# chain = build_tree([498] + [v for k in range(497, -1, -1) for v in (k, None)])
# assert [n.val for n in sol.create_list_of_leaves(chain)] == [0]
# assert [n.val for n in sol.create_list_of_leaves(TreeNode(-1, chain, TreeNode(-2)))] == [0, -2]
# full = build_tree(list(range(2 ** 13 - 1)))
# assert [n.val for n in sol.create_list_of_leaves(full)] == list(range(2 ** 12 - 1, 2 ** 13 - 1))
