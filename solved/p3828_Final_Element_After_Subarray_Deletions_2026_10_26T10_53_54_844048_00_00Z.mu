# URL: https://leetcode.com/problems/final-element-after-subarray-deletions/description/?envType=problem-list-v2&envId=vn57k9wr
#
# 3828. Final Element After Subarray Deletions
#
# You are given an integer array nums.
#
# Two players, Alice and Bob, play a game in turns, with Alice playing first.
#
# - In each turn, the current player chooses any nonempty subarray nums[l..r] such that r - l + 1 < m, where m is the current length of the array.
# - The selected subarray is removed, and the remaining elements are concatenated to form the new array.
# - The game continues until only one element remains.
#
# Alice aims to maximize the final element, while Bob aims to minimize it. Assuming both play optimally, return the value of the final remaining element.
#
# Example 1:
#
# Input: nums = [1,5,2]
# Output: 2
# Explanation:
# One valid optimal strategy:
# - Alice removes [1], array becomes [5, 2].
# - Bob removes [5], array becomes [2]. Thus, the answer is 2.
#
# Example 2:
#
# Input: nums = [3,7]
# Output: 7
# Explanation:
# Alice removes [3], leaving the array [7]. Since Bob cannot play a turn now, the answer is 7.
#
# Constraints:
#
#     1 <= nums.length <= 10^5
#     1 <= nums[i] <= 10^5
#
# ---
# solution provided in the hints... weird question.
# LEETCODE: Accepted (2 ms, 33.6 MB)

# mu 0.13

class Solution
  def finalElement(nums: [int]) -> int
    max(nums[0], nums[len(nums) - 1])


sol = Solution()

print(sol.finalElement([1, 5, 2]))  # 2

assert sol.finalElement([1, 5, 2]) == 2
assert sol.finalElement([3, 7]) == 7
assert Solution().finalElement([1]) == 1
assert Solution().finalElement([2, 2]) == 2
assert Solution().finalElement([5, 1]) == 5
assert Solution().finalElement([1, 2, 3, 4, 5]) == 5
assert Solution().finalElement([5, 4, 3, 2, 1]) == 5
assert Solution().finalElement([100000, 1, 100000]) == 100000
assert Solution().finalElement([1] * 100000) == 1
assert Solution().finalElement([1] + [100000] * 99998 + [2]) == 2
assert Solution().finalElement([2, 2, 2, 2, 2]) == 2
assert Solution().finalElement([10 ** 5]) == 100000
assert Solution().finalElement([10 ** 5, 10 ** 5]) == 100000
assert Solution().finalElement([10 ** 5] + [1] * 99998 + [10 ** 5]) == 100000
