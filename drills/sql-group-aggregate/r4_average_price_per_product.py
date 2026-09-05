"""
DRILL: Average Price Per Product
TRAINS: sql-group-aggregate

Given the table `Sales`, return each `product_id` with `average_price`: the
sum of `price` times `units` divided by the sum of `units`, rounded to 2
decimal places. No ordering required.

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
+------------+---------------+
| product_id | average_price |
+------------+---------------+
| 1          | 6.96          |
| 2          | 16.96         |
+------------+---------------+
Explanation: Product 1: 800 / 115 = 6.956..., rounded to 6.96. Product 2: 3900 / 230 = 16.956..., rounded to 16.96.

Example 2:

Input:
Sales table:
+---------+------------+-------+-------+
| sale_id | product_id | price | units |
+---------+------------+-------+-------+
| 9       | 4          | 7     | 3     |
| 10      | 4          | 8     | 1     |
+---------+------------+-------+-------+
Output:
+------------+---------------+
| product_id | average_price |
+------------+---------------+
| 4          | 7.25          |
+------------+---------------+
Explanation: (7 * 3 + 8 * 1) / 4 = 29 / 4 = 7.25.

Constraints:

    1 <= number of rows <= 10^4
    price and units are integers.

    REQUIRED: the division is a real division. sqlite truncates an integer
    divided by an integer (800 / 115 is 6); the query must not.

    FORBIDDEN: avg(price); Python.

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
INSERT INTO Sales VALUES (10, 4, 8, 1);
"""


sol = Solution()

sol.show(EXAMPLE_1)

# assert sol.run(EXAMPLE_1) == [(1, 6.96), (2, 16.96)]
# assert sol.run(EXAMPLE_2) == [(4, 7.25)]
