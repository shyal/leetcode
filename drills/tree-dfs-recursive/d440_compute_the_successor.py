"""
EPI 9.9 Compute the successor

Given node, a node of a binary tree, return its successor: the node that comes
right after it in an inorder traversal of the tree. Return None when the
node is the last in the inorder. Each node has a field parent that holds
its parent node, and the parent of the root is None. The root of the tree
is not given.

Example 1:

Input: tree = [1, 2, 3, 4, 5, 6, 7, None, None, 8, 9], node = the node 2
Output: the node 8
Explanation: the inorder is 4, 2, 8, 5, 9, 1, 6, 3, 7.

          1
        /   \\
       2     3
      / \\   / \\
     4   5 6   7
        / \\
       8   9

Example 2:

Input: the same tree, node = the node 9
Output: the node 1

Example 3:

Input: the same tree, node = the node 7
Output: None

Constraints:

    1 <= number of nodes <= 10^5
    node is a node of the tree.

    REQUIRED: O(h) time for a tree of height h, O(1) extra space. NO
    list of the inorder values. NO recursion.
"""


class Solution:
    def find_successor(self, node: TreeNode) -> TreeNode | None:
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
print(sol.find_successor(find_node(t, 2)).val)  # 8

# assert sol.find_successor(find_node(t, 2)) is find_node(t, 8)
# assert sol.find_successor(find_node(t, 9)) is t
# assert sol.find_successor(find_node(t, 7)) is None
# assert sol.find_successor(find_node(t, 4)) is find_node(t, 2)
# assert sol.find_successor(find_node(t, 8)) is find_node(t, 5)
# assert sol.find_successor(find_node(t, 5)) is find_node(t, 9)
# assert sol.find_successor(t) is find_node(t, 6)
# assert sol.find_successor(find_node(t, 6)) is find_node(t, 3)
# assert sol.find_successor(find_node(t, 3)) is find_node(t, 7)
# t = with_parents(build_tree([1]))
# assert sol.find_successor(t) is None
# t = with_parents(build_tree([1, 2]))
# assert sol.find_successor(find_node(t, 2)) is t
# assert sol.find_successor(t) is None
# t = with_parents(build_tree([1, None, 2, 3]))
# assert sol.find_successor(t).val == 3
# assert sol.find_successor(find_node(t, 3)).val == 2
# up = with_parents(TreeNode(500, build_tree([0] + [v for k in range(1, 500) for v in (None, k)])))
# assert sol.find_successor(find_node(up, 0)).val == 1
# assert sol.find_successor(find_node(up, 499)) is up
# assert sol.find_successor(up) is None
# left = with_parents(build_tree([498] + [v for k in range(497, -1, -1) for v in (k, None)]))
# assert sol.find_successor(find_node(left, 0)).val == 1
# assert sol.find_successor(find_node(left, 498)) is None
