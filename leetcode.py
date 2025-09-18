import sys
from typing import List, Optional
from rich import print

"""
151. Reverse Words in a String
Medium
Given an input string s, reverse the order of the words.

A word is defined as a sequence of non-space characters. The words in s will be separated by at least one space.

Return a string of the words in reverse order concatenated by a single space.

Note that s may contain leading or trailing spaces or multiple spaces between two words. The returned string should only have a single space separating the words. Do not include any extra spaces.
 

Example 1:

Input: s = "the sky is blue"
Output: "blue is sky the"
Example 2:

Input: s = "  hello world  "
Output: "world hello"
Explanation: Your reversed string should not contain leading or trailing spaces.
Example 3:

Input: s = "a good   example"
Output: "example good a"
Explanation: You need to reduce multiple spaces between two words to a single space in the reversed string.
 

Constraints:

1 <= s.length <= 104
s contains English letters (upper-case and lower-case), digits, and spaces ' '.
There is at least one word in s.
 

Follow-up: If the string data type is mutable in your language, can you solve it in-place with O(1) extra space?
"""


class Solution:
    def reverseWords(self, s: str) -> str:
        return " ".join(x for x in reversed(s.split()))


sol = Solution()

assert sol.reverseWords(s="the sky is blue") == "blue is sky the"
assert sol.reverseWords(s="  hello world  ") == "world hello"
assert sol.reverseWords(s="a good   example") == "example good a"
assert sol.reverseWords(s="hello") == "hello"
assert sol.reverseWords(s="   hello   ") == "hello"
assert sol.reverseWords(s="Python    is    great") == "great is Python"
assert sol.reverseWords(s="  OpenAI ChatGPT ") == "ChatGPT OpenAI"
assert sol.reverseWords(s="123 456 789") == "789 456 123"
assert sol.reverseWords(s="abc123 def456") == "def456 abc123"
assert (
    sol.reverseWords(s="one two three four five six seven eight nine ten")
    == "ten nine eight seven six five four three two one"
)
assert sol.reverseWords(s="a") == "a"
assert sol.reverseWords(s="word1                    word2") == "word2 word1"

"""
https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/description/

167. Two Sum II - Input Array Is Sorted
Medium
Given a 1-indexed array of integers numbers that is already sorted in non-decreasing order, find two numbers such that they add up to a specific target number. Let these two numbers be numbers[index1] and numbers[index2] where 1 <= index1 < index2 <= numbers.length.

Return the indices of the two numbers, index1 and index2, added by one as an integer array [index1, index2] of length 2.

The tests are generated such that there is exactly one solution. You may not use the same element twice.

Your solution must use only constant extra space.

Example 1:

Input: numbers = [2,7,11,15], target = 9
Output: [1,2]
Explanation: The sum of 2 and 7 is 9. Therefore, index1 = 1, index2 = 2. We return [1, 2].
Example 2:

Input: numbers = [2,3,4], target = 6
Output: [1,3]
Explanation: The sum of 2 and 4 is 6. Therefore index1 = 1, index2 = 3. We return [1, 3].
Example 3:

Input: numbers = [-1,0], target = -1
Output: [1,2]
Explanation: The sum of -1 and 0 is -1. Therefore index1 = 1, index2 = 2. We return [1, 2].
 

Constraints:

2 <= numbers.length <= 3 * 104
-1000 <= numbers[i] <= 1000
numbers is sorted in non-decreasing order.
-1000 <= target <= 1000
The tests are generated such that there is exactly one solution.
"""

"""
238. Product of Array Except Self
Medium
Given an integer array nums, return an array answer such that answer[i] is equal to the product of all the elements of nums except nums[i].
The product of any prefix or suffix of nums is guaranteed to fit in a 32-bit integer.
You must write an algorithm that runs in O(n) time and without using the division operation.

Example 1:

Input: nums = [1,2,3,4]
Output: [24,12,8,6]
Example 2:

Input: nums = [-1,1,0,-3,3]
Output: [0,0,9,0,0]

Constraints:

2 <= nums.length <= 105
-30 <= nums[i] <= 30
The input is generated such that answer[i] is guaranteed to fit in a 32-bit integer.
 

Follow up: Can you solve the problem in O(1) extra space complexity? (The output array does not count as extra space for space complexity analysis.)
"""


class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        res = [1] * len(nums)
        left = 1
        right = 1
        for i in range(len(nums)):
            res[i] *= left
            res[~i] *= right
            left *= nums[i]
            right *= nums[~i]
        return res


sol = Solution()
sol.productExceptSelf(nums=[1, 2, 3, 4])
assert sol.productExceptSelf(nums=[1, 2, 3, 4]) == [24, 12, 8, 6]


class Solution:
    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        left = 0
        right = len(numbers) - 1
        while left < right:
            total = numbers[left] + numbers[right]
            if total == target:
                return [left + 1, right + 1]
            if total < target:
                left += 1
            else:
                right -= 1


sol = Solution()

assert sol.twoSum(numbers=[2, 7, 11, 15], target=9) == [1, 2]
assert sol.twoSum(numbers=[2, 3, 4], target=6) == [1, 3]
assert sol.twoSum(numbers=[-1, 0], target=-1) == [1, 2]
assert sol.twoSum(numbers=[3, 3], target=6) == [1, 2]
assert sol.twoSum(numbers=[-1000, -1000], target=-2000) == [1, 2]
assert sol.twoSum(numbers=[-10, 10], target=0) == [1, 2]
assert sol.twoSum(numbers=[0, 0, 1, 2], target=0) == [1, 2]
assert sol.twoSum(numbers=[-5, -3, 0, 1], target=-8) == [1, 2]
assert sol.twoSum(numbers=[1, 2, 3, 4, 5], target=9) == [4, 5]
assert sol.twoSum(numbers=[1, 3, 5, 8], target=9) == [1, 4]
assert sol.twoSum(numbers=[-2, -1, 4], target=2) == [1, 3]
assert sol.twoSum(numbers=[999, 1000], target=1999) == [1, 2]
assert sol.twoSum(numbers=[-1, 0, 0, 1], target=0) == [1, 4]  # -1 + 1 = 0

"""
283. Move Zeroes
Easy
Given an integer array nums, move all 0's to the end of it while maintaining the relative order of the non-zero elements.

Note that you must do this in-place without making a copy of the array.

Example 1:

Input: nums = [0,1,0,3,12]
Output: [1,3,12,0,0]
Example 2:

Input: nums = [0]
Output: [0]
 

Constraints:

1 <= nums.length <= 104
-231 <= nums[i] <= 231 - 1
 

Follow up: Could you minimize the total number of operations done?
"""


class Solution:
    def moveZeroes(self, nums: List[int]) -> None:
        write = 0
        for read in range(len(nums)):
            if nums[read] != 0:
                nums[write], nums[read] = nums[read], nums[write]
                write += 1


sol = Solution()
nums = [0, 1, 0, 3, 12]
sol.moveZeroes(nums=nums)

nums = [0, 1, 0, 3, 12]
sol.moveZeroes(nums)
assert nums == [1, 3, 12, 0, 0]

nums = [0]
sol.moveZeroes(nums)
assert nums == [0]

nums = [1, 2, 3, 4, 5]
sol.moveZeroes(nums)
assert nums == [1, 2, 3, 4, 5]

nums = [0, 0, 0, 0]
sol.moveZeroes(nums)
assert nums == [0, 0, 0, 0]

nums = [1, 2, 3, 0, 0]
sol.moveZeroes(nums)
assert nums == [1, 2, 3, 0, 0]

nums = [0, 0, 1, 2, 3]
sol.moveZeroes(nums)
assert nums == [1, 2, 3, 0, 0]

nums = [0, 1, 0, 2, 0, 3, 0, 4]
sol.moveZeroes(nums)
assert nums == [1, 2, 3, 4, 0, 0, 0, 0]

nums = [0, -1, 0, -2, -3, 0]
sol.moveZeroes(nums)
assert nums == [-1, -2, -3, 0, 0, 0]

nums = [7]
sol.moveZeroes(nums)
assert nums == [7]

nums = [0, 5, 0, 0, 9, 8, 0, 7, 0, 6, 0, 0, 10]
sol.moveZeroes(nums)
assert nums == [5, 9, 8, 7, 6, 10, 0, 0, 0, 0, 0, 0, 0]


"""
https://leetcode.com/problems/increasing-triplet-subsequence/description

334. Increasing Triplet Subsequence
Medium
Given an integer array nums, return true if there exists a triple of indices (i, j, k) such that i < j < k and nums[i] < nums[j] < nums[k]. If no such indices exists, return false.

Example 1:

Input: nums = [1,2,3,4,5]
Output: true
Explanation: Any triplet where i < j < k is valid.
Example 2:

Input: nums = [5,4,3,2,1]
Output: false
Explanation: No triplet exists.
Example 3:

Input: nums = [2,1,5,0,4,6]
Output: true
Explanation: One of the valid triplet is (3, 4, 5), because nums[3] == 0 < nums[4] == 4 < nums[5] == 6.
 

Constraints:

1 <= nums.length <= 5 * 105
-231 <= nums[i] <= 231 - 1
 

Follow up: Could you implement a solution that runs in O(n) time complexity and O(1) space complexity?
"""


class Solution:  # stub
    def increasingTriplet(self, nums: List[int], N=3) -> bool:
        # todo
        pass


if False:
    sol = Solution()
    assert sol.increasingTriplet([1, 2, 3, 4, 5]) == True
    assert sol.increasingTriplet([5, 4, 3, 2, 1]) == False
    assert sol.increasingTriplet([2, 1, 5, 0, 4, 6]) == True


"""
345. Reverse Vowels of a String
Easy
Given a string s, reverse only all the vowels in the string and return it.

The vowels are 'a', 'e', 'i', 'o', and 'u', and they can appear in both lower and upper cases, more than once.

Example 1:

Input: s = "IceCreAm"

Output: "AceCreIm"

Explanation:

The vowels in s are ['I', 'e', 'e', 'A']. On reversing the vowels, s becomes "AceCreIm".

Example 2:

Input: s = "leetcode"

Output: "leotcede"


Constraints:

1 <= s.length <= 3 * 105
s consist of printable ASCII characters.
"""


class Solution:
    def reverseVowels(self, s: str) -> str:
        s = list(s)
        v = set("aeiouAEIOU")
        left = 0
        right = len(s) - 1
        while left <= right:
            left_is_vowel = s[left] in v
            right_is_vowel = s[right] in v
            if left_is_vowel and right_is_vowel:
                s[left], s[right] = s[right], s[left]
                left += 1
                right -= 1
                continue
            if not left_is_vowel:
                left += 1
            if not right_is_vowel:
                right -= 1
        return "".join(s)


sol = Solution()

assert sol.reverseVowels(s="IceCreAm") == "AceCreIm"
assert sol.reverseVowels(s="") == ""
assert sol.reverseVowels(s="a") == "a"
assert sol.reverseVowels(s="avi") == "iva"
assert sol.reverseVowels(s="aviz") == "ivaz"
assert sol.reverseVowels(s="foobar") == "faobor"
assert sol.reverseVowels(s="leetcode") == "leotcede"
assert sol.reverseVowels(s="hello") == "holle"
assert sol.reverseVowels(s="AEIOU") == "UOIEA"
assert sol.reverseVowels(s="why") == "why"
assert sol.reverseVowels(s="a!e") == "e!a"
assert sol.reverseVowels(s="aaee") == "eeaa"
assert sol.reverseVowels(s="bcdfg") == "bcdfg"
assert sol.reverseVowels(s="b") == "b"
assert sol.reverseVowels(s="123aei456ou789") == "123uoi456ea789"
assert sol.reverseVowels(s="AaEeIiOoUu") == "uUoOiIeEaA"
assert (
    sol.reverseVowels(s="A man a plan a canal: Panama")
    == "a man a plan a canal: PanamA"
)

"""
392. Is Subsequence
Solved
Easy
Topics
premium lock icon
Companies
Given two strings s and t, return true if s is a subsequence of t, or false otherwise.

A subsequence of a string is a new string that is formed from the original string by deleting some (can be none) of the characters without disturbing the relative positions of the remaining characters. (i.e., "ace" is a subsequence of "abcde" while "aec" is not).

 

Example 1:

Input: s = "abc", t = "ahbgdc"
Output: true
Example 2:

Input: s = "axc", t = "ahbgdc"
Output: false
 

Constraints:

0 <= s.length <= 100
0 <= t.length <= 104
s and t consist only of lowercase English letters.
 

Follow up: Suppose there are lots of incoming s, say s1, s2, ..., sk where k >= 109, and you want to check one by one to see if t has its subsequence. In this scenario, how would you change your code?
"""


class Solution:
    def isSubsequence(self, s: str, t: str) -> bool:
        if not s:
            return True
        i = 0
        for c in t:
            if s[i] == c:
                i += 1
            if i == len(s):
                return True
        return False


sol = Solution()

assert sol.isSubsequence(s="abc", t="ahbgdc") == True
assert sol.isSubsequence(s="axc", t="ahbgdc") == False
assert sol.isSubsequence(s="", t="ahbgdc") == True
assert sol.isSubsequence(s="a", t="") == False
assert sol.isSubsequence(s="", t="") == True
assert sol.isSubsequence(s="abc", t="ab") == False
assert sol.isSubsequence(s="leetcode", t="leetcode") == True
assert sol.isSubsequence(s="g", t="ahbgdc") == True
assert sol.isSubsequence(s="z", t="ahbgdc") == False
assert sol.isSubsequence(s="abc", t="aebdc") == True
assert sol.isSubsequence(s="cba", t="ahbgdc") == False
assert sol.isSubsequence(s="aaa", t="aa") == False
assert sol.isSubsequence(s="aaa", t="aaaaa") == True
assert sol.isSubsequence(s="dc", t="ahbgdc") == True
big_t = "a" * 5000 + "b" + "c" * 5000
assert sol.isSubsequence(s="abc", t=big_t) == True
big_s = "a" * 100 + "z"
big_t = "a" * 10000
assert sol.isSubsequence(s=big_s, t=big_t) == False

"""
https://leetcode.com/problems/string-compression/description/

443. String Compression
Medium
Given an array of characters chars, compress it using the following algorithm:

Begin with an empty string s. For each group of consecutive repeating characters in chars:

If the group's length is 1, append the character to s.
Otherwise, append the character followed by the group's length.
The compressed string s should not be returned separately, but instead, be stored in the input character array chars. Note that group lengths that are 10 or longer will be split into multiple characters in chars.

After you are done modifying the input array, return the new length of the array.

You must write an algorithm that uses only constant extra space.

Note: The characters in the array beyond the returned length do not matter and should be ignored.


Example 1:

Input: chars = ["a","a","b","b","c","c","c"]
Output: Return 6, and the first 6 characters of the input array should be: ["a","2","b","2","c","3"]
Explanation: The groups are "aa", "bb", and "ccc". This compresses to "a2b2c3".
Example 2:

Input: chars = ["a"]
Output: Return 1, and the first character of the input array should be: ["a"]
Explanation: The only group is "a", which remains uncompressed since it's a single character.
Example 3:

Input: chars = ["a","b","b","b","b","b","b","b","b","b","b","b","b"]
Output: Return 4, and the first 4 characters of the input array should be: ["a","b","1","2"].
Explanation: The groups are "a" and "bbbbbbbbbbbb". This compresses to "ab12".
 

Constraints:

1 <= chars.length <= 2000
chars[i] is a lowercase English letter, uppercase English letter, digit, or symbol.


"""
from itertools import groupby
from itertools import chain


class Solution:
    def compress(self, chars: List[str]) -> int:
        a = [
            *chain(
                *[
                    (char, *str(count)) if count > 1 else (char)
                    for char, count in [(c, len([*it])) for c, it in groupby(chars)]
                ]
            )
        ]
        chars[: len(a)] = a
        return len(a)


sol = Solution()

chars = ["a", "a", "b", "b", "c", "c", "c"]
ret = sol.compress(chars)
assert ret == 6
assert chars[:ret] == ["a", "2", "b", "2", "c", "3"]

chars = ["a"]
ret = sol.compress(chars)
assert ret == 1
assert chars[:ret] == ["a"]

chars = ["a", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b"]
ret = sol.compress(chars)
assert ret == 4
assert chars[:ret] == ["a", "b", "1", "2"]

chars = ["a", "a", "b", "a"]
ret = sol.compress(chars)
assert chars[:ret] == ["a", "2", "b", "a"]

chars = ["a", "b", "a", "b", "a", "b"]
ret = sol.compress(chars)
assert chars[:ret] == ["a", "b", "a", "b", "a", "b"]

chars = ["a", "b", "b", "a"]
ret = sol.compress(chars)
assert chars[:ret] == ["a", "b", "2", "a"]

chars = ["a", "a", "a", "b", "b", "a", "a"]
ret = sol.compress(chars)
assert chars[:ret] == ["a", "3", "b", "2", "a", "2"]

chars = ["x"] * 12 + ["y"] + ["x"] * 3
ret = sol.compress(chars)
assert chars[:ret] == ["x", "1", "2", "y", "x", "3"]

"""
498. Diagonal Traverse
Medium
Given an m x n matrix mat, return an array of all the elements of the array in a diagonal order.

Example 1:

Input: mat = [[1,2,3],[4,5,6],[7,8,9]]
Output: [1,2,4,7,5,3,6,8,9]
Example 2:

Input: mat = [[1,2],[3,4]]
Output: [1,2,3,4]

Constraints:

m == mat.length
n == mat[i].length
1 <= m, n <= 104
1 <= m * n <= 104
-105 <= mat[i][j] <= 105
"""


class Dir:
    up = 0
    down = 1


class Solution:
    def findDiagonalOrder(self, mat: List[List[int]]) -> List[int]:
        def diag_up(row, col):
            ret = []
            r = row
            c = col
            while r >= 0 and c <= len(mat[0]) - 1:
                ret.append(mat[r][c])
                c += 1
                r -= 1
            return ret

        def diag_down(row, col):
            return [*reversed(diag_up(row, col))]

        def diag(row, col, d):
            return diag_up(row, col) if d == Dir.up else diag_down(row, col)

        ret = []
        d = Dir.up
        rows = [*range(len(mat))] + ([len(mat) - 1] * (len(mat[0]) - 1))
        cols = [0] * len(mat) + [*range(1, len(mat[0]))]
        inds = [*zip(rows, cols)]
        for r, c in inds:
            ret.extend(diag(r, c, d))
            d = Dir.up if d == Dir.down else Dir.down
        return ret


sol = Solution()
assert sol.findDiagonalOrder(mat=[[1, 2, 3], [4, 5, 6], [7, 8, 9]]) == [
    1,
    2,
    4,
    7,
    5,
    3,
    6,
    8,
    9,
]
assert sol.findDiagonalOrder(mat=[[1]]) == [1]
assert sol.findDiagonalOrder(mat=[[1, 2], [3, 4]]) == [1, 2, 3, 4]
assert sol.findDiagonalOrder(
    mat=[[1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [11, 12, 13, 14, 15]]
) == [1, 2, 6, 11, 7, 3, 4, 8, 12, 13, 9, 5, 10, 14, 15]
assert sol.findDiagonalOrder(mat=[[1]]) == [1]
assert sol.findDiagonalOrder(mat=[[1, 2, 3, 4]]) == [1, 2, 3, 4]
assert sol.findDiagonalOrder(mat=[[1], [2], [3], [4]]) == [1, 2, 3, 4]
assert sol.findDiagonalOrder(mat=[[1, 2, 3], [4, 5, 6]]) == [1, 2, 4, 5, 3, 6]
assert sol.findDiagonalOrder(mat=[[1, 2], [3, 4], [5, 6]]) == [1, 2, 3, 5, 4, 6]
assert sol.findDiagonalOrder(mat=[[1, 2], [3, 4], [5, 6], [7, 8]]) == [
    1,
    2,
    3,
    5,
    4,
    6,
    7,
    8,
]
assert sol.findDiagonalOrder(mat=[[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]) == [
    1,
    2,
    5,
    9,
    6,
    3,
    4,
    7,
    10,
    11,
    8,
    12,
]
assert sol.findDiagonalOrder(mat=[[-1, -2, -3], [-4, -5, -6]]) == [
    -1,
    -2,
    -4,
    -5,
    -3,
    -6,
]


"""
https://leetcode.com/problems/base-7/description/

504. Base 7
Easy
Given an integer num, return a string of its base 7 representation.

Example 1:

Input: num = 100
Output: "202"
Example 2:

Input: num = -7
Output: "-10"

Constraints:

-107 <= num <= 107
"""


class Solution:
    def convertToBase7(self, num: int) -> str:
        if num == 0:
            return "0"
        res = ""
        sign = 1 if num >= 0 else -1
        num *= sign
        while num > 0:
            val, r = divmod(num, 7)
            res += str(r)
            num = val
        res = ("-" if sign == -1 else "") + res[::-1]
        return res


sol = Solution()
assert sol.convertToBase7(100) == "202"
assert sol.convertToBase7(-7) == "-10"
assert sol.convertToBase7(0) == "0"
assert sol.convertToBase7(1) == "1"
assert sol.convertToBase7(6) == "6"
assert sol.convertToBase7(7) == "10"
assert sol.convertToBase7(8) == "11"
assert sol.convertToBase7(48) == "66"
assert sol.convertToBase7(49) == "100"
assert sol.convertToBase7(50) == "101"
assert sol.convertToBase7(-1) == "-1"
assert sol.convertToBase7(-6) == "-6"
assert sol.convertToBase7(-8) == "-11"
assert sol.convertToBase7(343) == "1000"
assert sol.convertToBase7(-343) == "-1000"
assert sol.convertToBase7(1000000) == "11333311"
assert sol.convertToBase7(-1000000) == "-11333311"

"""
https://leetcode.com/problems/can-place-flowers/description

605. Can Place Flowers
Easy
You have a long flowerbed in which some of the plots are planted, and some are not. However, flowers cannot be planted in adjacent plots.

Given an integer array flowerbed containing 0's and 1's, where 0 means empty and 1 means not empty, and an integer n, return true if n new flowers can be planted in the flowerbed without violating the no-adjacent-flowers rule and false otherwise.

Example 1:

Input: flowerbed = [1,0,0,0,1], n = 1
Output: true
Example 2:

Input: flowerbed = [1,0,0,0,1], n = 2
Output: false

Constraints:

1 <= flowerbed.length <= 2 * 104
flowerbed[i] is 0 or 1.
There are no two adjacent flowers in flowerbed.
0 <= n <= flowerbed.length
"""


class Solution:
    def canPlaceFlowers(self, flowerbed: List[int], n: int) -> bool:
        added = 0
        for i in range(len(flowerbed)):
            left_slot_free = i == 0 or flowerbed[i - 1] == 0
            right_slot_free = i == len(flowerbed) - 1 or flowerbed[i + 1] == 0
            if (left_slot_free and right_slot_free) and flowerbed[i] == 0:
                if added < n:
                    flowerbed[i] = 1
                    added += 1
        return added == n


sol = Solution()
assert sol.canPlaceFlowers(flowerbed=[1, 0, 0, 0, 1], n=1) == True
assert sol.canPlaceFlowers(flowerbed=[1, 0, 0, 0, 1], n=2) == False
assert sol.canPlaceFlowers(flowerbed=[1, 0, 0, 0, 0, 0, 0, 1], n=2) == True
assert sol.canPlaceFlowers(flowerbed=[1, 0, 0, 1, 0, 0, 0, 1], n=1) == True
assert sol.canPlaceFlowers(flowerbed=[0, 1, 0, 1, 0, 0, 0, 1, 0, 1], n=1) == True
assert sol.canPlaceFlowers(flowerbed=[0], n=1) == True
assert sol.canPlaceFlowers(flowerbed=[0], n=0) == True
assert sol.canPlaceFlowers(flowerbed=[1], n=0) == True
assert sol.canPlaceFlowers(flowerbed=[1], n=1) == False
assert sol.canPlaceFlowers(flowerbed=[0, 0, 0], n=2) == True
assert sol.canPlaceFlowers(flowerbed=[0, 0, 0], n=1) == True
assert sol.canPlaceFlowers(flowerbed=[0, 0, 0], n=3) == False
assert sol.canPlaceFlowers(flowerbed=[0, 0, 1, 0, 0], n=2) == True
assert sol.canPlaceFlowers(flowerbed=[0, 0, 1, 0, 0], n=1) == True
assert sol.canPlaceFlowers(flowerbed=[0] * 5, n=3) == True
assert sol.canPlaceFlowers(flowerbed=[0] * 5, n=2) == True
assert sol.canPlaceFlowers(flowerbed=[1, 0, 1, 0, 1], n=0) == True
assert sol.canPlaceFlowers(flowerbed=[1, 0, 1, 0, 1], n=1) == False

"""
643. Maximum Average Subarray I
Easy
Topics
premium lock icon
Companies
You are given an integer array nums consisting of n elements, and an integer k.

Find a contiguous subarray whose length is equal to k that has the maximum average value and return this value. Any answer with a calculation error less than 10-5 will be accepted.

 

Example 1:

Input: nums = [1,12,-5,-6,50,3], k = 4
Output: 12.75000
Explanation: Maximum average is (12 - 5 - 6 + 50) / 4 = 51 / 4 = 12.75
Example 2:

Input: nums = [5], k = 1
Output: 5.00000
 

Constraints:

n == nums.length
1 <= k <= n <= 105
-104 <= nums[i] <= 104
"""


class Solution:
    def findMaxAverage(self, nums: List[int], k: int) -> float:
        left = 0
        right = k - 1
        av = sum(nums[:k]) / k
        _max = av
        for i in range(k, len(nums)):
            av -= nums[i - k] / k
            av += nums[i] / k
            _max = max(_max, av)
        return int((_max) * 10**5) / 10**5


sol = Solution()
assert sol.findMaxAverage(nums=[1, 12, -5, -6, 50, 3], k=4) == 12.75000
assert sol.findMaxAverage(nums=[5], k=1) == 5
assert sol.findMaxAverage(nums=[0], k=1) == 0.0
assert sol.findMaxAverage(nums=[-1], k=1) == -1.0
assert sol.findMaxAverage(nums=[1, 2, 3, 4, 5], k=3) == 4.0
assert sol.findMaxAverage(nums=[-1, -2, -3, -4, -5], k=3) == -2.0
assert sol.findMaxAverage(nums=[1, 2, 3, 4, 5, 6], k=6) == 3.5
assert sol.findMaxAverage(nums=[10, 20, 30, 40], k=2) == 35.0
assert sol.findMaxAverage(nums=[5, 5, 5, 5], k=4) == 5.0
assert sol.findMaxAverage(nums=[1, -1, 1, -1], k=1) == 1.0
assert sol.findMaxAverage(nums=[1, -1, 1, -1], k=4) == 0.0
assert sol.findMaxAverage(nums=[4, 2, 1, 3, 0, 5], k=2) == 3.0
assert sol.findMaxAverage(nums=[3, -2, 5, 1, 7], k=3) == 4.33333


"""
https://leetcode.com/problems/find-pivot-index/description

724. Find Pivot Index
Easy
Given an array of integers nums, calculate the pivot index of this array.

The pivot index is the index where the sum of all the numbers strictly to the left of the index is equal to the sum of all the numbers strictly to the index's right.

If the index is on the left edge of the array, then the left sum is 0 because there are no elements to the left. This also applies to the right edge of the array.

Return the leftmost pivot index. If no such index exists, return -1.
 

Example 1:

Input: nums = [1,7,3,6,5,6]
Output: 3
Explanation:
The pivot index is 3.
Left sum = nums[0] + nums[1] + nums[2] = 1 + 7 + 3 = 11
Right sum = nums[4] + nums[5] = 5 + 6 = 11
Example 2:

Input: nums = [1,2,3]
Output: -1
Explanation:
There is no index that satisfies the conditions in the problem statement.
Example 3:

Input: nums = [2,1,-1]
Output: 0
Explanation:
The pivot index is 0.
Left sum = 0 (no elements to the left of index 0)
Right sum = nums[1] + nums[2] = 1 + -1 = 0
 

Constraints:

1 <= nums.length <= 104
-1000 <= nums[i] <= 1000
 

Note: This question is the same as 1991: https://leetcode.com/problems/find-the-middle-index-in-array/
"""


class Solution:
    def pivotIndex(self, nums: List[int]) -> int:
        total = sum(nums)
        prefix_sum = 0
        for i, n in enumerate(nums):
            total -= n
            if prefix_sum == total:
                return i
            prefix_sum += n
        return -1


sol = Solution()

assert sol.pivotIndex([1, 7, 3, 6, 5, 6]) == 3
assert sol.pivotIndex([1, 2, 3]) == -1
assert sol.pivotIndex([2, 1, -1]) == 0
assert sol.pivotIndex([5]) == 0
assert sol.pivotIndex([1, -1]) == -1
assert sol.pivotIndex([0, 0, 0]) == 0
assert sol.pivotIndex([-1, -1, 0, 1, 1, 0]) == 5
assert sol.pivotIndex([1000, -1000, 0]) == 2
assert sol.pivotIndex([10, 20, 30, 40]) == -1
assert sol.pivotIndex([0, 0, 0, 0]) == 0
assert sol.pivotIndex([-2, -1, -1, -2, -6]) == -1
assert sol.pivotIndex([1, 2, 3, 4, 6]) == 3

"""
https://leetcode.com/problems/transpose-matrix/description/

867. Transpose Matrix
Easy
Given a 2D integer array matrix, return the transpose of matrix.

The transpose of a matrix is the matrix flipped over its main diagonal, switching the matrix's row and column indices.

Example 1:

Input: matrix = [[1,2,3],[4,5,6],[7,8,9]]
Output: [[1,4,7],[2,5,8],[3,6,9]]
Example 2:

Input: matrix = [[1,2,3],[4,5,6]]
Output: [[1,4],[2,5],[3,6]]
 

Constraints:

m == matrix.length
n == matrix[i].length
1 <= m, n <= 1000
1 <= m * n <= 105
-109 <= matrix[i][j] <= 109
"""

"""
1 2 3
4 5 6
7 8 9


"""


class Solution:
    def transpose(self, matrix: List[List[int]]) -> List[List[int]]:
        return [list(x) for x in zip(*matrix)]


sol = Solution()
assert sol.transpose(matrix=[[1, 2, 3], [4, 5, 6], [7, 8, 9]]) == [
    [1, 4, 7],
    [2, 5, 8],
    [3, 6, 9],
]

assert sol.transpose(matrix=[[1, 2, 3], [4, 5, 6]]) == [[1, 4], [2, 5], [3, 6]]
assert sol.transpose(matrix=[[1]]) == [[1]]
assert sol.transpose(matrix=[[1, 2], [3, 4]]) == [[1, 3], [2, 4]]
assert sol.transpose(matrix=[[5]]) == [[5]]
assert sol.transpose(matrix=[[1, 2, 3, 4]]) == [[1], [2], [3], [4]]
assert sol.transpose(matrix=[[1], [2], [3], [4]]) == [[1, 2, 3, 4]]
assert sol.transpose(matrix=[[0, 0, 0], [0, 0, 0], [0, 0, 0]]) == [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]
assert sol.transpose(matrix=[[1, 2], [3, 4], [5, 6]]) == [[1, 3, 5], [2, 4, 6]]
assert sol.transpose(matrix=[[1, 3, 5], [2, 4, 6]]) == [[1, 2], [3, 4], [5, 6]]
assert sol.transpose(matrix=[[-1, -2], [-3, -4]]) == [[-1, -3], [-2, -4]]
assert sol.transpose(matrix=[[10, 20, 30], [40, 50, 60]]) == [
    [10, 40],
    [20, 50],
    [30, 60],
]
assert sol.transpose(matrix=[[7, 8, 9], [1, 2, 3], [4, 5, 6]]) == [
    [7, 1, 4],
    [8, 2, 5],
    [9, 3, 6],
]
assert sol.transpose(matrix=[[2]]) == [[2]]
assert sol.transpose(matrix=[[1, 2, 3]]) == [[1], [2], [3]]
assert sol.transpose(matrix=[[1], [2], [3]]) == [[1, 2, 3]]
assert sol.transpose(matrix=[[0]]) == [[0]]


"""
https://leetcode.com/problems/leaf-similar-trees/description/

872. Leaf-Similar Trees
Consider all the leaves of a binary tree, from left to right order, the values of those leaves form a leaf value sequence.

For example, in the given tree above, the leaf value sequence is (6, 7, 4, 9, 8).

Two binary trees are considered leaf-similar if their leaf value sequence is the same.

Return true if and only if the two given trees with head nodes root1 and root2 are leaf-similar.

Example 1:

Input: root1 = [3,5,1,6,2,9,8,null,null,7,4], root2 = [3,5,1,6,7,4,2,null,null,null,null,null,null,9,8]
Output: true
Example 2:

Input: root1 = [1,2,3], root2 = [1,3,2]
Output: false

Constraints:

The number of nodes in each tree will be in the range [1, 200].
Both of the given trees will have values in the range [0, 200].
"""


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def leafSimilar(self, root1: Optional[TreeNode], root2: Optional[TreeNode]) -> bool:

        def dfs(node, leaves):
            if not node:
                return
            is_leaf = node.left == node.right == None
            if is_leaf:
                leaves.append(node.val)
                return
            dfs(node.left, leaves)
            dfs(node.right, leaves)

        leaves1 = []
        leaves2 = []
        dfs(root1, leaves1)
        dfs(root2, leaves2)
        return leaves1 == leaves2


sol = Solution()

root1 = TreeNode(
    3,
    TreeNode(5, TreeNode(6), TreeNode(2, TreeNode(7), TreeNode(4))),
    TreeNode(1, TreeNode(9), TreeNode(8)),
)
root2 = TreeNode(
    3,
    TreeNode(5, TreeNode(6), TreeNode(7)),
    TreeNode(1, TreeNode(4), TreeNode(2, TreeNode(9), TreeNode(8))),
)
assert sol.leafSimilar(root1, root2) == True
root1 = TreeNode(1, TreeNode(2), TreeNode(3))
root2 = TreeNode(1, TreeNode(3), TreeNode(2))
assert sol.leafSimilar(root1, root2) == False
root1 = TreeNode(1)
root2 = TreeNode(1)
assert sol.leafSimilar(root1, root2) == True
root1 = TreeNode(1)
root2 = TreeNode(2)
assert sol.leafSimilar(root1, root2) == False
root1 = TreeNode(1, TreeNode(2))
root2 = TreeNode(1, None, TreeNode(2))
assert sol.leafSimilar(root1, root2) == True
root1 = TreeNode(1, TreeNode(2))
root2 = TreeNode(1, None, TreeNode(3))
assert sol.leafSimilar(root1, root2) == False
root1 = TreeNode(1, TreeNode(2, TreeNode(4), TreeNode(5)), TreeNode(3))
root2 = TreeNode(1, TreeNode(2), TreeNode(3, TreeNode(4), TreeNode(5)))
assert sol.leafSimilar(root1, root2) == False
root1 = TreeNode(1, TreeNode(2, TreeNode(4), TreeNode(5)), TreeNode(3))
root2 = TreeNode(1, TreeNode(2), TreeNode(3, TreeNode(4)))
assert sol.leafSimilar(root1, root2) == False
root1 = TreeNode(0, TreeNode(1), TreeNode(1))
root2 = TreeNode(0, TreeNode(1), TreeNode(1))
assert sol.leafSimilar(root1, root2) == True
root1 = TreeNode(0, TreeNode(1, TreeNode(3)))
root2 = TreeNode(3)
assert sol.leafSimilar(root1, root2) == True
root1 = TreeNode(0, TreeNode(0))
root2 = TreeNode(0, None, TreeNode(0))
assert sol.leafSimilar(root1, root2) == True
root1 = TreeNode(200, TreeNode(0, TreeNode(0), TreeNode(0)), TreeNode(0))
root2 = TreeNode(100, TreeNode(0), TreeNode(0, TreeNode(0), TreeNode(0)))
assert sol.leafSimilar(root1, root2) == True
root1 = TreeNode(1, None, TreeNode(2, TreeNode(3)))
root2 = TreeNode(1, TreeNode(2, None, TreeNode(3)))
assert sol.leafSimilar(root1, root2) == True
root1 = TreeNode(1, TreeNode(2, TreeNode(3)))
root2 = TreeNode(3, TreeNode(2), TreeNode(1))
assert sol.leafSimilar(root1, root2) == False

"""
1004. Max Consecutive Ones III
Medium
Given a binary array nums and an integer k, return the maximum number of consecutive 1's in the array if you can flip at most k 0's.

Example 1:

Input: nums = [1,1,1,0,0,0,1,1,1,1,0], k = 2
Output: 6
Explanation: [1,1,1,0,0,1,1,1,1,1,1]
Bolded numbers were flipped from 0 to 1. The longest subarray is underlined.
Example 2:

Input: nums = [0,0,1,1,0,0,1,1,1,0,1,1,0,0,0,1,1,1,1], k = 3
Output: 10
Explanation: [0,0,1,1,1,1,1,1,1,1,1,1,0,0,0,1,1,1,1]
Bolded numbers were flipped from 0 to 1. The longest subarray is underlined.
 

Constraints:

1 <= nums.length <= 105
nums[i] is either 0 or 1.
0 <= k <= nums.length
"""


class Solution:
    def longestOnes(self, nums: List[int], k: int) -> int:
        one_count = 0
        zeros = 0
        ones = 0
        left = 0
        _max = 0
        for right in range(len(nums)):
            v = nums[right]
            ones += v == 1
            zeros += v == 0
            if zeros > k:
                ones -= nums[left] == 1
                zeros -= nums[left] == 0
                left += 1
            _max = max(_max, ones + zeros)
        return _max


sol = Solution()

assert sol.longestOnes(nums=[1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0], k=2) == 6
assert (
    sol.longestOnes(nums=[0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1], k=3)
    == 10
)
assert sol.longestOnes(nums=[1], k=0) == 1
assert sol.longestOnes(nums=[0], k=0) == 0
assert sol.longestOnes(nums=[0], k=1) == 1
assert sol.longestOnes(nums=[1, 1, 1], k=0) == 3
assert sol.longestOnes(nums=[1, 0, 1], k=1) == 3
assert sol.longestOnes(nums=[1, 0, 1], k=0) == 1
assert sol.longestOnes(nums=[0, 0, 0], k=2) == 2
assert sol.longestOnes(nums=[1, 1, 0, 0, 1, 1], k=1) == 3
assert sol.longestOnes(nums=[0, 1, 0, 1, 0], k=2) == 4
assert sol.longestOnes(nums=[1, 1, 1, 0, 1, 1, 1], k=1) == 7
assert sol.longestOnes(nums=[0] * 5, k=3) == 3
assert sol.longestOnes(nums=[1, 0, 0, 0, 1], k=2) == 3
assert sol.longestOnes(nums=[1, 1, 0, 1, 0, 1, 1], k=2) == 7

"""
https://leetcode.com/problems/greatest-common-divisor-of-strings/description

1071. Greatest Common Divisor of Strings
Easy
For two strings s and t, we say "t divides s" if and only if s = t + t + t + ... + t + t (i.e., t is concatenated with itself one or more times).

Given two strings str1 and str2, return the largest string x such that x divides both str1 and str2.

Example 1:

Input: str1 = "ABCABC", str2 = "ABC"
Output: "ABC"
Example 2:

Input: str1 = "ABABAB", str2 = "ABAB"
Output: "AB"
Example 3:

Input: str1 = "LEET", str2 = "CODE"
Output: ""

Constraints:

1 <= str1.length, str2.length <= 1000
str1 and str2 consist of English uppercase letters.

"""

from itertools import zip_longest


class Solution:
    def gcdOfStrings(self, str1: str, str2: str) -> str:
        def batched(s, n=1):
            r = list(range(0, len(s), n))
            return [s[a:b] for a, b in zip_longest(r, r[1:])]

        batch_match = lambda x: all([a == b for a, b in zip(x, x[1:])])

        for n in range(len(str2), 0, -1):
            b1, b2 = batched(str1, n), batched(str2, n)
            if b1[0] == b2[0] and batch_match(b1) and batch_match(b2):
                return b1[0]

        return ""


sol = Solution()

assert sol.gcdOfStrings(str1="ABCABC", str2="ABC") == "ABC"
assert sol.gcdOfStrings(str1="ABABAB", str2="ABAB") == "AB"
assert sol.gcdOfStrings(str1="LEET", str2="CODE") == ""
assert sol.gcdOfStrings(str1="A", str2="A") == "A"
assert sol.gcdOfStrings(str1="A", str2="B") == ""
assert sol.gcdOfStrings(str1="A", str2="AAA") == "A"
assert sol.gcdOfStrings(str1="AAAA", str2="AA") == "AA"
assert sol.gcdOfStrings(str1="AAA", str2="AA") == "A"
assert sol.gcdOfStrings(str1="ABCDEF", str2="ABC") == ""
assert sol.gcdOfStrings(str1="ABC", str2="ABC") == "ABC"
assert sol.gcdOfStrings(str1="AB", str2="ABABAB") == "AB"
assert sol.gcdOfStrings(str1="ABAB", str2="BABA") == ""
assert sol.gcdOfStrings(str1="ABCABCABCABC", str2="ABCABCABC") == "ABC"

"""
1431. Kids With the Greatest Number of Candies
Easy
There are n kids with candies. You are given an integer array candies, where each candies[i] represents the number of candies the ith kid has, and an integer extraCandies, denoting the number of extra candies that you have.

Return a boolean array result of length n, where result[i] is true if, after giving the ith kid all the extraCandies, they will have the greatest number of candies among all the kids, or false otherwise.

Note that multiple kids can have the greatest number of candies.

 

Example 1:

Input: candies = [2,3,5,1,3], extraCandies = 3
Output: [true,true,true,false,true] 
Explanation: If you give all extraCandies to:
- Kid 1, they will have 2 + 3 = 5 candies, which is the greatest among the kids.
- Kid 2, they will have 3 + 3 = 6 candies, which is the greatest among the kids.
- Kid 3, they will have 5 + 3 = 8 candies, which is the greatest among the kids.
- Kid 4, they will have 1 + 3 = 4 candies, which is not the greatest among the kids.
- Kid 5, they will have 3 + 3 = 6 candies, which is the greatest among the kids.
Example 2:

Input: candies = [4,2,1,1,2], extraCandies = 1
Output: [true,false,false,false,false] 
Explanation: There is only 1 extra candy.
Kid 1 will always have the greatest number of candies, even if a different kid is given the extra candy.
Example 3:

Input: candies = [12,1,12], extraCandies = 10
Output: [true,false,true]
 

Constraints:

n == candies.length
2 <= n <= 100
1 <= candies[i] <= 100
1 <= extraCandies <= 50
"""


class Solution:
    def kidsWithCandies(self, candies: List[int], extraCandies: int) -> List[bool]:
        _max = max(candies)
        return [x + extraCandies >= _max for x in candies]


sol = Solution()

true = True
false = False

assert sol.kidsWithCandies(candies=[2, 3, 5, 1, 3], extraCandies=3) == [
    True,
    True,
    True,
    False,
    True,
]
assert sol.kidsWithCandies(candies=[4, 2, 1, 1, 2], extraCandies=1) == [
    True,
    False,
    False,
    False,
    False,
]
assert sol.kidsWithCandies(candies=[12, 1, 12], extraCandies=10) == [True, False, True]
assert sol.kidsWithCandies(candies=[1, 1], extraCandies=1) == [True, True]
assert sol.kidsWithCandies(candies=[1, 100], extraCandies=1) == [False, True]
assert sol.kidsWithCandies(candies=[50, 50, 50, 50], extraCandies=1) == [
    True,
    True,
    True,
    True,
]
assert sol.kidsWithCandies(candies=[1, 1, 1], extraCandies=50) == [True, True, True]
assert sol.kidsWithCandies(candies=[100, 100], extraCandies=1) == [True, True]
assert sol.kidsWithCandies(candies=[1, 2, 3], extraCandies=2) == [True, True, True]
assert sol.kidsWithCandies(candies=[1, 2, 3], extraCandies=1) == [False, True, True]
assert sol.kidsWithCandies(candies=[5, 3, 5, 4], extraCandies=1) == [
    True,
    False,
    True,
    True,
]


"""
https://leetcode.com/problems/shuffle-the-array/

1470. Shuffle the Array
Easy
Given the array nums consisting of 2n elements in the form [x1,x2,...,xn,y1,y2,...,yn].

Return the array in the form [x1,y1,x2,y2,...,xn,yn].

Example 1:

Input: nums = [2,5,1,3,4,7], n = 3
Output: [2,3,5,4,1,7] 
Explanation: Since x1=2, x2=5, x3=1, y1=3, y2=4, y3=7 then the answer is [2,3,5,4,1,7].
Example 2:

Input: nums = [1,2,3,4,4,3,2,1], n = 4
Output: [1,4,2,3,3,2,4,1]
Example 3:

Input: nums = [1,1,2,2], n = 2
Output: [1,2,1,2]
 

Constraints:

1 <= n <= 500
nums.length == 2n
1 <= nums[i] <= 10^3
"""

from itertools import chain


class Solution:
    def shuffle(self, nums: List[int], n: int) -> List[int]:
        return [*chain(*[[nums[i], nums[n + i]] for i in range(n)])]


sol = Solution()
assert sol.shuffle(nums=[2, 5, 1, 3, 4, 7], n=3) == [2, 3, 5, 4, 1, 7]
assert sol.shuffle(nums=[1, 2, 3, 4, 4, 3, 2, 1], n=4) == [1, 4, 2, 3, 3, 2, 4, 1]
assert sol.shuffle(nums=[1, 1, 2, 2], n=2) == [1, 2, 1, 2]
assert sol.shuffle(nums=[1, 2], n=1) == [1, 2]
assert sol.shuffle(nums=[5, 6], n=1) == [5, 6]
assert sol.shuffle(nums=[1, 3, 5, 7, 2, 4, 6, 8], n=4) == [1, 2, 3, 4, 5, 6, 7, 8]
assert sol.shuffle(nums=[10, 20, 30, 40, 50, 60], n=3) == [10, 40, 20, 50, 30, 60]
assert sol.shuffle(nums=[100, 200], n=1) == [100, 200]
assert sol.shuffle(nums=[1, 1, 1, 1, 1, 1], n=3) == [1, 1, 1, 1, 1, 1]
assert sol.shuffle(nums=[2, 4, 6, 8, 10, 12, 1, 3, 5, 7, 9, 11], n=6) == [
    2,
    1,
    4,
    3,
    6,
    5,
    8,
    7,
    10,
    9,
    12,
    11,
]
assert sol.shuffle(nums=[999, 1000, 1, 2], n=2) == [999, 1, 1000, 2]
assert sol.shuffle(nums=[3, 6, 9, 12, 15, 18, 21, 24, 1, 2, 3, 4, 5, 6, 7, 8], n=8) == [
    3,
    1,
    6,
    2,
    9,
    3,
    12,
    4,
    15,
    5,
    18,
    6,
    21,
    7,
    24,
    8,
]
assert sol.shuffle(nums=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], n=5) == [
    1,
    6,
    2,
    7,
    3,
    8,
    4,
    9,
    5,
    10,
]
assert sol.shuffle(nums=[50, 51, 52, 53], n=2) == [50, 52, 51, 53]
assert sol.shuffle(nums=[1000, 999, 998, 1, 2, 3], n=3) == [1000, 1, 999, 2, 998, 3]
assert sol.shuffle(nums=[7, 14], n=1) == [7, 14]

"""
https://leetcode.com/problems/valid-boomerang/

1037 - Valid Boomerang

Given an array points where points[i] = [xi, yi] represents a point on the X-Y plane, return true if these points are a boomerang.
A boomerang is a set of three points that are all distinct and not in a straight line.

Example 1:

Input: points = [[1,1],[2,3],[3,2]]
Output: true
Example 2:

Input: points = [[1,1],[2,2],[3,3]]
Output: false


Constraints:

points.length == 3
points[i].length == 2
0 <= xi, yi <= 100


# Notes:

This isn't the slop, it's the inverse. 

Todo: Revisit with cross multiplication.

"""


class Solution:
    def isBoomerang(self, points: List[List[int]]) -> bool:
        non_overlapping = all(a != b for a, b in zip(points, points[1:]))

        def get_slope(a, b):
            if a[0] == b[0]:
                return float("-inf")
            elif a[1] == b[1]:
                return float("inf")
            else:
                return (a[0] - b[0]) / (a[1] - b[1])

        slopes = [get_slope(a, b) for a, b in zip(points, points[1:])]
        return non_overlapping and slopes[0] != slopes[1]


sol = Solution()
assert sol.isBoomerang([[1, 1], [2, 3], [3, 2]]) == True
assert sol.isBoomerang([[1, 1], [2, 2], [3, 3]]) == False
assert sol.isBoomerang([[0, 1], [0, 2], [1, 2]]) == True
assert sol.isBoomerang([[0, 2], [2, 1], [0, 0]]) == True
assert sol.isBoomerang([[0, 0], [0, 0], [1, 1]]) == False
assert sol.isBoomerang([[0, 0], [0, 0], [0, 0]]) == False
assert sol.isBoomerang([[0, 0], [1, 0], [0, 0]]) == False
assert sol.isBoomerang([[0, 0], [0, 1], [0, 2]]) == False
assert sol.isBoomerang([[0, 0], [1, 0], [2, 0]]) == False
assert sol.isBoomerang([[0, 0], [1, 1], [2, 2]]) == False
assert sol.isBoomerang([[1, 2], [3, 4], [5, 6]]) == False
assert sol.isBoomerang([[-1, 0], [0, 0], [1, 0]]) == False
assert sol.isBoomerang([[0, 0], [1, 1], [2, 3]]) == True
assert sol.isBoomerang([[0, 0], [0, 1], [1, 0]]) == True
assert sol.isBoomerang([[1, 1], [2, 2], [3, 4]]) == True
assert sol.isBoomerang([[-1, -1], [0, 0], [1, 2]]) == True
assert sol.isBoomerang([[100, 100], [200, 200], [300, 301]]) == True
assert sol.isBoomerang([[0, 1], [1, 0], [2, 0]]) == True
assert sol.isBoomerang([[1, 0], [1, 1], [1, 2]]) == False
assert sol.isBoomerang([[2, 2], [3, 3], [1, 1]]) == False


"""
https://leetcode.com/problems/maximum-number-of-vowels-in-a-substring-of-given-length/description/

1456. Maximum Number of Vowels in a Substring of Given Length
Medium
Given a string s and an integer k, return the maximum number of vowel letters in any substring of s with length k.

Vowel letters in English are 'a', 'e', 'i', 'o', and 'u'.

Example 1:

Input: s = "abciiidef", k = 3
Output: 3
Explanation: The substring "iii" contains 3 vowel letters.
Example 2:

Input: s = "aeiou", k = 2
Output: 2
Explanation: Any substring of length 2 contains 2 vowels.
Example 3:

Input: s = "leetcode", k = 3
Output: 2
Explanation: "lee", "eet" and "ode" contain 2 vowels.
 

Constraints:

1 <= s.length <= 105
s consists of lowercase English letters.
1 <= k <= s.length
"""


class Solution:
    def maxVowels(self, s: str, k: int) -> int:
        v = set("aeiou")
        _max = sum([x in v for x in s[:k]])
        count = _max
        for i in range(k, len(s)):
            count -= s[i - k] in v
            count += s[i] in v
            _max = max(_max, count)
        return _max


sol = Solution()
assert sol.maxVowels(s="tryhard", k=4) == 1
assert sol.maxVowels(s="abciiidef", k=3) == 3
assert sol.maxVowels(s="aeiou", k=2) == 2
assert sol.maxVowels(s="leetcode", k=3) == 2
assert sol.maxVowels(s="a", k=1) == 1
assert sol.maxVowels(s="b", k=1) == 0
assert sol.maxVowels(s="aeiou", k=5) == 5
assert sol.maxVowels(s="aeiou", k=3) == 3
assert sol.maxVowels(s="consonants", k=4) == 2
assert sol.maxVowels(s="abcdeiou", k=3) == 3
assert sol.maxVowels(s="leetcode", k=1) == 1
assert sol.maxVowels(s="rhythms", k=3) == 0
assert sol.maxVowels(s="tryhard", k=2) == 1
assert sol.maxVowels(s="weallloveyou", k=7) == 4

"""
1493. Longest Subarray of 1's After Deleting One Element
Medium
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

Hint 1
Maintain a sliding window where there is at most one zero in it.
"""


class Solution:  # stub
    def longestSubarray(self, nums: List[int]) -> int:
        # todo
        pass


if False:
    sol = Solution()
    assert sol.longestSubarray(nums=[1, 1, 0, 1]) == 3
    assert sol.longestSubarray(nums=[0, 1, 1, 1, 0, 1, 1, 0, 1]) == 5
    assert sol.longestSubarray(nums=[1, 1, 1]) == 2
    assert sol.longestSubarray(nums=[1]) == 0
    assert sol.longestSubarray(nums=[1, 1, 1, 1, 0]) == 4
    assert sol.longestSubarray(nums=[1, 1, 0, 1, 1]) == 4
    assert sol.longestSubarray(nums=[1, 1, 0, 0, 1, 1]) == 2

"""
https://leetcode.com/problems/water-bottles/

1518. Water Bottles
There are numBottles water bottles that are initially full of water. You can exchange numExchange empty water bottles from the market with one full water bottle.

The operation of drinking a full water bottle turns it into an empty bottle.

Given the two integers numBottles and numExchange, return the maximum number of water bottles you can drink.

Example 1:

Input: numBottles = 9, numExchange = 3
Output: 13
Explanation: You can exchange 3 empty bottles to get 1 full water bottle.
Number of water bottles you can drink: 9 + 3 + 1 = 13.
Example 2:


Input: numBottles = 15, numExchange = 4
Output: 19
Explanation: You can exchange 4 empty bottles to get 1 full water bottle. 
Number of water bottles you can drink: 15 + 3 + 1 = 19.
 

Constraints:

1 <= numBottles <= 100
2 <= numExchange <= 100
"""


class Solution:
    def numWaterBottles(self, numBottles: int, numExchange: int) -> int:
        drink = numBottles
        remainder = 0
        while numBottles + remainder >= numExchange:
            numBottles, remainder = divmod(numBottles + remainder, numExchange)
            drink += numBottles
        return drink


sol = Solution()
assert sol.numWaterBottles(9, 3) == 13
assert sol.numWaterBottles(15, 4) == 19
assert sol.numWaterBottles(5, 3) == 7
assert sol.numWaterBottles(1, 2) == 1
assert sol.numWaterBottles(2, 2) == 3
assert sol.numWaterBottles(100, 2) == 199
assert sol.numWaterBottles(10, 5) == 12
assert sol.numWaterBottles(7, 3) == 10
assert sol.numWaterBottles(4, 3) == 5
assert sol.numWaterBottles(3, 3) == 4
assert sol.numWaterBottles(99, 100) == 99
assert sol.numWaterBottles(100, 100) == 101
assert sol.numWaterBottles(2, 3) == 2
assert sol.numWaterBottles(3, 2) == 5
assert sol.numWaterBottles(50, 5) == 62
assert sol.numWaterBottles(20, 6) == 23
assert sol.numWaterBottles(8, 4) == 10


"""
1679. Max Number of K-Sum Pairs
Medium
You are given an integer array nums and an integer k.

In one operation, you can pick two numbers from the array whose sum equals k and remove them from the array.

Return the maximum number of operations you can perform on the array.

Example 1:

Input: nums = [1,2,3,4], k = 5
Output: 2
Explanation: Starting with nums = [1,2,3,4]:
- Remove numbers 1 and 4, then nums = [2,3]
- Remove numbers 2 and 3, then nums = []
There are no more pairs that sum up to 5, hence a total of 2 operations.
Example 2:

Input: nums = [3,1,3,4,3], k = 6
Output: 1
Explanation: Starting with nums = [3,1,3,4,3]:
- Remove the first two 3's, then nums = [1,4,3]
There are no more pairs that sum up to 6, hence a total of 1 operation.
 

Constraints:

1 <= nums.length <= 105
1 <= nums[i] <= 109
1 <= k <= 109
"""


from collections import defaultdict


class Solution:
    def maxOperations(self, nums: List[int], k: int) -> int:
        nums.sort()
        left, right = 0, len(nums) - 1
        count = 0
        while left < right:
            total = nums[left] + nums[right]
            if total == k:
                left += 1
                right -= 1
                count += 1
            elif total > k:
                right -= 1
            else:
                left += 1
        return count


sol = Solution()
assert sol.maxOperations(nums=[1, 2, 3, 4], k=5) == 2
assert sol.maxOperations(nums=[3, 1, 3, 4, 3], k=6) == 1
assert sol.maxOperations([1], 1) == 0
assert sol.maxOperations([1, 4], 5) == 1
assert sol.maxOperations([1, 4], 6) == 0
assert sol.maxOperations([2, 2, 2, 2], 4) == 2
assert sol.maxOperations([2, 2, 2], 4) == 1
assert sol.maxOperations([1, 3, 5, 7], 10) == 1
assert sol.maxOperations([1, 2, 3], 100) == 0
assert sol.maxOperations([4, 2, 1], 6) == 1
assert sol.maxOperations([5, 1, 3, 7, 4, 2], 6) == 2
assert sol.maxOperations([3, 3, 3, 3], 6) == 2
assert sol.maxOperations([1, 2, 3, 4, 5, 6], 7) == 3
assert sol.maxOperations([10, 20, 30], 40) == 1
assert sol.maxOperations([1, 1, 1, 1, 1], 2) == 2


"""
https://leetcode.com/problems/find-the-highest-altitude/description

1732. Find the Highest Altitude
Easy
Topics
premium lock icon
Companies
Hint
There is a biker going on a road trip. The road trip consists of n + 1 points at different altitudes. The biker starts his trip on point 0 with altitude equal 0.

You are given an integer array gain of length n where gain[i] is the net gain in altitude between points i​​​​​​ and i + 1 for all (0 <= i < n). Return the highest altitude of a point.

 

Example 1:

Input: gain = [-5,1,5,0,-7]
Output: 1
Explanation: The altitudes are [0,-5,-4,1,1,-6]. The highest is 1.
Example 2:

Input: gain = [-4,-3,-2,-1,4,3,2]
Output: 0
Explanation: The altitudes are [0,-4,-7,-9,-10,-6,-3,-1]. The highest is 0.
 

Constraints:

n == gain.length
1 <= n <= 100
-100 <= gain[i] <= 100
"""


class Solution:
    def largestAltitude(self, gain: List[int]) -> int:
        altitude = 0
        _max = 0
        for g in gain:
            altitude += g
            _max = max(altitude, _max)
        return _max


sol = Solution()
assert sol.largestAltitude([-5, 1, 5, 0, -7]) == 1
assert sol.largestAltitude([-4, -3, -2, -1, 4, 3, 2]) == 0
assert sol.largestAltitude([10]) == 10
assert sol.largestAltitude([0]) == 0
assert sol.largestAltitude([-10]) == 0

"""
https://leetcode.com/problems/greatest-common-divisor-of-strings/description/

1768. Merge Strings Alternately
Easy
You are given two strings word1 and word2. Merge the strings by adding letters in alternating order, starting with word1. If a string is longer than the other, append the additional letters onto the end of the merged string.

Return the merged string.

Example 1:

Input: word1 = "abc", word2 = "pqr"
Output: "apbqcr"
Explanation: The merged string will be merged as so:
word1:  a   b   c
word2:    p   q   r
merged: a p b q c r
Example 2:

Input: word1 = "ab", word2 = "pqrs"
Output: "apbqrs"
Explanation: Notice that as word2 is longer, "rs" is appended to the end.
word1:  a   b 
word2:    p   q   r   s
merged: a p b q   r   s
Example 3:

Input: word1 = "abcd", word2 = "pq"
Output: "apbqcd"
Explanation: Notice that as word1 is longer, "cd" is appended to the end.
word1:  a   b   c   d
word2:    p   q 
merged: a p b q c   d
 

Constraints:

1 <= word1.length, word2.length <= 100
word1 and word2 consist of lowercase English letters.
"""

from itertools import zip_longest


class Solution:
    def mergeAlternately(self, word1: str, word2: str) -> str:
        return "".join((a or "") + (b or "") for a, b in zip_longest(word1, word2))


sol = Solution()

assert sol.mergeAlternately(word1="abc", word2="pqr") == "apbqcr"
assert sol.mergeAlternately(word1="ab", word2="pqrs") == "apbqrs"
assert sol.mergeAlternately(word1="abcd", word2="pq") == "apbqcd"
assert sol.mergeAlternately(word1="a", word2="b") == "ab"
assert sol.mergeAlternately(word1="a", word2="bcdef") == "abcdef"
assert sol.mergeAlternately(word1="abcde", word2="f") == "afbcde"
assert sol.mergeAlternately(word1="aaa", word2="bbb") == "ababab"
assert sol.mergeAlternately(word1="aa", word2="bbbb") == "ababbb"
assert sol.mergeAlternately(word1="aaaa", word2="bb") == "ababaa"
assert sol.mergeAlternately(word1="a" * 100, word2="b" * 100) == ("ab" * 100)
assert sol.mergeAlternately(word1="a" * 100, word2="b") == ("a" + "b" + "a" * 99)
assert sol.mergeAlternately(word1="a", word2="b" * 100) == ("a" + "b" * 100)
assert sol.mergeAlternately(word1="xyz", word2="12345") == "x1y2z345"
