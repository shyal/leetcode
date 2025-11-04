"""
URL: https://leetcode.com/problems/same-tree/description/

100. Same Tree

Given the roots of two binary trees p and q, write a function to check if they are the same or not.

Two binary trees are considered the same if they are structurally identical, and the nodes have the same value.


Example 1:

Input: p = [1,2,3], q = [1,2,3]
Output: true

Example 2:

Input: p = [1,2], q = [1,null,2]
Output: false

Example 3:

Input: p = [1,2,1], q = [1,1,2]
Output: false


Constraints:

    The number of nodes in both trees is in the range [0, 100].
    -104 <= Node.val <= 104


---

Ok need to think about this one a little bit. In the dfs function:

- If one root exists, but not the other, they differ, so return false
- if they're both none, return true because that's valid
- if they both exist
    - recursively call dfs on both children, since they'll return
    the base cases, `and` the result from both
"""


class Solution:
    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        def dfs(n1, n2):
            if (n1 and not n2) or (n2 and not n1):
                return False
            if not (n1 and n2):
                return True
            return (
                n1.val == n2.val and dfs(n1.left, n2.left) and dfs(n1.right, n2.right)
            )

        return dfs(p, q)


sol = Solution()
p = build_tree([1, 2, 3])
q = build_tree([1, 2, 3])
draw_tree(p)
draw_tree(q)
assert sol.isSameTree(p, q) == True

sol = Solution()
p = build_tree([1, 2])
q = build_tree([1, None, 2])
draw_tree(p)
draw_tree(q)
assert sol.isSameTree(p, q) == False

sol = Solution()
p = build_tree([1, 2, 1])
q = build_tree([1, 1, 2])
draw_tree(p)
draw_tree(q)
assert sol.isSameTree(p, q) == False
