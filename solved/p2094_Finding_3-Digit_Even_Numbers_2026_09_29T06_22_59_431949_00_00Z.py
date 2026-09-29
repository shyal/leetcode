"""
URL: https://leetcode.com/problems/finding-3-digit-even-numbers/description/?envType=problem-list-v2&envId=vn57k9wr

2094. Finding 3-Digit Even Numbers

You are given an integer array digits, where each element is a digit. The array may contain duplicates.

You need to find all the unique integers that follow the given requirements:

- The integer consists of the concatenation of three elements from digits in any arbitrary order.
- The integer does not have leading zeros.
- The integer is even.

For example, if the given digits were [1, 2, 3], integers 132 and 312 follow the requirements.

Return a sorted array of the unique integers.

Example 1:

Input: digits = [2,1,3,0]
Output: [102,120,130,132,210,230,302,310,312,320]
Explanation: All the possible integers that follow the requirements are in the output array.
Notice that there are no odd integers or integers with leading zeros.

Example 2:

Input: digits = [2,2,8,8,2]
Output: [222,228,282,288,822,828,882]
Explanation: The same digit can be used as many times as it appears in digits.
In this example, the digit 8 is used twice each time in 288, 828, and 882.

Example 3:

Input: digits = [3,7,5]
Output: []
Explanation: No even integers can be formed using the given digits.

Constraints:

    3 <= digits.length <= 100
    0 <= digits[i] <= 9
---
def findEvenNumbers(digits: [int]) -> [int]
  def helper(i, total, num_digits)
      if num_digits == 3
        if even(total) and total // 100 != 0
          ret.append(total)
        return
      for j in range(i, len(digits))
        curr <- digits[j]
        helper(j+1, total * 10 + digits[j], num_digits + 1)
        curr .


  digits.sort()
  curr = []
  ret = []
  helper(0, 0, 0)
  ret

LEETCODE: Accepted (6511 ms, 467.9 MB)
"""


# mu 0.6
# def findEvenNumbers(nums: [int]) -> [int]
#   def helper(i, total, num_digits)
#     if len(curr) == 3
#       if even(total) and total // 100 != 0
#         ret.append(total)
#       return
#     for j in range(len(nums))
#       if take[j]
#         continue
#       # if j > i and nums[j] > nums[j - 1]
#         # continue
#       take[j] = True
#       curr.append(nums[j])
#       helper(j + 1, total * 10 + nums[j], num_digits + 1)
#       curr.pop()
#       take[j] = False
#
#   ret = []
#   curr = []
#   take = [False] * len(nums)
#   nums.sort()
#   helper(0, 0, 0)
#   return [*sorted(set(ret))]

def even(n):
    return n % 2 == 0


class Solution:
    def findEvenNumbers(self, nums: list[int]) -> list[int]:
        def helper(i, total, num_digits):
            if len(curr) == 3:
                if even(total) and total // 100 != 0:
                    ret.append(total)
                return
            for j in range(len(nums)):
                if take[j]:
                    continue
                take[j] = True
                curr.append(nums[j])
                helper(j + 1, total * 10 + nums[j], num_digits + 1)
                curr.pop()
                take[j] = False
        ret = []
        curr = []
        take = [False] * len(nums)
        nums.sort()
        helper(0, 0, 0)
        return [*sorted(set(ret))]


sol = Solution()
print(sol.findEvenNumbers([2, 1, 3, 0]))
assert sol.findEvenNumbers([2, 1, 3, 0]) == [102, 120, 130, 132, 210, 230, 302, 310, 312, 320]
assert sol.findEvenNumbers([2, 2, 8, 8, 2]) == [222, 228, 282, 288, 822, 828, 882]
assert sol.findEvenNumbers([3, 7, 5]) == []
assert sol.findEvenNumbers([0, 0, 0]) == []
assert sol.findEvenNumbers([0, 1, 2]) == [102, 120, 210]
assert sol.findEvenNumbers([9, 9, 8]) == [998]
assert sol.findEvenNumbers([1, 1, 1, 2, 2, 2]) == [112, 122, 212, 222]
assert sol.findEvenNumbers([4, 4, 4, 4]) == [444]
assert sol.findEvenNumbers([0, 2, 4, 6, 8]) == [204, 206, 208, 240, 246, 248, 260, 264, 268, 280, 284, 286, 402, 406, 408, 420, 426, 428, 460, 462, 468, 480, 482, 486, 602, 604, 608, 620, 624, 628, 640, 642, 648, 680, 682, 684, 802, 804, 806, 820, 824, 826, 840, 842, 846, 860, 862, 864]
assert sol.findEvenNumbers([1, 3, 5, 7, 9]) == []
assert sol.findEvenNumbers([0, 0, 2]) == [200]
assert sol.findEvenNumbers([2, 2, 2]) == [222]
assert sol.findEvenNumbers([1, 0, 0]) == [100]
assert sol.findEvenNumbers([8, 8, 8, 8, 8, 8, 8, 8, 8, 8]) == [888]
