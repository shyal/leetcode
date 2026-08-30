"""
DRILL: Unique Id Or Null
TRAINS: sql-join-left-keep

Given the tables `Employees` and `EmployeeUNI`, return the `unique_id` and
`name` of every employee. Show NULL as the `unique_id` when the employee has
none. No ordering required.

Table: Employees

    +-------------+---------+
    | Column Name | Type    |
    +-------------+---------+
    | id          | int     |
    | name        | varchar |
    +-------------+---------+
    id is the primary key.

    Table: EmployeeUNI

    +-------------+------+
    | Column Name | Type |
    +-------------+------+
    | id          | int  |
    | unique_id   | int  |
    +-------------+------+
    (id, unique_id) is the primary key. Not every employee has a row here.

Example 1:

Input:
Employees table:
+----+----------+
| id | name     |
+----+----------+
| 1  | Alice    |
| 7  | Bob      |
| 11 | Meir     |
| 90 | Winston  |
| 3  | Jonathan |
+----+----------+
EmployeeUNI table:
+----+-----------+
| id | unique_id |
+----+-----------+
| 3  | 1         |
| 11 | 2         |
| 90 | 3         |
+----+-----------+
Output:
+-----------+----------+
| unique_id | name     |
+-----------+----------+
| null      | Alice    |
| 1         | Jonathan |
| null      | Bob      |
| 2         | Meir     |
| 3         | Winston  |
+-----------+----------+
Explanation: Alice and Bob have no unique id and still appear, with NULL.

Example 2:

Input:
Employees table:
+----+-------+
| id | name  |
+----+-------+
| 1  | Alice |
| 2  | Bob   |
+----+-------+
EmployeeUNI table:
+----+-----------+
| id | unique_id |
+----+-----------+
+----+-----------+
Output:
+-----------+-------+
| unique_id | name  |
+-----------+-------+
| null      | Alice |
| null      | Bob   |
+-----------+-------+
Explanation: EmployeeUNI is empty; every employee appears with NULL.

Constraints:

    1 <= rows in Employees <= 10^4
    0 <= rows in EmployeeUNI <= 10^4

    REQUIRED: every employee appears exactly once, with NULL where no
    unique_id exists.

    FORBIDDEN: an inner join (it drops the unmatched employees).

    Runner: sqlite3 in memory. Write portable SQL: CASE not IF, COALESCE,
    || for concatenation, strftime()/julianday()/date() for dates.

---

The tag kind of gives the answer away.

"""

from dsa.sql import SQLDrill


class Solution(SQLDrill):

    def query(self) -> str:
        return """
            select
                unique_id,
                e.name
            from Employees as e
            left join EmployeeUNI as u on e.id = u.id
            ;
        """


EXAMPLE_1 = """
CREATE TABLE Employees (id INTEGER, name TEXT);
INSERT INTO Employees VALUES (1, 'Alice');
INSERT INTO Employees VALUES (7, 'Bob');
INSERT INTO Employees VALUES (11, 'Meir');
INSERT INTO Employees VALUES (90, 'Winston');
INSERT INTO Employees VALUES (3, 'Jonathan');
CREATE TABLE EmployeeUNI (id INTEGER, unique_id INTEGER);
INSERT INTO EmployeeUNI VALUES (3, 1);
INSERT INTO EmployeeUNI VALUES (11, 2);
INSERT INTO EmployeeUNI VALUES (90, 3);
"""

EXAMPLE_2 = """
CREATE TABLE Employees (id INTEGER, name TEXT);
INSERT INTO Employees VALUES (1, 'Alice');
INSERT INTO Employees VALUES (2, 'Bob');
CREATE TABLE EmployeeUNI (id INTEGER, unique_id INTEGER);
"""


sol = Solution()

sol.show(EXAMPLE_1)

assert sol.run(EXAMPLE_1) == [
    (1, "Jonathan"),
    (2, "Meir"),
    (3, "Winston"),
    (None, "Alice"),
    (None, "Bob"),
]
assert sol.run(EXAMPLE_2) == [(None, "Alice"), (None, "Bob")]
