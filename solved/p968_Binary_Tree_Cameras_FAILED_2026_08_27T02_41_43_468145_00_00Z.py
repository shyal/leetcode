"""
URL: https://leetcode.com/problems/binary-tree-cameras/description/?envType=problem-list-v2&envId=vn57k9wr

968. Binary Tree Cameras

You are given the root of a binary tree. We install cameras on the tree nodes where each camera at a node can monitor its parent, itself, and its immediate children.

Return the minimum number of cameras needed to monitor all nodes of the tree.

Example 1:

Input: root = [0,0,null,0,0]
Output: 1
Explanation: One camera is enough to monitor all nodes if placed as shown.

Example 2:

Input: root = [0,0,null,0,null,0,null,null,0]
Output: 2
Explanation: At least two cameras are needed to monitor all nodes of the tree. The above image shows one of the valid configurations of camera placement.

Constraints:

    The number of nodes in the tree is in the range [1, 1000].
    Node.val == 0
"""


class Status:

    uncovered = 0
    cam = 1
    covered = 2


class Solution:
    def minCameraCover(self, root: Optional[TreeNode]) -> int:

        def DP(n):
            if not n:
                return [Status.uncovered, 0]

            is_leaf = n.left == n.right == None

            if is_leaf:
                return [Status.uncovered, 0]

            left, left_count = DP(n.left)
            right, right_count = DP(n.right)

            if left == Status.cam and right == Status.cam:
                return [Status.covered, left_count + right_count]
            elif not (left == Status.uncovered) and not (right == Status.uncovered):
                return (
                    [Status.covered, left_count + right_count]
                    if n != root
                    else [Status.cam, left_count + right_count + 1]
                )
            elif left == Status.uncovered or right == Status.uncovered:
                return [Status.cam, left_count + right_count + (1 if n != root else 0)]

        return DP(root)[1]


sol = Solution()

tree = build_tree([0, 1, None, 2, 3])
draw_tree(tree)

print(sol.minCameraCover(tree))  # 1

assert sol.minCameraCover(build_tree([0, 0, None, 0, 0])) == 1
assert sol.minCameraCover(build_tree([0, 0, None, 0, None, 0, None, None, 0])) == 2

assert Solution().minCameraCover(build_tree([0])) == 1
assert Solution().minCameraCover(build_tree([0, 0, 0, 0, 0, 0, 0])) == 2
assert Solution().minCameraCover(build_tree([0, None, 0, None, 0, None, 0])) == 2
assert Solution().minCameraCover(build_tree([0] * 1000)) == 288
assert Solution().minCameraCover(build_tree([0] + [None] * 999)) == 1
assert (
    Solution().minCameraCover(build_tree([0, 0, None, 0, None, 0, None, 0, None, 0]))
    == 2
)
assert (
    Solution().minCameraCover(build_tree([0, 0, 0, None, None, 0, 0, None, None, 0, 0]))
    == 3
)
assert Solution().minCameraCover(build_tree([0] * 10)) == 3
assert (
    Solution().minCameraCover(
        build_tree([0, 0, 0, 0, None, None, 0, None, None, None, 0])
    )
    == 2
)
assert (
    Solution().minCameraCover(build_tree([0, 0, None, 0, None, None, 0, None, 0])) == 2
)
assert (
    Solution().minCameraCover(build_tree([0, 0, 0, 0, 0, None, None, None, None, 0, 0]))
    == 3
)
assert (
    Solution().minCameraCover(build_tree([0, None, 0, 0, None, None, 0, 0, None])) == 2
)


# FAILED: walked away after 65m 21s; no working solution.
# Judge the moves actually attempted as struggled, not clean.
