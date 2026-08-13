"""
URL: https://leetcode.com/problems/longest-consecutive-sequence/description/?envType=problem-list-v2&envId=vn57k9wr

128. Longest Consecutive Sequence

Given an unsorted array of integers nums, return the length of the longest
consecutive elements sequence.

You must write an algorithm that runs in O(n) time.


Example 1:

Input: nums = [100,4,200,1,3,2]
Output: 4
Explanation: The longest consecutive elements sequence is [1, 2, 3, 4].
Therefore its length is 4.

Example 2:

Input: nums = [0,3,7,2,5,8,4,6,0,1]
Output: 9

Example 3:

Input: nums = [1,0,1,2]
Output: 3


Constraints:

    0 <= nums.length <= 10^5
    -10^9 <= nums[i] <= 10^9

---

Sacrificial question. Looked up the answer. Learning moment, and the first question in the
generate-and-test-neighbors node.

We can't sort, because of the O(1) constraint. So we put the numbers in a set, and generate the neighbour
candidates with while m + 1 in S.. these are basically guesses, that we test with set membership. If
we had a lucky guess, then we increment m.

m - n + 1 means we're tracking the actual count, not the value.

"""


class Solution:
    def longestConsecutive_v1(self, nums: List[int]) -> int:
        S = set(nums)
        res = 0
        for n in S:
            if n - 1 not in S:
                m = n
                while m + 1 in S:
                    m += 1
                res = max(res, m - n + 1)
        return res

    def longestConsecutive_v2(self, nums: List[int]) -> int:
        S = set(nums)
        res = 0
        for n in S:
            if n - 1 not in S:
                m = n
                count = 1
                while m + 1 in S:
                    m += 1
                    count += 1
                res = max(res, count)
        return res

    def longestConsecutive(self, nums: List[int]) -> int:
        v1 = self.longestConsecutive_v1(nums)
        v2 = self.longestConsecutive_v2(nums)
        assert v1 == v2
        return v1

sol = Solution()

# print(sol.longestConsecutive([100, 4, 200, 1, 3, 2]))  # 4

assert sol.longestConsecutive([100, 4, 200, 1, 3, 2]) == 4
assert sol.longestConsecutive([0, 3, 7, 2, 5, 8, 4, 6, 0, 1]) == 9
assert sol.longestConsecutive([1, 0, 1, 2]) == 3
assert sol.longestConsecutive([]) == 0
assert sol.longestConsecutive([7]) == 1
assert sol.longestConsecutive([2, 2, 2]) == 1
assert sol.longestConsecutive([1, 3, 5, 7]) == 1
assert sol.longestConsecutive([5, 4, 3, 2, 1]) == 5
assert sol.longestConsecutive([-2, -1, 0, 1]) == 4
assert sol.longestConsecutive([-3, -2, -1, 0, 1, 2, 3]) == 7
assert sol.longestConsecutive([-1000000000, 1000000000]) == 1
assert sol.longestConsecutive([-1000000000, -999999999, -999999998]) == 3
assert sol.longestConsecutive([10, 11, 12, 50, 51, 52]) == 3
assert sol.longestConsecutive([9, 1, 4, 7, 3, -1, 0, 5, 8, -1, 6]) == 7
assert sol.longestConsecutive([0, 0]) == 1