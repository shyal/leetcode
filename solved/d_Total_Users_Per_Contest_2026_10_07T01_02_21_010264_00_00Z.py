"""
DRILL: Total Users Per Contest

Given the tables `Users` and `Register`, return one row per `contest_id`
with `total_users`: the number of rows in `Users`. The value is the same on
every row. No ordering required.

Table: Users

    +-------------+------+
    | Column Name | Type |
    +-------------+------+
    | user_id     | int  |
    +-------------+------+
    user_id is the primary key.

Table: Register

    +-------------+------+
    | Column Name | Type |
    +-------------+------+
    | contest_id  | int  |
    | user_id     | int  |
    +-------------+------+
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
| 209        | 7       |
+------------+---------+
Output:
+------------+-------------+
| contest_id | total_users |
+------------+-------------+
| 209        | 3           |
| 215        | 3           |
+------------+-------------+
Explanation: Two contests; Users has 3 rows, so both show 3.

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
+------------+-------------+
| contest_id | total_users |
+------------+-------------+
| 100        | 4           |
+------------+-------------+
Explanation: Only one user registered, but total_users counts all 4 users.

Constraints:

    1 <= number of rows in each table <= 10^4

    REQUIRED: one query, one row per contest; the user count comes from
    Users at run time.

    FORBIDDEN: a hard-coded count; joining Users into the grouped query (its
    row count is the registrations, not the users).

    Runner: sqlite3 in memory. Write portable SQL: CASE not IF, COALESCE,
    || for concatenation, strftime()/julianday()/date() for dates.
---
Learning
"""

from dsa.sql import SQLDrill


# mu 0.7
# extends SQLDrill
#
# def query() -> str
#   return """
#     select
#       contest_id,
#       (select count(*) from Users) as total_users
#     from Register
#     ;
#   """

class Solution(SQLDrill):
    def query(self) -> str:
        return """
    select
      contest_id,
      (select count(*) from Users) as total_users
    from Register
    ;
  """


EXAMPLE_1 = '\nCREATE TABLE Users (user_id INTEGER);\nINSERT INTO Users VALUES (6);\nINSERT INTO Users VALUES (2);\nINSERT INTO Users VALUES (7);\nCREATE TABLE Register (contest_id INTEGER, user_id INTEGER);\nINSERT INTO Register VALUES (215, 6);\nINSERT INTO Register VALUES (209, 2);\nINSERT INTO Register VALUES (209, 7);\n'
EXAMPLE_2 = '\nCREATE TABLE Users (user_id INTEGER);\nINSERT INTO Users VALUES (1);\nINSERT INTO Users VALUES (2);\nINSERT INTO Users VALUES (3);\nINSERT INTO Users VALUES (4);\nCREATE TABLE Register (contest_id INTEGER, user_id INTEGER);\nINSERT INTO Register VALUES (100, 1);\n'
sol = Solution()
sol.show(EXAMPLE_1)
