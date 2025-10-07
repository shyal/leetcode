"""
URL: https://leetcode.com/problems/root-equals-sum-of-children/description/

2236. Root Equals Sum of Children

You are given the root of a binary tree that consists of exactly 3 nodes: the root, its left child, and its right child.

Return true if the value of the root is equal to the sum of the values of its two children, or false otherwise.


Example 1:

Input: root = [10,4,6]
Output: true
Explanation: The values of the root, its left child, and its right child are 10, 4, and 6, respectively.
4 + 6 = 10, which equals the root value.

Example 2:

Input: root = [2,3,4]
Output: false
Explanation: The values of the root, its left child, and its right child are 2, 3, and 4, respectively.
3 + 4 = 7, which does not equal the root value.


Constraints:

    The tree consists exactly of 3 nodes: root, left child, and right child.
    -100 <= Node.val <= 100
"""


class Solution:
    def checkTree(self, root: Optional[TreeNode]) -> bool:
        return root.val == root.left.val + root.right.val


sol = Solution()

assert sol.checkTree(build_tree([10, 4, 6])) == True
assert sol.checkTree(build_tree([2, 3, 4])) == False
assert sol.checkTree(build_tree([0, 0, 0])) == True
assert sol.checkTree(build_tree([0, 1, -1])) == True
assert sol.checkTree(build_tree([0, 1, 0])) == False
assert sol.checkTree(build_tree([-5, -2, -3])) == True
assert sol.checkTree(build_tree([-5, -2, -4])) == False
assert sol.checkTree(build_tree([1, -1, 2])) == True
assert sol.checkTree(build_tree([1, -1, 3])) == False
assert sol.checkTree(build_tree([100, 50, 50])) == True
assert sol.checkTree(build_tree([100, 50, 51])) == False
assert sol.checkTree(build_tree([-100, -50, -50])) == True
assert sol.checkTree(build_tree([-100, -50, -51])) == False
assert sol.checkTree(build_tree([100, 100, 0])) == True
assert sol.checkTree(build_tree([100, 100, 1])) == False
assert sol.checkTree(build_tree([-100, -100, 0])) == True
assert sol.checkTree(build_tree([-100, -100, 1])) == False
