"""
URL: https://leetcode.com/problems/successful-pairs-of-spells-and-potions/description/?envType=problem-list-v2&envId=vn57k9wr

2300. Successful Pairs of Spells and Potions

You are given two positive integer arrays spells and potions, of length n and m
respectively, where spells[i] represents the strength of the ith spell and
potions[j] represents the strength of the jth potion.

You are also given an integer success. A spell and potion pair is considered
successful if the product of their strengths is at least success.

Return an integer array pairs of length n where pairs[i] is the number of
potions that will form a successful pair with the ith spell.


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
    1 <= n, m <= 10^5
    1 <= spells[i], potions[i] <= 10^5
    1 <= success <= 10^10
"""


class Solution:

    def successfulPairsBruteForce(self, spells: List[int], potions: List[int], success: int) -> List[int]:
        res = []
        for spell in spells:
            valid = 0
            for potion in potions:
                if spell * potion >= success:
                    valid += 1
            res.append(valid)
        return res


    def successfulPairsBS(self, spells: List[int], potions: List[int], success: int) -> List[int]:
        potions.sort()
        ret = []
        for spell in spells:
            left, right = 0, len(potions)
            while left <= right:
                mid = (left + right) // 2
                if mid >= len(potions):
                    break
                res = spell * potions[mid]
                if res >= success:
                    right = mid - 1
                else:
                    left = mid + 1
            ret.append(len(potions) - left)
        return ret


    def successfulPairs(self, spells: List[int], potions: List[int], success: int) -> List[int]:
        return self.successfulPairsBS(spells, potions, success)


sol = Solution()

print(sol.successfulPairs([5, 1, 3], [1, 2, 3, 4, 5], 7))  # [4, 0, 3]

assert sol.successfulPairs([5, 1, 3], [1, 2, 3, 4, 5], 7) == [4, 0, 3]
assert sol.successfulPairs([3, 1, 2], [8, 5, 8], 16) == [2, 0, 2]
assert sol.successfulPairs([2], [3], 6) == [1]
assert sol.successfulPairs([2], [3], 7) == [0]
assert sol.successfulPairs([1], [1], 1) == [1]
assert sol.successfulPairs([1, 2], [1, 1, 1], 1) == [3, 3]
assert sol.successfulPairs([1], [1, 2, 3], 100) == [0]
assert sol.successfulPairs([10], [1, 2, 3], 5) == [3]
assert sol.successfulPairs([4], [1, 2, 3, 4, 5], 8) == [4]
assert sol.successfulPairs([4], [1, 2, 3, 4, 5], 9) == [3]
assert sol.successfulPairs([3], [2, 3, 4], 9) == [2]
assert sol.successfulPairs([2], [3, 3, 3, 4], 7) == [1]
assert sol.successfulPairs([2, 3], [5, 1, 4, 2], 8) == [2, 2]
assert sol.successfulPairs([10, 20], [10, 20, 30], 200) == [2, 3]
assert sol.successfulPairs([100000], [100000], 10**10) == [1]
assert sol.successfulPairs([99999], [100000], 10**10) == [0]
assert sol.successfulPairs([100000, 99999, 1], [100000, 100000], 10**10) == [2, 0, 0]