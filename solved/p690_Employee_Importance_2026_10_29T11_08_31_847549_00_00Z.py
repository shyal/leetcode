"""
URL: https://leetcode.com/problems/employee-importance/description/?envType=problem-list-v2&envId=vn57k9wr

690. Employee Importance

You have a data structure of employee information, including the employee's unique ID, importance value, and direct subordinates' IDs.

You are given an array of employees employees where:

- employees[i].id is the ID of the iᵗʰ employee.
- employees[i].importance is the importance value of the iᵗʰ employee.
- employees[i].subordinates is a list of the IDs of the direct subordinates of the iᵗʰ employee.

Given an integer id that represents an employee's ID, return the total importance value of this employee and all their direct and indirect subordinates.

Example 1:

Input: employees = [[1,5,[2,3]],[2,3,[]],[3,3,[]]], id = 1
Output: 11
Explanation: Employee 1 has an importance value of 5 and has two direct subordinates: employee 2 and employee 3.
They both have an importance value of 3.
Thus, the total importance value of employee 1 is 5 + 3 + 3 = 11.

Example 2:

Input: employees = [[1,2,[5]],[5,-3,[]]], id = 5
Output: -3
Explanation: Employee 5 has an importance value of -3 and has no direct subordinates.
Thus, the total importance value of employee 5 is -3.

Constraints:

    1 <= employees.length <= 2000
    1 <= employees[i].id <= 2000
    All employees[i].id are unique.
    -100 <= employees[i].importance <= 100
    One employee has at most one direct leader and may have several subordinates.
    The IDs in employees[i].subordinates are valid IDs.

---

LEETCODE: Accepted (143 ms, 21 MB)
"""


# Definition for Employee.
class Employee:
    def __init__(self, id: int, importance: int, subordinates: List[int]):
        pass


# mu 0.14
# from dataclasses import dataclass
#
# @dataclass
# class Employee
#   id: int
#   importance: int
#   subordinates: list
#
# class Solution
#   def getImportance(employees: [Employee], id: int) -> int
#     by_id = {}
#     for emp in employees
#       by_id[emp.id] = emp
#     {
#       id ->
#         return by_id[id].importance + sum([mu(emp) for emp in by_id[id].subordinates])
#     }(id)

from dataclasses import dataclass


class Rec(dict):
    """A dict that also gives its keys as attributes: d.k is d["k"]."""

    def __getattr__(self, k):
        try:
            return self[k]
        except KeyError:
            raise AttributeError(k) from None

    def __setattr__(self, k, v):
        self[k] = v

    def __delattr__(self, k):
        try:
            del self[k]
        except KeyError:
            raise AttributeError(k) from None


@dataclass
class Employee:
    id: int
    importance: int
    subordinates: list


class Solution:
    def getImportance(self, employees: list[Employee], id: int) -> int:
        by_id = Rec()
        for emp in employees:
            by_id[emp.id] = emp
        def _mu1(id):
            return by_id[id].importance + sum([_mu1(emp) for emp in by_id[id].subordinates])
        return _mu1(id)


sol = Solution()
print(sol.getImportance([Employee(1, 5, [2, 3]), Employee(2, 3, []), Employee(3, 3, [])], 1))
_l, _r = sol.getImportance([Employee(1, 5, [2, 3]), Employee(2, 3, []), Employee(3, 3, [])], 1), 11
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.getImportance([Employee(1, 2, [5]), Employee(5, -3, [])], 5), -3
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.getImportance([Employee(1, 0, [])], 1), 0
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.getImportance([Employee(1, 100, [])], 1), 100
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.getImportance([Employee(1, -100, [])], 1), -100
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.getImportance([Employee(i, 1, []) for i in range(1, 2001)], 1000), 1
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.getImportance([Employee(1, 10, list(range(2, 2001)))] + [Employee(i, 1, []) for i in range(2, 2001)], 1), 2009
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.getImportance([Employee(1, 5, [2]), Employee(2, 5, [3]), Employee(3, 5, [4]), Employee(4, 5, [])], 1), 20
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.getImportance([Employee(1, 5, [2, 3]), Employee(2, 5, [4]), Employee(3, 5, [4]), Employee(4, 5, [])], 1), 25
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.getImportance([Employee(1, 5, [2]), Employee(2, 5, [3]), Employee(3, -10, [])], 1), 0
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.getImportance([Employee(1, 5, [2, 3]), Employee(2, 5, [4]), Employee(3, -10, []), Employee(4, 10, [])], 1), 10
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.getImportance([Employee(1, 5, [2]), Employee(2, 5, [3]), Employee(3, 5, [4]), Employee(4, 5, [5]), Employee(5, 5, [])], 1), 25
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
_l, _r = sol.getImportance([Employee(1, 0, [2]), Employee(2, 0, [3]), Employee(3, 0, [4]), Employee(4, 0, [5]), Employee(5, 0, [])], 1), 0
assert _l == _r, (lambda l, r: f"left : {l.lstrip()}\nright: {r.lstrip()}" if "\n" not in l + r else f"left :\n{l}\nright:\n{r}")(*(__import__("textwrap").indent(__import__("pprint").pformat(v, width=__import__("shutil").get_terminal_size().columns - 2, sort_dicts=False), "  ") for v in (_l, _r)))
