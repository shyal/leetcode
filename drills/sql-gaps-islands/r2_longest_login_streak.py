"""
DRILL: Longest Login Streak Per User
TRAINS: sql-gaps-islands

Given the table Logins with one row per user per day they logged in, return
user_id and streak: the length of that user's longest run of consecutive
calendar days with a login. Order by user_id.

Table: Logins

    +-------------+------+
    | Column Name | Type |
    +-------------+------+
    | user_id     | int  |
    | login_date  | date |
    +-------------+------+
    (user_id, login_date) is the primary key.

Example 1:

Input:
Logins table:
+---------+------------+
| user_id | login_date |
+---------+------------+
| 1       | 2026-08-01 |
| 1       | 2026-08-02 |
| 1       | 2026-08-03 |
| 1       | 2026-08-05 |
| 2       | 2026-08-10 |
| 2       | 2026-08-12 |
+---------+------------+
Output:
+---------+--------+
| user_id | streak |
+---------+--------+
| 1       | 3      |
| 2       | 1      |
+---------+--------+
Explanation: User 1 logged in on the 1st, 2nd and 3rd (a streak of 3), then the 5th. User 2 never logged in on consecutive days.

Example 2:

Input:
Logins table:
+---------+------------+
| user_id | login_date |
+---------+------------+
| 7       | 2026-01-30 |
| 7       | 2026-01-31 |
| 7       | 2026-02-01 |
| 7       | 2026-02-10 |
| 7       | 2026-02-11 |
+---------+------------+
Output:
+---------+--------+
| user_id | streak |
+---------+--------+
| 7       | 3      |
+---------+--------+
Explanation: A streak of three spans the month boundary; a later streak is only two.

Constraints:

    1 <= number of rows <= 10^5

    REQUIRED: within each user, the date minus ROW_NUMBER() OVER (PARTITION BY
    user_id ORDER BY login_date) is constant across a streak:
    julianday(login_date) - rn in sqlite, login_date - rn in Postgres,
    DATE_SUB in MySQL, date_add('day', -rn, ...) in Presto. Group on (user_id,
    that difference), count each island, take the MAX per user. Comparing to
    the previous day with LAG finds where streaks break but not how long they
    are without a second running sum; the row-number difference does it in one
    step.

    Runner: sqlite3 in memory. Write portable SQL: CASE not IF, COALESCE,
    || for concatenation, strftime()/julianday()/date() for dates.
"""

import sqlite3

EXAMPLE_1 = """
CREATE TABLE Logins (user_id INTEGER, login_date TEXT);
INSERT INTO Logins VALUES (1, '2026-08-01');
INSERT INTO Logins VALUES (1, '2026-08-02');
INSERT INTO Logins VALUES (1, '2026-08-03');
INSERT INTO Logins VALUES (1, '2026-08-05');
INSERT INTO Logins VALUES (2, '2026-08-10');
INSERT INTO Logins VALUES (2, '2026-08-12');
"""

EXAMPLE_2 = """
CREATE TABLE Logins (user_id INTEGER, login_date TEXT);
INSERT INTO Logins VALUES (7, '2026-01-30');
INSERT INTO Logins VALUES (7, '2026-01-31');
INSERT INTO Logins VALUES (7, '2026-02-01');
INSERT INTO Logins VALUES (7, '2026-02-10');
INSERT INTO Logins VALUES (7, '2026-02-11');
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

print(run(EXAMPLE_1, sol.query()))  # [(1, 3), (2, 1)]

# assert run(EXAMPLE_1, sol.query()) == [(1, 3), (2, 1)]
# assert run(EXAMPLE_2, sol.query()) == [(7, 3)]
