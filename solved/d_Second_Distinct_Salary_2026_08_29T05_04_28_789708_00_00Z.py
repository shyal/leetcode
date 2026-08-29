"""
DRILL: Second Distinct Salary
TRAINS: sql-nth-value

Given the table Employee, return the second highest distinct salary as a
single row with one column, SecondHighestSalary. The table always holds at
least two distinct salaries.

Table: Employee

    +-------------+------+
    | Column Name | Type |
    +-------------+------+
    | salary      | int  |
    +-------------+------+
    Salaries can repeat.

Example 1:

Input:
Employee table:
+--------+
| salary |
+--------+
| 100    |
| 200    |
| 300    |
+--------+
Output:
+---------------------+
| SecondHighestSalary |
+---------------------+
| 200                 |
+---------------------+

Example 2:

Input:
Employee table:
+--------+
| salary |
+--------+
| 300    |
| 300    |
| 100    |
+--------+
Output:
+---------------------+
| SecondHighestSalary |
+---------------------+
| 100                 |
+---------------------+
Explanation: 300 appears twice but is one distinct salary; the second distinct salary is 100.

Constraints:

    2 <= number of rows <= 10^4

    REQUIRED: one query that skips past the highest distinct salary;
    repeated salaries count once.

    FORBIDDEN: a self-join; MAX of the salaries below the MAX.

    Runner: sqlite3 in memory. Write portable SQL: CASE not IF, COALESCE,
    || for concatenation, strftime()/julianday()/date() for dates.

---

New to limit and offset. Assisted.

"""

from dsa.sql import SQLDrill


class Solution(SQLDrill):

    def query(self) -> str:
        return """
            select distinct salary as salary
            from Employee
            order by salary DESC
            limit 1
            offset 1;
        """


EXAMPLE_1 = """
CREATE TABLE Employee (salary INTEGER);
INSERT INTO Employee VALUES (100);
INSERT INTO Employee VALUES (200);
INSERT INTO Employee VALUES (300);
"""

EXAMPLE_2 = """
CREATE TABLE Employee (salary INTEGER);
INSERT INTO Employee VALUES (300);
INSERT INTO Employee VALUES (300);
INSERT INTO Employee VALUES (100);
"""


sol = Solution()

sol.show(EXAMPLE_1)
sol.show(EXAMPLE_2)

assert sol.run(EXAMPLE_1) == [(200,)]
assert sol.run(EXAMPLE_2) == [(100,)]
