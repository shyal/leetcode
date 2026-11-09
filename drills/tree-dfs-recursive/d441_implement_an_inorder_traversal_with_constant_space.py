"""
EPI 9.10 Implement an inorder traversal with constant space

Given tree, the root of a binary tree, return the list of its node values
in inorder: the left subtree, then the node, then the right subtree. Each
node has a field parent that holds its parent node, and the parent of the
root is None. An empty tree gives an empty list.

Example 1:

Input: tree = [1, 2, 3, 4, 5, None, 6, None, None, 7, 8]
Output: [4, 2, 7, 5, 8, 1, 3, 6]

          1
         / \\
        2   3
       / \\   \\
      4   5   6
         / \\
        7   8

Example 2:

Input: tree = [1, None, 2, 3]
Output: [1, 3, 2]

Example 3:

Input: tree = []
Output: []

Constraints:

    0 <= number of nodes <= 10^5
    -10^9 <= node.val <= 10^9

    REQUIRED: O(n) time for n nodes, O(1) extra space, not counting the
    output. NO recursion. NO stack. NO changes to the tree.
"""


class Solution:
    def inorder_traversal(self, tree: TreeNode | None) -> list[int]:
        pass


sol = Solution()


def with_parents(root: TreeNode | None) -> TreeNode | None:
    nodes = [root] if root else []
    for node in nodes:
        for child in (node.left, node.right):
            if child:
                child.parent = node
                nodes.append(child)
    if root:
        root.parent = None
    return root


t = with_parents(build_tree([1, 2, 3, 4, 5, None, 6, None, None, 7, 8]))
draw_tree(t)
print(sol.inorder_traversal(t))  # [4, 2, 7, 5, 8, 1, 3, 6]

# assert sol.inorder_traversal(t) == [4, 2, 7, 5, 8, 1, 3, 6]
# assert sol.inorder_traversal(with_parents(build_tree([1, None, 2, 3]))) == [1, 3, 2]
# assert sol.inorder_traversal(with_parents(None)) == []
# assert sol.inorder_traversal(with_parents(build_tree([1]))) == [1]
# assert sol.inorder_traversal(with_parents(build_tree([1, 2]))) == [2, 1]
# assert sol.inorder_traversal(with_parents(build_tree([1, None, 2]))) == [1, 2]
# assert sol.inorder_traversal(with_parents(build_tree([1, 2, 3]))) == [2, 1, 3]
# assert sol.inorder_traversal(with_parents(build_tree([1, 2, None, None, 3, 4]))) == [2, 4, 3, 1]
# assert sol.inorder_traversal(with_parents(build_tree([5, 5, 5, 5]))) == [5, 5, 5, 5]
# assert sol.inorder_traversal(with_parents(build_tree([0, -1, 1, -2]))) == [-2, -1, 0, 1]
# left = with_parents(build_tree([4999] + [v for k in range(4998, -1, -1) for v in (k, None)]))
# assert sol.inorder_traversal(left) == list(range(5000))
# right = with_parents(build_tree([0] + [v for k in range(1, 5000) for v in (None, k)]))
# assert sol.inorder_traversal(right) == list(range(5000))
# full = with_parents(build_tree(list(range(2 ** 15 - 1))))
# assert sol.inorder_traversal(full) == get_inorder(full)
