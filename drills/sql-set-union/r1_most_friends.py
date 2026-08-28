"""
DRILL: Who Has The Most Friends
TRAINS: sql-set-union

Given the table RequestAccepted, return the id and num (number of friends) of
the person with the most friends. An accepted request makes both people
friends of each other. The test data has a unique answer.

Table: RequestAccepted

    +----------------+---------+
    | Column Name    | Type    |
    +----------------+---------+
    | requester_id   | int     |
    | accepter_id    | int     |
    | accept_date    | date    |
    +----------------+---------+
    (requester_id, accepter_id) is the primary key.

Example 1:

Input:
RequestAccepted table:
+--------------+-------------+-------------+
| requester_id | accepter_id | accept_date |
+--------------+-------------+-------------+
| 1            | 2           | 2016-06-03  |
| 1            | 3           | 2016-06-08  |
| 2            | 3           | 2016-06-08  |
| 3            | 4           | 2016-06-09  |
+--------------+-------------+-------------+
Output:
+----+-----+
| id | num |
+----+-----+
| 3  | 3   |
+----+-----+
Explanation: Person 3 is friends with 1, 2 and 4.

Example 2:

Input:
RequestAccepted table:
+--------------+-------------+-------------+
| requester_id | accepter_id | accept_date |
+--------------+-------------+-------------+
| 5            | 1           | 2016-06-03  |
| 6            | 1           | 2016-06-04  |
| 1            | 7           | 2016-06-05  |
+--------------+-------------+-------------+
Output:
+----+-----+
| id | num |
+----+-----+
| 1  | 3   |
+----+-----+
Explanation: Person 1 accepted two requests and made one: three friends.

Constraints:

    1 <= number of rows <= 10^4

    REQUIRED: a friendship counts for both sides: stack requester and accepter
    with UNION ALL into one column, then GROUP BY and take the top row.
    Counting only one column, or using UNION (which drops repeated ids before
    counting), is the failure mode this drill exists to kill.

    Runner: sqlite3 in memory. Write portable SQL: CASE not IF, COALESCE,
    || for concatenation, strftime()/julianday()/date() for dates.
"""

import sqlite3

EXAMPLE_1 = """
CREATE TABLE RequestAccepted (requester_id INTEGER, accepter_id INTEGER, accept_date TEXT);
INSERT INTO RequestAccepted VALUES (1, 2, '2016-06-03');
INSERT INTO RequestAccepted VALUES (1, 3, '2016-06-08');
INSERT INTO RequestAccepted VALUES (2, 3, '2016-06-08');
INSERT INTO RequestAccepted VALUES (3, 4, '2016-06-09');
"""

EXAMPLE_2 = """
CREATE TABLE RequestAccepted (requester_id INTEGER, accepter_id INTEGER, accept_date TEXT);
INSERT INTO RequestAccepted VALUES (5, 1, '2016-06-03');
INSERT INTO RequestAccepted VALUES (6, 1, '2016-06-04');
INSERT INTO RequestAccepted VALUES (1, 7, '2016-06-05');
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

print(run(EXAMPLE_1, sol.query()))  # [(3, 3)]

# assert run(EXAMPLE_1, sol.query()) == [(3, 3)]
# assert run(EXAMPLE_2, sol.query()) == [(1, 3)]
