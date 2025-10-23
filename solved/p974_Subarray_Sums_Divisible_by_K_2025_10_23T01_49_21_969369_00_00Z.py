"""
URL: https://leetcode.com/problems/subarray-sums-divisible-by-k/description/

974. Subarray Sums Divisible by K

Given an integer array nums and an integer k, return the number of non-empty subarrays that have a sum divisible by k.

A subarray is a contiguous part of an array.


Example 1:

Input: nums = [4,5,0,-2,-3,1], k = 5
Output: 7
Explanation: There are 7 subarrays with a sum divisible by k = 5:
[4, 5, 0, -2, -3, 1], [5], [5, 0], [5, 0, -2, -3], [0], [0, -2, -3], [-2, -3]

Example 2:

Input: nums = [5], k = 9
Output: 0


Constraints:

    1 <= nums.length <= 3 * 104
    -104 <= nums[i] <= 104
    2 <= k <= 104

---

I actually stepped through this solution very carefully yesterday, and the
pattern clicked so let's hope i can summon it up again.

It really helped to just treat this as a subarray sum equals k first.

Ok i had to look up subarray sum equals k. I guess i got confused after 3 sum, because
the pattern is somewhat similar, but not.

With subarray sum equals k, the complement is `prefix - k`, and we need to initialize
the dict with D[0] = 1.

Now to transform this into a subarray sum divisible by k, we need to think of the properties
of modulor arithmetic, and how they jive with the subarray sum problem.

In the subarray sum problem, the sum of the range i to j is prefix[j] - prefix[i - 1].
In our case we want to check for divisibility, i.e:

(prefix[j] - prefix[i - 1]) % k = 0

Using modulo arithmetic:

prefix[j] % k - prefix[i - 1] % k  = 0

prefix[j] % k = prefix[i - 1] % k

Hmm ok i think this passes.. but i'll need to revisit this soon, still on a learning basis.

"""


class Solution:

    def subarraysDivByK(self, nums: List[int], k: int) -> int:
        prefix = 0
        D = defaultdict(int)
        D[0] = 1
        res = 0
        for n in nums:
            prefix += n
            complement = prefix % k
            if complement in D:
                res += D[complement]
            D[prefix % k] += 1
        return res


sol = Solution()

assert sol.subarraysDivByK([4, 5, 0, -2, -3, 1], 5) == 7
assert sol.subarraysDivByK([5], 9) == 0
