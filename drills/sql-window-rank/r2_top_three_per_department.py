"""
DRILL: Department Top Three Salaries
TRAINS: sql-window-rank

Given the tables Employee and Department, return Department, Employee and
Salary for every employee whose salary is among the three highest distinct
salaries in their department. Order by Department, then Salary descending,
then Employee.

Table: Employee

    +--------------+---------+
    | Column Name  | Type    |
    +--------------+---------+
    | id           | int     |
    | name         | varchar |
    | salary       | int     |
    | departmentId | int     |
    +--------------+---------+
    id is the primary key. departmentId refers to Department.

    Table: Department

    +-------------+---------+
    | Column Name | Type    |
    +-------------+---------+
    | id          | int     |
    | name        | varchar |
    +-------------+---------+
    id is the primary key.

Example 1:

Input:
Employee table:
+----+-------+--------+--------------+
| id | name  | salary | departmentId |
+----+-------+--------+--------------+
| 1  | Joe   | 85000  | 1            |
| 2  | Henry | 80000  | 2            |
| 3  | Sam   | 60000  | 2            |
| 4  | Max   | 90000  | 1            |
| 5  | Janet | 69000  | 1            |
| 6  | Randy | 85000  | 1            |
| 7  | Will  | 70000  | 1            |
+----+-------+--------+--------------+
Department table:
+----+-------+
| id | name  |
+----+-------+
| 1  | IT    |
| 2  | Sales |
+----+-------+
Output:
+------------+----------+--------+
| Department | Employee | Salary |
+------------+----------+--------+
| IT         | Max      | 90000  |
| IT         | Joe      | 85000  |
| IT         | Randy    | 85000  |
| IT         | Will     | 70000  |
| Sales      | Henry    | 80000  |
| Sales      | Sam      | 60000  |
+------------+----------+--------+
Explanation: IT's distinct top three are 90000, 85000, 70000; Joe and Randy both earn 85000 and both appear. Sales has only two salaries.

Example 2:

Input:
Employee table:
+----+------+--------+--------------+
| id | name | salary | departmentId |
+----+------+--------+--------------+
| 1  | Ann  | 10     | 1            |
| 2  | Ben  | 20     | 1            |
| 3  | Cal  | 30     | 1            |
| 4  | Dee  | 40     | 1            |
| 5  | Eve  | 40     | 1            |
+----+------+--------+--------------+
Department table:
+----+------+
| id | name |
+----+------+
| 1  | Ops  |
+----+------+
Output:
+------------+----------+--------+
| Department | Employee | Salary |
+------------+----------+--------+
| Ops        | Dee      | 40     |
| Ops        | Eve      | 40     |
| Ops        | Cal      | 30     |
| Ops        | Ben      | 20     |
+------------+----------+--------+
Explanation: Distinct top three in Ops are 40, 30, 20; Dee and Eve tie at 40; Ann is out.

Constraints:

    1 <= rows in Employee <= 10^4
    1 <= rows in Department <= 10^3

    REQUIRED: DENSE_RANK() OVER (PARTITION BY departmentId ORDER BY salary
    DESC) in a CTE or subquery, then WHERE rk <= 3 outside it. A window
    function cannot be referenced in the WHERE of the query that computes it
    (windows run after WHERE); that is the failure mode this drill exists to
    kill. ROW_NUMBER would drop Randy, who ties with Joe.

    Runner: sqlite3 in memory. Write portable SQL: CASE not IF, COALESCE,
    || for concatenation, strftime()/julianday()/date() for dates.
"""

import sqlite3

EXAMPLE_1 = """
CREATE TABLE Employee (id INTEGER, name TEXT, salary INTEGER, departmentId INTEGER);
INSERT INTO Employee VALUES (1, 'Joe', 85000, 1);
INSERT INTO Employee VALUES (2, 'Henry', 80000, 2);
INSERT INTO Employee VALUES (3, 'Sam', 60000, 2);
INSERT INTO Employee VALUES (4, 'Max', 90000, 1);
INSERT INTO Employee VALUES (5, 'Janet', 69000, 1);
INSERT INTO Employee VALUES (6, 'Randy', 85000, 1);
INSERT INTO Employee VALUES (7, 'Will', 70000, 1);
CREATE TABLE Department (id INTEGER, name TEXT);
INSERT INTO Department VALUES (1, 'IT');
INSERT INTO Department VALUES (2, 'Sales');
"""

EXAMPLE_2 = """
CREATE TABLE Employee (id INTEGER, name TEXT, salary INTEGER, departmentId INTEGER);
INSERT INTO Employee VALUES (1, 'Ann', 10, 1);
INSERT INTO Employee VALUES (2, 'Ben', 20, 1);
INSERT INTO Employee VALUES (3, 'Cal', 30, 1);
INSERT INTO Employee VALUES (4, 'Dee', 40, 1);
INSERT INTO Employee VALUES (5, 'Eve', 40, 1);
CREATE TABLE Department (id INTEGER, name TEXT);
INSERT INTO Department VALUES (1, 'Ops');
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

print(run(EXAMPLE_1, sol.query()))  # [('IT', 'Max', 90000), ('IT', 'Joe', 85000), ('IT', 'Randy', 85000), ('IT', 'Will', 70000), ('Sales', 'Henry', 80000), ('Sales', 'Sam', 60000)]

# assert run(EXAMPLE_1, sol.query()) == [('IT', 'Max', 90000), ('IT', 'Joe', 85000), ('IT', 'Randy', 85000), ('IT', 'Will', 70000), ('Sales', 'Henry', 80000), ('Sales', 'Sam', 60000)]
# assert run(EXAMPLE_2, sol.query()) == [('Ops', 'Dee', 40), ('Ops', 'Eve', 40), ('Ops', 'Cal', 30), ('Ops', 'Ben', 20)]
