"""
DRILL: Average Years Per Project
TRAINS: sql-group-aggregate

Given the table `Project`, return each `project_id` with `average_years`:
the average `experience_years` of its employees, rounded to 2 decimal
places. No ordering required.

Table: Project

    +------------------+---------+
    | Column Name      | Type    |
    +------------------+---------+
    | project_id       | int     |
    | employee_id      | int     |
    | experience_years | int     |
    +------------------+---------+
    (project_id, employee_id) is the primary key.

Example 1:

Input:
Project table:
+------------+-------------+------------------+
| project_id | employee_id | experience_years |
+------------+-------------+------------------+
| 1          | 1           | 3                |
| 1          | 2           | 2                |
| 1          | 3           | 1                |
| 2          | 1           | 3                |
| 2          | 4           | 2                |
+------------+-------------+------------------+
Output:
+------------+---------------+
| project_id | average_years |
+------------+---------------+
| 1          | 2.0           |
| 2          | 2.5           |
+------------+---------------+
Explanation: Project 1: (3 + 2 + 1) / 3 = 2.00. Project 2: (3 + 2) / 2 = 2.50.

Example 2:

Input:
Project table:
+------------+-------------+------------------+
| project_id | employee_id | experience_years |
+------------+-------------+------------------+
| 5          | 1           | 1                |
| 5          | 2           | 1                |
| 5          | 3           | 2                |
+------------+-------------+------------------+
Output:
+------------+---------------+
| project_id | average_years |
+------------+---------------+
| 5          | 1.33          |
+------------+---------------+
Explanation: 4 / 3 = 1.333..., rounded to 1.33.

Constraints:

    1 <= number of rows <= 10^4

    REQUIRED: the rounding happens in SQL, on the aggregate.

    FORBIDDEN: rounding in Python; a value with more than 2 decimals.

    Runner: sqlite3 in memory. Write portable SQL: CASE not IF, COALESCE,
    || for concatenation, strftime()/julianday()/date() for dates.
"""

from dsa.sql import SQLDrill


class Solution(SQLDrill):

    def query(self) -> str:
        return """

        """


EXAMPLE_1 = """
CREATE TABLE Project (project_id INTEGER, employee_id INTEGER, experience_years INTEGER);
INSERT INTO Project VALUES (1, 1, 3);
INSERT INTO Project VALUES (1, 2, 2);
INSERT INTO Project VALUES (1, 3, 1);
INSERT INTO Project VALUES (2, 1, 3);
INSERT INTO Project VALUES (2, 4, 2);
"""

EXAMPLE_2 = """
CREATE TABLE Project (project_id INTEGER, employee_id INTEGER, experience_years INTEGER);
INSERT INTO Project VALUES (5, 1, 1);
INSERT INTO Project VALUES (5, 2, 1);
INSERT INTO Project VALUES (5, 3, 2);
"""


sol = Solution()

sol.show(EXAMPLE_1)

# assert sol.run(EXAMPLE_1) == [(1, 2.0), (2, 2.5)]
# assert sol.run(EXAMPLE_2) == [(5, 1.33)]
