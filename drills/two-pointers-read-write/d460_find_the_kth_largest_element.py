"""
EPI 11.8 Find the kth largest element

Given an integer k and an array A of distinct integers, return the kth
largest value of A. The 1st largest value is the largest value. You
are allowed to reorder A. Use quickselect.

Example 1:

Input: k = 2, A = [3, 1, -1, 2]
Output: 2

Example 2:

Input: k = 4, A = [3, 1, -1, 2]
Output: -1
Explanation: the 4th largest of four values is the smallest.

Example 3:

Input: k = 1, A = [5]
Output: 5

Constraints:

    1 <= k <= len(A) <= 10^5
    -10^9 <= A[i] <= 10^9
    The values of A are distinct.

    REQUIRED: O(n) expected time, O(1) extra space. NO sorting, NO
    sorted(), NO heapq, NO copy of A.
"""


class Solution:
    def find_kth_largest(self, k: int, A: list[int]) -> int:
        pass


sol = Solution()

print(sol.find_kth_largest(2, [3, 1, -1, 2]))  # 2

# assert sol.find_kth_largest(2, [3, 1, -1, 2]) == 2
# assert sol.find_kth_largest(4, [3, 1, -1, 2]) == -1
# assert sol.find_kth_largest(1, [3, 1, -1, 2]) == 3
# assert sol.find_kth_largest(3, [3, 1, -1, 2]) == 1
# assert sol.find_kth_largest(1, [5]) == 5
# assert sol.find_kth_largest(1, [1, 2]) == 2
# assert sol.find_kth_largest(2, [1, 2]) == 1
# assert sol.find_kth_largest(3, [9, 8, 7, 6, 5]) == 7
# assert sol.find_kth_largest(3, [5, 6, 7, 8, 9]) == 7
# assert sol.find_kth_largest(2, [-10 ** 9, 10 ** 9, 0]) == 0
# A = list(range(10 ** 5))
# assert sol.find_kth_largest(1, A) == 10 ** 5 - 1
# assert sol.find_kth_largest(10 ** 5, A) == 0
# assert sol.find_kth_largest(5 * 10 ** 4, A) == 5 * 10 ** 4
# B = random.Random(7).sample(range(-10 ** 9, 10 ** 9), 10 ** 5)
# want = sorted(B, reverse=True)
# assert sol.find_kth_largest(1, B) == want[0]
# assert sol.find_kth_largest(12345, B) == want[12344]
# assert sol.find_kth_largest(10 ** 5, B) == want[-1]
