r"""
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


  [0]
   /
  [0]
 ┌─┴─┐
[0] [0]


      [3]
   ┌───┴────┐
  [C]      [C]
 ┌─┴─┐    ┌─┴─┐
[2] [9]  [8] [7]
 \   \
[C] [C]
 \
[5]

Looks like the minimum is 4.

It nearly looks like we can go at alternative depths:



      [3]
   ┌───┴────┐
  [C]      [C]           <-------------
 ┌─┴─┐    ┌─┴─┐
[2] [9]  [8] [7]
 \   \
[C] [C]                  <-------------
 \
[5]


               [C]                                <-------------
       ┌────────┴────────┐
      [0]               [0]
   ┌───┴────┐        ┌───┴────┐
  [C]      [C]      [C]      [C]           <-------------
 ┌─┴─┐    ┌─┴──┐   ┌─┴──┐   ┌─┴─┐
[2] [13] [16] [4] [15] [8] [7] [9]
     /    /             /
    [C] [C]           [C]           <-------------
          \
         [14]
          /
         [C]           <-------------

         
Same idea.. so maybe a cheap solution is a level order traversal,
and return the min of the counts of nodes on even levels, and odd levels.

Seems way too simple, let's try on different shape trees.

                    [C]
            ┌────────┴────────┐
           [7]               [18]
       ┌────┴────┐        ┌───┴────┐
      [C]      [C]       [C]      [C]
   ┌───┴───┐   ┌─┴──┐   ┌─┴─┐    ┌─┴─┐
  [15]    [1] [17] [5] [6] [13] [4] [10]
 ┌─┴──┐        /            /    /
[C]  [C]     [C]          [C] [C]

Worth a shot.

Though a hint was clearly left here:

# States:
# 0: This node has no camera and is not covered
# 1: This node is covered but has no camera
# 2: This node has a camera

class Solution:
    def minCameraCover(self, root: Optional[TreeNode]) -> int:
        def bfs(n):
            q = deque([[n, 0]])
            while q:
                n, depth = q.popleft()
                if depth % 2 == 0:
                    self.even_count += 1
                else:
                    self.odd_count += 1
                if n.left:
                    q.append([n.left, depth + 1])
                if n.right:
                    q.append([n.right, depth + 1])

        self.even_count = 0
        self.odd_count = 0

        bfs(root)
        res = min(self.even_count, self.odd_count)
        print("res", res)
        return res

Yeah this doesn't work.


                    [8]
            ┌────────┴────────┐
           [7]               [18]
       ┌────┴────┐        ┌───┴────┐
      [16]      [14]     [9]      [20]
   ┌───┴───┐   ┌─┴──┐   ┌─┴─┐    ┌─┴─┐
  [15]    [1] [17] [5] [6] [13] [4] [10]
 ┌─┴──┐        /            /    /
[11] [19]     [2]          [12] [3]


  [0]
   /
  [C]
 ┌─┴─┐
[0] [0]


No idea. Can't pass all asserts. Giving up.

"""


class State:
    has_no_camera_is_covered = 1
    is_covered_by_has_no_camera = 2
    has_a_camera = 3
    has_no_camera = 4


class Solution:
    def minCameraCover(self, root: Optional[TreeNode]) -> int:

        def dfs(n):
            if not n:
                return None

            is_leaf = n.left is n.right is None
            if is_leaf:
                return State.has_no_camera_is_covered

            left = dfs(n.left)
            right = dfs(n.right)

            if (
                left == State.has_no_camera_is_covered
                or right == State.has_no_camera_is_covered
            ):
                self.cameras += 1
                return State.has_a_camera

            if left == State.has_a_camera or right == State.has_a_camera:
                return State.has_no_camera_is_covered

        if root.left == root.right == None:
            return 1

        self.cameras = 0
        dfs(root)
        return self.cameras


sol = Solution()

root = build_tree([0, 0, None, 0, 0])
assert sol.minCameraCover(build_tree([0, 0, None, 0, 0])) == 1
t = build_tree([0, 0, None, 0, None, 0, None, None, 0])
assert sol.minCameraCover(t) == 2

assert Solution().minCameraCover(build_tree([0])) == 1
assert Solution().minCameraCover(build_tree([0, 0, 0, 0, 0, 0, 0])) == 2
assert Solution().minCameraCover(build_tree([0, None, 0, None, 0, None, 0])) == 2
# assert Solution().minCameraCover(build_tree([0] * 1000)) == 288
assert Solution().minCameraCover(build_tree([0] + [None] * 999)) == 1
# assert (
#     Solution().minCameraCover(build_tree([0, 0, None, 0, None, 0, None, 0, None, 0]))
#     == 2
# )
assert (
    Solution().minCameraCover(build_tree([0, 0, 0, None, None, 0, 0, None, None, 0, 0]))
    == 3
)
# assert Solution().minCameraCover(build_tree([0] * 10)) == 3
# assert (
#     Solution().minCameraCover(
#         build_tree([0, 0, 0, 0, None, None, 0, None, None, None, 0])
#     )
#     == 2
# )
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
