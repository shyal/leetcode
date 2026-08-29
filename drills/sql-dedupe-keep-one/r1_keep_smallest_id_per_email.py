"""
DRILL: Keep Smallest Id Per Email
TRAINS: sql-dedupe-keep-one

Given the table Person, return the id and email of the rows to keep after
removing duplicate emails: for each email, the row with the smallest id. Order
by id.

Table: Person

    +-------------+---------+
    | Column Name | Type    |
    +-------------+---------+
    | id          | int     |
    | email       | varchar |
    +-------------+---------+
    id is the primary key. email is not unique.

Example 1:

Input:
Person table:
+----+------------------+
| id | email            |
+----+------------------+
| 1  | john@example.com |
| 2  | bob@example.com  |
| 3  | john@example.com |
+----+------------------+
Output:
+----+------------------+
| id | email            |
+----+------------------+
| 1  | john@example.com |
| 2  | bob@example.com  |
+----+------------------+
Explanation: Row 3 duplicates row 1's email and has the larger id.

Example 2:

Input:
Person table:
+----+---------+
| id | email   |
+----+---------+
| 7  | a@x.com |
| 4  | a@x.com |
| 9  | a@x.com |
+----+---------+
Output:
+----+---------+
| id | email   |
+----+---------+
| 4  | a@x.com |
+----+---------+
Explanation: Three copies; the smallest id is 4.

Constraints:

    1 <= number of rows <= 10^4

    REQUIRED: one row per email, the one with MIN(id): GROUP BY email
    selecting MIN(id) and the email. Selecting DISTINCT email loses the id,
    and selecting a bare id alongside GROUP BY email returns an arbitrary row
    in most engines; both are the failure mode this drill exists to kill.

    Runner: sqlite3 in memory. Write portable SQL: CASE not IF, COALESCE,
    || for concatenation, strftime()/julianday()/date() for dates.
"""

from dsa.sql import SQLDrill

EXAMPLE_1 = """
CREATE TABLE Person (id INTEGER, email TEXT);
INSERT INTO Person VALUES (1, 'john@example.com');
INSERT INTO Person VALUES (2, 'bob@example.com');
INSERT INTO Person VALUES (3, 'john@example.com');
"""

EXAMPLE_2 = """
CREATE TABLE Person (id INTEGER, email TEXT);
INSERT INTO Person VALUES (7, 'a@x.com');
INSERT INTO Person VALUES (4, 'a@x.com');
INSERT INTO Person VALUES (9, 'a@x.com');
"""


class Solution(SQLDrill):

    def query(self) -> str:
        return """

        """


sol = Solution()

sol.show(EXAMPLE_1)

# assert sol.run(EXAMPLE_1) == [(1, 'john@example.com'), (2, 'bob@example.com')]
# assert sol.run(EXAMPLE_2) == [(4, 'a@x.com')]
