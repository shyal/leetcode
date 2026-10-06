"""
DRILL: Hire
TRAINS: py-dataclass

Write a dataclass Employee with the fields name, dept and salary, and
a method `hire` that, given those three values, returns an Employee.
Two employees with the same three values are equal, and printing one
shows its fields.

Example 1:

Input: name = "john", dept = "computer lab", salary = 1000
Output: Employee(name='john', dept='computer lab', salary=1000)

Example 2:

Input: name = "ann", dept = "ops", salary = 0
Output: Employee(name='ann', dept='ops', salary=0)

Constraints:

    0 <= salary <= 10^7

    REQUIRED: @dataclass on Employee with three annotated fields and no
    methods written by hand; equality and repr come from the decorator.
    NO __init__, NO __eq__, NO __repr__, NO tuple, NO dict.
"""

from dataclasses import dataclass


class Employee:
    pass


class Solution:

    def hire(self, name: str, dept: str, salary: int) -> Employee:
        pass


sol = Solution()

print(sol.hire("john", "computer lab", 1000))  # Employee(name='john', dept='computer lab', salary=1000)

# assert sol.hire("john", "computer lab", 1000) == Employee("john", "computer lab", 1000)
# assert sol.hire("ann", "ops", 0) == Employee("ann", "ops", 0)
# assert sol.hire("john", "computer lab", 1000) != Employee("john", "computer lab", 1001)
# assert sol.hire("john", "computer lab", 1000).dept == "computer lab"
# assert repr(sol.hire("ann", "ops", 0)) == "Employee(name='ann', dept='ops', salary=0)"
