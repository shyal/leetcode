"""
URL: https://leetcode.com/problems/container-with-most-water/description/?envType=study-plan-v2&envId=leetcode-75

11. Container With Most Water

You are given an integer array height of length n. There are n vertical lines drawn such that the two endpoints of the ith line are (i, 0) and (i, height[i]).

Find two lines that together with the x-axis form a container, such that the container contains the most water.

Return the maximum amount of water a container can store.

Notice that you may not slant the container.


Example 1:

Input: height = [1,8,6,2,5,4,8,3,7]
Output: 49
Explanation: The above vertical lines are represented by array [1,8,6,2,5,4,8,3,7]. In this case, the max area of water (blue section) the container can contain is 49.

Example 2:

Input: height = [1,1]
Output: 1


Constraints:

        n == height.length
        2 <= n <= 105
        0 <= height[i] <= 104
"""


class Solution:
    def maxArea(self, height: List[int]) -> int:
        L, R = 0, len(height) - 1
        _max = 0
        while L < R:
            h = min(height[L], height[R])
            area = h * (R - L)
            _max = max(_max, area)
            if height[L] < height[R]:
                L += 1
            else:
                R -= 1
        return _max


sol = Solution()

res = sol.maxArea(height=[1, 8, 6, 2, 5, 4, 8, 3, 7])
assert res == 49

res = sol.maxArea(height=[1, 1])
assert res == 1

res = sol.maxArea(height=[1, 8, 6, 2, 5, 4, 8, 3, 7])
assert res == 49

res = sol.maxArea(height=[1, 1])
assert res == 1

res = sol.maxArea(height=[0, 0])
assert res == 0

res = sol.maxArea(height=[0, 1])
assert res == 0

res = sol.maxArea(height=[1, 0])
assert res == 0

res = sol.maxArea(height=[1, 0, 1])
assert res == 2

res = sol.maxArea(height=[4, 3, 2, 1])
assert res == 4

res = sol.maxArea(height=[1, 2, 3, 4])
assert res == 4

res = sol.maxArea(height=[5, 5, 5])
assert res == 10

res = sol.maxArea(height=[1, 100, 1])
assert res == 2

res = sol.maxArea(height=[5, 1, 1, 5])
assert res == 15

res = sol.maxArea(height=[1, 2, 4, 3])
assert res == 4

res = sol.maxArea(height=[2, 3, 10, 5, 7, 8, 9])
assert res == 36

res = sol.maxArea(height=[1, 3, 2, 5, 25, 24, 5])
assert res == 24

res = sol.maxArea(height=[10000, 10000])
assert res == 10000

res = sol.maxArea(height=[4, 0, 3])
assert res == 6
"""
URL: https://leetcode.com/problems/remove-duplicates-from-sorted-array/description/

26. Remove Duplicates from Sorted Array

Given an integer array nums sorted in non-decreasing order, remove the duplicates in-place such that each unique element appears only once. The relative order of the elements should be kept the same. Then return the number of unique elements in nums.

Consider the number of unique elements of nums to be k, to get accepted, you need to do the following things:

        Change the array nums such that the first k elements of nums contain the unique elements in the order they were present in nums initially. The remaining elements of nums are not important as well as the size of nums.
        Return k.

Custom Judge:

The judge will test your solution with the following code:

int[] nums = [...]; // Input array
int[] expectedNums = [...]; // The expected answer with correct length

int k = removeDuplicates(nums); // Calls your implementation

assert k == expectedNums.length;
for (int i = 0; i < k; i++) {
    assert nums[i] == expectedNums[i];
}

If all assertions pass, then your solution will be accepted.


Example 1:

Input: nums = [1,1,2]
Output: 2, nums = [1,2,_]
Explanation: Your function should return k = 2, with the first two elements of nums being 1 and 2 respectively.
It does not matter what you leave beyond the returned k (hence they are underscores).

Example 2:

Input: nums = [0,0,1,1,1,2,2,3,3,4]
Output: 5, nums = [0,1,2,3,4,_,_,_,_,_]
Explanation: Your function should return k = 5, with the first five elements of nums being 0, 1, 2, 3, and 4 respectively.
It does not matter what you leave beyond the returned k (hence they are underscores).


Constraints:

        1 <= nums.length <= 3 * 104
        -100 <= nums[i] <= 100
        nums is sorted in non-decreasing order.

-----------

 w  r
[0, 1, 1, 1, 2, 2, 3, 3, 4]
    x.    x. x     x.    x

"""


class Solution:
    def bf0(self, nums):
        s = set(nums)
        nums[: len(s)] = [*sorted(list(s))]
        return len(s)

    def removeDuplicates(self, nums: List[int]) -> int:
        write = 1
        for i in range(1, len(nums)):
            if nums[i] != nums[i - 1]:
                nums[write] = nums[i]
                write += 1
        return write


sol = Solution()

nums = [1, 1, 2]
k = sol.removeDuplicates(nums)
assert k == 2
assert nums[:k] == [1, 2]

nums = [0, 0, 1, 1, 1, 2, 2, 3, 3, 4]
k = sol.removeDuplicates(nums)
assert k == 5
assert nums[:k] == [0, 1, 2, 3, 4]

nums = [5]
k = sol.removeDuplicates(nums)
assert k == 1
assert nums[:k] == [5]

nums = [1, 2, 3, 4, 5]
k = sol.removeDuplicates(nums)
assert k == 5
assert nums[:k] == [1, 2, 3, 4, 5]

nums = [7, 7, 7, 7]
k = sol.removeDuplicates(nums)
assert k == 1
assert nums[:k] == [7]

nums = [-1, -1]
k = sol.removeDuplicates(nums)
assert k == 1
assert nums[:k] == [-1]

nums = [-100, 100]
k = sol.removeDuplicates(nums)
assert k == 2
assert nums[:k] == [-100, 100]

nums = [-100, -100, -50, 0, 0, 50, 100, 100]
k = sol.removeDuplicates(nums)
assert k == 5
assert nums[:k] == [-100, -50, 0, 50, 100]

nums = [1, 2, 2, 3]
k = sol.removeDuplicates(nums)
assert k == 3
assert nums[:k] == [1, 2, 3]
"""
URL: https://leetcode.com/problems/length-of-last-word/description/

58. Length of Last Word

Given a string s consisting of words and spaces, return the length of the last word in the string.

A word is a maximal substring consisting of non-space characters only.


Example 1:

Input: s = "Hello World"
Output: 5
Explanation: The last word is "World" with length 5.

Example 2:

Input: s = "   fly me   to   the moon  "
Output: 4
Explanation: The last word is "moon" with length 4.

Example 3:

Input: s = "luffy is still joyboy"
Output: 6
Explanation: The last word is "joyboy" with length 6.


Constraints:

        1 <= s.length <= 104
        s consists of only English letters and spaces ' '.
        There will be at least one word in s.
"""


class Solution:
    def lengthOfLastWord(self, s: str) -> int:
        if not s:
            return 0
        first_non_space = None
        first_space_after_non_space = None
        _len = 0
        for i in range(len(s) - 1, -1, -1):
            if first_non_space is None and s[i] != " ":
                first_non_space = i
                _len += 1
            elif first_non_space is not None and s[i] != " ":
                _len += 1
            elif first_non_space is not None and s[i] == " ":
                break
        return _len


sol = Solution()
assert sol.lengthOfLastWord("Hello World") == 5
assert sol.lengthOfLastWord("Hello World ") == 5
assert sol.lengthOfLastWord("Hello World                ") == 5
assert sol.lengthOfLastWord("   fly me   to   the moon  ") == 4
assert sol.lengthOfLastWord("luffy is still joyboy") == 6
assert sol.lengthOfLastWord("") == 0
assert sol.lengthOfLastWord("asdf") == 4
assert sol.lengthOfLastWord("    asdf") == 4
assert sol.lengthOfLastWord("    a") == 1
assert sol.lengthOfLastWord("    ") == 0


"""
URL: https://leetcode.com/problems/symmetric-tree/description/

101. Symmetric Tree

Given the root of a binary tree, check whether it is a mirror of itself (i.e., symmetric around its center).


Example 1:

Input: root = [1,2,2,3,4,4,3]
Output: true

Example 2:

Input: root = [1,2,2, None,3, None,3]
Output: false


Constraints:

        The number of nodes in the tree is in the range [1, 1000].
        -100 <= Node.val <= 100


Follow up: Could you solve it both recursively and iteratively?

---

      [1]
   ┌───┴───┐
  [2]     [2]
 ┌─┴─┐   ┌─┴─┐
[3] [4] [4] [3]

  [1]
 ┌─┴─┐
[2] [2]
 ┐   ┐
[3] [3]

"""


class Solution:
    def isSymmetric(self, root: Optional[TreeNode]) -> bool:
        def dfs(node, depth=0, _dir=0):
            if not node:
                yield None
                return
            yield node.val
            choice = (node.left, node.right)
            yield from dfs(choice[_dir], depth + 1, _dir)
            if depth > 0:
                yield from dfs(choice[not _dir], depth + 1, _dir)

        return all(a == b for a, b in zip(dfs(root, _dir=0), dfs(root, _dir=1)))


sol = Solution()

tree = build_tree([1, 2, 2, 3, 4, 4, 3])
assert sol.isSymmetric(tree) == True
tree = build_tree([1, 2, 2, None, 3, None, 3])
assert sol.isSymmetric(tree) == False
tree = build_tree([1])
assert sol.isSymmetric(tree) == True
tree = build_tree([1, 2])
assert sol.isSymmetric(tree) == False
tree = build_tree([1, None, 2])
assert sol.isSymmetric(tree) == False
tree = build_tree([1, 2, 2])
assert sol.isSymmetric(tree) == True
tree = build_tree([1, 2, 3])
assert sol.isSymmetric(tree) == False
tree = build_tree([1, -1, -1])
assert sol.isSymmetric(tree) == True
tree = build_tree([1, -1, 1])
assert sol.isSymmetric(tree) == False
tree = build_tree([1, 2, 2, 3, None, None, 3])
assert sol.isSymmetric(tree) == True
tree = build_tree([1, 2, 2, None, 3, 3, None])
assert sol.isSymmetric(tree) == True
tree = build_tree([1, 2, 2, 3, None, 3, None])
assert sol.isSymmetric(tree) == False
tree = build_tree([1, 2, 2, 3, 4, 4, 5])
assert sol.isSymmetric(tree) == False
tree = build_tree([1, 2, 2, 3, 4, 4, 3, 5, 6, 7, 8, 8, 7, 6, 5])
assert sol.isSymmetric(tree) == True
tree = build_tree([1, 2, 2, 3, 4, 4, 3, 5, 6, 7, 8, 8, 7, 6, 4])
assert sol.isSymmetric(tree) == False
tree = build_tree([1, 2, 3, 4, None, None, None, None, 5])
assert sol.isSymmetric(tree) == False
"""
URL: https://leetcode.com/problems/maximum-depth-of-binary-tree/description/?envType=study-plan-v2&envId=leetcode-75

104. Maximum Depth of Binary Tree

Given the root of a binary tree, return its maximum depth.

A binary tree's maximum depth is the number of nodes along the longest path from the root node down to the farthest leaf node.


Example 1:

Input: root = [3,9,20,null,null,15,7]
Output: 3

Example 2:

Input: root = [1,null,2]
Output: 2


Constraints:

        The number of nodes in the tree is in the range [0, 104].
        -100 <= Node.val <= 100
"""

from typing import List, Optional
from tree_utils import build_tree


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:

        def helper(node):
            return 1 + max(
                helper(node.left) if node.left else 0,
                helper(node.right) if node.right else 0,
            )

        return helper(root) if root else 0


sol = Solution()

tree1 = build_tree([3, 9, 20, None, None, 15, 7])
assert sol.maxDepth(tree1) == 3

tree2 = build_tree([1, None, 2])
assert sol.maxDepth(tree2) == 2

tree3 = build_tree([])
assert sol.maxDepth(tree3) == 0

tree4 = build_tree([5])
assert sol.maxDepth(tree4) == 1

tree5 = build_tree([1, 2])
assert sol.maxDepth(tree5) == 2

tree6 = build_tree([1, 2, None, 3, None, None, 4])
assert sol.maxDepth(tree6) == 4

tree7 = build_tree([1, None, 2, None, 3, None, 4])
assert sol.maxDepth(tree7) == 4

tree8 = build_tree([1, 2, 3, 4, 5])
assert sol.maxDepth(tree8) == 3

tree9 = build_tree([1, 2, 3, 4, None, None, None, 5])
assert sol.maxDepth(tree9) == 4

tree10 = build_tree([1, None, 2, None, 3])
assert sol.maxDepth(tree10) == 3


"""
URL: https://leetcode.com/problems/convert-sorted-array-to-binary-search-tree/description/

108. Convert Sorted Array to Binary Search Tree

Given an integer array nums where the elements are sorted in ascending order, convert it to a height-balanced binary search tree.


Example 1:

Input: nums = [-10,-3,0,5,9]
Output: [0,-3,9,-10,null,5]
Explanation: [0,-10,5,null,-3,null,9] is also accepted:

Example 2:

Input: nums = [1,3]
Output: [3,1]
Explanation: [1,null,3] and [3,1] are both height-balanced BSTs.


Constraints:

        1 <= nums.length <= 104
        -104 <= nums[i] <= 104
        nums is sorted in a strictly increasing order.

------

  [2]
 ┌─┴─┐
[1] [4]
 /   /
[0] [3]


[1]
 /
[0]


     [3]
   ┌──┴──┐
  [1]   [5]
 ┌─┴─┐   /
[0] [2] [4]


                                 [20]
               ┌──────────────────┴───────────────────┐
              [10]                                   [30]
       ┌───────┴────────┐                   ┌─────────┴─────────┐
      [5]              [15]                [25]                [35]
   ┌───┴───┐       ┌────┴────┐         ┌────┴────┐         ┌────┴────┐
  [2]     [8]     [13]      [18]      [23]      [28]      [33]      [38]
 ┌─┴─┐   ┌─┴─┐   ┌─┴──┐    ┌─┴──┐    ┌─┴──┐    ┌─┴──┐    ┌─┴──┐    ┌─┴──┐
[1] [4] [7] [9] [12] [14] [17] [19] [22] [24] [27] [29] [32] [34] [37] [39]
 /   /   /       /         /         /         /         /         /
[0] [3] [6]     [11]      [16]      [21]      [26]      [31]      [36]


"""


class Solution:
    def sortedArrayToBST(self, nums: List[int]) -> Optional[TreeNode]:
        def helper(start, end):
            if start < end:
                mid = (start + end) // 2
                return TreeNode(nums[mid], helper(start, mid), helper(mid + 1, end))

        return helper(0, len(nums))


sol = Solution()

assert get_inorder(sol.sortedArrayToBST([-10, -3, 0, 5, 9])) == [-10, -3, 0, 5, 9]
assert is_balanced(sol.sortedArrayToBST([-10, -3, 0, 5, 9]))
assert is_valid_bst(sol.sortedArrayToBST([-10, -3, 0, 5, 9]))
assert get_inorder(sol.sortedArrayToBST([1, 3])) == [1, 3]
assert is_balanced(sol.sortedArrayToBST([1, 3]))
assert is_valid_bst(sol.sortedArrayToBST([1, 3]))
assert get_inorder(sol.sortedArrayToBST([1])) == [1]
assert is_balanced(sol.sortedArrayToBST([1]))
assert is_valid_bst(sol.sortedArrayToBST([1]))
assert get_inorder(sol.sortedArrayToBST([0, 1, 2, 3, 4, 5, 6])) == [0, 1, 2, 3, 4, 5, 6]
assert is_balanced(sol.sortedArrayToBST([0, 1, 2, 3, 4, 5, 6]))
assert is_valid_bst(sol.sortedArrayToBST([0, 1, 2, 3, 4, 5, 6]))
assert get_inorder(sol.sortedArrayToBST([-3, -2, -1])) == [-3, -2, -1]
assert is_balanced(sol.sortedArrayToBST([-3, -2, -1]))
assert is_valid_bst(sol.sortedArrayToBST([-3, -2, -1]))
assert get_inorder(sol.sortedArrayToBST([])) == []
assert is_balanced(sol.sortedArrayToBST([]))
assert is_valid_bst(sol.sortedArrayToBST([]))
assert get_inorder(sol.sortedArrayToBST([1, 2, 3])) == [1, 2, 3]
assert is_balanced(sol.sortedArrayToBST([1, 2, 3]))
assert is_valid_bst(sol.sortedArrayToBST([1, 2, 3]))
assert get_inorder(sol.sortedArrayToBST([-10000, 0, 10000])) == [-10000, 0, 10000]
assert is_balanced(sol.sortedArrayToBST([-10000, 0, 10000]))
assert is_valid_bst(sol.sortedArrayToBST([-10000, 0, 10000]))
assert get_inorder(sol.sortedArrayToBST([0, 1, 2, 3])) == [0, 1, 2, 3]
assert is_balanced(sol.sortedArrayToBST([0, 1, 2, 3]))
assert is_valid_bst(sol.sortedArrayToBST([0, 1, 2, 3]))
"""
URL: https://leetcode.com/problems/minimum-depth-of-binary-tree/description/

111. Minimum Depth of Binary Tree

Given a binary tree, find its minimum depth.

The minimum depth is the number of nodes along the shortest path from the root node down to the nearest leaf node.

Note: A leaf is a node with no children.


Example 1:

Input: root = [3,9,20,null,null,15,7]
Output: 2

Example 2:

Input: root = [2,null,3,null,4,null,5,null,6]
Output: 5


Constraints:

        The number of nodes in the tree is in the range [0, 105].
        -1000 <= Node.val <= 1000
"""


class Solution:
    def minDepth(self, root: Optional[TreeNode]) -> int:
        def dfs(node, depth):
            if not node:
                return float("inf")

            is_leaf = node.left is None and node.right is None

            if is_leaf:
                return depth

            return min(dfs(node.left, depth + 1), dfs(node.right, depth + 1))

        return dfs(root, 1) if root else 0


sol = Solution()
tree = build_tree([3, 9, 20, None, None, 15, 7])
res = sol.minDepth(tree)
assert res == 2

sol = Solution()
tree = build_tree([])
res = sol.minDepth(tree)
assert res == 0

sol = Solution()
tree = build_tree([1])
res = sol.minDepth(tree)
assert res == 1


"""
URL: https://leetcode.com/problems/single-number/description/?envType=study-plan-v2&envId=leetcode-75

136. Single Number

Given a non-empty array of integers nums, every element appears twice except for one. Find that single one.

You must implement a solution with a linear runtime complexity and use only constant extra space.


Example 1:

Input: nums = [2,2,1]

Output: 1

Example 2:

Input: nums = [4,1,2,1,2]

Output: 4

Example 3:

Input: nums = [1]

Output: 1


Constraints:

        1 <= nums.length <= 3 * 104
        -3 * 104 <= nums[i] <= 3 * 104
        Each element in the array appears twice except for one element which appears only once.
"""

from typing import List
from functools import reduce
from operator import xor


class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        return reduce(xor, nums)


sol = Solution()
assert sol.singleNumber([2, 2, 1]) == 1
assert sol.singleNumber([4, 1, 2, 1, 2]) == 4
assert sol.singleNumber([1]) == 1


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
URL: https://leetcode.com/problems/binary-tree-right-side-view/description/?envType=study-plan-v2&envId=leetcode-75

199. Binary Tree Right Side View

Given the root of a binary tree, imagine yourself standing on the right side of it, return the values of the nodes you can see ordered from top to bottom.


Example 1:

Input: root = [1,2,3,None,5,None,4]

Output: [1,3,4]

Explanation:

Example 2:

Input: root = [1,2,3,4,None,None,None,5]

Output: [1,3,4,5]

Explanation:

Example 3:

Input: root = [1,None,3]

Output: [1,3]

Example 4:

Input: root = []

Output: []


Constraints:

        The number of nodes in the tree is in the range [0, 100].
        -100 <= Node.val <= 100
"""

from tree_utils import build_tree, draw_tree
from typing import Optional, List


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:
        def dfs(node, depth=0):
            if not node:
                return
            if depth > data["max_depth"]:
                right_side.append(node.val)
                data["max_depth"] = depth
            dfs(node.right, depth + 1)
            dfs(node.left, depth + 1)

        data = {"max_depth": -1}
        right_side = []
        dfs(root, 0)
        return right_side


sol = Solution()

tree = build_tree([1, 2, 3, None, 5, None, 4])
res = sol.rightSideView(tree)
assert res == [1, 3, 4]

tree = build_tree([1, 2, 3, 4, None, None, None, 5])
res = sol.rightSideView(tree)
assert res == [1, 3, 4, 5]

tree = build_tree([1, 2, 3, 4, 7, 6, 8, 5])
res = sol.rightSideView(tree)
assert res == [1, 3, 8, 5]

tree = build_tree([])
res = sol.rightSideView(tree)
assert res == []

tree = build_tree([1])
res = sol.rightSideView(tree)
assert res == [1]

tree = build_tree([1, None, 3])
res = sol.rightSideView(tree)
assert res == [1, 3]

tree = build_tree([1, 2, None])
res = sol.rightSideView(tree)
assert res == [1, 2]

tree = build_tree([1, 2, 3])
res = sol.rightSideView(tree)
assert res == [1, 3]

tree = build_tree([1, 2, 3, 4, 5, 6, 7])
res = sol.rightSideView(tree)
assert res == [1, 3, 7]

tree = build_tree([1, 2, None, 3, None, 4, None])
res = sol.rightSideView(tree)
assert res == [1, 2, 3, 4]

tree = build_tree([1, None, 2, None, 3])
res = sol.rightSideView(tree)
assert res == [1, 2, 3]

tree = build_tree([1, -2, 3, None, 4, None, 5])
res = sol.rightSideView(tree)
assert res == [1, 3, 5]

tree = build_tree([10, 20, 30, 40, 50, None, None, None, None, 60])
res = sol.rightSideView(tree)
assert res == [10, 30, 50, 60]

tree = build_tree([5, 4, None, 3, None, 2, None])
res = sol.rightSideView(tree)
assert res == [5, 4, 3, 2]

tree = build_tree([100, 99, 98, 97, 96])
res = sol.rightSideView(tree)
assert res == [100, 98, 96]

tree = build_tree([1, 3, 2])
res = sol.rightSideView(tree)
assert res == [1, 2]

tree = build_tree([1, 2, 3, 4, 5])
res = sol.rightSideView(tree)
assert res == [1, 3, 5]

tree = build_tree([0, -100, 100, -50, 50])
res = sol.rightSideView(tree)
assert res == [0, 100, 50]


"""
URL: https://leetcode.com/problems/contains-duplicate/description/

217. Contains Duplicate

Given an integer array nums, return true if any value appears at least twice in the array, and return false if every element is distinct.


Example 1:

Input: nums = [1,2,3,1]

Output: true

Explanation:

The element 1 occurs at the indices 0 and 3.

Example 2:

Input: nums = [1,2,3,4]

Output: false

Explanation:

All elements are distinct.

Example 3:

Input: nums = [1,1,1,3,3,4,3,2,4,2]

Output: true


Constraints:

        1 <= nums.length <= 105
        -109 <= nums[i] <= 109
"""


class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        return len(nums) != len(set(nums))


sol = Solution()
assert sol.containsDuplicate([1, 2, 3, 1]) == True
assert sol.containsDuplicate([1]) == False
assert sol.containsDuplicate([1, 2]) == False
assert sol.containsDuplicate([1, 1]) == True


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
URL: https://leetcode.com/problems/guess-number-higher-or-lower/description/?envType=study-plan-v2&envId=leetcode-75

374. Guess Number Higher or Lower

We are playing the Guess Game. The game is as follows:

I pick a number from 1 to n. You have to guess which number I picked (the number I picked stays the same throughout the game).

Every time you guess wrong, I will tell you whether the number I picked is higher or lower than your guess.

You call a pre-defined API int guess(int num), which returns three possible results:

        -1: Your guess is higher than the number I picked (i.e. num > pick).
        1: Your guess is lower than the number I picked (i.e. num < pick).
        0: your guess is equal to the number I picked (i.e. num == pick).

Return the number that I picked.


Example 1:

Input: n = 10, pick = 6
Output: 6

Example 2:

Input: n = 1, pick = 1
Output: 1

Example 3:

Input: n = 2, pick = 1
Output: 1


Constraints:

        1 <= n <= 231 - 1
        1 <= pick <= n
"""


def guess(num):
    global pick
    if num > pick:
        return -1
    elif num < pick:
        return 1
    else:
        return 0


class Solution:
    def guessNumber(self, n: int) -> int:
        left, right = 0, n
        while left <= right:
            mid = (left + right) // 2
            res = guess(mid)
            if res == -1:
                right = mid - 1
            elif res == 1:
                left = mid + 1
            else:
                return mid


# Test cases
pick = 6
n = 10
sol = Solution()
assert sol.guessNumber(n) == 6

pick = 1
n = 1
assert sol.guessNumber(n) == 1

pick = 1
n = 2
assert sol.guessNumber(n) == 1

pick = 2
n = 2
assert sol.guessNumber(n) == 2

pick = 1
n = 1000000000
assert sol.guessNumber(n) == 1

pick = 1000000000
n = 1000000000
assert sol.guessNumber(n) == 1000000000


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
URL: https://leetcode.com/problems/rotate-string/description/

796. Rotate String

Given two strings s and goal, return true if and only if s can become goal after some number of shifts on s.

A shift on s consists of moving the leftmost character of s to the rightmost position.

        For example, if s = "abcde", then it will be "bcdea" after one shift.


Example 1:
Input: s = "abcde", goal = "cdeab"
Output: true
Example 2:
Input: s = "abcde", goal = "abced"
Output: false


Constraints:

        1 <= s.length, goal.length <= 100
        s and goal consist of lowercase English letters.
"""

from itertools import islice, chain


class Solution:
    def rotateString(self, s: str, goal: str) -> bool:
        if s == goal:
            return True

        if len(s) != len(goal):
            return False

        def rotate(s, r):
            return chain(islice(s, r, None), islice(s, None, r))

        for shift in range(len(s)):
            r = rotate(s, shift)
            if all(a == b for a, b in zip(r, goal)):
                return True

        return False


sol = Solution()
assert sol.rotateString(s="abcde", goal="cdeab") == True
assert sol.rotateString(s="abcd", goal="cdeab") == False
assert sol.rotateString(s="123", goal="124") == False
assert sol.rotateString(s="", goal="") == True
assert sol.rotateString(s="hello", goal="lohel") == True
"""
URL: https://leetcode.com/problems/most-common-word/description/

819. Most Common Word

Given a string paragraph and a string array of the banned words banned, return the most frequent word that is not banned. It is guaranteed there is at least one word that is not banned, and that the answer is unique.

The words in paragraph are case-insensitive and the answer should be returned in lowercase.

Note that words can not contain punctuation symbols.


Example 1:

Input: paragraph = "Bob hit a ball, the hit BALL flew far after it was hit.", banned = ["hit"]
Output: "ball"
Explanation:
"hit" occurs 3 times, but it is a banned word.
"ball" occurs twice (and no other word does), so it is the most frequent non-banned word in the paragraph.
Note that words in the paragraph are not case sensitive,
that punctuation is ignored (even if adjacent to words, such as "ball,"),
and that "hit" isn't the answer even though it occurs more because it is banned.

Example 2:

Input: paragraph = "a.", banned = []
Output: "a"


Constraints:

        1 <= paragraph.length <= 1000
        paragraph consists of English letters, space ' ', or one of the symbols: "!?',;.".
        0 <= banned.length <= 100
        1 <= banned[i].length <= 10
        banned[i] consists of only lowercase English letters.
"""

from collections import Counter

rem = set("!?',;.")


class Solution:
    def mostCommonWord(self, paragraph: str, banned: List[str]) -> str:
        banned = set(banned)
        tmp = []
        for c in paragraph:
            if c in rem:
                tmp.append(" ")
            else:
                tmp.append(c.lower())
        count = dict(Counter("".join(tmp).split()))
        res = next(
            iter(max(count.items(), key=lambda x: x[1] if x[0] not in banned else 0)),
            "",
        )
        return res if res not in banned else ""


sol = Solution()

res = sol.mostCommonWord(paragraph="a, a, a, a, b,b,b,c, c", banned=["a"])
assert res == "b"

res = sol.mostCommonWord(
    paragraph="Bob hit a ball, the hit BALL flew far after it was hit.", banned=["hit"]
)
assert res == "ball"

res = sol.mostCommonWord(paragraph="a.", banned=[])
assert res == "a"

res = sol.mostCommonWord(paragraph="foo", banned=["foo"])
assert res == ""

res = sol.mostCommonWord(paragraph="foo foo foo", banned=["foo"])
assert res == ""

res = sol.mostCommonWord(paragraph="f f f f b b b c c", banned=["f"])
assert res == "b"

"""
URL: https://leetcode.com/problems/positions-of-large-groups/description/

830. Positions of Large Groups

In a string s of lowercase letters, these letters form consecutive groups of the same character.

For example, a string like s = "abbxxxxzyy" has the groups "a", "bb", "xxxx", "z", and "yy".

A group is identified by an interval [start, end], where start and end denote the start and end indices (inclusive) of the group. In the above example, "xxxx" has the interval [3,6].

A group is considered large if it has 3 or more characters.

Return the intervals of every large group sorted in increasing order by start index.


Example 1:

Input: s = "abbxxxxzzy"
Output: [[3,6]]
Explanation: "xxxx" is the only large group with start index 3 and end index 6.

Example 2:

Input: s = "abc"
Output: []
Explanation: We have groups "a", "b", and "c", none of which are large groups.

Example 3:

Input: s = "abcdddeeeeaabbbcd"
Output: [[3,5],[6,9],[12,14]]
Explanation: The large groups are "ddd", "eeee", and "bbb".


Constraints:

        1 <= s.length <= 1000
        s contains lowercase English letters only.
"""

from itertools import groupby
from collections import namedtuple


class Solution:
    def largeGroupPositions(self, s: str) -> List[List[int]]:
        G = groupby(s)
        Interval = namedtuple("Interval", ["chars", "interval"])
        intervals = []
        i = 0
        for letter, it in G:
            val = "".join(it)
            if len(val) >= 3:
                interval = Interval(val, [i, i + len(val) - 1])
                intervals.append(interval)
            i += len(val)
        intervals.sort(key=lambda x: x.interval[0])
        return [interval.interval for interval in intervals]


sol = Solution()

res = sol.largeGroupPositions(s="abbxxxxzzy")
assert res == [[3, 6]]

res = sol.largeGroupPositions(s="abc")
assert res == []

res = sol.largeGroupPositions(s="abcdddeeeeaabbbcd")
assert res == [[3, 5], [6, 9], [12, 14]]

res = sol.largeGroupPositions(s="")
assert res == []

res = sol.largeGroupPositions(s="abcabcabcabcabcabcabcabcabcabcabcabcabcaaa")
assert res == [[39, 41]]
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
URL: https://leetcode.com/problems/n-th-tribonacci-number/description/?envType=study-plan-v2&envId=leetcode-75

1137. N-th Tribonacci Number

The Tribonacci sequence Tn is defined as follows:

T0 = 0, T1 = 1, T2 = 1, and Tn+3 = Tn + Tn+1 + Tn+2 for n >= 0.

Given n, return the value of Tn.


Example 1:

Input: n = 4
Output: 4
Explanation:
T_3 = 0 + 1 + 1 = 2
T_4 = 1 + 1 + 2 = 4

Example 2:

Input: n = 25
Output: 1389537


Constraints:

        0 <= n <= 37
        The answer is guaranteed to fit within a 32-bit integer, ie. answer <= 2^31 - 1.
"""

from functools import cache


class Solution:
    @cache
    def tribonacci(self, n: int) -> int:
        if n <= 1:
            return n
        elif n == 2:
            return 1
        return self.tribonacci(n - 3) + self.tribonacci(n - 2) + self.tribonacci(n - 1)


sol = Solution()

result = sol.tribonacci(0)
assert result == 0

result = sol.tribonacci(1)
assert result == 1

result = sol.tribonacci(2)
assert result == 1

result = sol.tribonacci(3)
assert result == 2

result = sol.tribonacci(4)
assert result == 4

result = sol.tribonacci(5)
assert result == 7

result = sol.tribonacci(6)
assert result == 13

result = sol.tribonacci(7)
assert result == 24

result = sol.tribonacci(8)
assert result == 44

result = sol.tribonacci(9)
assert result == 81

result = sol.tribonacci(10)
assert result == 149

result = sol.tribonacci(11)
assert result == 274

result = sol.tribonacci(12)
assert result == 504

result = sol.tribonacci(13)
assert result == 927

result = sol.tribonacci(14)
assert result == 1705

result = sol.tribonacci(15)
assert result == 3136

result = sol.tribonacci(16)
assert result == 5768

result = sol.tribonacci(17)
assert result == 10609

result = sol.tribonacci(18)
assert result == 19513

result = sol.tribonacci(19)
assert result == 35890

result = sol.tribonacci(20)
assert result == 66012

result = sol.tribonacci(21)
assert result == 121415

result = sol.tribonacci(22)
assert result == 223317

result = sol.tribonacci(23)
assert result == 410744

result = sol.tribonacci(24)
assert result == 755476

result = sol.tribonacci(25)
assert result == 1389537

result = sol.tribonacci(26)
assert result == 2555757

result = sol.tribonacci(27)
assert result == 4700770

result = sol.tribonacci(28)
assert result == 8646064

result = sol.tribonacci(29)
assert result == 15902591

result = sol.tribonacci(30)
assert result == 29249425

result = sol.tribonacci(31)
assert result == 53798080

result = sol.tribonacci(32)
assert result == 98950096

result = sol.tribonacci(33)
assert result == 181997601

result = sol.tribonacci(34)
assert result == 334745777

result = sol.tribonacci(35)
assert result == 615693474

result = sol.tribonacci(36)
assert result == 1132436852

result = sol.tribonacci(37)
assert result == 2082876103


"""
https://leetcode.com/problems/unique-number-of-occurrences/description

1207. Unique Number of Occurrences
Easy
Given an array of integers arr, return true if the number of occurrences of each value in the array is unique or false otherwise.

Example 1:

Input: arr = [1,2,2,1,1,3]
Output: true
Explanation: The value 1 has 3 occurrences, 2 has 2 and 3 has 1. No two values have the same number of occurrences.
Example 2:

Input: arr = [1,2]
Output: false
Example 3:

Input: arr = [-3,0,1,-3,1,1,1,-3,10,0]
Output: true
 

Constraints:

1 <= arr.length <= 1000
-1000 <= arr[i] <= 1000
"""

from collections import Counter


class Solution:
    def uniqueOccurrences(self, arr: List[int]) -> bool:
        occurrences = [count for val, count in Counter(arr).items()]
        return len(occurrences) == len(set(occurrences))


sol = Solution()
sol.uniqueOccurrences([1, 2, 2, 1, 1, 3]) == True
sol.uniqueOccurrences([1, 2]) == False
sol.uniqueOccurrences([-3, 0, 1, -3, 1, 1, 1, -3, 10, 0]) == True
sol.uniqueOccurrences([1]) == True
sol.uniqueOccurrences([1, 1]) == True


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


"""
https://leetcode.com/problems/find-the-difference-of-two-arrays/description

2215. Find the Difference of Two Arrays
Easy
Given two 0-indexed integer arrays nums1 and nums2, return a list answer of size 2 where:

answer[0] is a list of all distinct integers in nums1 which are not present in nums2.
answer[1] is a list of all distinct integers in nums2 which are not present in nums1.
Note that the integers in the lists may be returned in any order.

Example 1:

Input: nums1 = [1,2,3], nums2 = [2,4,6]
Output: [[1,3],[4,6]]
Explanation:
For nums1, nums1[1] = 2 is present at index 0 of nums2, whereas nums1[0] = 1 and nums1[2] = 3 are not present in nums2. Therefore, answer[0] = [1,3].
For nums2, nums2[0] = 2 is present at index 1 of nums1, whereas nums2[1] = 4 and nums2[2] = 6 are not present in nums1. Therefore, answer[1] = [4,6].
Example 2:

Input: nums1 = [1,2,3,3], nums2 = [1,1,2,2]
Output: [[3],[]]
Explanation:
For nums1, nums1[2] and nums1[3] are not present in nums2. Since nums1[2] == nums1[3], their value is only included once and answer[0] = [3].
Every integer in nums2 is present in nums1. Therefore, answer[1] = [].
 

Constraints:

1 <= nums1.length, nums2.length <= 1000
-1000 <= nums1[i], nums2[i] <= 1000
"""


class Solution:
    def findDifference(self, nums1: List[int], nums2: List[int]) -> List[List[int]]:
        nums1 = set(nums1)
        nums2 = set(nums2)
        return [list(nums1 - nums2), list(nums2 - nums1)]


sol = Solution()
sol.findDifference(nums1=[1, 2, 3], nums2=[2, 4, 6]) == [[1, 3], [4, 6]]
sol.findDifference(nums1=[1, 2, 3, 3], nums2=[1, 1, 2, 2]) == [[3], []]
sol.findDifference(nums1=[], nums2=[]) == [[], []]
sol.findDifference(nums1=[1], nums2=[]) == [[1], []]


"""
2390. Removing Stars From a String
Medium
Topics
premium lock icon
Companies
Hint
You are given a string s, which contains stars *.

In one operation, you can:

Choose a star in s.
Remove the closest non-star character to its left, as well as remove the star itself.
Return the string after all stars have been removed.

Note:

The input will be generated such that the operation is always possible.
It can be shown that the resulting string will always be unique.
 

Example 1:

Input: s = "leet**cod*e"
Output: "lecoe"
Explanation: Performing the removals from left to right:
- The closest character to the 1st star is 't' in "leet**cod*e". s becomes "lee*cod*e".
- The closest character to the 2nd star is 'e' in "lee*cod*e". s becomes "lecod*e".
- The closest character to the 3rd star is 'd' in "lecod*e". s becomes "lecoe".
There are no more stars, so we return "lecoe".
Example 2:

Input: s = "erase*****"
Output: ""
Explanation: The entire string is removed, so we return an empty string.
 

Constraints:

1 <= s.length <= 105
s consists of lowercase English letters and stars *.
The operation above can be performed on s.
"""


class Solution:
    def removeStars(self, s: str) -> str:
        stack = []
        for c in s:
            if c != "*":
                stack.append(c)
            else:
                if stack:
                    stack.pop()
        return "".join(stack)


sol = Solution()
assert sol.removeStars(s="leet**cod*e") == "lecoe"
assert sol.removeStars(s="erase*****") == ""
assert sol.removeStars("a") == "a"
assert sol.removeStars("a*") == ""
assert sol.removeStars("ab*") == "a"
assert sol.removeStars("a*b*") == ""
assert sol.removeStars("abc") == "abc"
assert sol.removeStars("abc***") == ""
assert sol.removeStars("abcd***") == "a"
assert sol.removeStars("aa*bb*cc*") == "abc"
assert sol.removeStars("ab*cdef**") == "acd"


