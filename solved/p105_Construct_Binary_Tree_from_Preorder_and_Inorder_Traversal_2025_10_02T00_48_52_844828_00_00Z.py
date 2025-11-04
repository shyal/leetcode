"""
URL: https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/description/

105. Construct Binary Tree from Preorder and Inorder Traversal

Given two integer arrays preorder and inorder where preorder is the preorder traversal of a binary tree and inorder is the inorder traversal of the same tree, construct and return the binary tree.


Example 1:

Input: preorder = [3,9,20,15,7], inorder = [9,3,15,20,7]
Output: [3,9,20,null,null,15,7]

Example 2:

Input: preorder = [-1], inorder = [-1]
Output: [-1]


Constraints:

    1 <= preorder.length <= 3000
    inorder.length == preorder.length
    -3000 <= preorder[i], inorder[i] <= 3000
    preorder and inorder consist of unique values.
    Each value of inorder also appears in preorder.
    preorder is guaranteed to be the preorder traversal of the tree.
    inorder is guaranteed to be the inorder traversal of the tree.


---

Starting with a simple example:

tree = sol.buildTree([3, 9, 20], [9, 3, 20])

We notice that 3 is at the start of the list in the pre order, so the root node
and in the in-order, it's in the middle of the list, so 9 must be the left child
and 20 the right

tree = sol.buildTree([3, 9, 20, 15, 7], [9, 3, 15, 20, 7])

Here we notice the same thing, 3 only has 1 left child, and 3 right children.
Then if we move on to 20, we notice that it to has 1 left and 1 right child.

This perhapse suggests recursion, with certain bounds within the list to check
children / subtrees.

I might build a solution for the simple version of the tree, then expand it for
the more complex versions.

For the simple version:

- start with first node of inorder (3)
- get its index in in-order
    - use remaining values for left and right child

class Solution:
    def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
        def dfs(pos=0):
            val = preorder[pos]
            val_inorder_index = inorder.index(val)
            left_vals = inorder[:val_inorder_index]
            right_vals = inorder[val_inorder_index + 1 :]
            node = TreeNode(val, TreeNode(left_vals[0]), TreeNode(right_vals[0]))
            return node

        return dfs()

  [3]
 ┌─┴─┐
[9] [20]

OK that rebuilds the tree nicely. Now let's think about how we'll deal with the more complex
example.

tree = sol.buildTree([3, 9, 20, 15, 7], [9, 3, 15, 20, 7])

Clearly we need to call dfs recursively, and pass bounds for the indices, or sublists
to make it even simpler.

Failed. Looked up solution.

"""


class Solution:

    def buildTreeSimple(
        self, preorder: List[int], inorder: List[int]
    ) -> Optional[TreeNode]:
        def dfs(pos=0):
            val = preorder[pos]
            val_inorder_index = inorder.index(val)
            left_vals = inorder[:val_inorder_index]
            right_vals = inorder[val_inorder_index + 1 :]
            node = TreeNode(val, TreeNode(left_vals[0]), TreeNode(right_vals[0]))
            return node

        return dfs()

    def buildTree(self, preorder, inorder):
        # Not my solution
        if inorder:
            ind = inorder.index(preorder.pop(0))
            root = TreeNode(inorder[ind])
            root.left = self.buildTree(preorder, inorder[0:ind])
            root.right = self.buildTree(preorder, inorder[ind + 1 :])
            return root


def to_list(root: Optional[TreeNode]) -> List[Optional[int]]:
    if not root:
        return []
    res = []
    q = [root]
    while q:
        node = q.pop(0)
        res.append(node.val if node else None)
        if node:
            q.append(node.left)
            q.append(node.right)
    while res and res[-1] is None:
        res.pop()
    return res


sol = Solution()

tree = sol.buildTree([3, 9, 20], [9, 3, 20])
draw_tree(tree)
to_list(tree) == [3, 9, 20]

tree = sol.buildTree([3, 9, 20, 15, 7], [9, 3, 15, 20, 7])
draw_tree(tree)
assert to_list(tree) == [3, 9, 20, None, None, 15, 7]

tree = sol.buildTree([-1], [-1])
draw_tree(tree)
assert to_list(tree) == [-1]
