"""
DRILL: Percentage Of All Users Per Contest
TRAINS: sql-subquery

Given the tables Users and Register, return each contest_id with percentage:
the share of all users registered in that contest, as a percentage rounded to
2 decimal places. Any row order.

Table: Users

    +-------------+---------+
    | Column Name | Type    |
    +-------------+---------+
    | user_id     | int     |
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
+---------+
| user_id |
+---------+
| 6       |
| 2       |
| 7       |
+---------+
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
+---------+
| user_id |
+---------+
| 1       |
| 2       |
| 3       |
| 4       |
+---------+
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

    REQUIRED: the denominator is the count of all users, computed once, in
    SQL.

    FORBIDDEN: a hard-coded user count; joining Users into the grouped query
    and counting its rows.

    Runner: sqlite3 in memory. Write portable SQL: CASE not IF, COALESCE,
    || for concatenation, strftime()/julianday()/date() for dates.
"""

from dsa.sql import SQLDrill


class Solution(SQLDrill):

    def query(self) -> str:
        return """

        """


EXAMPLE_1 = """
CREATE TABLE Users (user_id INTEGER);
INSERT INTO Users VALUES (6);
INSERT INTO Users VALUES (2);
INSERT INTO Users VALUES (7);
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
CREATE TABLE Users (user_id INTEGER);
INSERT INTO Users VALUES (1);
INSERT INTO Users VALUES (2);
INSERT INTO Users VALUES (3);
INSERT INTO Users VALUES (4);
CREATE TABLE Register (contest_id INTEGER, user_id INTEGER);
INSERT INTO Register VALUES (100, 1);
"""


sol = Solution()

sol.show(EXAMPLE_1)

# assert sol.run(EXAMPLE_1) == [(207, 33.33), (208, 100.0), (209, 100.0), (210, 100.0), (215, 66.67)]
# assert sol.run(EXAMPLE_2) == [(100, 25.0)]
