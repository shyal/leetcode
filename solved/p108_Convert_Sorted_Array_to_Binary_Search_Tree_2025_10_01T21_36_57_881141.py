"""
URL: https://leetcode.com/problems/convert-sorted-array-to-binary-search-tree/description/

108. Convert Sorted Array to Binary Search Tree

Given an integer array nums where the elements are sorted in ascending order, convert it to a height-balanced binary search tree.


Example 1:

Input: nums = [-10,-3,0,5,9]
Output: [0,-3,9,-10,null,5]
Explanation: [0,-10,5,null,-3,null,9] is also accepted:

Example 2:

Input: nums = [1,3]
Output: [3,1]
Explanation: [1,null,3] and [3,1] are both height-balanced BSTs.


Constraints:

        1 <= nums.length <= 104
        -104 <= nums[i] <= 104
        nums is sorted in a strictly increasing order.

------

  [2]
 ┌─┴─┐
[1] [4]
 /   /
[0] [3]


[1]
 /
[0]


     [3]
   ┌──┴──┐
  [1]   [5]
 ┌─┴─┐   /
[0] [2] [4]


                                 [20]
               ┌──────────────────┴───────────────────┐
              [10]                                   [30]
       ┌───────┴────────┐                   ┌─────────┴─────────┐
      [5]              [15]                [25]                [35]
   ┌───┴───┐       ┌────┴────┐         ┌────┴────┐         ┌────┴────┐
  [2]     [8]     [13]      [18]      [23]      [28]      [33]      [38]
 ┌─┴─┐   ┌─┴─┐   ┌─┴──┐    ┌─┴──┐    ┌─┴──┐    ┌─┴──┐    ┌─┴──┐    ┌─┴──┐
[1] [4] [7] [9] [12] [14] [17] [19] [22] [24] [27] [29] [32] [34] [37] [39]
 /   /   /       /         /         /         /         /         /
[0] [3] [6]     [11]      [16]      [21]      [26]      [31]      [36]


"""


class Solution:
    def sortedArrayToBST(self, nums: List[int]) -> Optional[TreeNode]:
        def helper(start, end):
            if start < end:
                mid = (start + end) // 2
                return TreeNode(nums[mid], helper(start, mid), helper(mid + 1, end))

        return helper(0, len(nums))


sol = Solution()

assert get_inorder(sol.sortedArrayToBST([-10, -3, 0, 5, 9])) == [-10, -3, 0, 5, 9]
assert is_balanced(sol.sortedArrayToBST([-10, -3, 0, 5, 9]))
assert is_valid_bst(sol.sortedArrayToBST([-10, -3, 0, 5, 9]))
assert get_inorder(sol.sortedArrayToBST([1, 3])) == [1, 3]
assert is_balanced(sol.sortedArrayToBST([1, 3]))
assert is_valid_bst(sol.sortedArrayToBST([1, 3]))
assert get_inorder(sol.sortedArrayToBST([1])) == [1]
assert is_balanced(sol.sortedArrayToBST([1]))
assert is_valid_bst(sol.sortedArrayToBST([1]))
assert get_inorder(sol.sortedArrayToBST([0, 1, 2, 3, 4, 5, 6])) == [0, 1, 2, 3, 4, 5, 6]
assert is_balanced(sol.sortedArrayToBST([0, 1, 2, 3, 4, 5, 6]))
assert is_valid_bst(sol.sortedArrayToBST([0, 1, 2, 3, 4, 5, 6]))
assert get_inorder(sol.sortedArrayToBST([-3, -2, -1])) == [-3, -2, -1]
assert is_balanced(sol.sortedArrayToBST([-3, -2, -1]))
assert is_valid_bst(sol.sortedArrayToBST([-3, -2, -1]))
assert get_inorder(sol.sortedArrayToBST([])) == []
assert is_balanced(sol.sortedArrayToBST([]))
assert is_valid_bst(sol.sortedArrayToBST([]))
assert get_inorder(sol.sortedArrayToBST([1, 2, 3])) == [1, 2, 3]
assert is_balanced(sol.sortedArrayToBST([1, 2, 3]))
assert is_valid_bst(sol.sortedArrayToBST([1, 2, 3]))
assert get_inorder(sol.sortedArrayToBST([-10000, 0, 10000])) == [-10000, 0, 10000]
assert is_balanced(sol.sortedArrayToBST([-10000, 0, 10000]))
assert is_valid_bst(sol.sortedArrayToBST([-10000, 0, 10000]))
assert get_inorder(sol.sortedArrayToBST([0, 1, 2, 3])) == [0, 1, 2, 3]
assert is_balanced(sol.sortedArrayToBST([0, 1, 2, 3]))
assert is_valid_bst(sol.sortedArrayToBST([0, 1, 2, 3]))
