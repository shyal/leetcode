"""
DRILL: Second Highest Salary
TRAINS: sql-nth-value, sql-subquery

Given the table `Employee`, return the second highest distinct `salary` as
a single row with one column, `SecondHighestSalary`. If there is no second
highest salary, return one row containing NULL.

Table: Employee

    +-------------+------+
    | Column Name | Type |
    +-------------+------+
    | id          | int  |
    | salary      | int  |
    +-------------+------+
    id is the primary key.

Example 1:

Input:
Employee table:
+----+--------+
| id | salary |
+----+--------+
| 1  | 100    |
| 2  | 200    |
| 3  | 300    |
+----+--------+
Output:
+---------------------+
| SecondHighestSalary |
+---------------------+
| 200                 |
+---------------------+
Explanation: The distinct salaries are 100, 200, 300; the second highest is 200.

Example 2:

Input:
Employee table:
+----+--------+
| id | salary |
+----+--------+
| 1  | 100    |
+----+--------+
Output:
+---------------------+
| SecondHighestSalary |
+---------------------+
| null                |
+---------------------+
Explanation: Only one salary: the answer is a row holding NULL, not an empty result.

Example 3:

Input:
Employee table:
+----+--------+
| id | salary |
+----+--------+
| 1  | 100    |
| 2  | 100    |
| 3  | 200    |
+----+--------+
Output:
+---------------------+
| SecondHighestSalary |
+---------------------+
| 100                 |
+---------------------+
Explanation: Distinct salaries are 100 and 200; the second highest is 100.

Constraints:

    1 <= number of rows <= 10^4

    REQUIRED: salaries are compared DISTINCT; with no second highest, the
    result is one row containing NULL.

    FORBIDDEN: returning zero rows in that case (a bare skip-one query does
    exactly that).

    Runner: sqlite3 in memory. Write portable SQL: CASE not IF, COALESCE,
    || for concatenation, strftime()/julianday()/date() for dates.
"""

from dsa.sql import SQLDrill


class Solution(SQLDrill):

    def query(self) -> str:
        return """

        """


EXAMPLE_1 = """
CREATE TABLE Employee (id INTEGER, salary INTEGER);
INSERT INTO Employee VALUES (1, 100);
INSERT INTO Employee VALUES (2, 200);
INSERT INTO Employee VALUES (3, 300);
"""

EXAMPLE_2 = """
CREATE TABLE Employee (id INTEGER, salary INTEGER);
INSERT INTO Employee VALUES (1, 100);
"""

EXAMPLE_3 = """
CREATE TABLE Employee (id INTEGER, salary INTEGER);
INSERT INTO Employee VALUES (1, 100);
INSERT INTO Employee VALUES (2, 100);
INSERT INTO Employee VALUES (3, 200);
"""


sol = Solution()

sol.show(EXAMPLE_1)

# assert sol.run(EXAMPLE_1) == [(200,)]
# assert sol.run(EXAMPLE_2) == [(None,)]
# assert sol.run(EXAMPLE_3) == [(100,)]
