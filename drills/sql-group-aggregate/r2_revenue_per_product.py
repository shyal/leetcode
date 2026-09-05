"""
DRILL: Revenue Per Product
TRAINS: sql-group-aggregate

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


class Solution(SQLDrill):

    def query(self) -> str:
        return """

        """


EXAMPLE_1 = """
CREATE TABLE Sales (sale_id INTEGER, product_id INTEGER, price INTEGER, units INTEGER);
INSERT INTO Sales VALUES (1, 1, 5, 100);
INSERT INTO Sales VALUES (2, 1, 20, 15);
INSERT INTO Sales VALUES (3, 2, 15, 200);
INSERT INTO Sales VALUES (4, 2, 30, 30);
"""

EXAMPLE_2 = """
CREATE TABLE Sales (sale_id INTEGER, product_id INTEGER, price INTEGER, units INTEGER);
INSERT INTO Sales VALUES (9, 4, 7, 3);
"""


sol = Solution()

sol.show(EXAMPLE_1)

# assert sol.run(EXAMPLE_1) == [(1, 800), (2, 3900)]
# assert sol.run(EXAMPLE_2) == [(4, 21)]
