"""
DRILL: Who Has The Most Friends
TRAINS: sql-set-union, sql-group-aggregate

Given the table RequestAccepted, return the id and num (number of friends) of
the person with the most friends. An accepted request makes both people
friends of each other. The test data has a unique answer.

Table: RequestAccepted

    +----------------+---------+
    | Column Name    | Type    |
    +----------------+---------+
    | requester_id   | int     |
    | accepter_id    | int     |
    +----------------+---------+
    (requester_id, accepter_id) is the primary key.

Example 1:

Input:
RequestAccepted table:
+--------------+-------------+
| requester_id | accepter_id |
+--------------+-------------+
| 1            | 2           |
| 1            | 3           |
| 2            | 3           |
| 3            | 4           |
+--------------+-------------+
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
+--------------+-------------+
| requester_id | accepter_id |
+--------------+-------------+
| 5            | 1           |
| 6            | 1           |
| 1            | 7           |
+--------------+-------------+
Output:
+----+-----+
| id | num |
+----+-----+
| 1  | 3   |
+----+-----+
Explanation: Person 1 accepted two requests and made one: three friends.

Constraints:

    1 <= number of rows <= 10^4

    REQUIRED: a friendship counts for both sides. Counting only one column,
    or dropping repeated ids before counting, is the failure mode this drill
    exists to kill.

    Runner: sqlite3 in memory. Write portable SQL: CASE not IF, COALESCE,
    || for concatenation, strftime()/julianday()/date() for dates.
"""

from dsa.sql import SQLDrill


class Solution(SQLDrill):

    def query(self) -> str:
        return """

        """


EXAMPLE_1 = """
CREATE TABLE RequestAccepted (requester_id INTEGER, accepter_id INTEGER);
INSERT INTO RequestAccepted VALUES (1, 2);
INSERT INTO RequestAccepted VALUES (1, 3);
INSERT INTO RequestAccepted VALUES (2, 3);
INSERT INTO RequestAccepted VALUES (3, 4);
"""

EXAMPLE_2 = """
CREATE TABLE RequestAccepted (requester_id INTEGER, accepter_id INTEGER);
INSERT INTO RequestAccepted VALUES (5, 1);
INSERT INTO RequestAccepted VALUES (6, 1);
INSERT INTO RequestAccepted VALUES (1, 7);
"""


sol = Solution()

sol.show(EXAMPLE_1)

# assert sol.run(EXAMPLE_1) == [(3, 3)]
# assert sol.run(EXAMPLE_2) == [(1, 3)]
