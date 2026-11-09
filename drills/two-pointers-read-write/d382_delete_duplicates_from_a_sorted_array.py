"""
EPI 5.5 Delete duplicates from a sorted array

Given a sorted list of integers A, remove the repeated values in place
and return k, the number of distinct values. After the call, A[:k] must
hold the distinct values in increasing order. The elements from index k
onward can hold any values, and len(A) does not change.

Example 1:

Input: A = [2, 3, 5, 5, 7, 11, 11, 11, 13]
Output: 6, A[:6] = [2, 3, 5, 7, 11, 13]

Example 2:

Input: A = [1, 1, 1]
Output: 1, A[:1] = [1]

Example 3:

Input: A = []
Output: 0

Constraints:

    0 <= len(A) <= 10^5
    -10^9 <= A[i] <= 10^9
    A is sorted in non-decreasing order.

    REQUIRED: O(n) time, O(1) extra space. NO set(), NO second list,
    NO del, NO pop().
"""


class Solution:
    def delete_duplicates(self, A: list[int]) -> int:
        pass


sol = Solution()

A = [2, 3, 5, 5, 7, 11, 11, 11, 13]
print(sol.delete_duplicates(A), A[:6])  # 6 [2, 3, 5, 7, 11, 13]

# A = [2, 3, 5, 5, 7, 11, 11, 11, 13]
# k = sol.delete_duplicates(A)
# assert k == 6 and A[:k] == [2, 3, 5, 7, 11, 13] and len(A) == 9
# A = [1, 1, 1]
# k = sol.delete_duplicates(A)
# assert k == 1 and A[:k] == [1] and len(A) == 3
# A = []
# assert sol.delete_duplicates(A) == 0
# A = [4]
# k = sol.delete_duplicates(A)
# assert k == 1 and A == [4]
# A = [1, 2]
# k = sol.delete_duplicates(A)
# assert k == 2 and A == [1, 2]
# A = [1, 2, 3, 4]
# k = sol.delete_duplicates(A)
# assert k == 4 and A == [1, 2, 3, 4]
# A = [-3, -3, 0, 0, 0, 8]
# k = sol.delete_duplicates(A)
# assert k == 3 and A[:k] == [-3, 0, 8]
# A = [1, 1, 2]
# k = sol.delete_duplicates(A)
# assert k == 2 and A[:k] == [1, 2]
# A = [1, 2, 2]
# k = sol.delete_duplicates(A)
# assert k == 2 and A[:k] == [1, 2]
# A = [0, 0, 1, 1, 1, 2, 2, 3, 3, 4]
# k = sol.delete_duplicates(A)
# assert k == 5 and A[:k] == [0, 1, 2, 3, 4] and len(A) == 10
# A = [7] * 10 ** 5
# k = sol.delete_duplicates(A)
# assert k == 1 and A[:k] == [7] and len(A) == 10 ** 5
# A = [i // 2 for i in range(10 ** 5)]
# k = sol.delete_duplicates(A)
# assert k == 50000 and A[:k] == list(range(50000))
# A = list(range(10 ** 5))
# k = sol.delete_duplicates(A)
# assert k == 10 ** 5 and A == list(range(10 ** 5))
