"""
DRILL: Not Referred By Customer Two

Given the table `Customer`, return the `name` of every customer who was not
referred by the customer with `id` 2. A customer with no referee counts as
not referred by 2. No ordering required.

Table: Customer

    +-------------+---------+
    | Column Name | Type    |
    +-------------+---------+
    | id          | int     |
    | name        | varchar |
    | referee_id  | int     |
    +-------------+---------+
    id is the primary key. referee_id is NULL when nobody referred the customer.

Example 1:

Input:
Customer table:
+----+------+------------+
| id | name | referee_id |
+----+------+------------+
| 1  | Will | null       |
| 2  | Jane | null       |
| 3  | Alex | 2          |
| 4  | Bill | null       |
| 5  | Zack | 1          |
| 6  | Mark | 2          |
+----+------+------------+
Output:
+------+
| name |
+------+
| Will |
| Jane |
| Bill |
| Zack |
+------+
Explanation: Alex and Mark were referred by 2. Will, Jane and Bill have no referee and must still appear.

Example 2:

Input:
Customer table:
+----+------+------------+
| id | name | referee_id |
+----+------+------------+
| 1  | Ann  | null       |
| 2  | Ben  | null       |
+----+------+------------+
Output:
+------+
| name |
+------+
| Ann  |
| Ben  |
+------+
Explanation: Nobody has a referee, so everyone is returned.

Constraints:

    1 <= number of rows <= 10^4

    REQUIRED: rows with a NULL referee_id appear in the result.

    FORBIDDEN: a bare inequality against referee_id on its own (NULL
    compared with anything is neither true nor false, so those rows silently
    vanish).

    Runner: sqlite3 in memory. Write portable SQL: CASE not IF, COALESCE,
    || for concatenation, strftime()/julianday()/date() for dates.
"""

from dsa.sql import SQLDrill


# mu 0.7
# extends SQLDrill
#
# def query() -> str
#   """
#   select
#     name
#   from Customer
#   where referee_id is not 2
#   ;
#   """

class Solution(SQLDrill):
    def query(self) -> str:
        return """
  select
    name
  from Customer
  where referee_id is not 2
  ;
  """


EXAMPLE_1 = "\nCREATE TABLE Customer (id INTEGER, name TEXT, referee_id INTEGER);\nINSERT INTO Customer VALUES (1, 'Will', NULL);\nINSERT INTO Customer VALUES (2, 'Jane', NULL);\nINSERT INTO Customer VALUES (3, 'Alex', 2);\nINSERT INTO Customer VALUES (4, 'Bill', NULL);\nINSERT INTO Customer VALUES (5, 'Zack', 1);\nINSERT INTO Customer VALUES (6, 'Mark', 2);\n"
EXAMPLE_2 = "\nCREATE TABLE Customer (id INTEGER, name TEXT, referee_id INTEGER);\nINSERT INTO Customer VALUES (1, 'Ann', NULL);\nINSERT INTO Customer VALUES (2, 'Ben', NULL);\n"
sol = Solution()
sol.show(EXAMPLE_1)
_l, _r = sol.run(EXAMPLE_1), [('Bill',), ('Jane',), ('Will',), ('Zack',)]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.run(EXAMPLE_2), [('Ann',), ('Ben',)]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
