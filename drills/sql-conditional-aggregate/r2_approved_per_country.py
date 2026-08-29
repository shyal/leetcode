"""
DRILL: Approved Transactions Per Country
TRAINS: sql-conditional-aggregate

Given the table Transactions, return for each country: trans_count (all
transactions), approved_count, trans_total_amount (sum of all amounts) and
approved_total_amount (sum of approved amounts). Counts and sums must be 0,
not NULL, when nothing is approved. Any row order.

Table: Transactions

    +-------------+---------+
    | Column Name | Type    |
    +-------------+---------+
    | id          | int     |
    | country     | varchar |
    | state       | varchar |
    | amount      | int     |
    +-------------+---------+
    id is the primary key. state is 'approved' or 'declined'.

Example 1:

Input:
Transactions table:
+-----+---------+----------+--------+
| id  | country | state    | amount |
+-----+---------+----------+--------+
| 121 | US      | approved | 1000   |
| 122 | US      | declined | 2000   |
| 123 | US      | approved | 2000   |
| 124 | DE      | approved | 2000   |
+-----+---------+----------+--------+
Output:
+---------+-------------+----------------+--------------------+-----------------------+
| country | trans_count | approved_count | trans_total_amount | approved_total_amount |
+---------+-------------+----------------+--------------------+-----------------------+
| DE      | 1           | 1              | 2000               | 2000                  |
| US      | 3           | 2              | 5000               | 3000                  |
+---------+-------------+----------------+--------------------+-----------------------+
Explanation: US: three transactions, two approved, 5000 in total, 3000 approved.

Example 2:

Input:
Transactions table:
+----+---------+----------+--------+
| id | country | state    | amount |
+----+---------+----------+--------+
| 1  | FR      | declined | 500    |
| 2  | FR      | declined | 700    |
+----+---------+----------+--------+
Output:
+---------+-------------+----------------+--------------------+-----------------------+
| country | trans_count | approved_count | trans_total_amount | approved_total_amount |
+---------+-------------+----------------+--------------------+-----------------------+
| FR      | 2           | 0              | 1200               | 0                     |
+---------+-------------+----------------+--------------------+-----------------------+
Explanation: Nothing approved: the approved columns are 0, not NULL.

Constraints:

    1 <= number of rows <= 10^4

    REQUIRED: one query with ONE GROUP BY country and NO WHERE on state. A
    separate query per state, a self-join, or a NULL where a count or sum
    should be 0 is the failure mode this drill exists to kill.

    Runner: sqlite3 in memory. Write portable SQL: CASE not IF, COALESCE,
    || for concatenation, strftime()/julianday()/date() for dates.
"""

from dsa.sql import SQLDrill


class Solution(SQLDrill):

    def query(self) -> str:
        return """

        """


EXAMPLE_1 = """
CREATE TABLE Transactions (id INTEGER, country TEXT, state TEXT, amount INTEGER);
INSERT INTO Transactions VALUES (121, 'US', 'approved', 1000);
INSERT INTO Transactions VALUES (122, 'US', 'declined', 2000);
INSERT INTO Transactions VALUES (123, 'US', 'approved', 2000);
INSERT INTO Transactions VALUES (124, 'DE', 'approved', 2000);
"""

EXAMPLE_2 = """
CREATE TABLE Transactions (id INTEGER, country TEXT, state TEXT, amount INTEGER);
INSERT INTO Transactions VALUES (1, 'FR', 'declined', 500);
INSERT INTO Transactions VALUES (2, 'FR', 'declined', 700);
"""


sol = Solution()

sol.show(EXAMPLE_1)

# assert sol.run(EXAMPLE_1) == [('DE', 1, 1, 2000, 2000), ('US', 3, 2, 5000, 3000)]
# assert sol.run(EXAMPLE_2) == [('FR', 2, 0, 1200, 0)]
