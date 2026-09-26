"""
DRILL: Keep Smallest Id Per Email

Given the table `Person`, return the `id` and `email` of the rows to keep
after removing duplicate emails: for each `email`, the row with the smallest
`id`. No ordering required.

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

    REQUIRED: one query, one row per email, carrying that email's smallest
    id.

    FORBIDDEN: DISTINCT email alone (it loses the id); a bare id next to a
    grouped email (an arbitrary row in most engines).

    Runner: sqlite3 in memory. Write portable SQL: CASE not IF, COALESCE,
    || for concatenation, strftime()/julianday()/date() for dates.
---
Forgot about min(id) as id
learning
"""

from dsa.sql import SQLDrill


# mu 0.5
# extends SQLDrill
#
# def query() -> str
#   return '\n\n     select min(id) as id, email from Person group by email;  '

class Solution(SQLDrill):
    def query(self) -> str:
        return '\n\n     select min(id) as id, email from Person group by email;  '


EXAMPLE_1 = "\nCREATE TABLE Person (id INTEGER, email TEXT);\nINSERT INTO Person VALUES (1, 'john@example.com');\nINSERT INTO Person VALUES (2, 'bob@example.com');\nINSERT INTO Person VALUES (3, 'john@example.com');\n"
EXAMPLE_2 = "\nCREATE TABLE Person (id INTEGER, email TEXT);\nINSERT INTO Person VALUES (7, 'a@x.com');\nINSERT INTO Person VALUES (4, 'a@x.com');\nINSERT INTO Person VALUES (9, 'a@x.com');\n"
sol = Solution()
sol.show(EXAMPLE_1)
assert sol.run(EXAMPLE_1) == [(1, 'john@example.com'), (2, 'bob@example.com')]
assert sol.run(EXAMPLE_2) == [(4, 'a@x.com')]
