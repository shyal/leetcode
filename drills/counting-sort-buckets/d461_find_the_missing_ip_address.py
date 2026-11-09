"""
EPI 11.9 Find the missing IP address

Given a list stream of 32-bit unsigned integers that does not hold all
2^32 values, return an integer from 0 to 2^32 - 1 that is not in
stream. Values in stream can repeat. Any absent value is a correct
answer.

Example 1:

Input: stream = [0, 1, 2, 4]
Output: 3, or any other value from 5 to 2^32 - 1
Explanation: every value from 0 to 2^32 - 1 except 0, 1, 2 and 4 is
absent.

Example 2:

Input: stream = []
Output: any value from 0 to 2^32 - 1

Example 3:

Input: stream = [4294967295, 0]
Output: any value from 1 to 2^32 - 2

Constraints:

    0 <= len(stream) <= 10^6
    0 <= stream[i] <= 2^32 - 1

    REQUIRED: O(n) time, O(2^16) extra space. NO set or dict of the
    values, NO sorting, NO bitset of 2^32 bits.
"""


class Solution:
    def find_missing_element(self, stream: list[int]) -> int:
        pass


sol = Solution()

print(sol.find_missing_element([0, 1, 2, 4]))  # 3, or a value from 5 to 2^32 - 1


def absent(stream):
    got = sol.find_missing_element(stream)
    return 0 <= got < 2 ** 32 and got not in set(stream)


# assert absent([0, 1, 2, 4])
# assert absent([])
# assert absent([4294967295, 0])
# assert absent([0])
# assert absent([2 ** 32 - 1])
# assert absent([7, 7, 7])
# assert absent([2 ** 16, 2 ** 16 - 1, 2 ** 17])
# assert absent(list(range(2 ** 16)))
# assert absent(list(range(2 ** 17)) + [2 ** 32 - 1])
# assert absent([v for v in range(2 ** 16) if v != 12345] + [0] * 1000)
# assert absent(list(range(2 ** 32 - 2 ** 17, 2 ** 32)) + list(range(2 ** 16)))
# assert absent([v << 16 for v in range(2 ** 16)])
# assert absent([(v << 16) | 0xFFFF for v in range(2 ** 16)] + [v for v in range(2 ** 16)])
# assert absent(list(range(5 * 2 ** 16)) * 3)
