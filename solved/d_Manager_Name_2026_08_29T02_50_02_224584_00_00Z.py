"""
DRILL: Manager Name
TRAINS: sql-self-join

Given the table Employees, return employee_id, name and manager_name for every
employee who has a manager: manager_name is the name of the employee that
reports_to points at. Employees with no manager do not appear. Order by
employee_id.

Table: Employees

    +-------------+----------+
    | Column Name | Type     |
    +-------------+----------+
    | employee_id | int      |
    | name        | varchar  |
    | reports_to  | int      |
    | age         | int      |
    +-------------+----------+
    employee_id is the primary key. reports_to is the manager's employee_id, or NULL.

Example 1:

Input:
Employees table:
+-------------+---------+------------+-----+
| employee_id | name    | reports_to | age |
+-------------+---------+------------+-----+
| 9           | Hercy   | null       | 43  |
| 6           | Alice   | 9          | 41  |
| 4           | Bob     | 9          | 36  |
| 2           | Winston | null       | 37  |
+-------------+---------+------------+-----+
Output:
+-------------+-------+--------------+
| employee_id | name  | manager_name |
+-------------+-------+--------------+
| 4           | Bob   | Hercy        |
| 6           | Alice | Hercy        |
+-------------+-------+--------------+
Explanation: Alice and Bob report to Hercy. Hercy and Winston have no manager.

Example 2:

Input:
Employees table:
+-------------+------+------------+-----+
| employee_id | name | reports_to | age |
+-------------+------+------------+-----+
| 1           | Ann  | null       | 50  |
| 2           | Bob  | 1          | 40  |
| 3           | Cal  | 2          | 30  |
+-------------+------+------------+-----+
Output:
+-------------+------+--------------+
| employee_id | name | manager_name |
+-------------+------+--------------+
| 2           | Bob  | Ann          |
| 3           | Cal  | Bob          |
+-------------+------+--------------+
Explanation: A chain: Bob reports to Ann, Cal reports to Bob.

Constraints:

    1 <= number of rows <= 10^4

    REQUIRED: one query over Employees, NO subquery. Employees with no
    manager must NOT appear. A correlated subquery per row, or a name lookup
    in Python, is the failure mode this drill exists to kill.

    Runner: sqlite3 in memory. Write portable SQL: CASE not IF, COALESCE,
    || for concatenation, strftime()/julianday()/date() for dates.
"""

from dsa.sql import SQLDrill


class Solution(SQLDrill):

    def query(self) -> str:
        return """
        select e.employee_id, e.name, m.name
        from Employees as e
        join Employees as m on e.reports_to = m.employee_id
        order by e.employee_id;
        """


EXAMPLE_1 = """
CREATE TABLE Employees (employee_id INTEGER, name TEXT, reports_to INTEGER, age INTEGER);
INSERT INTO Employees VALUES (9, 'Hercy', NULL, 43);
INSERT INTO Employees VALUES (6, 'Alice', 9, 41);
INSERT INTO Employees VALUES (4, 'Bob', 9, 36);
INSERT INTO Employees VALUES (2, 'Winston', NULL, 37);
"""

EXAMPLE_2 = """
CREATE TABLE Employees (employee_id INTEGER, name TEXT, reports_to INTEGER, age INTEGER);
INSERT INTO Employees VALUES (1, 'Ann', NULL, 50);
INSERT INTO Employees VALUES (2, 'Bob', 1, 40);
INSERT INTO Employees VALUES (3, 'Cal', 2, 30);
"""


sol = Solution()

sol.show(EXAMPLE_1)

assert sol.run(EXAMPLE_1) == [(4, "Bob", "Hercy"), (6, "Alice", "Hercy")]
assert sol.run(EXAMPLE_2) == [(2, "Bob", "Ann"), (3, "Cal", "Bob")]
