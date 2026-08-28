"""
DRILL: Distinct Subjects Per Teacher
TRAINS: sql-group-aggregate

Given the table Teacher, return each teacher_id with cnt, the number of
distinct subjects they teach. Order by teacher_id.

Table: Teacher

    +-------------+------+
    | Column Name | Type |
    +-------------+------+
    | teacher_id  | int  |
    | subject_id  | int  |
    | dept_id     | int  |
    +-------------+------+
    (subject_id, dept_id) is the primary key. A teacher can teach one subject in several departments.

Example 1:

Input:
Teacher table:
+------------+------------+---------+
| teacher_id | subject_id | dept_id |
+------------+------------+---------+
| 1          | 2          | 3       |
| 1          | 2          | 4       |
| 1          | 3          | 3       |
| 2          | 1          | 1       |
| 2          | 2          | 1       |
| 2          | 3          | 1       |
| 2          | 4          | 1       |
+------------+------------+---------+
Output:
+------------+-----+
| teacher_id | cnt |
+------------+-----+
| 1          | 2   |
| 2          | 4   |
+------------+-----+
Explanation: Teacher 1 has three rows but teaches subjects 2 and 3 only.

Example 2:

Input:
Teacher table:
+------------+------------+---------+
| teacher_id | subject_id | dept_id |
+------------+------------+---------+
| 5          | 9          | 1       |
| 5          | 9          | 2       |
| 5          | 9          | 3       |
+------------+------------+---------+
Output:
+------------+-----+
| teacher_id | cnt |
+------------+-----+
| 5          | 1   |
+------------+-----+
Explanation: Three rows, one subject.

Constraints:

    1 <= number of rows <= 10^4

    REQUIRED: one row per teacher with COUNT(DISTINCT subject_id). Counting
    rows instead of distinct subjects is the failure mode this drill exists to
    kill: teacher 1 has three rows and two subjects.

    Runner: sqlite3 in memory. Write portable SQL: CASE not IF, COALESCE,
    || for concatenation, strftime()/julianday()/date() for dates.
"""

import sqlite3

EXAMPLE_1 = """
CREATE TABLE Teacher (teacher_id INTEGER, subject_id INTEGER, dept_id INTEGER);
INSERT INTO Teacher VALUES (1, 2, 3);
INSERT INTO Teacher VALUES (1, 2, 4);
INSERT INTO Teacher VALUES (1, 3, 3);
INSERT INTO Teacher VALUES (2, 1, 1);
INSERT INTO Teacher VALUES (2, 2, 1);
INSERT INTO Teacher VALUES (2, 3, 1);
INSERT INTO Teacher VALUES (2, 4, 1);
"""

EXAMPLE_2 = """
CREATE TABLE Teacher (teacher_id INTEGER, subject_id INTEGER, dept_id INTEGER);
INSERT INTO Teacher VALUES (5, 9, 1);
INSERT INTO Teacher VALUES (5, 9, 2);
INSERT INTO Teacher VALUES (5, 9, 3);
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

print(run(EXAMPLE_1, sol.query()))  # [(1, 2), (2, 4)]

# assert run(EXAMPLE_1, sol.query()) == [(1, 2), (2, 4)]
# assert run(EXAMPLE_2, sol.query()) == [(5, 1)]
