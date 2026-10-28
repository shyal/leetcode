# URL: https://leetcode.com/problems/h-index-ii/description/?envType=problem-list-v2&envId=vn57k9wr
#
# 275. H-Index II
#
# Given an array of integers citations where citations[i] is the number of citations a researcher received for their i-th paper and citations is sorted in non-descending order, return the researcher's h-index.
#
# According to the definition of h-index on Wikipedia: The h-index is defined as the maximum value of h such that the given researcher has published at least h papers that have each been cited at least h times.
#
# You must write an algorithm that runs in logarithmic time.
#
# Example 1:
#
# Input: citations = [0,1,3,5,6]
# Output: 3
# Explanation: [0,1,3,5,6] means the researcher has 5 papers in total and each of them had received 0, 1, 3, 5, 6 citations respectively.
# Since the researcher has 3 papers with at least 3 citations each and the remaining two with no more than 3 citations each, their h-index is 3.
#
# Example 2:
#
# Input: citations = [1,2,100]
# Output: 2
#
# Constraints:
#
#     n == citations.length
#     1 <= n <= 10^5
#     0 <= citations[i] <= 1000
#     citations is sorted in ascending order.
#
# ---
# learning.. the papers that count towards the h-index are towards the end of the array, thus counting from the end.
# not doing a binary search, as i trip up on the whole h-index thing in the first place

# mu 0.13

class Solution
  def hIndex(citations: [int]) -> int
    for i, c in enumerate(reversed citations, 1)
      if c < i
        return i - 1
    len citations

sol = Solution()

print(sol.hIndex([0, 1, 3, 5, 6]))  # 3

assert sol.hIndex([0, 1, 3, 5, 6]) == 3
assert sol.hIndex([1, 2, 100]) == 2
assert sol.hIndex([0]) == 0
assert sol.hIndex([1000]) == 1
assert sol.hIndex([0, 0, 0, 0, 0]) == 0
assert sol.hIndex([1000, 1000, 1000, 1000, 1000]) == 5
assert sol.hIndex([0, 0, 1, 1, 1]) == 1
assert sol.hIndex([0, 0, 0, 0, 5]) == 1
assert sol.hIndex([0, 0, 0, 0, 0, 0, 0, 0, 0, 10]) == 1
assert sol.hIndex([1, 1, 1, 1, 1, 1, 1, 1, 1, 1]) == 1
assert sol.hIndex([0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) == 0
assert sol.hIndex([0, 0, 0, 0, 0, 0, 0, 0, 0, 1000]) == 1
assert sol.hIndex([0, 0, 0, 0, 0, 0, 0, 0, 0, 9]) == 1
assert sol.hIndex([0] * 99999 + [1000]) == 1
