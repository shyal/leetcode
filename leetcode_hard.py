"""
URL: https://leetcode.com/problems/maximum-subarray/description/

53. Maximum Subarray

Given an integer array nums, find the subarray with the largest sum, and return its sum.


Example 1:

Input: nums = [-2,1,-3,4,-1,2,1,-5,4]
Output: 6
Explanation: The subarray [4,-1,2,1] has the largest sum 6.

Example 2:

Input: nums = [1]
Output: 1
Explanation: The subarray [1] has the largest sum 1.

Example 3:

Input: nums = [5,4,-1,7,8]
Output: 23
Explanation: The subarray [5,4,-1,7,8] has the largest sum 23.


Constraints:

    1 <= nums.length <= 105
    -104 <= nums[i] <= 104


Follow up: If you have figured out the O(n) solution, try coding another solution using the divide and conquer approach, which is more subtle.
"""


class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        current_sum = 0
        _max = float("-inf")
        for i, n in enumerate(nums):
            current_sum = max(n, n + current_sum) if i > 0 else n
            _max = max(_max, current_sum)
        return _max


sol = Solution()
assert sol.maxSubArray([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == 6
assert sol.maxSubArray([1]) == 1
assert sol.maxSubArray([5, 4, -1, 7, 8]) == 23
assert sol.maxSubArray([-1]) == -1
"""
URL: https://leetcode.com/problems/longest-subarray-of-1s-after-deleting-one-element/description/?envType=study-plan-v2&envId=leetcode-75

1493. Longest Subarray of 1's After Deleting One Element

Given a binary array nums, you should delete one element from it.

Return the size of the longest non-empty subarray containing only 1's in the resulting array. Return 0 if there is no such subarray.


Example 1:

Input: nums = [1,1,0,1]
Output: 3
Explanation: After deleting the number in position 2, [1,1,1] contains 3 numbers with value of 1's.

Example 2:

Input: nums = [0,1,1,1,0,1,1,0,1]
Output: 5
Explanation: After deleting the number in position 4, [0,1,1,1,1,1,0,1] longest subarray with value of 1's is [1,1,1,1,1].

Example 3:

Input: nums = [1,1,1]
Output: 2
Explanation: You must delete one element.


Constraints:

        1 <= nums.length <= 105
        nums[i] is either 0 or 1.
"""

from itertools import groupby


class Solution:
    def longestSubarray(self, nums: List[int]) -> int:
        counts = ((v, len([*it])) for v, it in groupby(nums))
        a, b, _max, zeroes = None, None, 0, False
        for num, count in counts:
            if num == 0:
                zeroes = True
            if num == 1 and a is None:
                a = count
                _max = max(_max, a)
            elif num == 0 and count > 1:
                a = None
            elif num == 1 and a is not None:
                _max = max(_max, a + count)
                a, b = count, None
        return _max - int(not zeroes)


sol = Solution()

assert sol.longestSubarray(nums=[1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1]) == 11

assert sol.longestSubarray(nums=[1, 1, 1]) == 2
assert sol.longestSubarray(nums=[0, 1, 1, 1, 0, 0, 1, 1, 0, 1]) == 3
assert sol.longestSubarray(nums=[0, 1, 1, 1, 0, 1, 1, 0, 1]) == 5
assert sol.longestSubarray(nums=[1, 1, 1, 0, 1, 1, 1]) == 6
assert sol.longestSubarray(nums=[1, 1, 1, 0, 0, 1, 1, 1]) == 3
assert sol.longestSubarray(nums=[0, 1, 1, 1, 0, 0, 1, 1, 1]) == 3
assert sol.longestSubarray(nums=[0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0]) == 3
assert sol.longestSubarray(nums=[0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0]) == 3
assert (
    sol.longestSubarray(nums=[0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0])
    == 6
)
assert sol.longestSubarray(nums=[1]) == 0
assert sol.longestSubarray(nums=[0]) == 0
assert sol.longestSubarray(nums=[1, 1]) == 1
assert sol.longestSubarray(nums=[0, 0]) == 0
assert sol.longestSubarray(nums=[1, 0, 1]) == 2
assert sol.longestSubarray(nums=[1, 0, 0, 1]) == 1
assert sol.longestSubarray(nums=[0, 1, 0]) == 1
assert sol.longestSubarray(nums=[1, 0, 1, 0, 1]) == 2
assert sol.longestSubarray(nums=[0, 1, 0, 1, 0, 1]) == 2
assert sol.longestSubarray(nums=[1, 0, 1, 0, 1, 0]) == 2
assert sol.longestSubarray(nums=[0, 0, 0, 0, 0]) == 0
assert sol.longestSubarray(nums=[1, 1, 1, 1, 1]) == 4
assert sol.longestSubarray(nums=[1, 1, 0, 0, 0, 1, 1]) == 2

"""
URL: https://leetcode.com/problems/divisor-game/description/

1025. Divisor Game

Alice and Bob take turns playing a game, with Alice starting first.

Initially, there is a number n on the chalkboard. On each player's turn, that player makes a move consisting of:

    Choosing any x with 0 < x < n and n % x == 0.
    Replacing the number n on the chalkboard with n - x.

Also, if a player cannot make a move, they lose the game.

Return true if and only if Alice wins the game, assuming both players play optimally.


Example 1:

Input: n = 2
Output: true
Explanation: Alice chooses 1, and Bob has no more moves.

Example 2:

Input: n = 3
Output: false
Explanation: Alice chooses 1, Bob chooses 1, and Alice has no more moves.


Constraints:

    1 <= n <= 1000


---------

Had to look up the solution for this. It may or may not fall in the DP arena, as
one can also take a pure maths approach.
"""


class Solution:
    def divisorGame(self, n: int) -> bool:
        return n % 2 == 0


sol = Solution()
assert sol.divisorGame(2) == True
assert sol.divisorGame(3) == False
assert sol.divisorGame(4) == True
assert sol.divisorGame(8) == True
"""
URL: https://leetcode.com/problems/fibonacci-number/description/

509. Fibonacci Number

The Fibonacci numbers, commonly denoted F(n) form a sequence, called the Fibonacci sequence, such that each number is the sum of the two preceding ones, starting from 0 and 1. That is,

F(0) = 0, F(1) = 1
F(n) = F(n - 1) + F(n - 2), for n > 1.

Given n, calculate F(n).


Example 1:

Input: n = 2
Output: 1
Explanation: F(2) = F(1) + F(0) = 1 + 0 = 1.

Example 2:

Input: n = 3
Output: 2
Explanation: F(3) = F(2) + F(1) = 1 + 1 = 2.

Example 3:

Input: n = 4
Output: 3
Explanation: F(4) = F(3) + F(2) = 2 + 1 = 3.


Constraints:

    0 <= n <= 30
"""

from functools import cache


class Solution:
    @cache
    def fib(self, n: int) -> int:
        if n <= 1:
            return n
        return self.fib(n - 1) + self.fib(n - 2)


sol = Solution()

assert sol.fib(2) == 1
assert sol.fib(3) == 2
assert sol.fib(4) == 3


"""
URL: https://leetcode.com/problems/palindrome-number/description/

9. Palindrome Number

Given an integer x, return true if x is a palindrome, and false otherwise.


Example 1:

Input: x = 121
Output: true
Explanation: 121 reads as 121 from left to right and from right to left.

Example 2:

Input: x = -121
Output: false
Explanation: From left to right, it reads -121. From right to left, it becomes 121-. Therefore it is not a palindrome.

Example 3:

Input: x = 10
Output: false
Explanation: Reads 01 from right to left. Therefore it is not a palindrome.


Constraints:

    -231 <= x <= 231 - 1


Follow up: Could you solve it without converting the integer to a string?
"""


class Solution:
    def isPalindrome(self, x: int) -> bool:
        neg = x < 0
        if neg:
            return False

        st = str(x)
        for i in range(len(st) // 2):
            if st[i] != st[len(st) - i - 1]:
                return False
        return True


sol = Solution()

assert sol.isPalindrome(1000021) == False
assert sol.isPalindrome(1000021) == False
assert sol.isPalindrome(-121) == False
assert sol.isPalindrome(121) == True
assert sol.isPalindrome(8228) == True
assert sol.isPalindrome(821128) == True
assert sol.isPalindrome(8215128) == True
assert sol.isPalindrome(82155128) == True
assert sol.isPalindrome(8215995128) == True
assert sol.isPalindrome(10) == False
assert sol.isPalindrome(11) == True
assert sol.isPalindrome(1) == True


"""
URL: https://leetcode.com/problems/valid-parentheses/description/

20. Valid Parentheses

Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.

An input string is valid if:

    Open brackets must be closed by the same type of brackets.
    Open brackets must be closed in the correct order.
    Every close bracket has a corresponding open bracket of the same type.


Example 1:
Input: s = "()"
Output: true

Example 2:
Input: s = "()[]{}"
Output: true

Example 3:
Input: s = "(]"
Output: false

Example 4:
Input: s = "([])"
Output: true

Example 5:
Input: s = "([)]"
Output: false


Constraints:

    1 <= s.length <= 104
    s consists of parentheses only '()[]{}'.

"""


class Solution:
    def isValid(self, s: str) -> bool:
        d = {")": "(", "]": "[", "}": "{"}
        stack = []
        for c in s:
            if c not in d:
                stack.append(c)
            else:
                if not stack:
                    return False
                if stack.pop() != d[c]:
                    return False
        return len(stack) == 0


sol = Solution()
assert sol.isValid("(") == False
assert sol.isValid("()") == True
assert sol.isValid("()[]{}") == True
assert sol.isValid("(]") == False
assert sol.isValid("([])") == True
assert sol.isValid("([)]") == False


"""
URL: https://leetcode.com/problems/merge-sorted-array/description/

88. Merge Sorted Array

You are given two integer arrays nums1 and nums2, sorted in non-decreasing order, and two integers m and n, representing the number of elements in nums1 and nums2 respectively.

Merge nums1 and nums2 into a single array sorted in non-decreasing order.

The final sorted array should not be returned by the function, but instead be stored inside the array nums1. To accommodate this, nums1 has a length of m + n, where the first m elements denote the elements that should be merged, and the last n elements are set to 0 and should be ignored. nums2 has a length of n.


Example 1:

Input: nums1 = [1,2,3,0,0,0], m = 3, nums2 = [2,5,6], n = 3
Output: [1,2,2,3,5,6]
Explanation: The arrays we are merging are [1,2,3] and [2,5,6].
The result of the merge is [1,2,2,3,5,6] with the underlined elements coming from nums1.

Example 2:

Input: nums1 = [1], m = 1, nums2 = [], n = 0
Output: [1]
Explanation: The arrays we are merging are [1] and [].
The result of the merge is [1].

Example 3:

Input: nums1 = [0], m = 0, nums2 = [1], n = 1
Output: [1]
Explanation: The arrays we are merging are [] and [1].
The result of the merge is [1].
Note that because m = 0, there are no elements in nums1. The 0 is only there to ensure the merge result can fit in nums1.


Constraints:

    nums1.length == m + n
    nums2.length == n
    0 <= m, n <= 200
    1 <= m + n <= 200
    -109 <= nums1[i], nums2[j] <= 109


Follow up: Can you come up with an algorithm that runs in O(m + n) time?


----------

             a
A = [1,2,3,4,5,0,0,0,0,0]
B = [3,4,5,6,7]
             b


             a
A = [1,2,3,4,5,0,0,0,0,7]
B = [3,4,5,6,7]
           b

             a
A = [1,2,3,4,5,0,0,0,6,7]
B = [3,4,5,6,7]
         b

           a
A = [1,2,3,4,5,0,0,5,6,7]
B = [3,4,5,6,7]
         b

etc.

"""


class Solution:
    def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
        A, B = nums1, nums2
        a = len(A) - len(B) - 1
        b = len(B) - 1
        end = len(A) - 1

        def consume(a, b):
            if a >= 0 and b >= 0:
                na, nb = A[a], B[b]
                if na > nb:
                    return a - 1, b, na
                else:
                    return a, b - 1, nb
            elif a >= 0:
                return a - 1, b, A[a]
            else:
                return a, b - 1, B[b]

        while end >= 0:
            a, b, nums1[end] = consume(a, b)
            end -= 1


sol = Solution()
nums1 = [1, 2, 3, 0, 0, 0]
m = 3
nums2 = [2, 5, 6]
n = 3
sol.merge(nums1, m, nums2, n)
assert nums1 == [1, 2, 2, 3, 5, 6]

nums1 = [1]
m = 1
nums2 = []
n = 0
sol.merge(nums1, m, nums2, n)
assert nums1 == [1]

nums1 = [0]
m = 0
nums2 = [1]
n = 1
sol.merge(nums1, m, nums2, n)
assert nums1 == [1]


"""
URL: https://leetcode.com/problems/plus-one/description/

66. Plus One

You are given a large integer represented as an integer array digits, where each digits[i] is the ith digit of the integer. The digits are ordered from most significant to least significant in left-to-right order. The large integer does not contain any leading 0's.

Increment the large integer by one and return the resulting array of digits.


Example 1:

Input: digits = [1,2,3]
Output: [1,2,4]
Explanation: The array represents the integer 123.
Incrementing by one gives 123 + 1 = 124.
Thus, the result should be [1,2,4].

Example 2:

Input: digits = [4,3,2,1]
Output: [4,3,2,2]
Explanation: The array represents the integer 4321.
Incrementing by one gives 4321 + 1 = 4322.
Thus, the result should be [4,3,2,2].

Example 3:

Input: digits = [9]
Output: [1,0]
Explanation: The array represents the integer 9.
Incrementing by one gives 9 + 1 = 10.
Thus, the result should be [1,0].


Constraints:

    1 <= digits.length <= 100
    0 <= digits[i] <= 9
    digits does not contain any leading 0's.

--------

1 2 3

This case is easy, we just add to the digits[-1] the problem arises if it's 9

1 2 9

In this case, we need to set digits[-1] to 0

1 2 0

then focus on the second to last element, and increment it

1 3 0

so the real edgecase is when it's all 9s

9 9 9

- carry = False
- iterate from right to left
    - if it's the last index:
        - if d < 9
            - add 1
        - else
            - carry = True
            - d = 0
    - elif carry:
        - if d == 9
            - d = 0
    - elif not carry:
        break

- if nums[0] == 0
    - insert 0 at front of digits

"""


class Solution:
    def plusOne(self, digits: List[int]) -> List[int]:
        carry = False
        for i in range(len(digits) - 1, -1, -1):
            d = digits[i]
            is_end = i == len(digits) - 1
            if is_end:
                if d < 9:
                    digits[i] += 1
                else:
                    carry = True
                    digits[i] = 0
            elif carry:
                if d == 9:
                    digits[i] = 0
                    carry = True
                else:
                    digits[i] += 1
                    carry = False
            elif not carry:
                break

        if digits[0] == 0:
            digits.insert(0, 1)

        return digits


sol = Solution()
assert sol.plusOne([1, 2, 3]) == [1, 2, 4]
assert sol.plusOne([4, 3, 2, 1]) == [4, 3, 2, 2]
assert sol.plusOne([0]) == [1]
assert sol.plusOne([1]) == [2]
assert sol.plusOne([9]) == [1, 0]
assert sol.plusOne([9, 9]) == [1, 0, 0]
assert sol.plusOne([1, 9, 9]) == [2, 0, 0]
assert sol.plusOne([1, 1, 9, 9]) == [1, 2, 0, 0]
assert sol.plusOne([9, 9, 9, 9]) == [1, 0, 0, 0, 0]


"""
URL: https://leetcode.com/problems/pascals-triangle-ii/description/

119. Pascal's Triangle II

Given an integer rowIndex, return the rowIndexth (0-indexed) row of the Pascal's triangle.

In Pascal's triangle, each number is the sum of the two numbers directly above it as shown:


Example 1:
Input: rowIndex = 3
Output: [1,3,3,1]
Example 2:
Input: rowIndex = 0
Output: [1]
Example 3:
Input: rowIndex = 1
Output: [1,1]


Constraints:

    0 <= rowIndex <= 33


Follow up: Could you optimize your algorithm to use only O(rowIndex) extra space?

-------

so the rows are:

1
1
12
132
146

"""


class Solution:
    def getRow(self, rowIndex: int) -> List[int]:
        if rowIndex == 0:
            return [1]
        dp = [1, 1]
        for i in range(2, rowIndex + 1):
            dp = [1] + [a + b for a, b in pairwise(dp)] + [1]
        return dp


sol = Solution()
assert sol.getRow(3) == [1, 3, 3, 1]
assert sol.getRow(0) == [1]
assert sol.getRow(1) == [1, 1]


