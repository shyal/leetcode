"""
DRILL: Revenue Per Product

Given the table `Sales`, return each `product_id` with its `revenue`: the sum
over its sales of `price` times `units`. No ordering required.

Table: Sales

    +-------------+---------+
    | Column Name | Type    |
    +-------------+---------+
    | sale_id     | int     |
    | product_id  | int     |
    | price       | int     |
    | units       | int     |
    +-------------+---------+
    sale_id is the primary key. price is the unit price of that sale.

Example 1:

Input:
Sales table:
+---------+------------+-------+-------+
| sale_id | product_id | price | units |
+---------+------------+-------+-------+
| 1       | 1          | 5     | 100   |
| 2       | 1          | 20    | 15    |
| 3       | 2          | 15    | 200   |
| 4       | 2          | 30    | 30    |
+---------+------------+-------+-------+
Output:
+------------+---------+
| product_id | revenue |
+------------+---------+
| 1          | 800     |
| 2          | 3900    |
+------------+---------+
Explanation: Product 1: 5 * 100 + 20 * 15 = 800. Product 2: 15 * 200 + 30 * 30 = 3900.

Example 2:

Input:
Sales table:
+---------+------------+-------+-------+
| sale_id | product_id | price | units |
+---------+------------+-------+-------+
| 9       | 4          | 7     | 3     |
+---------+------------+-------+-------+
Output:
+------------+---------+
| product_id | revenue |
+------------+---------+
| 4          | 21      |
+------------+---------+
Explanation: One sale: 7 * 3.

Constraints:

    1 <= number of rows <= 10^4

    REQUIRED: one query, one aggregate; the product is formed per row before
    it is summed.

    FORBIDDEN: sum(price) * sum(units); Python.

    Runner: sqlite3 in memory. Write portable SQL: CASE not IF, COALESCE,
    || for concatenation, strftime()/julianday()/date() for dates.
"""

from dsa.sql import SQLDrill


# mu 0.10
# class Solution extends SQLDrill
#   def query() -> str
#     """
#     select
#       product_id,
#       sum(price * units) as revenue
#     from Sales
#     group by product_id
#     """

class Solution(SQLDrill):
    def query(self) -> str:
        return """
    select
      product_id,
      sum(price * units) as revenue
    from Sales
    group by product_id
    """


EXAMPLE_1 = '\nCREATE TABLE Sales (sale_id INTEGER, product_id INTEGER, price INTEGER, units INTEGER);\nINSERT INTO Sales VALUES (1, 1, 5, 100);\nINSERT INTO Sales VALUES (2, 1, 20, 15);\nINSERT INTO Sales VALUES (3, 2, 15, 200);\nINSERT INTO Sales VALUES (4, 2, 30, 30);\n'
EXAMPLE_2 = '\nCREATE TABLE Sales (sale_id INTEGER, product_id INTEGER, price INTEGER, units INTEGER);\nINSERT INTO Sales VALUES (9, 4, 7, 3);\n'
sol = Solution()
sol.show(EXAMPLE_1)
_l, _r = sol.run(EXAMPLE_1), [(1, 800), (2, 3900)]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.run(EXAMPLE_2), [(4, 21)]
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
