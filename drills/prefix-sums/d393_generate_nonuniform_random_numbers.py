"""
EPI 5.16 Generate nonuniform random numbers

Given a list of distinct integers values and a list of floats
probabilities of the same length, return values[i] with probability
probabilities[i]. The probabilities sum to 1.

Example 1:

Input: values = [3, 5, 7, 11], probabilities = [9 / 18, 6 / 18, 2 / 18, 1 / 18]
Output: 3
Explanation: The call returns 3 with probability 1/2, 5 with
probability 1/3, 7 with probability 1/9 and 11 with probability 1/18.

Example 2:

Input: values = [1, 2, 3], probabilities = [0.5, 0.0, 0.5]
Output: 1
Explanation: 1 and 3 are equally likely. 2 is never returned.

Example 3:

Input: values = [4], probabilities = [1.0]
Output: 4

Constraints:

    1 <= len(values) <= 10^5
    len(probabilities) == len(values)
    0 <= probabilities[i] <= 1
    The probabilities sum to 1, within float rounding.

    REQUIRED: O(n) time for each call. NO choices().
"""


class Solution:
    def nonuniform_random_number_generation(self, values: list[int], probabilities: list[float]) -> int:
        pass


sol = Solution()


def draw_counts(values, probabilities, trials):
    return Counter(sol.nonuniform_random_number_generation(values, probabilities) for _ in range(trials))


print(sol.nonuniform_random_number_generation([3, 5, 7, 11], [9 / 18, 6 / 18, 2 / 18, 1 / 18]))  # 3, half of the time

# assert sol.nonuniform_random_number_generation([3, 5, 7, 11], [9 / 18, 6 / 18, 2 / 18, 1 / 18]) in (3, 5, 7, 11)
# assert sol.nonuniform_random_number_generation([4], [1.0]) == 4
# c = draw_counts([3, 5, 7, 11], [9 / 18, 6 / 18, 2 / 18, 1 / 18], 60000)
# assert abs(c[3] - 30000) < 600 and abs(c[5] - 20000) < 600
# assert abs(c[7] - 60000 / 9) < 400 and abs(c[11] - 60000 / 18) < 300
# assert set(c) == {3, 5, 7, 11}
# c = draw_counts([1, 2, 3], [0.5, 0.0, 0.5], 20000)
# assert c[2] == 0 and 9500 < c[1] < 10500
# c = draw_counts([1, 2], [1.0, 0.0], 1000)
# assert c == {1: 1000}
# c = draw_counts([1, 2], [0.0, 1.0], 1000)
# assert c == {2: 1000}
# c = draw_counts(list(range(10)), [0.1] * 10, 50000)
# assert set(c) == set(range(10)) and all(4500 < v < 5500 for v in c.values())
# c = draw_counts([-8, 0, 8], [0.2, 0.3, 0.5], 50000)
# assert abs(c[-8] - 10000) < 500 and abs(c[0] - 15000) < 600 and abs(c[8] - 25000) < 600
# assert 0 <= sol.nonuniform_random_number_generation(list(range(10 ** 5)), [1 / 10 ** 5] * 10 ** 5) < 10 ** 5
