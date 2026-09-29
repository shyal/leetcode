"""
DRILL: Largest By Flag
TRAINS: greedy-sort-take

Given an integer list nums and a boolean list flag of the same length,
split nums into two lists: the values whose flag is True and the values
whose flag is False. Sort each list. Then walk flag from left to right.
At each position, take the largest value still in the list of that flag.
Return the values taken, in order.

Example 1:

Input: nums = [3, 1, 4, 1, 5], flag = [True, False, True, False, True]
Output: [5, 1, 4, 1, 3]
Explanation: The True values 3, 4, 5 fill positions 0, 2 and 4, largest
first. The False values 1, 1 fill positions 1 and 3.

Example 2:

Input: nums = [2, 9, 6, 7, 1], flag = [False, True, True, False, False]
Output: [7, 9, 6, 2, 1]
Explanation: The True values 9, 6 keep positions 1 and 2. The False
values 2, 7, 1 fill positions 0, 3 and 4 as 7, 2, 1.

Example 3:

Input: nums = [4, 8, 2], flag = [True, True, True]
Output: [8, 4, 2]

Constraints:

    1 <= len(nums) == len(flag) <= 10^5
    0 <= nums[i] <= 10^9

    REQUIRED: O(n log n) time, two sorts and one pass over flag. NO
    search for the largest value at every position; that is O(n^2).
"""


class Solution:
    def largestByFlag(self, nums: List[int], flag: List[bool]) -> List[int]:
        pass


sol = Solution()

print(sol.largestByFlag([3, 1, 4, 1, 5], [True, False, True, False, True]))  # [5, 1, 4, 1, 3]

# assert sol.largestByFlag([3, 1, 4, 1, 5], [True, False, True, False, True]) == [5, 1, 4, 1, 3]
# assert sol.largestByFlag([2, 9, 6, 7, 1], [False, True, True, False, False]) == [7, 9, 6, 2, 1]
# assert sol.largestByFlag([4, 8, 2], [True, True, True]) == [8, 4, 2]
# assert sol.largestByFlag([7], [False]) == [7]
# assert sol.largestByFlag([1, 2, 3, 4, 5, 6], [False, False, False, True, True, True]) == [3, 2, 1, 6, 5, 4]
# assert sol.largestByFlag([5, 5, 5, 5], [True, False, True, False]) == [5, 5, 5, 5]
# assert sol.largestByFlag([0, 9, 0, 9, 0, 9], [True, False, True, False, True, False]) == [0, 9, 0, 9, 0, 9]
# assert sol.largestByFlag([1, 10, 2, 20, 3, 30], [True, False, True, False, True, False]) == [3, 30, 2, 20, 1, 10]
# assert sol.largestByFlag(list(range(1000)), [True] * 1000) == list(range(999, -1, -1))
# assert sol.largestByFlag(list(range(1000)), [True, False] * 500) == [998 - i if i % 2 == 0 else 1000 - i for i in range(1000)]
