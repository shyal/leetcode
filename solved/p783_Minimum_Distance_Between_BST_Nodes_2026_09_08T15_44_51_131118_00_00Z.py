"""
URL: https://leetcode.com/problems/minimum-distance-between-bst-nodes/description/?envType=problem-list-v2&envId=vn57k9wr

783. Minimum Distance Between BST Nodes

Given the root of a Binary Search Tree (BST), return the minimum difference between the values of any two different nodes in the tree.

Example 1:

Input: root = [4,2,6,1,3]
Output: 1

Example 2:

Input: root = [1,0,48,null,null,12,49]
Output: 1

Constraints:

    The number of nodes in the tree is in the range [2, 100].
    0 <= Node.val <= 10^5

Note: This question is the same as 530: https://leetcode.com/problems/minimum-absolute-difference-in-bst/
"""


class Solution:
    def minDiffInBST(self, root: Optional[TreeNode]) -> int:
        def dfs(n):
            if n.left:
                dfs(n.left)
            if self.prev != None:
                if n.val < self.prev:
                    self.res = -1
                self.res = min(self.res, n.val - self.prev)
            self.prev = n.val
            if n.right:
                dfs(n.right)

        self.prev = None
        self.res = float("inf")
        dfs(root)
        return self.res


sol = Solution()

# print(sol.minDiffInBST(build_tree([4, 2, 6, 1, 3])))  # 1
print(sol.minDiffInBST(build_tree([2, 1, None, None, 3])))

draw_tree(build_tree([2, 1, None, None, 3]))

assert sol.minDiffInBST(build_tree([4, 2, 6, 1, 3])) == 1
assert sol.minDiffInBST(build_tree([1, 0, 48, None, None, 12, 49])) == 1

assert sol.minDiffInBST(build_tree([1, 2])) == -1
assert sol.minDiffInBST(build_tree([100000, 99999])) == 1
assert sol.minDiffInBST(build_tree([10, 5, 15, 2, 7, 12, 20])) == 2
assert sol.minDiffInBST(build_tree([1, 1, 1, 1, 1])) == 0
assert sol.minDiffInBST(build_tree([0, 0])) == 0
assert sol.minDiffInBST(build_tree([2, 1, None, None, 3])) == -1
assert sol.minDiffInBST(build_tree([100000, 50000, 99999])) == -1
assert sol.minDiffInBST(build_tree([1, 0, None, None, 2])) == -1
assert sol.minDiffInBST(build_tree([10, 5, 15, 1, None, None, 22, 0])) == 1
assert sol.minDiffInBST(build_tree([2, 1, 3, None, None, None, 4])) == 1
assert (
    sol.minDiffInBST(
        build_tree([50, 25, 75, 12, 37, 62, 87, 6, 18, 30, 40, 55, 70, 80, 90])
    )
    == 3
)
assert (
    sol.minDiffInBST(build_tree([2, 1, 3, 0, None, None, 4, None, None, None, 5])) == 1
)
