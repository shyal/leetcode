"""
URL: https://leetcode.com/problems/binary-tree-preorder-traversal/description/

144. Binary Tree Preorder Traversal

Given the root of a binary tree, return the preorder traversal of its nodes' values.


Example 1:

Input: root = [1,None,2,3]

Output: [1,2,3]

Explanation:

Example 2:

Input: root = [1,2,3,4,5,None,8,None,None,6,7,9]

Output: [1,2,4,5,6,7,3,8,9]

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

--

[1]
 \\
[2]
 /
[3]


       [1]
    ┌───┴────┐
   [2]      [3]
 ┌──┴──┐     \\
[4]   [5]   [8]
     ┌─┴─┐   /
    [6] [7] [9]


[1]
"""


class Solution:
    def preorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        def dfs(node):
            if not node:
                return

            res.append(node.val)
            dfs(node.left)
            dfs(node.right)

        res = []
        dfs(root)
        return res


sol = Solution()
tree = build_tree([1, None, 2, 3])
assert sol.preorderTraversal(tree) == [1, 2, 3]

sol = Solution()
tree = build_tree([1, 2, 3, 4, 5, None, 8, None, None, 6, 7, 9])
assert sol.preorderTraversal(tree) == [1, 2, 4, 5, 6, 7, 3, 8, 9]

sol = Solution()
tree = build_tree([1])
assert sol.preorderTraversal(tree) == [1]
