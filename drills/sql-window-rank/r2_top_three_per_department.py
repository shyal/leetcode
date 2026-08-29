"""
DRILL: Department Top Three Salaries
TRAINS: sql-window-rank, sql-subquery

Given the table Employee, return departmentId, name and salary for every
employee whose salary is among the three highest distinct salaries in their
department. Any row order.

Table: Employee

    +--------------+---------+
    | Column Name  | Type    |
    +--------------+---------+
    | name         | varchar |
    | salary       | int     |
    | departmentId | int     |
    +--------------+---------+
    Names are unique.

Example 1:

Input:
Employee table:
+-------+--------+--------------+
| name  | salary | departmentId |
+-------+--------+--------------+
| Joe   | 85000  | 1            |
| Henry | 80000  | 2            |
| Sam   | 60000  | 2            |
| Max   | 90000  | 1            |
| Janet | 69000  | 1            |
| Randy | 85000  | 1            |
| Will  | 70000  | 1            |
+-------+--------+--------------+
Output:
+--------------+-------+--------+
| departmentId | name  | salary |
+--------------+-------+--------+
| 1            | Max   | 90000  |
| 1            | Joe   | 85000  |
| 1            | Randy | 85000  |
| 1            | Will  | 70000  |
| 2            | Henry | 80000  |
| 2            | Sam   | 60000  |
+--------------+-------+--------+
Explanation: Department 1's distinct top three are 90000, 85000, 70000; Joe and Randy both earn 85000 and both appear. Department 2 has only two salaries.

Example 2:

Input:
Employee table:
+------+--------+--------------+
| name | salary | departmentId |
+------+--------+--------------+
| Ann  | 10     | 1            |
| Ben  | 20     | 1            |
| Cal  | 30     | 1            |
| Dee  | 40     | 1            |
| Eve  | 40     | 1            |
+------+--------+--------------+
Output:
+--------------+------+--------+
| departmentId | name | salary |
+--------------+------+--------+
| 1            | Dee  | 40     |
| 1            | Eve  | 40     |
| 1            | Cal  | 30     |
| 1            | Ben  | 20     |
+--------------+------+--------+
Explanation: Distinct top three are 40, 30, 20; Dee and Eve tie at 40; Ann is out.

Constraints:

    1 <= number of rows <= 10^4

    REQUIRED: the rank is computed per department by a window function and
    filtered in an outer query or CTE; NO correlated subquery per row. A
    window function cannot be referenced in the WHERE of the query that
    computes it (windows run after WHERE), and a rank that breaks ties would
    drop Randy; both are the failure mode this drill exists to kill.

    Runner: sqlite3 in memory. Write portable SQL: CASE not IF, COALESCE,
    || for concatenation, strftime()/julianday()/date() for dates.
"""

from dsa.sql import SQLDrill


class Solution(SQLDrill):

    def query(self) -> str:
        return """

        """


EXAMPLE_1 = """
CREATE TABLE Employee (name TEXT, salary INTEGER, departmentId INTEGER);
INSERT INTO Employee VALUES ('Joe', 85000, 1);
INSERT INTO Employee VALUES ('Henry', 80000, 2);
INSERT INTO Employee VALUES ('Sam', 60000, 2);
INSERT INTO Employee VALUES ('Max', 90000, 1);
INSERT INTO Employee VALUES ('Janet', 69000, 1);
INSERT INTO Employee VALUES ('Randy', 85000, 1);
INSERT INTO Employee VALUES ('Will', 70000, 1);
"""

EXAMPLE_2 = """
CREATE TABLE Employee (name TEXT, salary INTEGER, departmentId INTEGER);
INSERT INTO Employee VALUES ('Ann', 10, 1);
INSERT INTO Employee VALUES ('Ben', 20, 1);
INSERT INTO Employee VALUES ('Cal', 30, 1);
INSERT INTO Employee VALUES ('Dee', 40, 1);
INSERT INTO Employee VALUES ('Eve', 40, 1);
"""


sol = Solution()

sol.show(EXAMPLE_1)

# assert sol.run(EXAMPLE_1) == [(1, 'Joe', 85000), (1, 'Max', 90000), (1, 'Randy', 85000), (1, 'Will', 70000), (2, 'Henry', 80000), (2, 'Sam', 60000)]
# assert sol.run(EXAMPLE_2) == [(1, 'Ben', 20), (1, 'Cal', 30), (1, 'Dee', 40), (1, 'Eve', 40)]
