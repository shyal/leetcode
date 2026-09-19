"""
DRILL: One More Cat
TRAINS: marginal-gain

A cage holds t animals, and a of them are cats. The cat ratio of the cage
is a / t. Given a and t, return how much the cat ratio grows when one more
cat is put in the cage.

Example 1:

Input: a = 1, t = 2
Output: 0.16666666666666663
Explanation: The ratio goes from 1/2 to 2/3.

Example 2:

Input: a = 2, t = 2
Output: 0.0
Explanation: Every animal is a cat before and after.

Example 3:

Input: a = 3, t = 9
Output: 0.06666666666666665

Constraints:

    1 <= a <= t <= 10^5

    REQUIRED: must run in O(1). NO loop. The new ratio counts the new cat
    in both the cats and the animals; a ratio over t alone is a fail.
"""


class Solution:

    def gain(self, a: int, t: int) -> float:
        return ((a + 1) / (t + 1)) - (a / t)


sol = Solution()

print(sol.gain(1, 2))  # 0.16666666666666663

assert abs(sol.gain(1, 2) - 1 / 6) < 1e-9
assert sol.gain(2, 2) == 0.0
assert abs(sol.gain(3, 9) - 1 / 15) < 1e-9
assert abs(sol.gain(1, 1)) < 1e-9
assert abs(sol.gain(3, 5) - (4 / 6 - 3 / 5)) < 1e-9
assert abs(sol.gain(99999, 100000) - (100000 / 100001 - 99999 / 100000)) < 1e-9
assert sol.gain(1, 100000) > 0
