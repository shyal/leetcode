"""
URL: https://leetcode.com/problems/combinations/description/?envType=problem-list-v2&envId=vn57k9wr

77. Combinations

Given two integers n and k, return all possible combinations of k numbers chosen from the range [1, n].

You may return the answer in any order.

Example 1:

Input: n = 4, k = 2
Output: [[1,2],[1,3],[1,4],[2,3],[2,4],[3,4]]
Explanation: There are 4 choose 2 = 6 total combinations.
Note that combinations are unordered, i.e., [1,2] and [2,1] are considered to be the same combination.

Example 2:

Input: n = 1, k = 1
Output: [[1]]
Explanation: There is 1 choose 1 = 1 total combination.

Constraints:

    1 <= n <= 20
    1 <= k <= n

---

Failed. Can't remember.

"""


class Solution:
    def combine(self, n: int, k: int) -> List[List[int]]:
        def helper(i):
            if i == k:
                res.append(curr[::])
                return

            for j in range(i, len(nums)):
                curr.append(nums[i])
                nums[i], nums[j] = nums[j], nums[i]
                helper(i + 1)
                nums[i], nums[j] = nums[j], nums[i]
                curr.pop()

        nums = [*range(1, n + 1)]
        res = []
        curr = []
        helper(0)
        return res


sol = Solution()

print(sol.combine(4, 2))  # [[1,2],[1,3],[1,4],[2,3],[2,4],[3,4]]

# assert sol.combine(4, 2) == [[1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]]
# assert sol.combine(1, 1) == [[1]]

# assert sol.combine(20, 1) == [
#     [1],
#     [2],
#     [3],
#     [4],
#     [5],
#     [6],
#     [7],
#     [8],
#     [9],
#     [10],
#     [11],
#     [12],
#     [13],
#     [14],
#     [15],
#     [16],
#     [17],
#     [18],
#     [19],
#     [20],
# ]
# assert sol.combine(20, 20) == [
#     [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
# ]
# assert sol.combine(5, 0) == [[]]
# assert sol.combine(2, 2) == [[1, 2]]
# assert sol.combine(3, 1) == [[1], [2], [3]]
# assert sol.combine(15, 15) == [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]]
# assert sol.combine(1, 1) == [[1]]
# assert sol.combine(6, 3) == [
#     [1, 2, 3],
#     [1, 2, 4],
#     [1, 2, 5],
#     [1, 2, 6],
#     [1, 3, 4],
#     [1, 3, 5],
#     [1, 3, 6],
#     [1, 4, 5],
#     [1, 4, 6],
#     [1, 5, 6],
#     [2, 3, 4],
#     [2, 3, 5],
#     [2, 3, 6],
#     [2, 4, 5],
#     [2, 4, 6],
#     [2, 5, 6],
#     [3, 4, 5],
#     [3, 4, 6],
#     [3, 5, 6],
#     [4, 5, 6],
# ]
# assert sol.combine(7, 7) == [[1, 2, 3, 4, 5, 6, 7]]
# assert sol.combine(8, 2) == [
#     [1, 2],
#     [1, 3],
#     [1, 4],
#     [1, 5],
#     [1, 6],
#     [1, 7],
#     [1, 8],
#     [2, 3],
#     [2, 4],
#     [2, 5],
#     [2, 6],
#     [2, 7],
#     [2, 8],
#     [3, 4],
#     [3, 5],
#     [3, 6],
#     [3, 7],
#     [3, 8],
#     [4, 5],
#     [4, 6],
#     [4, 7],
#     [4, 8],
#     [5, 6],
#     [5, 7],
#     [5, 8],
#     [6, 7],
#     [6, 8],
#     [7, 8],
# ]


# FAILED: walked away after 10m 41s; no working solution.
# Judge the moves actually attempted as struggled, not clean.
