"""
URL: https://leetcode.com/problems/convert-sorted-array-to-binary-search-tree/description/?envType=problem-list-v2&envId=vn57k9wr

108. Convert Sorted Array to Binary Search Tree

Given an integer array nums where the elements are sorted in ascending order,
convert it to a height-balanced binary search tree.


Example 1:

Input: nums = [-10,-3,0,5,9]
Output: [0,-3,9,-10,null,5]
Explanation: [0,-10,5,null,-3,null,9] is also accepted.

Example 2:

Input: nums = [1,3]
Output: [3,1]
Explanation: [1,null,3] and [3,1] are both height-balanced BSTs.


Constraints:

    1 <= nums.length <= 10^4
    -10^4 <= nums[i] <= 10^4
    nums is sorted in a strictly increasing order.
"""


class Solution:
    def sortedArrayToBST(self, nums: List[int]) -> Optional[TreeNode]:
        def helper(i, nums):
            left = nums[0:i]
            right = nums[i+1:]
            left_subtree = helper((len(left)-1) // 2, left) if nums else None
            right_subtree = helper((len(right)-1) // 2, right) if nums else None
            if nums:
                return TreeNode(nums[i], left_subtree, right_subtree)
        return helper(i=(len(nums)-1)//2, nums=nums)


sol = Solution()

r = sol.sortedArrayToBST([1, 2, 3, 4, 5, 6])

# draw_tree(r)

for nums in (
    [-10, -3, 0, 5, 9],
    [1, 3],
    [5],
    [0],
    [-10000],
    [10000],
    [1, 2, 3],
    [1, 2, 3, 4],
    [-10000, 10000],
    [-3, -2, -1, 0],
    [1, 2, 3, 4, 5, 6, 7],
    list(range(-5000, 5000)),
    list(range(-10000, 10001, 2)),
):
    root = sol.sortedArrayToBST(nums)
    assert get_inorder(root) == nums
    assert is_valid_bst(root)
    assert is_balanced(root)

assert sol.sortedArrayToBST([]) is None

root = sol.sortedArrayToBST([5])
assert root.val == 5
assert root.left is None
assert root.right is None

root = sol.sortedArrayToBST([1, 3])
assert root.val == 1
assert root.left is None
assert root.right.val == 3
assert root.right.left is None
assert root.right.right is None

root = sol.sortedArrayToBST([1, 2, 3])
assert root.val == 2
assert root.left.val == 1
assert root.right.val == 3

root = sol.sortedArrayToBST([1, 2, 3, 4])
assert root.val == 2
assert root.left.val == 1
assert root.right.val == 3
assert root.right.left is None
assert root.right.right.val == 4

root = sol.sortedArrayToBST([-10, -3, 0, 5, 9])
assert root.val == 0
assert root.left.val == -10
assert root.left.left is None
assert root.left.right.val == -3
assert root.right.val == 5
assert root.right.left is None
assert root.right.right.val == 9

root = sol.sortedArrayToBST([1, 2, 3, 4, 5, 6, 7])
assert root.val == 4
assert root.left.val == 2
assert root.left.left.val == 1
assert root.left.right.val == 3
assert root.right.val == 6
assert root.right.left.val == 5
assert root.right.right.val == 7

root = sol.sortedArrayToBST([-10000, 0, 10000])
assert root.val == 0
assert root.left.val == -10000
assert root.right.val == 10000


def height(node):
    if node is None:
        return -1
    return 1 + max(height(node.left), height(node.right))


assert height(sol.sortedArrayToBST([42])) == 0
assert height(sol.sortedArrayToBST([1, 3])) == 1
assert height(sol.sortedArrayToBST([1, 2, 3])) == 1
assert height(sol.sortedArrayToBST([1, 2, 3, 4])) == 2
assert height(sol.sortedArrayToBST(list(range(8)))) == 3
assert height(sol.sortedArrayToBST(list(range(10000)))) == 13