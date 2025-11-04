"""
URL: https://leetcode.com/problems/binary-tree-postorder-traversal/description/

145. Binary Tree Postorder Traversal

Given the root of a binary tree, return the postorder traversal of its nodes' values.


Example 1:

Input: root = [1,null,2,3]

Output: [3,2,1]

Explanation:

Example 2:

Input: root = [1,2,3,4,5,null,8,null,null,6,7,9]

Output: [4,6,7,5,2,9,8,3,1]

Explanation:

Example 3:

Input: root = []

Output: []

Example 4:

Input: root = [1]

Output: [1]


Constraints:

    The number of the nodes in the tree is in the range [0, 100].
    -100 <= Node.val <= 100


Follow up: Recursive solution is trivial, could you do it iteratively?
"""


class Solution:
    def postorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        def dfs(node):
            if not node:
                return
            dfs(node.left)
            dfs(node.right)
            ret.append(node.val)

        ret = []
        dfs(root)
        return ret


sol = Solution()
tree = build_tree([1, None, 2, 3])
draw_tree(tree)
assert sol.postorderTraversal(tree) == [3, 2, 1]

sol = Solution()
tree = build_tree([1, 2, 3, 4, 5, None, 8, None, None, 6, 7, 9])
draw_tree(tree)
assert sol.postorderTraversal(tree) == [4, 6, 7, 5, 2, 9, 8, 3, 1]

sol = Solution()
tree = build_tree([])
draw_tree(tree)
assert sol.postorderTraversal(tree) == []

sol = Solution()
tree = build_tree([1])
draw_tree(tree)
assert sol.postorderTraversal(tree) == [1]
