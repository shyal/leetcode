"""
EPI 4.10 Generate uniform random numbers

Given two integers lower_bound and upper_bound, return an integer from
lower_bound to upper_bound, both included, chosen uniformly at random:
each of the upper_bound - lower_bound + 1 values has the same
probability. The only source of randomness is zero_one_random(), which
returns 0 or 1, each with probability 1/2.

Example 1:

Input: lower_bound = 1, upper_bound = 6
Output: 1, 2, 3, 4, 5 or 6, each with probability 1/6

Example 2:

Input: lower_bound = 0, upper_bound = 4
Output: 0, 1, 2, 3 or 4, each with probability 1/5

Example 3:

Input: lower_bound = 7, upper_bound = 7
Output: 7

Constraints:

    -10^9 <= lower_bound <= upper_bound <= 10^9

    REQUIRED: O(log n) expected time, where n = upper_bound -
    lower_bound + 1. NO random module functions: NO randrange(), NO
    randint(), NO random(), NO choice(), NO getrandbits().
"""


def zero_one_random() -> int:
    return randrange(2)


class Solution:
    def uniform_random(self, lower_bound: int, upper_bound: int) -> int:
        pass


sol = Solution()

print(sol.uniform_random(1, 6))  # 1, 2, 3, 4, 5 or 6

# xs = [sol.uniform_random(1, 6) for _ in range(60000)]
# assert all(1 <= v <= 6 for v in xs)
# assert all(abs(xs.count(v) - 10000) < 600 for v in range(1, 7))
# xs = [sol.uniform_random(0, 4) for _ in range(50000)]
# assert all(0 <= v <= 4 for v in xs)
# assert all(abs(xs.count(v) - 10000) < 600 for v in range(5))
# xs = [sol.uniform_random(-3, 3) for _ in range(70000)]
# assert all(-3 <= v <= 3 for v in xs)
# assert all(abs(xs.count(v) - 10000) < 600 for v in range(-3, 4))
# xs = [sol.uniform_random(0, 1) for _ in range(20000)]
# assert all(abs(xs.count(v) - 10000) < 600 for v in range(2))
# xs = [sol.uniform_random(0, 7) for _ in range(80000)]
# assert all(abs(xs.count(v) - 10000) < 600 for v in range(8))
# assert all(sol.uniform_random(7, 7) == 7 for _ in range(100))
# assert all(sol.uniform_random(-10 ** 9, -10 ** 9) == -10 ** 9 for _ in range(100))
# xs = [sol.uniform_random(-10 ** 9, 10 ** 9) for _ in range(10000)]
# assert all(-10 ** 9 <= v <= 10 ** 9 for v in xs)
# assert len(set(xs)) > 9990
# assert abs(sum(xs) / len(xs)) < 4 * 10 ** 7
# assert sum(v < 0 for v in xs) > 4500 and sum(v > 0 for v in xs) > 4500
