from typing import List, Optional
from rich import print

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
