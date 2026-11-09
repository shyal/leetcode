"""
EPI 12.4 Compute the LCA, optimizing for close ancestors

Given two nodes node0 and node1 of the same binary tree, return their
lowest common ancestor. Each node has a parent field, and the parent of
the root is None. The lowest common ancestor is the deepest node that
has both node0 and node1 in its subtree. A node is in its own subtree.
You get the two nodes only, not the root.

Example 1:

Input: node0 = node 7, node1 = node 4, in the tree

          3
         / \\
        5   1
       / \\   \\
      6   2   8
         / \\
        7   4

Output: node 2

Example 2:

Input: node0 = node 6, node1 = node 4, in the tree of Example 1
Output: node 5

Example 3:

Input: node0 = node 5, node1 = node 4, in the tree of Example 1
Output: node 5
Explanation: node 5 is an ancestor of node 4, and a node is in its own
subtree.

Constraints:

    1 <= number of nodes <= 2 * 10^5
    Node values are distinct.
    node0 and node1 are in the same tree.

    REQUIRED: O(D0 + D1) time and space, where D0 and D1 are the numbers
    of steps from node0 and from node1 up to the answer.
"""


class Solution:
    def lca(self, node0: TreeNode, node1: TreeNode) -> TreeNode:
        pass


sol = Solution()


def with_parents(root):
    stack = [(root, None)]
    while stack:
        node, parent = stack.pop()
        if node:
            node.parent = parent
            stack += [(node.left, node), (node.right, node)]
    return root


def left_chain(leaf, n):
    t = leaf
    for k in range(1, n):
        t = TreeNode(k, t)
    return t


t = with_parents(build_tree([3, 5, 1, 6, 2, None, 8, None, None, 7, 4]))
draw_tree(t)
print(sol.lca(find_node(t, 7), find_node(t, 4)).val)  # 2

# assert sol.lca(find_node(t, 7), find_node(t, 4)) is find_node(t, 2)
# assert sol.lca(find_node(t, 6), find_node(t, 4)) is find_node(t, 5)
# assert sol.lca(find_node(t, 5), find_node(t, 4)) is find_node(t, 5)
# assert sol.lca(find_node(t, 4), find_node(t, 5)) is find_node(t, 5)
# assert sol.lca(find_node(t, 7), find_node(t, 8)) is find_node(t, 3)
# assert sol.lca(find_node(t, 8), find_node(t, 7)) is find_node(t, 3)
# assert sol.lca(find_node(t, 6), find_node(t, 1)) is find_node(t, 3)
# assert sol.lca(find_node(t, 2), find_node(t, 2)) is find_node(t, 2)
# assert sol.lca(find_node(t, 3), find_node(t, 4)) is find_node(t, 3)
# assert sol.lca(find_node(t, 1), find_node(t, 8)) is find_node(t, 1)
# single = with_parents(TreeNode(9))
# assert sol.lca(single, single) is single
# leaf = TreeNode(0)
# chain = left_chain(leaf, 2 * 10 ** 5)
# leaf.left = TreeNode(-1)
# leaf.right = TreeNode(-2)
# chain = with_parents(chain)
# assert sol.lca(leaf.left, leaf.right) is leaf
# assert sol.lca(leaf.right, leaf) is leaf
# assert sol.lca(leaf.left, chain) is chain
# assert sol.lca(chain.left, leaf.right) is chain.left
