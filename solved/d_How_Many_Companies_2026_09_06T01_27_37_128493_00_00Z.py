"""
DRILL: How Many Companies
TRAINS: union-find

Given n employees numbered 0 to n - 1 and pairs, where pairs[i] = [a, b]
means a and b work at the same company, return how many companies there
are. Solution extends UnionFind from dsa/union_find.py, built over the n
employees with each one in a company of their own. The call
self.union(a, b) merges the companies of a and b and returns True, or
returns False when they were already one company.

Example 1:

Input: n = 4, pairs = [[0, 1], [0, 2], [1, 2]]
Output: 2
Explanation: 0, 1 and 2 are one company. 3 is another. The third pair
merges nothing.

Example 2:

Input: n = 5, pairs = []
Output: 5

Constraints:

    1 <= n <= 1000
    0 <= len(pairs) <= 2000
    pairs[i] = [a, b] with 0 <= a, b < n

    REQUIRED: must use only what union returns. NO scan of self.parent at
    the end. NO find or union of your own.

---

Learning

"""

from dsa.union_find import UnionFind


class Solution(UnionFind):
    def countCompanies(self, pairs: List[List[int]]) -> int:
        count = len(self.parent)
        for a, b in pairs:
            if self.union(a, b):
                count -= 1
        return count


sol = Solution(4)

print(sol.countCompanies([[0, 1], [0, 2], [1, 2]]))  # 2

# assert Solution(4).countCompanies([[0, 1], [0, 2], [1, 2]]) == 2
# assert Solution(3).countCompanies([[0, 1], [1, 2]]) == 1
# assert Solution(5).countCompanies([]) == 5
# assert Solution(6).countCompanies([[0, 1], [2, 3], [4, 5], [0, 2], [3, 5]]) == 1
# assert Solution(4).countCompanies([[0, 1], [1, 0], [2, 3], [0, 3]]) == 1
# assert Solution(1).countCompanies([]) == 1
# assert Solution(2).countCompanies([[0, 1], [0, 1]]) == 1
# assert Solution(4).countCompanies([[0, 1], [2, 3]]) == 2
# assert Solution(3).countCompanies([[0, 0]]) == 3
