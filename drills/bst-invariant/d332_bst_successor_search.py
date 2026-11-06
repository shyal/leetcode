"""
Given the root of a binary search tree and a node inputNode of that
tree, return the inorder successor of inputNode: the node with the
smallest value greater than inputNode.val. Return None when inputNode
has the largest value in the tree. Every value in the tree is distinct.

Example 1:

Input: root = [20, 9, 25, 5, 12, None, None, None, None, 11, 14],
       inputNode = the node 9
Output: the node 11

          20
         /  \
        9    25
       / \
      5   12
         /  \
        11   14

Explanation: the values greater than 9 are 11, 12, 14, 20, 25, and 11 is
the smallest. It is in the subtree under 9, two levels down.

Example 2:

Input: the same tree, inputNode = the node 14
Output: the node 20
Explanation: 14 has no right child. The successor is above it.

Example 3:

Input: the same tree, inputNode = the node 25
Output: None

Constraints:

    1 <= number of nodes <= 10^5
    -10^9 <= node.val <= 10^9
    inputNode is a node of the tree.

    REQUIRED: O(h) time for a tree of height h, O(1) extra space. NO
    inorder traversal into a list. NO recursion.
"""


class Solution:
    def find_in_order_successor(self, root: TreeNode, inputNode: TreeNode) -> TreeNode:
        pass


sol = Solution()

t = build_tree([20, 9, 25, 5, 12, None, None, None, None, 11, 14])
draw_tree(t)
print(sol.find_in_order_successor(t, find_node(t, 9)).val)  # 11

# assert sol.find_in_order_successor(t, find_node(t, 9)).val == 11
# assert sol.find_in_order_successor(t, find_node(t, 14)).val == 20
# assert sol.find_in_order_successor(t, find_node(t, 25)) is None
# assert sol.find_in_order_successor(t, find_node(t, 5)).val == 9
# assert sol.find_in_order_successor(t, find_node(t, 11)).val == 12
# assert sol.find_in_order_successor(t, find_node(t, 12)).val == 14
# assert sol.find_in_order_successor(t, find_node(t, 20)).val == 25
# t = build_tree([8, 5, 9, 4, 7, None, 11, 1, None, None, None, None, 12, None, 3, None, None, 2])
# assert sol.find_in_order_successor(t, find_node(t, 3)).val == 4
# assert sol.find_in_order_successor(t, find_node(t, 11)).val == 12
# assert sol.find_in_order_successor(t, find_node(t, 12)) is None
# assert sol.find_in_order_successor(t, find_node(t, 1)).val == 2
# assert sol.find_in_order_successor(t, find_node(t, 2)).val == 3
# assert sol.find_in_order_successor(t, find_node(t, 7)).val == 8
# t = build_tree([10, 6, 18, 4, 8, 15, 21])
# assert sol.find_in_order_successor(t, find_node(t, 8)).val == 10
# assert sol.find_in_order_successor(t, find_node(t, 10)).val == 15
# assert sol.find_in_order_successor(t, find_node(t, 21)) is None
# assert sol.find_in_order_successor(t, find_node(t, 4)).val == 6
# t = build_tree([1])
# assert sol.find_in_order_successor(t, find_node(t, 1)) is None
# t = build_tree([2, 1])
# assert sol.find_in_order_successor(t, find_node(t, 1)).val == 2
# assert sol.find_in_order_successor(t, find_node(t, 2)) is None
# t = build_tree([1, None, 2])
# assert sol.find_in_order_successor(t, find_node(t, 1)).val == 2
# t = build_tree([500] + [v for k in range(1, 500) for v in (500 - k, None)])
# assert sol.find_in_order_successor(t, find_node(t, 1)).val == 2
