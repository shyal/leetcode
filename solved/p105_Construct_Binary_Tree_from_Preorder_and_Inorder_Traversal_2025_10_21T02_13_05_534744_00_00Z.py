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
"""


class Solution:

    def buildTree(self, preorder, inorder):
        if len(preorder) == 0 or len(inorder) == 0:
            return None
        val = preorder[0]
        index = inorder.index(val)
        num_left_nodes = index
        left_tree = self.buildTree(preorder[1 : num_left_nodes + 1], inorder[:index])
        right_tree = self.buildTree(
            preorder[1 + num_left_nodes :], inorder[num_left_nodes + 1 :]
        )
        node = TreeNode(val, left_tree, right_tree)
        return node


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
to_list(tree) == [3, 9, 20]
tree = sol.buildTree([3, 9, 20, 15, 7], [9, 3, 15, 20, 7])
# draw_tree(tree)
assert to_list(tree) == [3, 9, 20, None, None, 15, 7]
tree = sol.buildTree([-1], [-1])
assert to_list(tree) == [-1]
