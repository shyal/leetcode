"""
DRILL: Reports Per Manager
TRAINS: sql-self-join, sql-group-aggregate

Given the table `Employees`, return `employee_id`, `name`, `reports_count`
and `average_age` for every employee who has at least one direct report: the
number of employees reporting to them, and the average `age` of those
reports rounded to the nearest integer. No ordering required.

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
+-------------+-------+---------------+-------------+
| employee_id | name  | reports_count | average_age |
+-------------+-------+---------------+-------------+
| 9           | Hercy | 2             | 39.0        |
+-------------+-------+---------------+-------------+
Explanation: Hercy manages Alice and Bob; their average age is 38.5, rounded to 39.

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
+-------------+------+---------------+-------------+
| employee_id | name | reports_count | average_age |
+-------------+------+---------------+-------------+
| 1           | Ann  | 1             | 40.0        |
| 2           | Bob  | 1             | 30.0        |
+-------------+------+---------------+-------------+
Explanation: A chain: Ann manages Bob, Bob manages Cal.

Constraints:

    1 <= number of rows <= 10^4

    REQUIRED: one query over Employees, one row per manager.

    FORBIDDEN: a subquery per manager; a name lookup in Python.

    Runner: sqlite3 in memory. Write portable SQL: CASE not IF, COALESCE,
    || for concatenation, strftime()/julianday()/date() for dates.
"""

from dsa.sql import SQLDrill


class Solution(SQLDrill):

    def query(self) -> str:
        return """

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

# assert sol.run(EXAMPLE_1) == [(9, 'Hercy', 2, 39.0)]
# assert sol.run(EXAMPLE_2) == [(1, 'Ann', 1, 40.0), (2, 'Bob', 1, 30.0)]
