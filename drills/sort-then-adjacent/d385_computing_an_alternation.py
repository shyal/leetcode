"""
EPI 5.8 Computing an alternation

Given a list of integers A, reorder A in place so that
A[0] <= A[1] >= A[2] <= A[3] >= A[4] and so on to the end of A. Any
order with this property is correct.

Example 1:

Input: A = [3, 1, 2]
Output: A = [1, 3, 2]
Explanation: 1 <= 3 >= 2. [2, 3, 1] is also correct.

Example 2:

Input: A = [1, 2, 3, 4, 5]
Output: A = [1, 3, 2, 5, 4]
Explanation: 1 <= 3 >= 2 <= 5 >= 4.

Example 3:

Input: A = [4, 4, 4]
Output: A = [4, 4, 4]
Explanation: Equal neighbours satisfy both <= and >=.

Constraints:

    0 <= len(A) <= 10^5
    -10^9 <= A[i] <= 10^9

    REQUIRED: O(n) time, O(1) extra space. NO sort, NO median, NO
    second list.
"""


class Solution:
    def rearrange(self, A: list[int]) -> None:
        pass


sol = Solution()


def alternates(A):
    return all(A[i] <= A[i + 1] if i % 2 == 0 else A[i] >= A[i + 1] for i in range(len(A) - 1))


A = [3, 1, 2]
sol.rearrange(A)
print(A)  # [1, 3, 2]

# A = [3, 1, 2]
# sol.rearrange(A)
# assert A in ([1, 3, 2], [2, 3, 1])
# A = [1, 2, 3, 4, 5]
# sol.rearrange(A)
# assert sorted(A) == [1, 2, 3, 4, 5] and alternates(A)
# A = [4, 4, 4]
# sol.rearrange(A)
# assert A == [4, 4, 4]
# A = []
# sol.rearrange(A)
# assert A == []
# A = [7]
# sol.rearrange(A)
# assert A == [7]
# A = [2, 1]
# sol.rearrange(A)
# assert A == [1, 2]
# A = [1, 2]
# sol.rearrange(A)
# assert A == [1, 2]
# A = [5, 4, 3, 2, 1]
# sol.rearrange(A)
# assert sorted(A) == [1, 2, 3, 4, 5] and alternates(A)
# A = [1, 1, 2, 2, 3, 3]
# sol.rearrange(A)
# assert sorted(A) == [1, 1, 2, 2, 3, 3] and alternates(A)
# A = [-5, 0, -5, 0, 9, -1]
# sol.rearrange(A)
# assert sorted(A) == [-5, -5, -1, 0, 0, 9] and alternates(A)
# A = [randint(0, 9) for _ in range(1000)]
# B = sorted(A)
# sol.rearrange(A)
# assert sorted(A) == B and alternates(A)
# A = list(range(10 ** 5))
# sol.rearrange(A)
# assert sorted(A) == list(range(10 ** 5)) and alternates(A)
# A = list(range(10 ** 5, 0, -1))
# sol.rearrange(A)
# assert sorted(A) == list(range(1, 10 ** 5 + 1)) and alternates(A)
