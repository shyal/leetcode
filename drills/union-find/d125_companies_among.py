"""
DRILL: Companies Among

Given employees, a list of employee numbers, return how many different
companies they belong to. Solution extends UnionFind from
dsa/union_find.py: self.parent[i] is the manager of employee i, an
employee who is their own manager is a head, and self.find(x) returns the
head of x. Two employees belong to the same company when they have the
same head. Management chains never contain cycles.

Example 1:

Input: parent = [1, 2, 2, 4, 5, 5], employees = [0, 3, 1]
Output: 2
Explanation: the heads are 2, 5 and 2.

Example 2:

Input: parent = [1, 2, 5, 4, 5, 5], employees = [0, 3]
Output: 1
Explanation: both heads are 5.

Constraints:

    1 <= n <= 1000
    0 <= len(employees) <= n
    0 <= employees[i] < n
    parent is free of cycles

    REQUIRED: must call self.find once per employee. NO comparison of
    employees in pairs; NO scan of self.parent.
"""

from dsa.union_find import UnionFind


class Solution(UnionFind):
    def countCompaniesAmong(self, employees: List[int]) -> int:
        pass


sol = Solution(6)
sol.parent = [1, 2, 2, 4, 5, 5]

print(sol.countCompaniesAmong([0, 3, 1]))  # 2

## two heads among three employees
# sol = Solution(6)
# sol.parent = [1, 2, 2, 4, 5, 5]
# assert sol.countCompaniesAmong([0, 3, 1]) == 2

## every employee, still two heads
# assert sol.countCompaniesAmong([0, 1, 2, 3, 4, 5]) == 2

## one head, after union(0, 3)
# sol = Solution(6)
# sol.parent = [1, 2, 5, 4, 5, 5]
# assert sol.countCompaniesAmong([0, 3]) == 1

## no employees
# assert sol.countCompaniesAmong([]) == 0

## one employee
# assert sol.countCompaniesAmong([4]) == 1

## the same employee twice
# assert sol.countCompaniesAmong([2, 2]) == 1

## heads at the first, a middle and the last index
# sol = Solution(7)
# sol.parent = [0, 0, 1, 3, 3, 6, 6]
# assert sol.countCompaniesAmong([2, 4, 5]) == 3
# assert sol.countCompaniesAmong([1, 2]) == 1

## nobody merged, every employee is a company
# sol = Solution(1000)
# assert sol.countCompaniesAmong(list(range(1000))) == 1000
