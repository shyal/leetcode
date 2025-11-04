"""
URL: https://leetcode.com/problems/insert-into-a-binary-search-tree/description/

701. Insert into a Binary Search Tree

Given the root of a binary search tree (BST) and a value to insert into the BST, insert the value into the BST. Return the root of the BST after the insertion. It is guaranteed that the new value does not exist in the original BST.

A BST is defined as follows:

- The left subtree of a node contains only nodes with keys less than the node's key.
- The right subtree of a node contains only nodes with keys greater than the node's key.
- Both the left and right subtrees must also be binary search trees.

There may exist multiple valid ways for the insertion, as long as the tree remains a BST after insertion. You can return any of them.

Example 1:

Input: root = [4,2,7,1,3], val = 5
Output: [4,2,7,1,3,5]

Example 2:

Input: root = [40,20,60,10,30,50,70], val = 25
Output: [40,20,60,10,30,50,70,None,None,25]

Constraints:

    The number of nodes in the tree is in the range [0, 10^4].
    -10^8 <= Node.val <= 10^8
    All the values Node.val are unique.
    -10^8 <= val <= 10^8
    It's guaranteed that val does not exist in the original BST.
"""


class Solution:
    def insertIntoBST(self, root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
        def dfs(node, parent):
            if not node:
                parent.left = TreeNode(val)
                return
            is_leaf = node.left is None and node.right is None

            if is_leaf:
                if val > node.val:
                    node.right = TreeNode(val)
                else:
                    node.left = TreeNode(val)
            else:
                if val > node.val:
                    if node.right:
                        dfs(node.right, node)
                    else:
                        node.right = TreeNode(val)
                else:
                    if node.left:
                        dfs(node.left, node)
                    else:
                        node.left = TreeNode(val)

        d = TreeNode(float("-inf"), root)
        dfs(d.left, d)
        draw_tree(d)
        return d.left


sol = Solution()

# root = build_tree([4, 2, 7, 1, 3])
# result = sol.insertIntoBST(root, 5)
# print(get_level_order(result))
# assert get_level_order(result) == [[4], [2, 7], [1, 3, 5]]

root = build_tree([])
result = sol.insertIntoBST(root, 5)
draw_tree(result)

# root = build_tree([5, None, 14, 10, 77, None, None, None, 95, None, None])
# result = sol.insertIntoBST(root, 4)

# root = build_tree([40, 20, 60, 10, 30, 50, 70])
# result = sol.insertIntoBST(root, 25)
# # assert get_level_order(result) == [[40], [20, 60], [10, 30, 50, 70], [25]]

# root = build_tree([])
# result = sol.insertIntoBST(root, 5)
# # assert get_level_order(result) == [[5]]

# root = build_tree([4])
# result = sol.insertIntoBST(root, 2)
# # assert get_level_order(result) == [[4], [2]]

# root = build_tree([4])
# result = sol.insertIntoBST(root, 6)
# # assert get_level_order(result) == [[4], [6]]

# root = build_tree([4, 2, 7, 1, 3])
# result = sol.insertIntoBST(root, 8)
# # assert get_level_order(result) == [[4], [2, 7], [1, 3, 8]]

# root = build_tree([4, 2, 7, 1, 3])
# result = sol.insertIntoBST(root, 0)
# assert get_level_order(result) == [[4], [2, 7], [1, 3], [0]]

# root = build_tree([0, -5, 5])
# result = sol.insertIntoBST(root, -10)
# # assert get_level_order(result) == [[0], [-5, 5], [-10]]

# root = build_tree([1, None, 2, None, 3, None, 4])
# result = sol.insertIntoBST(root, 5)
# # assert get_level_order(result) == [[1], [2], [3], [4], [5]]

# root = build_tree([1, None, 2, None, 3, None, 4])
# result = sol.insertIntoBST(root, 0)
# # assert get_level_order(result) == [[1], [0, 2], [3], [4]]
