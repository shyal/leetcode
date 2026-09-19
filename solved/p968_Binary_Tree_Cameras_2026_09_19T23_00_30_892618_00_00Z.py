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

Forgot about 'in' which is what makes the use of Flag
syntactically beneficial.

Also two states might help.

Learning.

LEETCODE: Accepted (15 ms, 19.6 MB)
"""

from enum import Flag, auto


class State(Flag):
    camera = auto()
    covered = auto()


class Solution:
    def minCameraCover(self, root: Optional[TreeNode]) -> int:
        def helper(n):
            if not n:
                "if we don't exist, say we're covered, because it doesn't matter"
                return State.covered
            "simple get the states of left and right"
            l = helper(n.left)
            r = helper(n.right)
            if State.covered not in l & r:
                "if neither of our children cover us, we need cover"
                self.count += 1
                "merge both states: we have a camera | we're covered"
                return State.camera | State.covered
            if State.camera in l | r:
                "if there's a camera in either of our children"
                return State.covered
            return State(0)

        self.count = 0
        if helper(root) is State(0):
            self.count += 1
        return self.count


sol = Solution()

# root = build_tree([0, 0, None, 0, 0])
# assert sol.minCameraCover(build_tree([0, 0, None, 0, 0])) == 1

# root = build_tree([0, 0, None, 0, None, 0, None, None, 0])

# print(sol.minCameraCover(root))
# print(root)

tree = build_tree([0, 0, None, 0, None, 0, None, 0, None, 0])


Solution().minCameraCover(tree) == 2
print(tree)


# assert Solution().minCameraCover(build_tree([0])) == 1
# assert Solution().minCameraCover(build_tree([0] * 1000)) == 288
# assert Solution().minCameraCover(build_tree([0] + [None] * 999)) == 1

tree = build_tree([0, 0, 0, None, None, 0, 0, None, None, 0, 0])


print(Solution().minCameraCover(tree))
print(tree)

assert Solution().minCameraCover(tree) == 3
assert Solution().minCameraCover(build_tree([0] * 10)) == 3

assert (
    Solution().minCameraCover(build_tree([0, 0, 0, 0, 0, None, None, None, None, 0, 0]))
    == 3
)


assert Solution().minCameraCover(build_tree([0, 0, 0, 0, 0, 0, 0])) == 2
assert Solution().minCameraCover(build_tree([0, None, 0, None, 0, None, 0])) == 2
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
    Solution().minCameraCover(build_tree([0, None, 0, 0, None, None, 0, 0, None])) == 2
)
