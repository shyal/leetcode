# URL: https://leetcode.com/problems/max-chunks-to-make-sorted/description/?envType=problem-list-v2&envId=vn57k9wr
#
# 769. Max Chunks To Make Sorted
#
# You are given an integer array arr of length n that represents a permutation of the integers in the range [0, n - 1].
#
# We split arr into some number of chunks (i.e., partitions), and individually sort each chunk. After concatenating them, the result should equal the sorted array.
#
# Return the largest number of chunks we can make to sort the array.
#
# Example 1:
#
# Input: arr = [4,3,2,1,0]
# Output: 1
# Explanation:
# Splitting into two or more chunks will not return the required result.
# For example, splitting into [4, 3], [2, 1, 0] will result in [3, 4, 0, 1, 2], which isn't sorted.
#
# Example 2:
#
# Input: arr = [1,0,2,3,4]
# Output: 4
# Explanation:
# We can split into two chunks, such as [1, 0], [2, 3, 4].
# However, splitting into [1, 0], [2], [3], [4] is the highest number of chunks possible.
#
# Constraints:
#
#     n == arr.length
#     1 <= n <= 10
#     0 <= arr[i] < n
#     All the elements of arr are unique.
#
# ---
# 
# [1, 0, 3, 2, 5, 4, 7, 6, 9, 8]
#        p     p     p     p
# 

# mu 0.13

class Solution
  def maxChunksToSorted(arr: [int]) -> int
    ret count, high = 0
    for >i, x in arr
      high = max(high, x)
      count += high == i

sol = Solution()

print(sol.maxChunksToSorted([1, 0, 2, 3, 4]))


# print(sol.maxChunksToSorted([4, 3, 2, 1, 0]))  # 1

# assert sol.maxChunksToSorted([4, 3, 2, 1, 0]) == 1
# assert sol.maxChunksToSorted([1, 0, 2, 3, 4]) == 4
# assert sol.maxChunksToSorted([0]) == 1
# assert sol.maxChunksToSorted([0, 1]) == 2
# assert sol.maxChunksToSorted([1, 0]) == 1
# assert sol.maxChunksToSorted([0, 2, 1]) == 2
# assert sol.maxChunksToSorted([2, 0, 1]) == 1
# assert sol.maxChunksToSorted([3, 2, 1, 0]) == 1
# assert sol.maxChunksToSorted([0, 1, 2, 3]) == 4
# assert sol.maxChunksToSorted([1, 0, 3, 2]) == 2
# assert sol.maxChunksToSorted([9, 8, 7, 6, 5, 4, 3, 2, 1, 0]) == 1
# assert sol.maxChunksToSorted([0, 9, 8, 7, 6, 5, 4, 3, 2, 1]) == 2
# assert sol.maxChunksToSorted([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]) == 10
# assert sol.maxChunksToSorted([1, 0, 3, 2, 5, 4, 7, 6, 9, 8]) == 5


# FAILED: walked away after 25m 25s; no working solution.
# Judge the move the defect is in as struggled, not clean. A move the code never reached gets no verdict.
