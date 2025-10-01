"""
URL: https://leetcode.com/problems/binary-tree-inorder-traversal/description/

94. Binary Tree Inorder Traversal

Given the root of a binary tree, return the inorder traversal of its nodes' values.


Example 1:

Input: root = [1,null,2,3]

Output: [1,3,2]

Explanation:

Example 2:

Input: root = [1,2,3,4,5,null,8,null,null,6,7,9]

Output: [4,2,6,5,7,1,3,9,8]

Explanation:

Example 3:

Input: root = []

Output: []

Example 4:

Input: root = [1]

Output: [1]


Constraints:

    The number of nodes in the tree is in the range [0, 100].
    -100 <= Node.val <= 100


Follow up: Recursive solution is trivial, could you do it iteratively?
"""


class Solution:
    def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        def dfs(node):
            if not node:
                return
            dfs(node.left)
            res.append(node.val)
            dfs(node.right)

        res = []
        dfs(root)
        return res


sol = Solution()
tree = build_tree([1, None, 2, 3])
# draw_tree(tree)
assert sol.inorderTraversal(tree) == [1, 3, 2]

sol = Solution()
tree = build_tree([1, 2, 3, 4, 5, None, 8, None, None, 6, 7, 9])
# draw_tree(tree)
assert sol.inorderTraversal(tree) == [4, 2, 6, 5, 7, 1, 3, 9, 8]

sol = Solution()
tree = build_tree([])
# draw_tree(tree)
assert sol.inorderTraversal(tree) == []

sol = Solution()
tree = build_tree([1])
# draw_tree(tree)
assert sol.inorderTraversal(tree) == [1]
