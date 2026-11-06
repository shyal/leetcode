"""
Given a list arr of distinct nonnegative integers, return the smallest
nonnegative integer that is not in arr.

Example 1:

Input: arr = [100000]
Output: 0
Explanation: 0 is not in arr. The largest value plus one is 100001,
which is not the smallest.

Example 2:

Input: arr = [1, 0, 3, 4, 5]
Output: 2

Example 3:

Input: arr = [0, 1, 2, 3]
Output: 4
Explanation: every value from 0 to 3 is in arr.

Constraints:

    1 <= len(arr) <= 10^5
    0 <= arr[i] <= 2^31 - 1
    The values of arr are distinct.

    REQUIRED: O(n) time. NO sorting, NO set, NO dict.
"""


class Solution:
    def get_different_number(self, arr: list[int]) -> int:
        pass


sol = Solution()

print(sol.get_different_number([100000]))  # 0

# assert sol.get_different_number([100000]) == 0
# assert sol.get_different_number([1, 0, 3, 4, 5]) == 2
# assert sol.get_different_number([0, 1, 2, 3]) == 4
# assert sol.get_different_number([0]) == 1
# assert sol.get_different_number([0, 1, 2]) == 3
# assert sol.get_different_number([1, 3, 0, 2]) == 4
# assert sol.get_different_number([0, 100000]) == 1
# assert sol.get_different_number([0, 99999, 100000]) == 1
# assert sol.get_different_number([0, 5, 4, 1, 3, 6, 2]) == 7
# assert sol.get_different_number([2 ** 31 - 1]) == 0
# assert sol.get_different_number([0, 2 ** 31 - 1]) == 1
# assert sol.get_different_number(list(range(10 ** 5))) == 10 ** 5
# assert sol.get_different_number(list(range(1, 10 ** 5 + 1))) == 0
# assert sol.get_different_number(list(range(10 ** 5 - 1, -1, -1))) == 10 ** 5
