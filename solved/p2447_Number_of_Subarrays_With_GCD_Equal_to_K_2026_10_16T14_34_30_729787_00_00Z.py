"""
URL: https://leetcode.com/problems/number-of-subarrays-with-gcd-equal-to-k/description/?envType=problem-list-v2&envId=vn57k9wr

2447. Number of Subarrays With GCD Equal to K

Given an integer array nums and an integer k, return the number of subarrays of nums where the greatest common divisor of the subarray's elements is k.

A subarray is a contiguous non-empty sequence of elements within an array.

The greatest common divisor of an array is the largest integer that evenly divides all the array elements.

Example 1:

Input: nums = [9,3,1,2,6,3], k = 3
Output: 4
Explanation: The subarrays of nums where 3 is the greatest common divisor of all the subarray's elements are:
- [9,3]
- [3]
- [6,3]
- [3]

Example 2:

Input: nums = [4], k = 7
Output: 0
Explanation: There are no subarrays of nums where 7 is the greatest common divisor of all the subarray's elements.

Constraints:

    1 <= nums.length <= 1000
    1 <= nums[i], k <= 10^9

---

bf is easy. but optimal, not really sure.

class Solution
  def subarrayGCD(nums: [int], k: int) -> int
    ret count = 0
    for i, j in pairs(len(nums) + 1)
      sub = nums[i:j]
      count += gcd(*sub) == k

print(gcd(9, 3)) # 3
print(gcd(9, 3, 1)) # 1

ok the optimization here is realizing that we're looking for
a gcd of k, and the gcd of the subarray can only be k if
the items in the subarray are greater than k and a multiple of k
so this turns it into a divisibility problem?

arr = [9, 3, 1, 2, 6, 3]
print([x % 3 for x in arr])
gives us:
[0, 0, 1, 2, 0, 0]

class Solution
  def subarrayGCD(nums: [int], k: int) -> int
    remainders = [-1 if x % k == 0 else i for >i, x in nums]
    print(remainders)
    cnt = counter()
    res = 0
    for x in remainders
      res += cnt[x]
      cnt[x] += 1
    return res

Got solution from Claude
instead of calling gcd on the whole subarray
we call it two items at a time on the subarray
and stop if we have a remainder, since the gcd
can no longer be k

Learning

LEETCODE: Accepted (63 ms, 19.2 MB)
"""


# mu 0.12
# class Solution
#   def subarrayGCD(nums: [int], k: int) -> int
#     ret count = 0
#     for i, j in pairs(len(nums) + 1)
#       sub = nums[i:j]
#       count += gcd(*sub) == k

def pairs(n, type=tuple, back=False):
    if back:
        for j in range(n):
            for i in range(j):
                yield type((i, j))
        return
    for i in range(n):
        for j in range(i + 1, n):
            yield type((i, j))


# mu 0.12
# class Solution
#   def subarrayGCD(nums: [int], k: int) -> int
#     ret count = 0
#     for >i in nums
#       g = 0                    # gcd(0, x) == x, so the first item sets g
#       for x in nums[i:]
#         g = gcd(g, x)          # gcd of nums[i..j], from the previous gcd and one new item
#         if g % k != 0
#           break                # g only gets smaller or stays the same, so after this k cannot divide it
#         count += g == k

class Solution:
    def subarrayGCD(self, nums: list[int], k: int) -> int:
        count = 0
        for i in range(len(nums)):
            g = 0
            for x in nums[i:]:
                g = gcd(g, x)
                if g % k != 0:
                    break
                count += g == k
        return count


sol = Solution()
print(sol.subarrayGCD([9, 3, 1, 2, 6, 3], 3))
_l, _r = sol.subarrayGCD([9, 3, 1, 2, 6, 3], 3), 4
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.subarrayGCD([4], 7), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.subarrayGCD([1], 1), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.subarrayGCD([2, 4, 6, 8, 10], 2), 11
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.subarrayGCD([5, 5, 5, 5], 5), 10
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.subarrayGCD([10 ** 9, 10 ** 9, 10 ** 9], 10 ** 9), 6
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.subarrayGCD([3, 6, 9, 12, 15], 3), 11
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.subarrayGCD([7, 14, 21, 28], 7), 7
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.subarrayGCD([2, 3, 5, 7, 11, 13], 1), 15
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.subarrayGCD([12, 15, 18, 21, 24], 3), 10
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.subarrayGCD([6, 9, 12, 15, 18], 6), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.subarrayGCD([1, 1, 1, 1, 1], 1), 15
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.subarrayGCD([17], 17), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
