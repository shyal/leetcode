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

---

Learning

LEETCODE: Accepted (13 ms, 19.6 MB)
"""

from enum import Flag, auto


class State(Flag):
    uncovered = auto()
    covered = auto()
    cam = auto()


class Solution:
    def minCameraCover(self, root: Optional[TreeNode]) -> int:

        def helper(n):
            if n is None:
                return State.covered
            both = helper(n.left) | helper(n.right)
            if State.uncovered in both:
                self.count += 1
                return State.cam
            if State.cam in both:
                return State.covered
            return State.uncovered

        self.count = 0
        if helper(root) is State.uncovered:
            self.count += 1
        return self.count


sol = Solution()

root = build_tree([0, 0, None, 0, 0])
print(root)

print(sol.minCameraCover(root))  # 1

# assert sol.minCameraCover(build_tree([0, 0, None, 0, 0])) == 1
# assert sol.minCameraCover(build_tree([0, 0, None, 0, None, 0, None, None, 0])) == 2

# assert Solution().minCameraCover(build_tree([0])) == 1
# assert Solution().minCameraCover(build_tree([0, 0, 0, 0, 0, 0, 0])) == 2
# assert Solution().minCameraCover(build_tree([0, None, 0, None, 0, None, 0])) == 2
# assert Solution().minCameraCover(build_tree([0] * 1000)) == 288
# assert Solution().minCameraCover(build_tree([0] + [None] * 999)) == 1
# assert (
#     Solution().minCameraCover(build_tree([0, 0, None, 0, None, 0, None, 0, None, 0]))
#     == 2
# )
# assert (
#     Solution().minCameraCover(build_tree([0, 0, 0, None, None, 0, 0, None, None, 0, 0]))
#     == 3
# )
# assert Solution().minCameraCover(build_tree([0] * 10)) == 3
# assert (
#     Solution().minCameraCover(
#         build_tree([0, 0, 0, 0, None, None, 0, None, None, None, 0])
#     )
#     == 2
# )
# assert (
#     Solution().minCameraCover(build_tree([0, 0, None, 0, None, None, 0, None, 0])) == 2
# )
# assert (
#     Solution().minCameraCover(build_tree([0, 0, 0, 0, 0, None, None, None, None, 0, 0]))
#     == 3
# )
# assert (
#     Solution().minCameraCover(build_tree([0, None, 0, 0, None, None, 0, 0, None])) == 2
# )
