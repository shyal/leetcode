"""
URL: https://leetcode.com/problems/univalued-binary-tree/description/?envType=problem-list-v2&envId=vn57k9wr

965. Univalued Binary Tree

A binary tree is uni-valued if every node in the tree has the same value.

Given the root of a binary tree, return true if the given tree is uni-valued, or false otherwise.


Example 1:

Input: root = [1,1,1,1,1,null,1]
Output: true

Example 2:

Input: root = [2,2,2,5,2]
Output: false


Constraints:

        The number of nodes in the tree is in the range [1, 100].
        0 <= Node.val < 100
"""


class Solution:
    def isUnivalTree(self, root: Optional[TreeNode]) -> bool:
        def dfs(node):
            if not node:
                return True

            if not vals:
                vals.add(node.val)
            else:
                if node.val not in vals:
                    return False

            return dfs(node.left) and dfs(node.right)

        vals = set([])
        return dfs(root)


sol = Solution()
assert sol.isUnivalTree(root=build_tree([1, 1, 1, 1, 1, None, 1])) == True
assert sol.isUnivalTree(root=build_tree([2, 2, 2, 5, 2])) == False
