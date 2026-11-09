"""
EPI 14.4 Compute the LCA in a BST

Given tree, the root of a binary search tree, and two nodes s and b of that
tree, with s.val <= b.val, return their lowest common ancestor: the
deepest node that has both s and b in its subtree. A node is in its own
subtree. Every key in the tree is distinct.

Example 1:

Input: tree = [20, 9, 25, 5, 12, None, None, None, None, 11, 14],
       s = the node 11, b = the node 14
Output: the node 12

          20
         /  \\
        9    25
       / \\
      5   12
         /  \\
        11   14

Example 2:

Input: the same tree, s = the node 5, b = the node 14
Output: the node 9

Example 3:

Input: the same tree, s = the node 9, b = the node 11
Output: the node 9
Explanation: 11 is in the subtree of 9.

Constraints:

    1 <= number of nodes <= 10^5
    s and b are nodes of the tree, and s.val <= b.val.

    REQUIRED: O(h) time for a tree of height h, O(1) extra space. NO
    recursion.
"""


class Solution:
    def find_lca(self, tree: TreeNode, s: TreeNode, b: TreeNode) -> TreeNode:
        pass


sol = Solution()

t = build_tree([20, 9, 25, 5, 12, None, None, None, None, 11, 14])
draw_tree(t)
print(sol.find_lca(t, find_node(t, 11), find_node(t, 14)).val)  # 12

# assert sol.find_lca(t, find_node(t, 11), find_node(t, 14)) is find_node(t, 12)
# assert sol.find_lca(t, find_node(t, 5), find_node(t, 14)) is find_node(t, 9)
# assert sol.find_lca(t, find_node(t, 9), find_node(t, 11)) is find_node(t, 9)
# assert sol.find_lca(t, find_node(t, 5), find_node(t, 25)) is t
# assert sol.find_lca(t, find_node(t, 14), find_node(t, 20)) is t
# assert sol.find_lca(t, find_node(t, 12), find_node(t, 12)) is find_node(t, 12)
# assert sol.find_lca(t, t, t) is t
# assert sol.find_lca(t, find_node(t, 11), find_node(t, 12)) is find_node(t, 12)
# t = build_tree([1])
# assert sol.find_lca(t, t, t) is t
# t = build_tree([2, 1, 3])
# assert sol.find_lca(t, find_node(t, 1), find_node(t, 3)) is t
# chain = build_tree([498] + [v for k in range(497, -1, -1) for v in (k, None)])
# assert sol.find_lca(chain, find_node(chain, 0), find_node(chain, 250)).val == 250
# assert sol.find_lca(chain, find_node(chain, 0), chain) is chain
# keys = [(2 * p + 1) * 2 ** (15 - d) - 1 for d in range(16) for p in range(2 ** d)]
# big = build_tree(keys)
# assert sol.find_lca(big, find_node(big, 0), find_node(big, 2 ** 16 - 2)) is big
# assert sol.find_lca(big, find_node(big, 0), find_node(big, 2)).val == 1
# assert sol.find_lca(big, find_node(big, 100), find_node(big, 101)).val == 101
