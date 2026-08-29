"""
DRILL: Manager Name
TRAINS: sql-self-join

Given the table `Employees`, return `name` and `manager_name` for every
employee who has a manager: `manager_name` is the `name` of the employee
that `reports_to` points at. Employees with no manager do not appear. No
ordering required.

Table: Employees

    +-------------+----------+
    | Column Name | Type     |
    +-------------+----------+
    | employee_id | int      |
    | name        | varchar  |
    | reports_to  | int      |
    +-------------+----------+
    employee_id is the primary key. reports_to is the manager's employee_id, or NULL.

Example 1:

Input:
Employees table:
+-------------+---------+------------+
| employee_id | name    | reports_to |
+-------------+---------+------------+
| 9           | Hercy   | null       |
| 6           | Alice   | 9          |
| 4           | Bob     | 9          |
| 2           | Winston | null       |
+-------------+---------+------------+
Output:
+-------+--------------+
| name  | manager_name |
+-------+--------------+
| Alice | Hercy        |
| Bob   | Hercy        |
+-------+--------------+
Explanation: Alice and Bob report to Hercy. Hercy and Winston have no manager.

Example 2:

Input:
Employees table:
+-------------+------+------------+
| employee_id | name | reports_to |
+-------------+------+------------+
| 1           | Ann  | null       |
| 2           | Bob  | 1          |
| 3           | Cal  | 2          |
+-------------+------+------------+
Output:
+------+--------------+
| name | manager_name |
+------+--------------+
| Bob  | Ann          |
| Cal  | Bob          |
+------+--------------+
Explanation: A chain: Bob reports to Ann, Cal reports to Bob.

Constraints:

    1 <= number of rows <= 10^4

    REQUIRED: one query over Employees; employees with no manager do not
    appear.

    FORBIDDEN: a subquery; a correlated lookup per row; a name lookup in
    Python.

    Runner: sqlite3 in memory. Write portable SQL: CASE not IF, COALESCE,
    || for concatenation, strftime()/julianday()/date() for dates.
"""

from dsa.sql import SQLDrill


class Solution(SQLDrill):

    def query(self) -> str:
        return """

        """


EXAMPLE_1 = """
CREATE TABLE Employees (employee_id INTEGER, name TEXT, reports_to INTEGER);
INSERT INTO Employees VALUES (9, 'Hercy', NULL);
INSERT INTO Employees VALUES (6, 'Alice', 9);
INSERT INTO Employees VALUES (4, 'Bob', 9);
INSERT INTO Employees VALUES (2, 'Winston', NULL);
"""

EXAMPLE_2 = """
CREATE TABLE Employees (employee_id INTEGER, name TEXT, reports_to INTEGER);
INSERT INTO Employees VALUES (1, 'Ann', NULL);
INSERT INTO Employees VALUES (2, 'Bob', 1);
INSERT INTO Employees VALUES (3, 'Cal', 2);
"""


sol = Solution()

sol.show(EXAMPLE_1)

# assert sorted(sol.run(EXAMPLE_1)) == [('Alice', 'Hercy'), ('Bob', 'Hercy')]
# assert sorted(sol.run(EXAMPLE_2)) == [('Bob', 'Ann'), ('Cal', 'Bob')]
