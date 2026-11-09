"""
EPI 10.5 Compute the median of online data

Given an iterator sequence of integers, return a list of floats whose
entry i is the median of the first i + 1 elements of sequence. The
median of an even number of values is the mean of the two middle
values.

Example 1:

Input: sequence = iter([5, 15, 1, 3, 8])
Output: [5.0, 10.0, 5.0, 4.0, 5.0]
Explanation: after 5 and 15 the median is (5 + 15) / 2 = 10. After 1,
3 and 5 and 15 it is (3 + 5) / 2 = 4.

Example 2:

Input: sequence = iter([2, 2])
Output: [2.0, 2.0]

Example 3:

Input: sequence = iter([])
Output: []

Constraints:

    0 <= n <= 10^5, where n is the number of elements
    -10^9 <= element <= 10^9

    REQUIRED: O(log n) time for each element and O(n) space. NO
    sorted(), NO list.sort(), NO bisect.insort(), NO
    statistics.median().
"""


class Solution:
    def online_median(self, sequence: Iterator[int]) -> list[float]:
        pass


sol = Solution()

print(sol.online_median(iter([5, 15, 1, 3, 8])))  # [5.0, 10.0, 5.0, 4.0, 5.0]

# assert sol.online_median(iter([5, 15, 1, 3, 8])) == [5.0, 10.0, 5.0, 4.0, 5.0]
# assert sol.online_median(iter([2, 2])) == [2.0, 2.0]
# assert sol.online_median(iter([])) == []
# assert sol.online_median(iter([7])) == [7.0]
# assert sol.online_median(iter([-3])) == [-3.0]
# assert sol.online_median(iter([1, 2])) == [1.0, 1.5]
# assert sol.online_median(iter([2, 1])) == [2.0, 1.5]
# assert sol.online_median(iter([1, 2, 3, 4, 5])) == [1.0, 1.5, 2.0, 2.5, 3.0]
# assert sol.online_median(iter([5, 4, 3, 2, 1])) == [5.0, 4.5, 4.0, 3.5, 3.0]
# assert sol.online_median(iter([10, -10, 10, -10])) == [10.0, 0.0, 10.0, 0.0]
# assert sol.online_median(iter([0, 0, 0, 100, -100])) == [0.0, 0.0, 0.0, 0.0, 0.0]
# assert sol.online_median(iter([-10 ** 9, 10 ** 9, 10 ** 9])) == [-1e9, 0.0, 1e9]
# assert sol.online_median(iter(range(10 ** 5)))[-1] == 49999.5
# assert sol.online_median(iter(range(10 ** 5, 0, -1)))[::25000] == [100000.0, 87500.0, 75000.0, 62500.0]
# assert sol.online_median(iter(i * 7919 % 10 ** 5 for i in range(10 ** 5)))[-1] == 49999.5
