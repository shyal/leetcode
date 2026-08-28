"""
DRILL: Sales In Each Product's First Year
TRAINS: sql-subquery

Given the table Sales, return product_id, first_year, quantity and price for
every sale that happened in the first year its product was sold. Order by
product_id, then sale_id.

Table: Sales

    +-------------+-------+
    | Column Name | Type  |
    +-------------+-------+
    | sale_id     | int   |
    | product_id  | int   |
    | year        | int   |
    | quantity    | int   |
    | price       | int   |
    +-------------+-------+
    (sale_id, year) is the primary key.

Example 1:

Input:
Sales table:
+---------+------------+------+----------+-------+
| sale_id | product_id | year | quantity | price |
+---------+------------+------+----------+-------+
| 1       | 100        | 2008 | 10       | 5000  |
| 2       | 100        | 2009 | 12       | 5000  |
| 7       | 200        | 2011 | 15       | 9000  |
+---------+------------+------+----------+-------+
Output:
+------------+------------+----------+-------+
| product_id | first_year | quantity | price |
+------------+------------+----------+-------+
| 100        | 2008       | 10       | 5000  |
| 200        | 2011       | 15       | 9000  |
+------------+------------+----------+-------+
Explanation: Product 100 was first sold in 2008, product 200 in 2011.

Example 2:

Input:
Sales table:
+---------+------------+------+----------+-------+
| sale_id | product_id | year | quantity | price |
+---------+------------+------+----------+-------+
| 1       | 300        | 2012 | 3        | 10    |
| 2       | 300        | 2012 | 4        | 12    |
| 3       | 300        | 2013 | 5        | 14    |
+---------+------------+------+----------+-------+
Output:
+------------+------------+----------+-------+
| product_id | first_year | quantity | price |
+------------+------------+----------+-------+
| 300        | 2012       | 3        | 10    |
| 300        | 2012       | 4        | 12    |
+------------+------------+----------+-------+
Explanation: Two sales in the first year, both returned.

Constraints:

    1 <= number of rows <= 10^4

    REQUIRED: filter with (product_id, year) IN (SELECT product_id, MIN(year)
    FROM Sales GROUP BY product_id), or an equivalent join on that grouped
    subquery. Filtering on the single global MIN(year) is the failure mode
    this drill exists to kill: product 200's first year is 2011, not 2008.

    Runner: sqlite3 in memory. Write portable SQL: CASE not IF, COALESCE,
    || for concatenation, strftime()/julianday()/date() for dates.
"""

import sqlite3

EXAMPLE_1 = """
CREATE TABLE Sales (sale_id INTEGER, product_id INTEGER, year INTEGER, quantity INTEGER, price INTEGER);
INSERT INTO Sales VALUES (1, 100, 2008, 10, 5000);
INSERT INTO Sales VALUES (2, 100, 2009, 12, 5000);
INSERT INTO Sales VALUES (7, 200, 2011, 15, 9000);
"""

EXAMPLE_2 = """
CREATE TABLE Sales (sale_id INTEGER, product_id INTEGER, year INTEGER, quantity INTEGER, price INTEGER);
INSERT INTO Sales VALUES (1, 300, 2012, 3, 10);
INSERT INTO Sales VALUES (2, 300, 2012, 4, 12);
INSERT INTO Sales VALUES (3, 300, 2013, 5, 14);
"""


class Solution:

    def query(self) -> str:
        return """

        """


def run(schema: str, sql: str) -> list[tuple]:
    con = sqlite3.connect(":memory:")
    con.executescript(schema)
    return [tuple(row) for row in con.execute(sql).fetchall()]


sol = Solution()

print(run(EXAMPLE_1, sol.query()))  # [(100, 2008, 10, 5000), (200, 2011, 15, 9000)]

# assert run(EXAMPLE_1, sol.query()) == [(100, 2008, 10, 5000), (200, 2011, 15, 9000)]
# assert run(EXAMPLE_2, sol.query()) == [(300, 2012, 3, 10), (300, 2012, 4, 12)]
