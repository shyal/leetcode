"""
URL: https://leetcode.com/problems/koko-eating-bananas/description/?envType=study-plan-v2&envId=leetcode-75

875. Koko Eating Bananas

Koko loves to eat bananas. There are n piles of bananas, the ith pile has piles[i] bananas. The guards have gone and will come back in h hours.

Koko can decide her bananas-per-hour eating speed of k. Each hour, she chooses some pile of bananas and eats k bananas from that pile. If the pile has less than k bananas, she eats all of them instead and will not eat any more bananas during this hour.

Koko likes to eat slowly but still wants to finish eating all the bananas before the guards return.

Return the minimum integer k such that she can eat all the bananas within h hours.


Example 1:

Input: piles = [3,6,7,11], h = 8
Output: 4

Example 2:

Input: piles = [30,11,23,4,20], h = 5
Output: 30

Example 3:

Input: piles = [30,11,23,4,20], h = 6
Output: 23


Constraints:

        1 <= piles.length <= 104
        piles.length <= h <= 109
        1 <= piles[i] <= 109

---

Once again, using the minimization template made this a breeze.

"""


class Solution:

    def hoursToEatPiles(self, piles, k):
        h = 0
        for p in piles:
            div, mod = divmod(p, k)
            h += div
            if mod:
                h += 1
        return h

    # @viz_binary_search()
    def minEatingSpeed(self, piles: List[int], h: int) -> int:
        low = 1
        high = sum(piles)
        result = -1
        is_minimization = True

        while low <= high:
            mid = low + (high - low) // 2
            if self.hoursToEatPiles(piles, mid) <= h:
                result = mid
                if is_minimization:
                    high = mid - 1
                else:
                    low = mid + 1
            else:
                if is_minimization:
                    low = mid + 1
                else:
                    high = mid - 1

        return result


sol = Solution()

assert sol.hoursToEatPiles([1, 1, 1], 1) == 3
assert sol.hoursToEatPiles([3], 1) == 3
assert sol.hoursToEatPiles([4], 3) == 2
assert sol.hoursToEatPiles([4, 3], 3) == 3
assert sol.minEatingSpeed([3, 6, 7, 11], 8) == 4
assert sol.minEatingSpeed([30, 11, 23, 4, 20], 5) == 30
assert sol.minEatingSpeed([30, 11, 23, 4, 20], 6) == 23
assert sol.minEatingSpeed([1], 1) == 1
assert sol.minEatingSpeed([2], 1) == 2
assert sol.minEatingSpeed([2], 2) == 1
assert sol.minEatingSpeed([1000000000], 1) == 1000000000
assert sol.minEatingSpeed([1000000000], 2) == 500000000
assert sol.minEatingSpeed([1000000000], 1000000000) == 1
assert sol.minEatingSpeed([1, 1, 1, 999999999], 4) == 999999999
assert sol.minEatingSpeed([312884470], 312884469) == 2
assert sol.minEatingSpeed([1000000000, 1000000000], 3) == 1000000000
assert sol.minEatingSpeed([1000000000, 1000000000], 4) == 500000000
assert sol.minEatingSpeed([5, 2, 7], 4) == 5
assert sol.minEatingSpeed([1], 2) == 1
assert sol.minEatingSpeed([1, 1], 3) == 1
assert sol.minEatingSpeed([4], 3) == 2
assert sol.minEatingSpeed([1, 2, 3], 7) == 1
assert sol.minEatingSpeed([1, 1, 1], 4) == 1
assert sol.minEatingSpeed([1000000000, 1000000000], 5) == 500000000
assert sol.minEatingSpeed([3, 6, 7, 11], 4) == 11
assert sol.minEatingSpeed([1, 1, 2], 3) == 2
assert sol.minEatingSpeed([1, 2, 3], 5) == 2
assert sol.minEatingSpeed([5, 5, 5], 5) == 5
assert sol.minEatingSpeed([1000000000, 1000000000], 2) == 1000000000
assert sol.minEatingSpeed([1] * 100, 100) == 1
assert sol.minEatingSpeed([10, 10], 3) == 10
assert sol.minEatingSpeed([3, 3, 3], 5) == 3
assert sol.minEatingSpeed([1, 2, 3, 4, 5], 9) == 2
assert sol.minEatingSpeed([1, 2, 3, 4, 5], 14) == 2
assert sol.minEatingSpeed([1, 2, 3, 4, 5], 15) == 1
assert sol.minEatingSpeed([1, 2, 3, 4, 5], 5) == 5
assert sol.minEatingSpeed([1000000000] * 3, 6) == 500000000
assert sol.minEatingSpeed([1] * 10000, 10000) == 1
assert sol.minEatingSpeed([1000000000] * 3, 5) == 1000000000
assert sol.minEatingSpeed([8], 4) == 2
