"""
URL: https://leetcode.com/problems/maximum-beauty-of-an-array-after-applying-operation/description/?envType=problem-list-v2&envId=vn57k9wr

2779. Maximum Beauty of an Array After Applying Operation

You are given a 0-indexed array nums and a non-negative integer k.

In one operation, you can do the following:
- Choose an index i that hasn't been chosen before from the range [0, nums.length - 1].
- Replace nums[i] with any integer from the range [nums[i] - k, nums[i] + k].

The beauty of the array is the length of the longest subsequence consisting of equal elements.

Return the maximum possible beauty of the array nums after applying the operation any number of times.

Note that you can apply the operation to each index only once.

A subsequence of an array is a new array generated from the original array by deleting some elements (possibly none) without changing the order of the remaining elements.

Example 1:

Input: nums = [4,6,1,2], k = 2
Output: 3
Explanation: In this example, we apply the following operations:
- Choose index 1, replace it with 4 (from range [4,8]), nums = [4,4,1,2].
- Choose index 3, replace it with 4 (from range [0,4]), nums = [4,4,1,4].
After the applied operations, the beauty of the array nums is 3 (subsequence consisting of indices 0, 1, and 3).
It can be proven that 3 is the maximum possible length we can achieve.

Example 2:

Input: nums = [1,1,1,1], k = 10
Output: 4
Explanation: In this example we don't have to apply any operations.
The beauty of the array nums is 4 (whole array).

Constraints:

    1 <= nums.length <= 10^5
    0 <= nums[i], k <= 10^5

---

LEETCODE: Time Limit Exceeded (606/622 cases)
"""


# mu 0.12
# """
#
# Ok let's examine the wording of the question, and see what gives.
#
# "You are given a 0-indexed array nums and a non-negative integer k."
#
# This says we're given an array, e.g
#
# nums = [4, 6, 1, 2]
#
# and an integer k
#
# k = 2
#
# "In one operation, you can do the following:"
#
# This suggests multiple operations. But it could also be misleading. It's just describing the mechanics of an approach.
#
# "- Choose an index i that hasn't been chosen before from the range [0, nums.length - 1]."
#
# So pick something in the array that wasn't picked before. The suggests we need to track what was picked.
#
# "- Replace nums[i] with any integer from the range [nums[i] - k, nums[i] + k]."
#
# We can substitute that value for a value the range [nums[i] - k, nums[i] + k]
#
# e.g
#
# nums = [4, 6, 1, 2]
#
# becomes
#
# nums = [4, 4, 1, 2]
#
# "The beauty of the array is the length of the longest subsequence consisting of equal elements."
#
# We define a measurable 'beauty' which is the max count of elements in the array
#
# In the first example, we go to
#
# nums = [4, 4, 1, 4]
#
# So 3
#
# #     1 <= nums.length <= 10^5
# #     0 <= nums[i], k <= 10^5
#
# So the array can be up to 100_000 elements, and k can be as big as 100_000
#
# We might be able to solve this with a binary search.
#
# This would lead to an n log(n) solution. We have no way of knowing whether this will satisfy
# the TLE requirments of LC.
#
# So picking the correct bounds will really matter here.
#
# let's say we guess 4
#
# We scan:
#
# nums = [4, 6, 1, 2]
#
# The most bruteforce solution:
#
#
# class Solution
#   def maximumBeauty(nums: [int], k: int) -> int
#     f = guess -> sum(1 for >i in nums if abs(nums[i] - guess) <= k)
#     ret res = -inf
#     for v in min(nums)..max(nums)
#       res = max(f(v), res)
#
# We ask if the diff between (nums[i] - guess) <= k for every i, sum that. That's the number
# we're trying to maximize.
#
# We can't use binary search, since there's no clear boundary.
#
# A greedy approach would be start with the median, or the average, but this is inefficient.
#
# Another greedy approach might involve sorting the array, so:
#
#               v
# nums = [1, 2, 4, 6]
#
# No getting anywhere, so taking the offical LC hints:
#
# hint 1: Sort the array.
#
# So i got that part right.
#
# Hint 2:
#
# The problem becomes the following: find maximum subarray A[i … j] such that A[j] - A[i] ≤ 2 * k.
#
# Solved, by taking official hints.
#
# """
#
# class Solution
#   def maximumBeauty(nums: [int], k: int) -> int
#     if k == 0
#       return max(counter(nums).values())
#     nums.sort()
#     f = (i, j) -> nums[j] - nums[i] <= 2 * k
#     ret res = 0
#     for i, j in pairs(len(nums))
#       if f(i, j)
#         res = max(res, j - i + 1)

"""

Ok let's examine the wording of the question, and see what gives.

"You are given a 0-indexed array nums and a non-negative integer k."

This says we're given an array, e.g 

nums = [4, 6, 1, 2]

and an integer k

k = 2

"In one operation, you can do the following:"

This suggests multiple operations. But it could also be misleading. It's just describing the mechanics of an approach.

"- Choose an index i that hasn't been chosen before from the range [0, nums.length - 1]."

So pick something in the array that wasn't picked before. The suggests we need to track what was picked.

"- Replace nums[i] with any integer from the range [nums[i] - k, nums[i] + k]."

We can substitute that value for a value the range [nums[i] - k, nums[i] + k]

e.g

nums = [4, 6, 1, 2]

becomes

nums = [4, 4, 1, 2]

"The beauty of the array is the length of the longest subsequence consisting of equal elements."

We define a measurable 'beauty' which is the max count of elements in the array

In the first example, we go to 

nums = [4, 4, 1, 4]

So 3

#     1 <= nums.length <= 10^5
#     0 <= nums[i], k <= 10^5

So the array can be up to 100_000 elements, and k can be as big as 100_000

We might be able to solve this with a binary search.

This would lead to an n log(n) solution. We have no way of knowing whether this will satisfy
the TLE requirments of LC.

So picking the correct bounds will really matter here.

let's say we guess 4

We scan:

nums = [4, 6, 1, 2]

The most bruteforce solution:


class Solution
  def maximumBeauty(nums: [int], k: int) -> int
    f = guess -> sum(1 for >i in nums if abs(nums[i] - guess) <= k)
    ret res = -inf
    for v in min(nums)..max(nums)
      res = max(f(v), res)

We ask if the diff between (nums[i] - guess) <= k for every i, sum that. That's the number
we're trying to maximize.

We can't use binary search, since there's no clear boundary.

A greedy approach would be start with the median, or the average, but this is inefficient.

Another greedy approach might involve sorting the array, so:

              v
nums = [1, 2, 4, 6]

No getting anywhere, so taking the offical LC hints:

hint 1: Sort the array.

So i got that part right.

Hint 2:

The problem becomes the following: find maximum subarray A[i … j] such that A[j] - A[i] ≤ 2 * k.

Solved, by taking official hints.

"""


from collections import Counter


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
# """
#
# Ok let's examine the wording of the question, and see what gives.
#
# "You are given a 0-indexed array nums and a non-negative integer k."
#
# This says we're given an array, e.g
#
# nums = [4, 6, 1, 2]
#
# and an integer k
#
# k = 2
#
# "In one operation, you can do the following:"
#
# This suggests multiple operations. But it could also be misleading. It's just describing the mechanics of an approach.
#
# "- Choose an index i that hasn't been chosen before from the range [0, nums.length - 1]."
#
# So pick something in the array that wasn't picked before. The suggests we need to track what was picked.
#
# "- Replace nums[i] with any integer from the range [nums[i] - k, nums[i] + k]."
#
# We can substitute that value for a value the range [nums[i] - k, nums[i] + k]
#
# e.g
#
# nums = [4, 6, 1, 2]
#
# becomes
#
# nums = [4, 4, 1, 2]
#
# "The beauty of the array is the length of the longest subsequence consisting of equal elements."
#
# We define a measurable 'beauty' which is the max count of elements in the array
#
# In the first example, we go to
#
# nums = [4, 4, 1, 4]
#
# So 3
#
# #     1 <= nums.length <= 10^5
# #     0 <= nums[i], k <= 10^5
#
# So the array can be up to 100_000 elements, and k can be as big as 100_000
#
# We might be able to solve this with a binary search.
#
# This would lead to an n log(n) solution. We have no way of knowing whether this will satisfy
# the TLE requirments of LC.
#
# So picking the correct bounds will really matter here.
#
# let's say we guess 4
#
# We scan:
#
# nums = [4, 6, 1, 2]
#
# The most bruteforce solution:
#
#
# class Solution
#   def maximumBeauty(nums: [int], k: int) -> int
#     f = guess -> sum(1 for >i in nums if abs(nums[i] - guess) <= k)
#     ret res = -inf
#     for v in min(nums)..max(nums)
#       res = max(f(v), res)
#
# We ask if the diff between (nums[i] - guess) <= k for every i, sum that. That's the number
# we're trying to maximize.
#
# We can't use binary search, since there's no clear boundary.
#
# A greedy approach would be start with the median, or the average, but this is inefficient.
#
# Another greedy approach might involve sorting the array, so:
#
#               v
# nums = [1, 2, 4, 6]
#
# No getting anywhere, so taking the offical LC hints:
#
# hint 1: Sort the array.
#
# So i got that part right.
#
# Hint 2:
#
# The problem becomes the following: find maximum subarray A[i … j] such that A[j] - A[i] ≤ 2 * k.
#
# Solved, by taking official hints.
#
# """
#
# class Solution
#   def maximumBeauty(nums: [int], k: int) -> int
#     if k == 0
#       return max(counter(nums).values())
#     nums.sort()
#     f = (i, j) -> nums[j] - nums[i] <= 2 * k
#     ret res = min(len(nums), 1)
#     for i, j in pairs(len(nums))
#       if f(i, j)
#         res = max(res, j - i + 1)

"""

Ok let's examine the wording of the question, and see what gives.

"You are given a 0-indexed array nums and a non-negative integer k."

This says we're given an array, e.g 

nums = [4, 6, 1, 2]

and an integer k

k = 2

"In one operation, you can do the following:"

This suggests multiple operations. But it could also be misleading. It's just describing the mechanics of an approach.

"- Choose an index i that hasn't been chosen before from the range [0, nums.length - 1]."

So pick something in the array that wasn't picked before. The suggests we need to track what was picked.

"- Replace nums[i] with any integer from the range [nums[i] - k, nums[i] + k]."

We can substitute that value for a value the range [nums[i] - k, nums[i] + k]

e.g

nums = [4, 6, 1, 2]

becomes

nums = [4, 4, 1, 2]

"The beauty of the array is the length of the longest subsequence consisting of equal elements."

We define a measurable 'beauty' which is the max count of elements in the array

In the first example, we go to 

nums = [4, 4, 1, 4]

So 3

#     1 <= nums.length <= 10^5
#     0 <= nums[i], k <= 10^5

So the array can be up to 100_000 elements, and k can be as big as 100_000

We might be able to solve this with a binary search.

This would lead to an n log(n) solution. We have no way of knowing whether this will satisfy
the TLE requirments of LC.

So picking the correct bounds will really matter here.

let's say we guess 4

We scan:

nums = [4, 6, 1, 2]

The most bruteforce solution:


class Solution
  def maximumBeauty(nums: [int], k: int) -> int
    f = guess -> sum(1 for >i in nums if abs(nums[i] - guess) <= k)
    ret res = -inf
    for v in min(nums)..max(nums)
      res = max(f(v), res)

We ask if the diff between (nums[i] - guess) <= k for every i, sum that. That's the number
we're trying to maximize.

We can't use binary search, since there's no clear boundary.

A greedy approach would be start with the median, or the average, but this is inefficient.

Another greedy approach might involve sorting the array, so:

              v
nums = [1, 2, 4, 6]

No getting anywhere, so taking the offical LC hints:

hint 1: Sort the array.

So i got that part right.

Hint 2:

The problem becomes the following: find maximum subarray A[i … j] such that A[j] - A[i] ≤ 2 * k.

Solved, by taking official hints.

"""


from collections import Counter


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
# """
#
# Ok let's examine the wording of the question, and see what gives.
#
# "You are given a 0-indexed array nums and a non-negative integer k."
#
# This says we're given an array, e.g
#
# nums = [4, 6, 1, 2]
#
# and an integer k
#
# k = 2
#
# "In one operation, you can do the following:"
#
# This suggests multiple operations. But it could also be misleading. It's just describing the mechanics of an approach.
#
# "- Choose an index i that hasn't been chosen before from the range [0, nums.length - 1]."
#
# So pick something in the array that wasn't picked before. The suggests we need to track what was picked.
#
# "- Replace nums[i] with any integer from the range [nums[i] - k, nums[i] + k]."
#
# We can substitute that value for a value the range [nums[i] - k, nums[i] + k]
#
# e.g
#
# nums = [4, 6, 1, 2]
#
# becomes
#
# nums = [4, 4, 1, 2]
#
# "The beauty of the array is the length of the longest subsequence consisting of equal elements."
#
# We define a measurable 'beauty' which is the max count of elements in the array
#
# In the first example, we go to
#
# nums = [4, 4, 1, 4]
#
# So 3
#
# #     1 <= nums.length <= 10^5
# #     0 <= nums[i], k <= 10^5
#
# So the array can be up to 100_000 elements, and k can be as big as 100_000
#
# We might be able to solve this with a binary search.
#
# This would lead to an n log(n) solution. We have no way of knowing whether this will satisfy
# the TLE requirments of LC.
#
# So picking the correct bounds will really matter here.
#
# let's say we guess 4
#
# We scan:
#
# nums = [4, 6, 1, 2]
#
# The most bruteforce solution:
#
#
# class Solution
#   def maximumBeauty(nums: [int], k: int) -> int
#     f = guess -> sum(1 for >i in nums if abs(nums[i] - guess) <= k)
#     ret res = -inf
#     for v in min(nums)..max(nums)
#       res = max(f(v), res)
#
# We ask if the diff between (nums[i] - guess) <= k for every i, sum that. That's the number
# we're trying to maximize.
#
# We can't use binary search, since there's no clear boundary.
#
# A greedy approach would be start with the median, or the average, but this is inefficient.
#
# Another greedy approach might involve sorting the array, so:
#
#               v
# nums = [1, 2, 4, 6]
#
# No getting anywhere, so taking the offical LC hints:
#
# hint 1: Sort the array.
#
# So i got that part right.
#
# Hint 2:
#
# The problem becomes the following: find maximum subarray A[i … j] such that A[j] - A[i] ≤ 2 * k.
#
# Solved, by taking official hints, but hit TLE.
#
# Here's a better solve (not mine):
#
# class Solution
#   def maximumBeauty(nums: [int], k: int) -> int
#     nums.sort()
#     f = (i, j) -> nums[j] - nums[i] <= 2 * k
#     ret best, left = 0, 0
#     for >right in nums
#       if not f(left, right)
#         left += 1
#       best = max(best, right - left + 1)
#
# So i'm marking this as a fail.
#
#
# """
#
# class Solution
#   def maximumBeauty(nums: [int], k: int) -> int
#     nums.sort()
#     f = (i, j) -> nums[j] - nums[i] <= 2 * k
#     ret res = min(len(nums), 1)
#     for i, j in pairs(len(nums))
#       if f(i, j)
#         res = max(res, j - i + 1)

"""

Ok let's examine the wording of the question, and see what gives.

"You are given a 0-indexed array nums and a non-negative integer k."

This says we're given an array, e.g 

nums = [4, 6, 1, 2]

and an integer k

k = 2

"In one operation, you can do the following:"

This suggests multiple operations. But it could also be misleading. It's just describing the mechanics of an approach.

"- Choose an index i that hasn't been chosen before from the range [0, nums.length - 1]."

So pick something in the array that wasn't picked before. The suggests we need to track what was picked.

"- Replace nums[i] with any integer from the range [nums[i] - k, nums[i] + k]."

We can substitute that value for a value the range [nums[i] - k, nums[i] + k]

e.g

nums = [4, 6, 1, 2]

becomes

nums = [4, 4, 1, 2]

"The beauty of the array is the length of the longest subsequence consisting of equal elements."

We define a measurable 'beauty' which is the max count of elements in the array

In the first example, we go to 

nums = [4, 4, 1, 4]

So 3

#     1 <= nums.length <= 10^5
#     0 <= nums[i], k <= 10^5

So the array can be up to 100_000 elements, and k can be as big as 100_000

We might be able to solve this with a binary search.

This would lead to an n log(n) solution. We have no way of knowing whether this will satisfy
the TLE requirments of LC.

So picking the correct bounds will really matter here.

let's say we guess 4

We scan:

nums = [4, 6, 1, 2]

The most bruteforce solution:


class Solution
  def maximumBeauty(nums: [int], k: int) -> int
    f = guess -> sum(1 for >i in nums if abs(nums[i] - guess) <= k)
    ret res = -inf
    for v in min(nums)..max(nums)
      res = max(f(v), res)

We ask if the diff between (nums[i] - guess) <= k for every i, sum that. That's the number
we're trying to maximize.

We can't use binary search, since there's no clear boundary.

A greedy approach would be start with the median, or the average, but this is inefficient.

Another greedy approach might involve sorting the array, so:

              v
nums = [1, 2, 4, 6]

No getting anywhere, so taking the offical LC hints:

hint 1: Sort the array.

So i got that part right.

Hint 2:

The problem becomes the following: find maximum subarray A[i … j] such that A[j] - A[i] ≤ 2 * k.

Solved, by taking official hints, but hit TLE.

Here's a better solve (not mine):

class Solution
  def maximumBeauty(nums: [int], k: int) -> int
    nums.sort()
    f = (i, j) -> nums[j] - nums[i] <= 2 * k
    ret best, left = 0, 0
    for >right in nums
      if not f(left, right)
        left += 1
      best = max(best, right - left + 1)

So i'm marking this as a fail.


"""


def pairs(n, type=tuple, back=False):
    if back:
        for j in range(n):
            for i in range(j):
                yield type((i, j))
        return
    for i in range(n):
        for j in range(i + 1, n):
            yield type((i, j))


class Solution:
    def maximumBeauty(self, nums: list[int], k: int) -> int:
        nums.sort()
        f = lambda *_a: (lambda i, j: nums[j] - nums[i] <= 2 * k)(*(_a[0] if len(_a) == 1 else _a))
        res = min(len(nums), 1)
        for i, j in pairs(len(nums)):
            if f(i, j):
                res = max(res, j - i + 1)
        return res


sol = Solution()
print(sol.maximumBeauty([1, 2, 4, 6], 2))
_l, _r = sol.maximumBeauty([4, 6, 1, 2], 2), 3
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.maximumBeauty([1, 1, 1, 1], 10), 4
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.maximumBeauty([0], 0), 1
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.maximumBeauty([10 ** 5], 0), 1
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.maximumBeauty([1, 1, 1, 1, 1], 0), 5
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.maximumBeauty([1, 2, 3, 4, 5], 0), 1
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.maximumBeauty([1, 2, 3, 4, 5], 10 ** 5), 5
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.maximumBeauty([5, 5, 5, 5, 5], 10 ** 5), 5
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.maximumBeauty([1, 2, 2, 3, 3, 3], 1), 6
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.maximumBeauty([1, 2, 3, 4, 5], 1), 3
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.maximumBeauty([1, 100000, 200000], 100000), 3
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.maximumBeauty([0, 0, 0, 0, 0], 0), 5
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.maximumBeauty([10 ** 5, 10 ** 5, 10 ** 5], 0), 3
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.maximumBeauty([1, 2, 3, 4, 5], 2), 5
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.maximumBeauty([12, 71], 10), 1
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))


# FAILED: walked away after 70m 52s; no working solution.
# Judge the move the defect is in as struggled, not clean. A move the code never reached gets no verdict.
