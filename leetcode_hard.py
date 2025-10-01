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


