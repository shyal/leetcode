"""
DRILL: Stack Both Sides
TRAINS: sql-set-union

Given the table `RequestAccepted`, return one column `id` holding every
`requester_id` and every `accepter_id`, one row per appearance. A person who
appears in three requests appears three times. No ordering required.

Table: RequestAccepted

    +--------------+------+
    | Column Name  | Type |
    +--------------+------+
    | requester_id | int  |
    | accepter_id  | int  |
    +--------------+------+
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
+--------------+-------------+
Output:
+----+
| id |
+----+
| 1  |
| 1  |
| 2  |
| 2  |
| 3  |
| 3  |
+----+
Explanation: Six ids for three rows: each row contributes its requester and its accepter.

Example 2:

Input:
RequestAccepted table:
+--------------+-------------+
| requester_id | accepter_id |
+--------------+-------------+
| 5            | 1           |
+--------------+-------------+
Output:
+----+
| id |
+----+
| 1  |
| 5  |
+----+

Constraints:

    1 <= number of rows <= 10^4

    REQUIRED: the result has exactly twice as many rows as the table;
    repeats are kept.

    FORBIDDEN: anything that drops repeats; Python.

    Runner: sqlite3 in memory. Write portable SQL: CASE not IF, COALESCE,
    || for concatenation, strftime()/julianday()/date() for dates.

---

Asked for help as i wrote:

select requester_id
from RequestAccepted
join all
select accepter_id
from RequestAccepted;

instead of:

select requester_id
from RequestAccepted
union all
select accepter_id
from RequestAccepted;

Close.
"""

from dsa.sql import SQLDrill


class Solution(SQLDrill):

    def query(self) -> str:
        return """
            select requester_id
            from RequestAccepted
            union all
            select accepter_id
            from RequestAccepted;
        """


EXAMPLE_1 = """
CREATE TABLE RequestAccepted (requester_id INTEGER, accepter_id INTEGER);
INSERT INTO RequestAccepted VALUES (1, 2);
INSERT INTO RequestAccepted VALUES (1, 3);
INSERT INTO RequestAccepted VALUES (2, 3);
"""

EXAMPLE_2 = """
CREATE TABLE RequestAccepted (requester_id INTEGER, accepter_id INTEGER);
INSERT INTO RequestAccepted VALUES (5, 1);
"""


sol = Solution()

sol.show(EXAMPLE_1)

assert sol.run(EXAMPLE_1) == [(1,), (1,), (2,), (2,), (3,), (3,)]
assert sol.run(EXAMPLE_2) == [(1,), (5,)]
