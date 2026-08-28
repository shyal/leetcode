"""
DRILL: Employees Who Manage Nobody
TRAINS: sql-anti-join

Given the table Employees, return the employee_id of every employee who is not
the manager of anyone. Order by employee_id.

Table: Employees

    +-------------+---------+
    | Column Name | Type    |
    +-------------+---------+
    | employee_id | int     |
    | name        | varchar |
    | manager_id  | int     |
    +-------------+---------+
    employee_id is the primary key. manager_id is NULL for employees with no manager.

Example 1:

Input:
Employees table:
+-------------+------+------------+
| employee_id | name | manager_id |
+-------------+------+------------+
| 1           | Ann  | null       |
| 2           | Bob  | 1          |
| 3           | Cal  | 1          |
| 4           | Dee  | 3          |
| 5           | Eve  | null       |
+-------------+------+------------+
Output:
+-------------+
| employee_id |
+-------------+
| 2           |
| 4           |
| 5           |
+-------------+
Explanation: Managers are 1 and 3. Everyone else manages nobody.

Example 2:

Input:
Employees table:
+-------------+------+------------+
| employee_id | name | manager_id |
+-------------+------+------------+
| 1           | Ann  | null       |
| 2           | Bob  | null       |
+-------------+------+------------+
Output:
+-------------+
| employee_id |
+-------------+
| 1           |
| 2           |
+-------------+
Explanation: Nobody has a manager, so nobody is a manager.

Constraints:

    1 <= number of rows <= 10^4

    REQUIRED: the query must return the right rows when manager_id contains
    NULL. `employee_id NOT IN (SELECT manager_id FROM Employees)` returns
    nothing once a single NULL is in that list, because x NOT IN (..., NULL)
    is never true; that is the failure mode this drill exists to kill. Use NOT
    EXISTS, or a LEFT JOIN with IS NULL, or exclude the NULLs from the
    subquery.

    Runner: sqlite3 in memory. Write portable SQL: CASE not IF, COALESCE,
    || for concatenation, strftime()/julianday()/date() for dates.
"""

import sqlite3

EXAMPLE_1 = """
CREATE TABLE Employees (employee_id INTEGER, name TEXT, manager_id INTEGER);
INSERT INTO Employees VALUES (1, 'Ann', NULL);
INSERT INTO Employees VALUES (2, 'Bob', 1);
INSERT INTO Employees VALUES (3, 'Cal', 1);
INSERT INTO Employees VALUES (4, 'Dee', 3);
INSERT INTO Employees VALUES (5, 'Eve', NULL);
"""

EXAMPLE_2 = """
CREATE TABLE Employees (employee_id INTEGER, name TEXT, manager_id INTEGER);
INSERT INTO Employees VALUES (1, 'Ann', NULL);
INSERT INTO Employees VALUES (2, 'Bob', NULL);
"""


class Solution:

    def query(self) -> str:
        return """

        """


def run(schema: str, sql: str) -> list[tuple]:
    con = sqlite3.connect(":memory:")
    con.executescript(schema)
    return [tuple(row) for row in con.execute(sql).fetchall()]


sol = Solution()

print(run(EXAMPLE_1, sol.query()))  # [(2,), (4,), (5,)]

# assert run(EXAMPLE_1, sol.query()) == [(2,), (4,), (5,)]
# assert run(EXAMPLE_2, sol.query()) == [(1,), (2,)]
