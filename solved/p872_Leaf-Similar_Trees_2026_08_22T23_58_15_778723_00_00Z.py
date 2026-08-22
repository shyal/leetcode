"""
URL: https://leetcode.com/problems/leaf-similar-trees/description/?envType=problem-list-v2&envId=vn57k9wr

872. Leaf-Similar Trees

Consider all the leaves of a binary tree, from left to right order, the values of those leaves form a leaf value sequence.

For example, in the given tree above, the leaf value sequence is (6, 7, 4, 9, 8).

Two binary trees are considered leaf-similar if their leaf value sequence is the same.

Return true if and only if the two given trees with head nodes root1 and root2 are leaf-similar.

Example 1:

Input: root1 = [3,5,1,6,2,9,8,null,null,7,4], root2 = [3,5,1,6,7,4,2,null,null,null,null,null,null,9,8]
Output: true

Example 2:

Input: root1 = [1,2,3], root2 = [1,3,2]
Output: false

Constraints:

    The number of nodes in each tree will be in the range [1, 200].
    Both of the given trees will have values in the range [0, 200].
"""


class Solution:
    def leafSimilar(self, root1: Optional[TreeNode], root2: Optional[TreeNode]) -> bool:
        def helper(root, leaves):
            if root:
                if root.left == root.right == None:
                    leaves.append(root.val)
                else:
                    helper(root.left, leaves)
                    helper(root.right, leaves)

        root1_leaves = []
        helper(root1, root1_leaves)
        root2_leaves = []
        helper(root2, root2_leaves)
        return root1_leaves == root2_leaves


sol = Solution()

root1 = build_tree([3, 5, 1, 6, 2, 9, 8, None, None, 7, 4])
root2 = build_tree([3, 5, 1, 6, 7, 4, 2, None, None, None, None, None, None, 9, 8])
draw_tree(root1)
draw_tree(root2)

print(
    sol.leafSimilar(
        root1,
        root2,
    )
)  # True

assert (
    sol.leafSimilar(
        build_tree([3, 5, 1, 6, 2, 9, 8, None, None, 7, 4]),
        build_tree([3, 5, 1, 6, 7, 4, 2, None, None, None, None, None, None, 9, 8]),
    )
    == True
)
assert sol.leafSimilar(build_tree([1, 2, 3]), build_tree([1, 3, 2])) == False

assert sol.leafSimilar(build_tree([1]), build_tree([1])) == True
assert sol.leafSimilar(build_tree([1]), build_tree([2])) == False
assert sol.leafSimilar(build_tree([1, 1, 1, 1, 1]), build_tree([1, 1, 1, 1, 1])) == True
assert (
    sol.leafSimilar(
        build_tree([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
        build_tree([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
    )
    == True
)
assert (
    sol.leafSimilar(
        build_tree([1, None, 2, None, 3, None, 4, None, 5]),
        build_tree([1, None, 2, None, 3, None, 4, None, 5]),
    )
    == True
)
assert (
    sol.leafSimilar(
        build_tree([1, None, 2, None, 3, None, 4, None, 5]),
        build_tree([5, None, 4, None, 3, None, 2, None, 1]),
    )
    == False
)
assert sol.leafSimilar(build_tree([0] * 200), build_tree([0] * 200)) == True
assert sol.leafSimilar(build_tree([200] * 200), build_tree([200] * 200)) == True
assert (
    sol.leafSimilar(
        build_tree([1, 2, 2, 3, 3, 3, 3]), build_tree([1, 2, 2, 3, 3, 3, 4])
    )
    == False
)
assert (
    sol.leafSimilar(build_tree([1, -1, -1, -1, -1]), build_tree([1, -1, -1, -1, -1]))
    == True
)
assert (
    sol.leafSimilar(
        build_tree([1, 2, None, 3, None, 4, None, 5]),
        build_tree([1, 2, None, 3, None, 4, None, 6]),
    )
    == False
)
assert (
    sol.leafSimilar(
        build_tree([1, 2, 3, None, None, 4, 5]), build_tree([1, 2, 3, None, None, 4, 5])
    )
    == True
)
