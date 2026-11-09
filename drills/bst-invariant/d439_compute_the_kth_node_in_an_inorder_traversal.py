"""
EPI 9.8 Compute the kth node in an inorder traversal

Given tree, the root of a binary tree, and an integer k, return the node
that comes kth in an inorder traversal of the tree, counting from 1. Each
node has a field size that holds the number of nodes in its subtree,
itself included.

Example 1:

Input: tree = [1, 2, 3, 4, 5, 6, 7, None, None, 8, 9], k = 3
Output: the node 8
Explanation: the inorder is 4, 2, 8, 5, 9, 1, 6, 3, 7, and the third
node in it is 8. Node 2 has size 5 and node 5 has size 3.

          1
        /   \\
       2     3
      / \\   / \\
     4   5 6   7
        / \\
       8   9

Example 2:

Input: the same tree, k = 6
Output: the node 1

Example 3:

Input: the same tree, k = 9
Output: the node 7

Constraints:

    1 <= number of nodes <= 10^5
    1 <= k <= number of nodes
    The size field of every node is correct.

    REQUIRED: O(h) time for a tree of height h, O(1) extra space. NO
    list of the inorder values. NO recursion.
"""


class Solution:
    def find_kth_node_binary_tree(self, tree: TreeNode, k: int) -> TreeNode:
        pass


sol = Solution()


def with_sizes(root: TreeNode) -> TreeNode:
    nodes = [root]
    for node in nodes:
        nodes += [c for c in (node.left, node.right) if c]
    for node in reversed(nodes):
        node.size = 1 + sum(c.size for c in (node.left, node.right) if c)
    return root


t = with_sizes(build_tree([1, 2, 3, 4, 5, 6, 7, None, None, 8, 9]))
draw_tree(t)
print(sol.find_kth_node_binary_tree(t, 3).val)  # 8

# assert sol.find_kth_node_binary_tree(t, 3) is find_node(t, 8)
# assert sol.find_kth_node_binary_tree(t, 6) is t
# assert sol.find_kth_node_binary_tree(t, 9) is find_node(t, 7)
# assert sol.find_kth_node_binary_tree(t, 1) is find_node(t, 4)
# assert sol.find_kth_node_binary_tree(t, 2) is find_node(t, 2)
# assert sol.find_kth_node_binary_tree(t, 5) is find_node(t, 9)
# assert sol.find_kth_node_binary_tree(t, 8) is find_node(t, 3)
# t = with_sizes(build_tree([1]))
# assert sol.find_kth_node_binary_tree(t, 1) is t
# t = with_sizes(build_tree([1, 2]))
# assert sol.find_kth_node_binary_tree(t, 1).val == 2
# assert sol.find_kth_node_binary_tree(t, 2).val == 1
# t = with_sizes(build_tree([1, None, 2, 3]))
# assert sol.find_kth_node_binary_tree(t, 2).val == 3
# assert sol.find_kth_node_binary_tree(t, 3).val == 2
# right = with_sizes(build_tree([0] + [v for k in range(1, 5000) for v in (None, k)]))
# assert sol.find_kth_node_binary_tree(right, 5000).val == 4999
# assert sol.find_kth_node_binary_tree(right, 1).val == 0
# full = with_sizes(build_tree(list(range(2 ** 15 - 1))))
# order = get_inorder(full)
# assert sol.find_kth_node_binary_tree(full, 1).val == order[0]
# assert sol.find_kth_node_binary_tree(full, 12345).val == order[12344]
# assert sol.find_kth_node_binary_tree(full, 2 ** 15 - 1).val == order[-1]
