"""
URL: https://leetcode.com/problems/merge-two-binary-trees/description/

617. Merge Two Binary Trees

You are given two binary trees root1 and root2.

Imagine that when you put one of them to cover the other, some nodes of the two trees are overlapped while the others are not. You need to merge the two trees into a new binary tree. The merge rule is that if two nodes overlap, then sum node values up as the new value of the merged node. Otherwise, the NOT null node will be used as the node of the new tree.

Return the merged tree.

Note: The merging process must start from the root nodes of both trees.

Example 1:

Input: root1 = [1,3,2,5], root2 = [2,1,3,null,4,null,7]
Output: [3,4,5,5,4,null,7]

Example 2:

Input: root1 = [1], root2 = [1,2]
Output: [2,2]

Constraints:

    The number of nodes in both trees is in the range [0, 2000].
    -10^4 <= Node.val <= 10^4
"""


class Solution:
    def mergeTrees(
        self, t1: Optional[TreeNode], t2: Optional[TreeNode]
    ) -> Optional[TreeNode]:
        def dfs(a, b):
            if a is None and b is None:
                return
            if a and b:
                return TreeNode(
                    a.val + b.val, dfs(a.left, b.left), dfs(a.right, b.right)
                )
            else:
                c = a or b
                return TreeNode(
                    c.val,
                    dfs(a.left if a else None, b.left if b else None),
                    dfs(a.right if a else None, b.right if b else None),
                )

        return dfs(t1, t2)


sol = Solution()

t1 = build_tree([1, 3, 2, 5])
t2 = build_tree([2, 1, 3, None, 4, None, 7])
# draw_tree(t1)
# draw_tree(t2)
res = sol.mergeTrees(t1, t2)
# draw_tree(res)

# print(get_level_order(res))

assert get_level_order(
    sol.mergeTrees(build_tree([1, 3, 2, 5]), build_tree([2, 1, 3, None, 4, None, 7]))
) == [3, 4, 5, 5, 4, None, 7]
assert get_level_order(sol.mergeTrees(build_tree([1]), build_tree([1, 2]))) == [2, 2]
assert get_level_order(sol.mergeTrees(build_tree([]), build_tree([]))) == []
assert get_level_order(sol.mergeTrees(build_tree([]), build_tree([1]))) == [1]
assert get_level_order(sol.mergeTrees(build_tree([1]), build_tree([]))) == [1]
assert get_level_order(sol.mergeTrees(build_tree([-1]), build_tree([1]))) == [0]
assert get_level_order(
    sol.mergeTrees(build_tree([1, 2]), build_tree([3, None, 4]))
) == [4, 2, 4]
assert get_level_order(sol.mergeTrees(build_tree([1, 3, 2]), build_tree([2, 1]))) == [
    3,
    4,
    2,
]
assert get_level_order(sol.mergeTrees(build_tree([1, None, 2]), build_tree([]))) == [
    1,
    None,
    2,
]
assert get_level_order(
    sol.mergeTrees(build_tree([-5, -10, 5]), build_tree([3, 2, -1, None, 4]))
) == [-2, -8, 4, None, 4]
