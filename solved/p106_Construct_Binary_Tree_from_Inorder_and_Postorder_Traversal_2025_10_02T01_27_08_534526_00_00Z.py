"""
URL: https://leetcode.com/problems/construct-binary-tree-from-inorder-and-postorder-traversal/description/

106. Construct Binary Tree from Inorder and Postorder Traversal

Given two integer arrays inorder and postorder where inorder is the inorder traversal of a binary tree and postorder is the postorder traversal of the same tree, construct and return the binary tree.


Example 1:

Input: inorder = [9,3,15,20,7], postorder = [9,15,7,20,3]
Output: [3,9,20,null,null,15,7]

Example 2:

Input: inorder = [-1], postorder = [-1]
Output: [-1]


Constraints:

        1 <= inorder.length <= 3000
        postorder.length == inorder.length
        -3000 <= inorder[i], postorder[i] <= 3000
        inorder and postorder consist of unique values.
        Each value of postorder also appears in inorder.
        inorder is guaranteed to be the inorder traversal of the tree.
        postorder is guaranteed to be the postorder traversal of the tree.

---

What might work is popping the post order traversal (3) then getting its index
in the inorder traversal.

In order:

What's on the left of the index is the left subtree.
what's on the right of the index is the right subtree.

Post order:

The left subtree is the size of the inorder left subtree
The right subtree is what's left of the list

Tip for future solves: what really helped was using colour coding for left and right subtrees
on my paper notes. 3 colours, one for the root, one for the left, and one for the right.
This made spotting the pattern of which sublists matched which subtrees
a lot easier.

"""


class Solution:
    def buildTree(self, inorder, postorder):
        if not inorder:
            return
        index = inorder.index(postorder.pop())
        node = TreeNode(inorder[index])
        left = self.buildTree(inorder[:index], postorder[:index])
        right = self.buildTree(inorder[index + 1 :], postorder[index:])
        node.left = left
        node.right = right
        return node


sol = Solution()
inorder = [9, 3, 15, 20, 7]
postorder = [9, 15, 7, 20, 3]
tree = sol.buildTree(inorder, postorder)
draw_tree(tree)
assert tree.val == 3
assert tree.left.val == 9
assert tree.right.val == 20
assert tree.right.left.val == 15
assert tree.right.right.val == 7
assert tree.left.left is None
assert tree.left.right is None
assert tree.right.left.left is None
assert tree.right.left.right is None
assert tree.right.right.left is None
assert tree.right.right.right is None

sol = Solution()
inorder = [-1]
postorder = [-1]
tree = sol.buildTree(inorder, postorder)
draw_tree(tree)
assert tree.val == -1
assert tree.left is None
assert tree.right is None

sol = Solution()
inorder = [9, 3, 15, 20, 7]
postorder = [9, 15, 7, 20, 3]
tree = sol.buildTree(inorder, postorder)
assert tree.val == 3
assert tree.left.val == 9
assert tree.right.val == 20
assert tree.right.left.val == 15
assert tree.right.right.val == 7
assert tree.left.left is None
assert tree.left.right is None
assert tree.right.left.left is None
assert tree.right.left.right is None
assert tree.right.right.left is None
assert tree.right.right.right is None

sol = Solution()
inorder = [-1]
postorder = [-1]
tree = sol.buildTree(inorder, postorder)
assert tree.val == -1
assert tree.left is None
assert tree.right is None

sol = Solution()
inorder = [2, 1]
postorder = [2, 1]
tree = sol.buildTree(inorder, postorder)
assert tree.val == 1
assert tree.left.val == 2
assert tree.right is None
assert tree.left.left is None
assert tree.left.right is None

sol = Solution()
inorder = [1, 2]
postorder = [2, 1]
tree = sol.buildTree(inorder, postorder)
assert tree.val == 1
assert tree.right.val == 2
assert tree.left is None
assert tree.right.left is None
assert tree.right.right is None

sol = Solution()
inorder = [3, 2, 1]
postorder = [3, 2, 1]
tree = sol.buildTree(inorder, postorder)
assert tree.val == 1
assert tree.left.val == 2
assert tree.left.left.val == 3
assert tree.right is None
assert tree.left.right is None
assert tree.left.left.left is None
assert tree.left.left.right is None

sol = Solution()
inorder = [1, 2, 3]
postorder = [3, 2, 1]
tree = sol.buildTree(inorder, postorder)
assert tree.val == 1
assert tree.right.val == 2
assert tree.right.right.val == 3
assert tree.left is None
assert tree.right.left is None
assert tree.right.right.left is None
assert tree.right.right.right is None

sol = Solution()
inorder = [1, 2, 3]
postorder = [1, 3, 2]
tree = sol.buildTree(inorder, postorder)
assert tree.val == 2
assert tree.left.val == 1
assert tree.right.val == 3
assert tree.left.left is None
assert tree.left.right is None
assert tree.right.left is None
assert tree.right.right is None

sol = Solution()
inorder = [-3, -2, -1]
postorder = [-3, -2, -1]
tree = sol.buildTree(inorder, postorder)
assert tree.val == -1
assert tree.left.val == -2
assert tree.left.left.val == -3
assert tree.right is None
assert tree.left.right is None
assert tree.left.left.left is None
assert tree.left.left.right is None

sol = Solution()
inorder = [4, 2, 5, 1, 6, 3]
postorder = [4, 5, 2, 6, 3, 1]
tree = sol.buildTree(inorder, postorder)
assert tree.val == 1
assert tree.left.val == 2
assert tree.left.left.val == 4
assert tree.left.right.val == 5
assert tree.right.val == 3
assert tree.right.left.val == 6
assert tree.left.left.left is None
assert tree.left.left.right is None
assert tree.left.right.left is None
assert tree.left.right.right is None
assert tree.right.left.left is None
assert tree.right.left.right is None
assert tree.right.right is None
