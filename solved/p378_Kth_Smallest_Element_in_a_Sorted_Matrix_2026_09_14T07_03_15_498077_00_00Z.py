"""
URL: https://leetcode.com/problems/kth-smallest-element-in-a-sorted-matrix/description/?envType=problem-list-v2&envId=vn57k9wr

378. Kth Smallest Element in a Sorted Matrix

Given an n x n matrix where each of the rows and columns is sorted in ascending order, return the kth smallest element in the matrix.

Note that it is the kth smallest element in the sorted order, not the kth distinct element.

You must find a solution with a memory complexity better than O(n^2).

Example 1:

Input: matrix = [[1,5,9],[10,11,13],[12,13,15]], k = 8
Output: 13
Explanation: The elements in the matrix are [1,5,9,10,11,12,13,13,15], and the 8th smallest number is 13

Example 2:

Input: matrix = [[-5]], k = 1
Output: -5

Constraints:

    n == matrix.length == matrix[i].length
    1 <= n <= 300
    -10^9 <= matrix[i][j] <= 10^9
    All the rows and columns of matrix are guaranteed to be sorted in non-decreasing order.
    1 <= k <= n^2

Follow up:

    Could you solve the problem with a constant memory (i.e., O(1) memory complexity)?
    Could you solve the problem in O(n) time complexity? The solution may be too advanced for an interview but you may find reading this paper fun.

---


Not sure what took me so long. but i got there.

LEETCODE: Accepted (88 ms, 24.6 MB)
"""


class Solution:

    def kthSmallestBF1(self, matrix: List[List[int]], k: int) -> int:
        """
        most brute force solution out there, but it doesn't follow
        the constraint:  You must find a solution with a memory
        complexity better than O(n^2).
        """
        m = matrix
        res = []
        for i, j in cells(m):
            res.append(m[i][j])
        res.sort()
        return res[k - 1]

    def kthSmallestBF2(self, matrix: List[List[int]], k: int) -> int:
        m = matrix
        res = []
        for i, j in cells(m):
            maxheappush(res, m[i][j])
            if len(res) > k:
                maxheappop(res)
        return maxheappeek(res)

    def kthSmallest(self, matrix: List[List[int]], k: int) -> int:
        print(matrix)
        return self.kthSmallestBF2(matrix, k)


sol = Solution()

Solution().kthSmallest([[1, 2], [1, 3]], 3)

print(sol.kthSmallest([[1, 5, 9], [10, 11, 13], [12, 13, 15]], 8))  # 13

assert sol.kthSmallest([[1, 5, 9], [10, 11, 13], [12, 13, 15]], 8) == 13
assert sol.kthSmallest([[-5]], 1) == -5

assert Solution().kthSmallest([[1]], 1) == 1
assert Solution().kthSmallest([[1, 2], [1, 3]], 2) == 1
assert Solution().kthSmallest([[1, 2], [1, 3]], 3) == 2
assert Solution().kthSmallest([[1, 1, 1], [1, 1, 1], [1, 1, 1]], 5) == 1
assert (
    Solution().kthSmallest([[-(10**9), -(10**9) + 1], [-(10**9) + 2, -(10**9) + 3]], 3)
    == -999999998
)
assert (
    Solution().kthSmallest([[10**9 - 3, 10**9 - 2], [10**9 - 1, 10**9]], 4)
    == 1000000000
)
assert (
    Solution().kthSmallest([[1, 2, 3, 4], [2, 3, 4, 5], [3, 4, 5, 6], [4, 5, 6, 7]], 10)
    == 4
)
assert (
    Solution().kthSmallest([[1, 2, 2, 2], [2, 2, 2, 3], [2, 2, 3, 4], [2, 3, 4, 5]], 7)
    == 2
)
assert Solution().kthSmallest([[1, 3, 5], [6, 7, 12], [11, 14, 14]], 6) == 11
assert Solution().kthSmallest([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 9) == 9
assert Solution().kthSmallest([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 1) == 1
assert Solution().kthSmallest([[1, 1, 2], [1, 2, 3], [2, 3, 4]], 4) == 2
