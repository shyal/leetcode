"""
URL: https://leetcode.com/problems/balanced-binary-tree/description/

110. Balanced Binary Tree

Given a binary tree, determine if it is height-balanced.


Example 1:

Input: root = [3,9,20, None, None,15,7]
Output: true

Example 2:

Input: root = [1,2,2,3,3, None, None,4,4]
Output: false

Example 3:

Input: root = []
Output: true


Constraints:

        The number of nodes in the tree is in the range [0, 5000].
        -104 <= Node.val <= 104


A height-balanced binary tree is a binary tree in which the depth of the two subtrees of every node never differs by more than one.

     [0]
   ┌──┴──┐
  [1]   [1]
 ┌─┴─┐   /
[2] [2] [2]
 /
[3]

"""


class Solution:
    def isBalanced(self, root: Optional[TreeNode]) -> bool:
        def dfs(node, height):
            if not node:
                yield (height, True)
                return (height, True)
            else:
                left_height, left_balanced = yield from dfs(node.left, height + 1)
                right_height, right_balanced = yield from dfs(node.right, height + 1)
                height, is_balanced = (
                    max(left_height, right_height),
                    abs(left_height - right_height) <= 1
                    and left_balanced
                    and right_balanced,
                )
                yield height, is_balanced
                return height, is_balanced

        return all(x[1] for x in dfs(root, 0))


sol = Solution()

tree = build_tree([1, 2, 3, 4, 5, 6, None, 8])
res = sol.isBalanced(tree)
assert res == True


tree = build_tree([3, 9, 20, None, None, 15, 7])
res = sol.isBalanced(tree)
assert res == True


tree = build_tree([1, 2, 2, 3, None, 4, 4, 5, None])
res = sol.isBalanced(tree)
assert res == False


tree = build_tree([0])
res = sol.isBalanced(tree)
assert res == True


tree = build_tree([])
res = sol.isBalanced(tree)
assert res == True

