"""
URL: https://leetcode.com/problems/kth-smallest-element-in-a-sorted-matrix/description/?envType=problem-list-v2&envId=heap-priority-queue

378. Kth Smallest Element in a Sorted Matrix

Given an n x n matrix where each of the rows and columns is sorted in ascending order, return the kth smallest element in the matrix.

Note that it is the kth smallest element in the sorted order, not the kth distinct element.

You must find a solution with a memory complexity better than O(n2).


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
        -109 <= matrix[i][j] <= 109
        All the rows and columns of matrix are guaranteed to be sorted in non-decreasing order.
        1 <= k <= n2


Follow up:

        Could you solve the problem with a constant memory (i.e., O(1) memory complexity)?
        Could you solve the problem in O(n) time complexity? The solution may be too advanced for an interview but you may find reading this paper fun.

---

I came up with a solution involving sort, so didn't follow the explicit memory constraints.

Had to look up a solution. k-way merge. Great solution. Will have to revisit.

"""


class Solution:
    def kthSmallest(self, matrix: List[List[int]], k: int) -> int:
        # k-way merge not my solution
        heap = []
        for i, row in enumerate(matrix):
            heappush(heap, (row[0], i, 0))

        for i in range(k - 1):
            val, row, col = heappop(heap)
            if col + 1 < len(matrix):
                heappush(heap, (matrix[row][col + 1], row, col + 1))

        return heap[0][0]


sol = Solution()

res = sol.kthSmallest(matrix=[[1, 5, 9], [10, 11, 13], [12, 13, 15]], k=8)
# print(res)

# assert sol.kthSmallest(matrix=[[1, 5, 9], [10, 11, 13], [12, 13, 15]], k=8) == 13
# assert sol.kthSmallest(matrix=[[-5]], k=1) == -5
# assert sol.kthSmallest(matrix=[[1, 5, 9], [10, 11, 13], [12, 13, 15]], k=1) == 1
# assert sol.kthSmallest(matrix=[[1, 5, 9], [10, 11, 13], [12, 13, 15]], k=9) == 15
# assert sol.kthSmallest(matrix=[[1, 3], [2, 4]], k=3) == 3
# assert sol.kthSmallest(matrix=[[1, 2, 3], [2, 3, 4], [3, 4, 5]], k=5) == 3
# assert sol.kthSmallest(matrix=[[0, 0], [0, 0]], k=2) == 0
# assert sol.kthSmallest(matrix=[[-10, -5, 0], [1, 5, 10], [2, 6, 11]], k=5) == 2
# assert sol.kthSmallest(matrix=[[1]], k=1) == 1
# assert sol.kthSmallest(matrix=[[1, 2], [3, 4]], k=4) == 4
