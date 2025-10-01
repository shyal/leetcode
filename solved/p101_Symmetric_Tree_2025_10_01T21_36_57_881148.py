"""
URL: https://leetcode.com/problems/symmetric-tree/description/

101. Symmetric Tree

Given the root of a binary tree, check whether it is a mirror of itself (i.e., symmetric around its center).


Example 1:

Input: root = [1,2,2,3,4,4,3]
Output: true

Example 2:

Input: root = [1,2,2, None,3, None,3]
Output: false


Constraints:

        The number of nodes in the tree is in the range [1, 1000].
        -100 <= Node.val <= 100


Follow up: Could you solve it both recursively and iteratively?

---

      [1]
   ┌───┴───┐
  [2]     [2]
 ┌─┴─┐   ┌─┴─┐
[3] [4] [4] [3]

  [1]
 ┌─┴─┐
[2] [2]
 ┐   ┐
[3] [3]

"""


class Solution:
    def isSymmetric(self, root: Optional[TreeNode]) -> bool:
        def dfs(node, depth=0, _dir=0):
            if not node:
                yield None
                return
            yield node.val
            choice = (node.left, node.right)
            yield from dfs(choice[_dir], depth + 1, _dir)
            if depth > 0:
                yield from dfs(choice[not _dir], depth + 1, _dir)

        return all(a == b for a, b in zip(dfs(root, _dir=0), dfs(root, _dir=1)))


sol = Solution()

tree = build_tree([1, 2, 2, 3, 4, 4, 3])
assert sol.isSymmetric(tree) == True
tree = build_tree([1, 2, 2, None, 3, None, 3])
assert sol.isSymmetric(tree) == False
tree = build_tree([1])
assert sol.isSymmetric(tree) == True
tree = build_tree([1, 2])
assert sol.isSymmetric(tree) == False
tree = build_tree([1, None, 2])
assert sol.isSymmetric(tree) == False
tree = build_tree([1, 2, 2])
assert sol.isSymmetric(tree) == True
tree = build_tree([1, 2, 3])
assert sol.isSymmetric(tree) == False
tree = build_tree([1, -1, -1])
assert sol.isSymmetric(tree) == True
tree = build_tree([1, -1, 1])
assert sol.isSymmetric(tree) == False
tree = build_tree([1, 2, 2, 3, None, None, 3])
assert sol.isSymmetric(tree) == True
tree = build_tree([1, 2, 2, None, 3, 3, None])
assert sol.isSymmetric(tree) == True
tree = build_tree([1, 2, 2, 3, None, 3, None])
assert sol.isSymmetric(tree) == False
tree = build_tree([1, 2, 2, 3, 4, 4, 5])
assert sol.isSymmetric(tree) == False
tree = build_tree([1, 2, 2, 3, 4, 4, 3, 5, 6, 7, 8, 8, 7, 6, 5])
assert sol.isSymmetric(tree) == True
tree = build_tree([1, 2, 2, 3, 4, 4, 3, 5, 6, 7, 8, 8, 7, 6, 4])
assert sol.isSymmetric(tree) == False
tree = build_tree([1, 2, 3, 4, None, None, None, None, 5])
assert sol.isSymmetric(tree) == False
