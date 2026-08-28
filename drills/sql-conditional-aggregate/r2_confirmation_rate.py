"""
DRILL: Confirmation Rate
TRAINS: sql-conditional-aggregate

Given the tables Signups and Confirmations, return each user_id with their
confirmation_rate: the number of 'confirmed' messages divided by the number of
confirmation messages they received, rounded to 2 decimal places. A user with
no confirmation messages has a rate of 0. Order by user_id.

Table: Signups

    +----------------+----------+
    | Column Name    | Type     |
    +----------------+----------+
    | user_id        | int      |
    | time_stamp     | datetime |
    +----------------+----------+
    user_id is the primary key.

    Table: Confirmations

    +----------------+----------+
    | Column Name    | Type     |
    +----------------+----------+
    | user_id        | int      |
    | time_stamp     | datetime |
    | action         | varchar  |
    +----------------+----------+
    (user_id, time_stamp) is the primary key. action is 'confirmed' or 'timeout'.

Example 1:

Input:
Signups table:
+---------+---------------------+
| user_id | time_stamp          |
+---------+---------------------+
| 3       | 2020-03-21 10:16:13 |
| 7       | 2020-01-04 13:57:59 |
| 2       | 2020-07-29 23:09:44 |
| 6       | 2020-12-09 10:39:37 |
+---------+---------------------+
Confirmations table:
+---------+---------------------+-----------+
| user_id | time_stamp          | action    |
+---------+---------------------+-----------+
| 3       | 2021-01-06 03:30:46 | timeout   |
| 3       | 2021-07-14 14:00:00 | timeout   |
| 7       | 2021-06-12 11:57:29 | confirmed |
| 7       | 2021-06-13 12:58:28 | confirmed |
| 7       | 2021-06-14 13:59:27 | confirmed |
| 2       | 2021-01-22 00:00:00 | confirmed |
| 2       | 2021-02-28 23:59:59 | timeout   |
+---------+---------------------+-----------+
Output:
+---------+-------------------+
| user_id | confirmation_rate |
+---------+-------------------+
| 2       | 0.5               |
| 3       | 0.0               |
| 6       | 0.0               |
| 7       | 1.0               |
+---------+-------------------+
Explanation: User 6 received no messages: 0. User 3: 0 of 2. User 7: 3 of 3. User 2: 1 of 2.

Example 2:

Input:
Signups table:
+---------+---------------------+
| user_id | time_stamp          |
+---------+---------------------+
| 1       | 2020-01-01 00:00:00 |
+---------+---------------------+
Confirmations table:
+---------+------------+--------+
| user_id | time_stamp | action |
+---------+------------+--------+
+---------+------------+--------+
Output:
+---------+-------------------+
| user_id | confirmation_rate |
+---------+-------------------+
| 1       | 0.0               |
+---------+-------------------+
Explanation: No confirmation rows at all: the only user has rate 0.

Constraints:

    1 <= rows in Signups <= 10^4
    0 <= rows in Confirmations <= 10^4

    REQUIRED: a rate is the mean of a 0/1 flag: AVG(CASE WHEN action =
    'confirmed' THEN 1.0 ELSE 0 END), or SUM over COUNT. Users with no
    confirmation rows must show 0.00, so the join must be LEFT; an inner join,
    or a NULL rate, is the failure mode this drill exists to kill.

    Runner: sqlite3 in memory. Write portable SQL: CASE not IF, COALESCE,
    || for concatenation, strftime()/julianday()/date() for dates.
"""

import sqlite3

EXAMPLE_1 = """
CREATE TABLE Signups (user_id INTEGER, time_stamp TEXT);
INSERT INTO Signups VALUES (3, '2020-03-21 10:16:13');
INSERT INTO Signups VALUES (7, '2020-01-04 13:57:59');
INSERT INTO Signups VALUES (2, '2020-07-29 23:09:44');
INSERT INTO Signups VALUES (6, '2020-12-09 10:39:37');
CREATE TABLE Confirmations (user_id INTEGER, time_stamp TEXT, action TEXT);
INSERT INTO Confirmations VALUES (3, '2021-01-06 03:30:46', 'timeout');
INSERT INTO Confirmations VALUES (3, '2021-07-14 14:00:00', 'timeout');
INSERT INTO Confirmations VALUES (7, '2021-06-12 11:57:29', 'confirmed');
INSERT INTO Confirmations VALUES (7, '2021-06-13 12:58:28', 'confirmed');
INSERT INTO Confirmations VALUES (7, '2021-06-14 13:59:27', 'confirmed');
INSERT INTO Confirmations VALUES (2, '2021-01-22 00:00:00', 'confirmed');
INSERT INTO Confirmations VALUES (2, '2021-02-28 23:59:59', 'timeout');
"""

EXAMPLE_2 = """
CREATE TABLE Signups (user_id INTEGER, time_stamp TEXT);
INSERT INTO Signups VALUES (1, '2020-01-01 00:00:00');
CREATE TABLE Confirmations (user_id INTEGER, time_stamp TEXT, action TEXT);
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

print(run(EXAMPLE_1, sol.query()))  # [(2, 0.5), (3, 0.0), (6, 0.0), (7, 1.0)]

# assert run(EXAMPLE_1, sol.query()) == [(2, 0.5), (3, 0.0), (6, 0.0), (7, 1.0)]
# assert run(EXAMPLE_2, sol.query()) == [(1, 0.0)]
