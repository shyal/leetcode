"""
EPI 5.13 Sample online data

Given an iterator stream of distinct integers and an integer k, read
stream once and return a list of k of its elements, chosen at random.
Every subset of k elements must be equally likely. The length of stream
is not known before the end. Use reservoir sampling.

Example 1:

Input: stream = iter([3, 7, 5, 11]), k = 2
Output: [11, 3]
Explanation: The stream has six subsets of 2 elements. Each subset is
returned with probability 1/6, in any order.

Example 2:

Input: stream = iter([1, 2, 3]), k = 3
Output: [1, 2, 3]
Explanation: All of the stream, in any order.

Constraints:

    1 <= k <= number of elements in stream <= 10^6

    REQUIRED: O(n) time and O(k) extra space, where n is the number of
    elements in stream. NO list(stream), NO sample().
"""


class Solution:
    def online_random_sample(self, stream: Iterator[int], k: int) -> list[int]:
        pass


sol = Solution()


def sample_counts(values, k, trials):
    return Counter(frozenset(sol.online_random_sample(iter(values), k)) for _ in range(trials))


print(sol.online_random_sample(iter([3, 7, 5, 11]), 2))  # [11, 3], or any other 2 elements

# r = sol.online_random_sample(iter([3, 7, 5, 11]), 2)
# assert len(r) == 2 and len(set(r)) == 2 and set(r) <= {3, 7, 5, 11}
# assert sorted(sol.online_random_sample(iter([1, 2, 3]), 3)) == [1, 2, 3]
# assert sol.online_random_sample(iter([9]), 1) == [9]
# assert sorted(sol.online_random_sample((x * x for x in range(5)), 5)) == [0, 1, 4, 9, 16]
# c = sample_counts([3, 7, 5, 11], 2, 60000)
# assert len(c) == 6 and all(9500 < v < 10500 for v in c.values())
# c = sample_counts([3, 7, 5, 11], 3, 40000)
# assert len(c) == 4 and all(9500 < v < 10500 for v in c.values())
# c = sample_counts([1, 2, 3, 4, 5, 6], 1, 60000)
# assert len(c) == 6 and all(9500 < v < 10500 for v in c.values())
# c = sample_counts(list(range(10)), 1, 50000)
# assert 4500 < c[frozenset([0])] < 5500 and 4500 < c[frozenset([9])] < 5500
# r = sol.online_random_sample(iter(range(10 ** 6)), 3)
# assert len(r) == 3 and len(set(r)) == 3 and all(0 <= x < 10 ** 6 for x in r)
# r = sol.online_random_sample(iter(range(10 ** 5)), 10 ** 5)
# assert sorted(r) == list(range(10 ** 5))
