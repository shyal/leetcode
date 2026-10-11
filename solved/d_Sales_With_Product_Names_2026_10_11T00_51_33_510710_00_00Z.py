"""
DRILL: Sales With Product Names

Given the tables `Sales` and `Product`, return `product_name`, `year` and
`price` for every sale. No ordering required.

Table: Sales

    +-------------+-------+
    | Column Name | Type  |
    +-------------+-------+
    | sale_id     | int   |
    | product_id  | int   |
    | year        | int   |
    | price       | int   |
    +-------------+-------+
    (sale_id, year) is the primary key. product_id refers to Product.

    Table: Product

    +--------------+---------+
    | Column Name  | Type    |
    +--------------+---------+
    | product_id   | int     |
    | product_name | varchar |
    +--------------+---------+
    product_id is the primary key.

Example 1:

Input:
Sales table:
+---------+------------+------+-------+
| sale_id | product_id | year | price |
+---------+------------+------+-------+
| 1       | 100        | 2008 | 5000  |
| 2       | 100        | 2009 | 5000  |
| 7       | 200        | 2011 | 9000  |
+---------+------------+------+-------+
Product table:
+------------+--------------+
| product_id | product_name |
+------------+--------------+
| 100        | Nokia        |
| 200        | Apple        |
| 300        | Samsung      |
+------------+--------------+
Output:
+--------------+------+-------+
| product_name | year | price |
+--------------+------+-------+
| Nokia        | 2008 | 5000  |
| Nokia        | 2009 | 5000  |
| Apple        | 2011 | 9000  |
+--------------+------+-------+
Explanation: Samsung has no sales and does not appear.

Example 2:

Input:
Sales table:
+---------+------------+------+-------+
| sale_id | product_id | year | price |
+---------+------------+------+-------+
| 1       | 100        | 2008 | 5000  |
| 2       | 999        | 2009 | 10    |
+---------+------------+------+-------+
Product table:
+------------+--------------+
| product_id | product_name |
+------------+--------------+
| 100        | Nokia        |
+------------+--------------+
Output:
+--------------+------+-------+
| product_name | year | price |
+--------------+------+-------+
| Nokia        | 2008 | 5000  |
+--------------+------+-------+
Explanation: Sale 2 refers to a product that does not exist, so it does not appear either.

Constraints:

    1 <= rows in each table <= 10^4

    REQUIRED: the two tables are joined on product_id.

    FORBIDDEN: listing both tables without a join condition (a cross join,
    filtered afterwards or not at all).

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
#     p.product_name,
#     s.year,
#     s.price
#   from Sales as s
#   join Product as p on p.product_id = s.product_id
#   ;
#   """

class Solution(SQLDrill):
    def query(self) -> str:
        return """
  select
    p.product_name,
    s.year,
    s.price
  from Sales as s
  join Product as p on p.product_id = s.product_id
  ;
  """


EXAMPLE_1 = "\nCREATE TABLE Sales (sale_id INTEGER, product_id INTEGER, year INTEGER, price INTEGER);\nINSERT INTO Sales VALUES (1, 100, 2008, 5000);\nINSERT INTO Sales VALUES (2, 100, 2009, 5000);\nINSERT INTO Sales VALUES (7, 200, 2011, 9000);\nCREATE TABLE Product (product_id INTEGER, product_name TEXT);\nINSERT INTO Product VALUES (100, 'Nokia');\nINSERT INTO Product VALUES (200, 'Apple');\nINSERT INTO Product VALUES (300, 'Samsung');\n"
EXAMPLE_2 = "\nCREATE TABLE Sales (sale_id INTEGER, product_id INTEGER, year INTEGER, price INTEGER);\nINSERT INTO Sales VALUES (1, 100, 2008, 5000);\nINSERT INTO Sales VALUES (2, 999, 2009, 10);\nCREATE TABLE Product (product_id INTEGER, product_name TEXT);\nINSERT INTO Product VALUES (100, 'Nokia');\n"
sol = Solution()
sol.show(EXAMPLE_1)
_l, _r = sol.run(EXAMPLE_1), [('Apple', 2011, 9000), ('Nokia', 2008, 5000), ('Nokia', 2009, 5000)]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.run(EXAMPLE_2), [('Nokia', 2008, 5000)]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
