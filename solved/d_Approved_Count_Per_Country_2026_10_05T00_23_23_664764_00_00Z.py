"""
DRILL: Approved Count Per Country

Given the table `Transactions`, return `country` and `approved_count` for
every country: the number of that country's transactions whose `state` is
'approved'. A country with no approved transaction shows 0, not NULL. No
ordering required.

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
---
Failed again. Created mnenomic for syntax: CWTEE cows wear ties every evening
Learning.
"""

from dsa.sql import SQLDrill


# mu 0.7
# extends SQLDrill
#
# def query() -> str
#   return 'select country, sum(case when state = "approved" then 1  else 0 end) as approved_count from Transactions group by country;'

class Solution(SQLDrill):
    def query(self) -> str:
        return 'select country, sum(case when state = "approved" then 1  else 0 end) as approved_count from Transactions group by country;'


EXAMPLE_1 = "\nCREATE TABLE Transactions (country TEXT, state TEXT);\nINSERT INTO Transactions VALUES ('US', 'approved');\nINSERT INTO Transactions VALUES ('US', 'declined');\nINSERT INTO Transactions VALUES ('US', 'approved');\nINSERT INTO Transactions VALUES ('DE', 'approved');\n"
EXAMPLE_2 = "\nCREATE TABLE Transactions (country TEXT, state TEXT);\nINSERT INTO Transactions VALUES ('FR', 'declined');\nINSERT INTO Transactions VALUES ('FR', 'declined');\n"
sol = Solution()
sol.show(EXAMPLE_1)
assert sol.run(EXAMPLE_1) == [('DE', 1), ('US', 2)]
assert sol.run(EXAMPLE_2) == [('FR', 0)]
