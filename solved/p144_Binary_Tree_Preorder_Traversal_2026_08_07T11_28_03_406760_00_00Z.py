"""
URL: https://leetcode.com/problems/binary-tree-preorder-traversal/description/?envType=problem-list-v2&envId=vn57k9wr

144. Binary Tree Preorder Traversal

Given the root of a binary tree, return the preorder traversal of its nodes' values.


Example 1:

Input: root = [1,null,2,3]
Output: [1,2,3]
Explanation:
    1
     \
      2
     /
    3

Example 2:

Input: root = [1,2,3,4,5,null,8,null,null,6,7,9]
Output: [1,2,4,5,6,7,3,8,9]

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
    def preorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        ret = []
        def helper(root):
            if root:
                ret.append(root.val)
                helper(root.left)
                helper(root.right)
            return ret
        return helper(root)


sol = Solution()

# draw_tree(build_tree([1, None, 2, 3]))
# print(sol.preorderTraversal(build_tree([1, None, 2, 3])))  # [1, 2, 3]

assert sol.preorderTraversal(build_tree([1, None, 2, 3])) == [1, 2, 3]
assert sol.preorderTraversal(
    build_tree([1, 2, 3, 4, 5, None, 8, None, None, 6, 7, 9])
) == [1, 2, 4, 5, 6, 7, 3, 8, 9]
assert sol.preorderTraversal(build_tree([])) == []
assert sol.preorderTraversal(build_tree([1])) == [1]
assert sol.preorderTraversal(build_tree([1, 2])) == [1, 2]
assert sol.preorderTraversal(build_tree([1, None, 2])) == [1, 2]
assert sol.preorderTraversal(build_tree([1, 2, 3])) == [1, 2, 3]
assert sol.preorderTraversal(build_tree([3, 1, 2])) == [3, 1, 2]
assert sol.preorderTraversal(build_tree([1, 2, None, 3, None, 4, None])) == [1, 2, 3, 4]
assert sol.preorderTraversal(build_tree([1, None, 2, None, 3, None, 4])) == [1, 2, 3, 4]
assert sol.preorderTraversal(build_tree([1, 2, None, None, 3])) == [1, 2, 3]
assert sol.preorderTraversal(build_tree([1, 2, 3, None, 4, None, None])) == [1, 2, 4, 3]
assert sol.preorderTraversal(build_tree([1, 2, 3, 4, 5, 6, 7])) == [1, 2, 4, 5, 3, 6, 7]
assert sol.preorderTraversal(
    build_tree([10, 5, 15, 3, 7, 12, 20, 1, None, 6, None, None, 13])
) == [10, 5, 3, 1, 7, 6, 15, 12, 13, 20]
assert sol.preorderTraversal(build_tree([-100])) == [-100]
assert sol.preorderTraversal(build_tree([100])) == [100]
assert sol.preorderTraversal(build_tree([0, -100, 100])) == [0, -100, 100]
assert sol.preorderTraversal(build_tree([100, -100])) == [100, -100]
assert sol.preorderTraversal(build_tree([2, 2, 2, 2])) == [2, 2, 2, 2]