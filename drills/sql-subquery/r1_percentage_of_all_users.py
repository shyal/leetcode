"""
DRILL: Percentage Of All Users Per Contest
TRAINS: sql-subquery

Given the tables Users and Register, return each contest_id with percentage:
the share of all users registered in that contest, as a percentage rounded to
2 decimal places. Order by percentage descending, then contest_id ascending.

Table: Users

    +-------------+---------+
    | Column Name | Type    |
    +-------------+---------+
    | user_id     | int     |
    | user_name   | varchar |
    +-------------+---------+
    user_id is the primary key.

    Table: Register

    +-------------+---------+
    | Column Name | Type    |
    +-------------+---------+
    | contest_id  | int     |
    | user_id     | int     |
    +-------------+---------+
    (contest_id, user_id) is the primary key.

Example 1:

Input:
Users table:
+---------+-----------+
| user_id | user_name |
+---------+-----------+
| 6       | Alice     |
| 2       | Bob       |
| 7       | Alex      |
+---------+-----------+
Register table:
+------------+---------+
| contest_id | user_id |
+------------+---------+
| 215        | 6       |
| 209        | 2       |
| 208        | 2       |
| 210        | 6       |
| 208        | 6       |
| 209        | 7       |
| 209        | 6       |
| 215        | 7       |
| 208        | 7       |
| 210        | 2       |
| 207        | 2       |
| 210        | 7       |
+------------+---------+
Output:
+------------+------------+
| contest_id | percentage |
+------------+------------+
| 208        | 100.0      |
| 209        | 100.0      |
| 210        | 100.0      |
| 215        | 66.67      |
| 207        | 33.33      |
+------------+------------+
Explanation: Three users. Contests 208, 209 and 210 have all three; 215 has two (66.67); 207 has one (33.33).

Example 2:

Input:
Users table:
+---------+-----------+
| user_id | user_name |
+---------+-----------+
| 1       | Ann       |
| 2       | Ben       |
| 3       | Cal       |
| 4       | Dee       |
+---------+-----------+
Register table:
+------------+---------+
| contest_id | user_id |
+------------+---------+
| 100        | 1       |
+------------+---------+
Output:
+------------+------------+
| contest_id | percentage |
+------------+------------+
| 100        | 25.0       |
+------------+------------+
Explanation: Four users, one registered: 25.00.

Constraints:

    1 <= rows in Users <= 10^4
    1 <= rows in Register <= 10^4

    REQUIRED: the denominator is a scalar subquery over Users, evaluated once.
    Hard-coding the user count, or joining Users into the grouped query and
    counting its rows, is the failure mode this drill exists to kill.

    Runner: sqlite3 in memory. Write portable SQL: CASE not IF, COALESCE,
    || for concatenation, strftime()/julianday()/date() for dates.
"""

import sqlite3

EXAMPLE_1 = """
CREATE TABLE Users (user_id INTEGER, user_name TEXT);
INSERT INTO Users VALUES (6, 'Alice');
INSERT INTO Users VALUES (2, 'Bob');
INSERT INTO Users VALUES (7, 'Alex');
CREATE TABLE Register (contest_id INTEGER, user_id INTEGER);
INSERT INTO Register VALUES (215, 6);
INSERT INTO Register VALUES (209, 2);
INSERT INTO Register VALUES (208, 2);
INSERT INTO Register VALUES (210, 6);
INSERT INTO Register VALUES (208, 6);
INSERT INTO Register VALUES (209, 7);
INSERT INTO Register VALUES (209, 6);
INSERT INTO Register VALUES (215, 7);
INSERT INTO Register VALUES (208, 7);
INSERT INTO Register VALUES (210, 2);
INSERT INTO Register VALUES (207, 2);
INSERT INTO Register VALUES (210, 7);
"""

EXAMPLE_2 = """
CREATE TABLE Users (user_id INTEGER, user_name TEXT);
INSERT INTO Users VALUES (1, 'Ann');
INSERT INTO Users VALUES (2, 'Ben');
INSERT INTO Users VALUES (3, 'Cal');
INSERT INTO Users VALUES (4, 'Dee');
CREATE TABLE Register (contest_id INTEGER, user_id INTEGER);
INSERT INTO Register VALUES (100, 1);
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

print(run(EXAMPLE_1, sol.query()))  # [(208, 100.0), (209, 100.0), (210, 100.0), (215, 66.67), (207, 33.33)]

# assert run(EXAMPLE_1, sol.query()) == [(208, 100.0), (209, 100.0), (210, 100.0), (215, 66.67), (207, 33.33)]
# assert run(EXAMPLE_2, sol.query()) == [(100, 25.0)]
