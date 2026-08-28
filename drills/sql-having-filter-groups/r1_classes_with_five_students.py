"""
DRILL: Classes With At Least Five Students
TRAINS: sql-having-filter-groups

Given the table Courses, return every class with at least five students. Order
by class.

Table: Courses

    +-------------+---------+
    | Column Name | Type    |
    +-------------+---------+
    | student     | varchar |
    | class       | varchar |
    +-------------+---------+
    (student, class) is the primary key.

Example 1:

Input:
Courses table:
+---------+----------+
| student | class    |
+---------+----------+
| A       | Math     |
| B       | English  |
| C       | Math     |
| D       | Biology  |
| E       | Math     |
| F       | Computer |
| G       | Math     |
| H       | Math     |
| I       | Math     |
+---------+----------+
Output:
+-------+
| class |
+-------+
| Math  |
+-------+
Explanation: Math has 6 students; every other class has 1.

Example 2:

Input:
Courses table:
+---------+-------+
| student | class |
+---------+-------+
| A       | Art   |
| B       | Art   |
| C       | Art   |
| D       | Art   |
| E       | Art   |
| A       | Gym   |
| B       | Gym   |
| C       | Gym   |
| D       | Gym   |
+---------+-------+
Output:
+-------+
| class |
+-------+
| Art   |
+-------+
Explanation: Art has exactly 5, Gym has 4.

Constraints:

    1 <= number of rows <= 10^4

    REQUIRED: the count condition must be a HAVING on the group. WHERE runs
    before grouping and cannot see COUNT; a WHERE on the count, or counting in
    Python, is the failure mode this drill exists to kill.

    Runner: sqlite3 in memory. Write portable SQL: CASE not IF, COALESCE,
    || for concatenation, strftime()/julianday()/date() for dates.
"""

import sqlite3

EXAMPLE_1 = """
CREATE TABLE Courses (student TEXT, class TEXT);
INSERT INTO Courses VALUES ('A', 'Math');
INSERT INTO Courses VALUES ('B', 'English');
INSERT INTO Courses VALUES ('C', 'Math');
INSERT INTO Courses VALUES ('D', 'Biology');
INSERT INTO Courses VALUES ('E', 'Math');
INSERT INTO Courses VALUES ('F', 'Computer');
INSERT INTO Courses VALUES ('G', 'Math');
INSERT INTO Courses VALUES ('H', 'Math');
INSERT INTO Courses VALUES ('I', 'Math');
"""

EXAMPLE_2 = """
CREATE TABLE Courses (student TEXT, class TEXT);
INSERT INTO Courses VALUES ('A', 'Art');
INSERT INTO Courses VALUES ('B', 'Art');
INSERT INTO Courses VALUES ('C', 'Art');
INSERT INTO Courses VALUES ('D', 'Art');
INSERT INTO Courses VALUES ('E', 'Art');
INSERT INTO Courses VALUES ('A', 'Gym');
INSERT INTO Courses VALUES ('B', 'Gym');
INSERT INTO Courses VALUES ('C', 'Gym');
INSERT INTO Courses VALUES ('D', 'Gym');
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

print(run(EXAMPLE_1, sol.query()))  # [('Math',)]

# assert run(EXAMPLE_1, sol.query()) == [('Math',)]
# assert run(EXAMPLE_2, sol.query()) == [('Art',)]
