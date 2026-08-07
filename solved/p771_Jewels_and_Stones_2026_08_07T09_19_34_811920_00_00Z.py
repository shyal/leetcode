"""
URL: https://leetcode.com/problems/jewels-and-stones/description/?envType=problem-list-v2&envId=vn57k9wr

771. Jewels and Stones

You're given strings jewels representing the types of stones that are jewels,
and stones representing the stones you have. Each character in stones is a type
of stone you have. You want to know how many of the stones you have are also
jewels.

Letters are case sensitive, so "a" is considered a different type of stone from
"A".


Example 1:

Input: jewels = "aA", stones = "aAAbbbb"
Output: 3

Example 2:

Input: jewels = "z", stones = "ZZ"
Output: 0


Constraints:

    1 <= jewels.length, stones.length <= 50
    jewels and stones consist of only English letters.
    All the characters of jewels are unique.
"""


class Solution:
    def numJewelsInStones(self, jewels: str, stones: str) -> int:
        c = Counter(stones)
        return sum(c[x] for x in jewels)


sol = Solution()

# print(sol.numJewelsInStones("aA", "aAAbbbb"))  # 3

assert sol.numJewelsInStones("aA", "aAAbbbb") == 3
assert sol.numJewelsInStones("z", "ZZ") == 0
assert sol.numJewelsInStones("a", "a") == 1
assert sol.numJewelsInStones("a", "A") == 0
assert sol.numJewelsInStones("A", "a") == 0
assert sol.numJewelsInStones("abc", "aabbcc") == 6
assert sol.numJewelsInStones("A", "AAAAA") == 5
assert sol.numJewelsInStones("zZ", "zZzZzZ") == 6
assert sol.numJewelsInStones("abc", "xyz") == 0
assert sol.numJewelsInStones("b", "aba") == 1
assert sol.numJewelsInStones("abcdefghijklmnopqrstuvwxyz", "z") == 1
assert sol.numJewelsInStones("a", "a" * 50) == 50
assert sol.numJewelsInStones("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWX", "YZ") == 0
assert sol.numJewelsInStones("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWX", "XY") == 1
assert sol.numJewelsInStones("Aa", "aaaAAA") == 6