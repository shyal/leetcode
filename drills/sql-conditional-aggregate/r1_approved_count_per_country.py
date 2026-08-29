"""
DRILL: Approved Count Per Country
TRAINS: sql-conditional-aggregate

Given the table Transactions, return country and approved_count for every
country: the number of that country's transactions whose state is
'approved'. A country with no approved transaction shows 0, not NULL. Any row
order.

Table: Transactions

    +-------------+---------+
    | Column Name | Type    |
    +-------------+---------+
    | country     | varchar |
    | state       | varchar |
    +-------------+---------+
    One row per transaction. state is 'approved' or 'declined'.

Example 1:

Input:
Transactions table:
+---------+----------+
| country | state    |
+---------+----------+
| US      | approved |
| US      | declined |
| US      | approved |
| DE      | approved |
+---------+----------+
Output:
+---------+----------------+
| country | approved_count |
+---------+----------------+
| DE      | 1              |
| US      | 2              |
+---------+----------------+
Explanation: US has three transactions, two of them approved.

Example 2:

Input:
Transactions table:
+---------+----------+
| country | state    |
+---------+----------+
| FR      | declined |
| FR      | declined |
+---------+----------+
Output:
+---------+----------------+
| country | approved_count |
+---------+----------------+
| FR      | 0              |
+---------+----------------+
Explanation: FR still appears, with 0 rather than NULL.

Constraints:

    1 <= number of rows <= 10^4

    REQUIRED: one query, one GROUP BY country; a country with nothing
    approved shows 0.

    FORBIDDEN: a WHERE on state (it drops the country entirely); a separate
    query per state.

    Runner: sqlite3 in memory. Write portable SQL: CASE not IF, COALESCE,
    || for concatenation, strftime()/julianday()/date() for dates.
"""

from dsa.sql import SQLDrill


class Solution(SQLDrill):

    def query(self) -> str:
        return """

        """


EXAMPLE_1 = """
CREATE TABLE Transactions (country TEXT, state TEXT);
INSERT INTO Transactions VALUES ('US', 'approved');
INSERT INTO Transactions VALUES ('US', 'declined');
INSERT INTO Transactions VALUES ('US', 'approved');
INSERT INTO Transactions VALUES ('DE', 'approved');
"""

EXAMPLE_2 = """
CREATE TABLE Transactions (country TEXT, state TEXT);
INSERT INTO Transactions VALUES ('FR', 'declined');
INSERT INTO Transactions VALUES ('FR', 'declined');
"""


sol = Solution()

sol.show(EXAMPLE_1)

# assert sol.run(EXAMPLE_1) == [('DE', 1), ('US', 2)]
# assert sol.run(EXAMPLE_2) == [('FR', 0)]
