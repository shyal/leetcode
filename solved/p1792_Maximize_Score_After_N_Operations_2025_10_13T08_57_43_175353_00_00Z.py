"""
URL: https://leetcode.com/problems/maximize-score-after-n-operations/description/

1792. Maximize Score After N Operations

You are given a 0-indexed integer array nums of length 2 * n.

You must perform n operations on this array.

In the kth operation (1-indexed), you will apply the following on the array:

    Choose two elements, x and y, that have not been chosen in any previous operation.
    Remove x and y from the array.
    Add k * gcd(x, y) to your score.

Return the maximum score it is possible to achieve after performing n operations.

The test cases are generated so that all the elements will be used in some operation.


Example 1:

Input: nums = [1,2]
Output: 1
Explanation: There is only one possible operation: choose 1 and 2, gcd(1,2) = 1, score = 1 * 1 = 1.

Example 2:

Input: nums = [3,4,6,8]
Output: 11
Explanation: One optimal way is:
- Operation 1: choose 3 and 6, gcd(3,6) = 3, score += 1 * 3 = 3
- Operation 2: choose 4 and 8, gcd(4,8) = 4, score += 2 * 4 = 8
Total score = 3 + 8 = 11.
Another way:
- Operation 1: choose 4 and 8, gcd=4, score +=1*4=4
- Operation 2: choose 3 and 6, gcd=3, score +=2*3=6
Total = 10, which is less than 11.

Example 3:

Input: nums = [1,2,3,4,5,6]
Output: 14
Explanation: One optimal way is to pair (1,2) gcd=1, (3,6) gcd=3, (4,5) gcd=1.
Then assign the gcds 1,1,3 to operations with multipliers sorted to maximize: 3 to 3, 1 to 2, 1 to 1: 3*3 + 1*2 + 1*1 = 9+2+1=12? Wait, but output is 14.
Wait, better pairing: (2,4) gcd=2, (3,6) gcd=3, (1,5) gcd=1.
Then gcds 1,2,3, assign 3 to 3, 2 to 2, 1 to 1: 9+4+1=14. Yes.


Constraints:

    1 <= n <= 7
    nums.length == 2 * n
    1 <= nums[i] <= 10^6

---

Hm the not so simple here is deciding which elements to pick from the array to maximize
the result.

Let's run through some options by hand, and see whether we can spot a pattern.

[3,4,6,8]

Here are all the options we have for GCD

gcd(3, 4) -> 1
gcd(3, 6) -> 3
gcd(3, 8) -> 1
gcd(4, 6) -> 2
gcd(4, 8) -> 4
gcd(6, 8) -> 2

The best picks are, and we note they have the greatest GCDs:

gcd(3, 6) -> 3
gcd(4, 8) -> 4

I'm not really sure what the whole 'n' business is about, since we don't get passed an n. Maybe they
mean that n = len(nums) // 2.

Looking at the provided hints:

Hint 1
Find every way to split the array until n groups of 2. Brute force recursion is acceptable.
Hint 2
Calculate the gcd of every pair and greedily multiply the largest gcds.

I'm not really clear what hint 1 means. If we want groups of 2, we don't get to choose how many groups we get.

For example: `[*combinations(nums, 2)]` gives us:

[(3, 4), (3, 6), (3, 8), (4, 6), (4, 8), (6, 8)]

We can take their gcds:

[1, 3, 1, 2, 4, 2]

sort it and take the two largest numbers.

groups = islice(
    sorted([gcd(*x) for x in combinations(nums, 2)], reverse=True),
    0,
    len(nums) // 2,
)
groups = [*groups][::-1]
return sum(x[0] * x[1] for x in enumerate(groups, start=1))

This works for the given example. But it might be by chance. Let's try others.

Works on many values, but not on:

# assert sol.maxScore([1, 2, 3, 6]) == 7
# assert sol.maxScore([9, 3, 6, 2]) == 8
# assert sol.maxScore([1, 2, 3, 4, 5, 6]) == 14

ok i can see what the problem is. The problem is, combinations leads to repeats, which breaks the constraints.
So i'd need to write a recursive function which breaks up the array into groups of two, without repeats.

I'm a bit rusty with this.. very similar to knapsack in a way. Will revisit this soon.

"""

from typing import List
from math import gcd
from itertools import islice


class Solution:
    def maxScore(self, nums: List[int]) -> int:
        combs = [*combinations(nums, 2)]
        combs.sort(key=lambda x: gcd(*x), reverse=True)
        # print(combs)
        groups = islice(
            sorted([gcd(*x) for x in combs], reverse=True),
            0,
            len(nums) // 2,
        )
        groups = [*groups][::-1]
        # print(groups)
        return sum(x[0] * x[1] for x in enumerate(groups, start=1))


sol = Solution()

# print(sol.maxScore([1, 2, 3, 4, 5, 6]))  # 14

# assert sol.maxScore([1, 2, 3, 6]) == 7
# assert sol.maxScore([9, 3, 6, 2]) == 8
# assert sol.maxScore([1, 2, 3, 4, 5, 6]) == 14

# works:

# assert sol.maxScore([1, 2]) == 1
# assert sol.maxScore([3, 4, 6, 8]) == 11
# assert sol.maxScore([1, 1]) == 1
# assert sol.maxScore([1000000, 1000000]) == 1000000
# assert sol.maxScore([1, 1000000]) == 1
# assert sol.maxScore([1, 1, 1, 1]) == 3
# assert sol.maxScore([4, 8, 12, 16]) == 20
# assert sol.maxScore([1, 1, 1, 1, 1, 1]) == 6
# assert sol.maxScore([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]) == 28
