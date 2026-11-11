# URL: https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/description/?envType=problem-list-v2&envId=vn57k9wr
#
# 105. Construct Binary Tree from Preorder and Inorder Traversal
#
# Given two integer arrays preorder and inorder where preorder is the preorder traversal of a binary tree and inorder is the inorder traversal of the same tree, construct and return the binary tree.
#
# Example 1:
#
# Input: preorder = [3,9,20,15,7], inorder = [9,3,15,20,7]
# Output: [3,9,20,null,null,15,7]
#
# Example 2:
#
# Input: preorder = [-1], inorder = [-1]
# Output: [-1]
#
# Constraints:
#
#     1 <= preorder.length <= 3000
#     inorder.length == preorder.length
#     -3000 <= preorder[i], inorder[i] <= 3000
#     preorder and inorder consist of unique values.
#     Each value of inorder also appears in preorder.
#     preorder is guaranteed to be the preorder traversal of the tree.
#     inorder is guaranteed to be the inorder traversal of the tree.
#
# ---
# LEETCODE: Accepted (107 ms, 91.1 MB)

# mu 0.17

class Solution
  def buildTree(preorder: [int], inorder: [int]) -> TreeNode?
    if not preorder
      return
    root = preorder[0]
    root_in_index = inorder.index(root)
    in_left = inorder[:root_in_index]
    pre_left = preorder[1:len(in_left) + 1]
    in_right = inorder[root_in_index + 1:]
    pre_right = preorder[1 + len(pre_left):]
    TreeNode(root, left=self.buildTree(pre_left, in_left), right=self.buildTree(pre_right, in_right))

sol = Solution()

# Example 1
root1 = sol.buildTree([3, 9, 20, 15, 7], [9, 3, 15, 20, 7])
print(get_level_order(root1))  # [3,9,20,None,None,15,7]

# # Example 2
root2 = sol.buildTree([-1], [-1])
print(get_level_order(root2))  # [-1]

assert get_level_order(sol.buildTree([3, 9, 20, 15, 7], [9, 3, 15, 20, 7])) == [3, 9, 20, none, none, 15, 7]
assert get_level_order(sol.buildTree([-1], [-1])) == [-1]

assert get_level_order(sol.buildTree([], [])) == []
assert get_level_order(sol.buildTree([1], [1])) == [1]
assert get_level_order(sol.buildTree([1, 2], [2, 1])) == [1, 2]
assert get_level_order(sol.buildTree([1, 2], [1, 2])) == [1, none, 2]
assert get_level_order(sol.buildTree([-3000], [-3000])) == [-3000]
assert get_level_order(sol.buildTree([i for i in 1..<11], [i for i in 1..<11])) == [1, none, 2, none, 3, none, 4, none, 5, none, 6, none, 7, none, 8, none, 9, none, 10]
assert get_level_order(sol.buildTree([10, 9, 8, 7, 6, 5, 4, 3, 2, 1], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])) == [10, 9, none, 8, none, 7, none, 6, none, 5, none, 4, none, 3, none, 2, none, 1]
assert get_level_order(sol.buildTree([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [10, 9, 8, 7, 6, 5, 4, 3, 2, 1])) == [1, 2, none, 3, none, 4, none, 5, none, 6, none, 7, none, 8, none, 9, none, 10]
assert get_level_order(sol.buildTree([1, 2, 3, 4, 5], [3, 2, 4, 1, 5])) == [1, 2, 5, 3, 4]
assert get_level_order(sol.buildTree([2, 1, 3], [1, 2, 3])) == [2, 1, 3]
assert get_level_order(sol.buildTree([2, 3, 1], [3, 2, 1])) == [2, 3, 1]
