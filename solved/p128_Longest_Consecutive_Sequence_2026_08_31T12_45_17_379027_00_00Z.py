"""
URL: https://leetcode.com/problems/longest-consecutive-sequence/description/?envType=problem-list-v2&envId=vn57k9wr

128. Longest Consecutive Sequence

Given an unsorted array of integers nums, return the length of the longest consecutive elements sequence.

You must write an algorithm that runs in O(n) time.

Example 1:

Input: nums = [100,4,200,1,3,2]
Output: 4
Explanation: The longest consecutive elements sequence is [1, 2, 3, 4]. Therefore its length is 4.

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

I vaguely remember this.. it has to do with generating candidates
and testing set membership.

[100,4,200,1,3,2]

So maybe loop through the numbers and check if n + 1
exists, but i'm not really sure how to turn this into the
longest consecurity sequence

Algorithm says O(n) but has no space requirement. So extra space is game.


[100,4,200,1,3,2]

0: 100 + 1 is not present
1: 4 + 1 is not present
2: ...
3: 1 + 1 is present.
4: 3 + 1 is present.
5: 2 + 1 is present.

But that's pure coincidence based on the numbers we were given.

[1,100,4,200,3,2]

0: 1 + 1 is present
1: 100 + 1 is not
2: 4 + 1 is not
3: ...
4: 3 + 1 is present
5: 2 + 1 is present


Hint: your check "is n + 1 present?" runs from every number, which is why the order looked like coincidence. Ask a different question first: which numbers in the set can be the start of a run? Only those are worth walking from. Plain words: starting at a number n, check n + 1, then n + 2, then n + 3, and keep going as long as each one is in the set, counting how many you found. That count is the length of the run that begins at n.
"""


class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        numss = set(nums)
        _min = float("inf")
        longest = 0

        for i in range(len(nums)):
            if nums[i] < _min:
                length = 0
                gen = nums[i]
                while gen in numss:
                    length += 1
                    longest = max(longest, length)
                    gen += 1
            _min = min(nums[i], _min)

        return longest


sol = Solution()

print(sol.longestConsecutive([100, 4, 200, 1, 3, 2]))  # 4

assert sol.longestConsecutive([100, 4, 200, 1, 3, 2]) == 4
assert sol.longestConsecutive([0, 3, 7, 2, 5, 8, 4, 6, 0, 1]) == 9
assert sol.longestConsecutive([1, 0, 1, 2]) == 3

assert sol.longestConsecutive([]) == 0
assert sol.longestConsecutive([1]) == 1
assert sol.longestConsecutive([2, 2, 2, 2]) == 1
assert sol.longestConsecutive([-1, -2, -3, -4]) == 4
assert sol.longestConsecutive([10**9, 10**9 - 1, 10**9 - 2]) == 3
assert sol.longestConsecutive([-(10**9), -(10**9) + 1, -(10**9) + 2]) == 3
assert sol.longestConsecutive(list(range(100000))) == 100000
assert sol.longestConsecutive(list(range(0, 100000, 2))) == 1
assert sol.longestConsecutive([5, 4, 3, 2, 1]) == 5
assert sol.longestConsecutive([1, 3, 5, 7, 9, 11]) == 1
assert sol.longestConsecutive([1, 2, 2, 3, 4, 4, 5]) == 5
assert sol.longestConsecutive([0]) == 1
