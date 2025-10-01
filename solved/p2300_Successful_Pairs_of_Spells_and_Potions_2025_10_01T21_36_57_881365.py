"""
URL: https://leetcode.com/problems/successful-pairs-of-spells-and-potions/description/?envType=study-plan-v2&envId=leetcode-75

2300. Successful Pairs of Spells and Potions

You are given two positive integer arrays spells and potions, of length n and m respectively, where spells[i] represents the strength of the ith spell and potions[j] represents the strength of the jth potion.

You are also given an integer success. A spell and potion pair is considered successful if the product of their strengths is at least success.

Return an integer array pairs of length n where pairs[i] is the number of potions that will form a successful pair with the ith spell.


Example 1:

Input: spells = [5,1,3], potions = [1,2,3,4,5], success = 7
Output: [4,0,3]
Explanation:
- 0th spell: 5 * [1,2,3,4,5] = [5,10,15,20,25]. 4 pairs are successful.
- 1st spell: 1 * [1,2,3,4,5] = [1,2,3,4,5]. 0 pairs are successful.
- 2nd spell: 3 * [1,2,3,4,5] = [3,6,9,12,15]. 3 pairs are successful.
Thus, [4,0,3] is returned.

Example 2:

Input: spells = [3,1,2], potions = [8,5,8], success = 16
Output: [2,0,2]
Explanation:
- 0th spell: 3 * [8,5,8] = [24,15,24]. 2 pairs are successful.
- 1st spell: 1 * [8,5,8] = [8,5,8]. 0 pairs are successful.
- 2nd spell: 2 * [8,5,8] = [16,10,16]. 2 pairs are successful.
Thus, [2,0,2] is returned.


Constraints:

        n == spells.length
        m == potions.length
        1 <= n, m <= 105
        1 <= spells[i], potions[i] <= 105
        1 <= success <= 1010
"""

from typing import List
from functools import cache


class Solution:
    def successfulPairs(
        self, spells: List[int], potions: List[int], success: int
    ) -> List[int]:

        def bin_search_first_valid_spell(spell, success):
            left, right = 0, len(potions) - 1
            ans = 0
            while left <= right:
                mid = (left + right) // 2
                res = potions[mid] * spell
                if res < success:
                    left = mid + 1
                elif res >= success:
                    right = mid - 1
                    if potions[mid - 1] * spell < success:
                        break
            return mid if potions[mid] * spell >= success else None

        @cache
        def get_num_valid_spells(spell, success):
            first_idx = bin_search_first_valid_spell(spell, success)
            if first_idx is None:
                return 0
            else:
                return len(potions) - first_idx

        potions.sort()

        count = []
        for spell in spells:
            num = get_num_valid_spells(spell, success)
            count.append(num)
        return count


sol = Solution()


def brute_force(spells, potions, success):
    return [sum(1 for p in potions if s * p >= success) for s in spells]


spells = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
potions = [1, 2, 3, 4, 5]
success = 7
res = sol.successfulPairs(spells, potions, success)
expected = brute_force(spells, potions, success)
assert res == expected

spells = [5, 1, 3]
potions = [1, 2, 3, 4, 5]
success = 7
res = sol.successfulPairs(spells, potions, success)
expected = brute_force(spells, potions, success)
assert res == expected

spells = [3, 1, 2]
potions = [8, 5, 8]
success = 16
res = sol.successfulPairs(spells, potions, success)
expected = brute_force(spells, potions, success)
assert res == expected

spells = [10]
potions = [1, 2, 3]
success = 5
res = sol.successfulPairs(spells, potions, success)
expected = brute_force(spells, potions, success)
assert res == expected

spells = [1]
potions = [1]
success = 2
res = sol.successfulPairs(spells, potions, success)
expected = brute_force(spells, potions, success)
assert res == expected

spells = [1]
potions = [1]
success = 1
res = sol.successfulPairs(spells, potions, success)
expected = brute_force(spells, potions, success)
assert res == expected

spells = [2]
potions = [1, 1, 2, 2]
success = 3
res = sol.successfulPairs(spells, potions, success)
expected = brute_force(spells, potions, success)
assert res == expected

spells = [1, 2]
potions = [1, 2, 3]
success = 1
res = sol.successfulPairs(spells, potions, success)
expected = brute_force(spells, potions, success)
assert res == expected

spells = [2]
potions = [3]
success = 6
res = sol.successfulPairs(spells, potions, success)
expected = brute_force(spells, potions, success)
assert res == expected

spells = [100000]
potions = [100000]
success = 100000 * 100000
res = sol.successfulPairs(spells, potions, success)
expected = brute_force(spells, potions, success)
assert res == expected

spells = [100000]
potions = [100000]
success = 100000 * 100000 + 1
res = sol.successfulPairs(spells, potions, success)
expected = brute_force(spells, potions, success)
assert res == expected

spells = [1, 100000]
potions = [1, 100000]
success = 100000
res = sol.successfulPairs(spells, potions, success)
expected = brute_force(spells, potions, success)
assert res == expected

spells = [3]
potions = [1, 2, 2, 3, 3]
success = 6
res = sol.successfulPairs(spells, potions, success)
expected = brute_force(spells, potions, success)
assert res == expected
