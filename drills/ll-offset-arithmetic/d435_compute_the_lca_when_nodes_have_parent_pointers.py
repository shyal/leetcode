"""
EPI 9.4 Compute the LCA when nodes have parent pointers

Given two nodes node0 and node1 of a binary tree, return their lowest
common ancestor: the deepest node that has both node0 and node1 in its
subtree. A node is in its own subtree. Each node has a field parent that
holds its parent node, and the parent of the root is None. The root of
the tree is not given.

Example 1:

Input: tree = [1, 2, 3, 4, 5, 6, 7, None, None, 8, 9],
       node0 = the node 8, node1 = the node 4
Output: the node 2
Explanation: 8 and 4 are both under 2, and they are under different
children of 2.

          1
        /   \\
       2     3
      / \\   / \\
     4   5 6   7
        / \\
       8   9

Example 2:

Input: the same tree, node0 = the node 5, node1 = the node 9
Output: the node 5
Explanation: 9 is in the subtree of 5.

Example 3:

Input: the same tree, node0 = the node 9, node1 = the node 7
Output: the node 1

Constraints:

    1 <= number of nodes <= 10^5
    node0 and node1 are nodes of the same tree.

    REQUIRED: O(h) time for a tree of height h, O(1) extra space. NO set
    or dict of nodes. NO recursion.
"""


class Solution:
    def lca(self, node0: TreeNode, node1: TreeNode) -> TreeNode:
        pass


sol = Solution()


def with_parents(root: TreeNode) -> TreeNode:
    root.parent = None
    nodes = [root]
    for node in nodes:
        for child in (node.left, node.right):
            if child:
                child.parent = node
                nodes.append(child)
    return root


t = with_parents(build_tree([1, 2, 3, 4, 5, 6, 7, None, None, 8, 9]))
draw_tree(t)
print(sol.lca(find_node(t, 8), find_node(t, 4)).val)  # 2

# assert sol.lca(find_node(t, 8), find_node(t, 4)) is find_node(t, 2)
# assert sol.lca(find_node(t, 5), find_node(t, 9)) is find_node(t, 5)
# assert sol.lca(find_node(t, 9), find_node(t, 5)) is find_node(t, 5)
# assert sol.lca(find_node(t, 9), find_node(t, 7)) is t
# assert sol.lca(find_node(t, 8), find_node(t, 9)) is find_node(t, 5)
# assert sol.lca(find_node(t, 6), find_node(t, 7)) is find_node(t, 3)
# assert sol.lca(find_node(t, 1), find_node(t, 8)) is t
# assert sol.lca(find_node(t, 4), find_node(t, 4)) is find_node(t, 4)
# assert sol.lca(find_node(t, 3), find_node(t, 8)) is t
# t = with_parents(build_tree([1]))
# assert sol.lca(t, t) is t
# t = with_parents(build_tree([1, 2]))
# assert sol.lca(find_node(t, 2), t) is t
# t = with_parents(build_tree([1, None, 2, None, 3, 4]))
# assert sol.lca(find_node(t, 4), find_node(t, 3)) is find_node(t, 3)
# chain = with_parents(build_tree([498] + [v for k in range(497, -1, -1) for v in (k, None)]))
# assert sol.lca(find_node(chain, 0), find_node(chain, 250)).val == 250
# assert sol.lca(find_node(chain, 498), find_node(chain, 0)) is chain
# full = with_parents(build_tree(list(range(2 ** 13 - 1))))
# assert sol.lca(find_node(full, 2 ** 12 - 1), find_node(full, 2 ** 13 - 2)) is full
# assert sol.lca(find_node(full, 2 ** 12 - 1), find_node(full, 2)).val == 0
# assert sol.lca(find_node(full, 2 ** 12 - 1), find_node(full, 2 ** 12)).val == 2 ** 11 - 1
