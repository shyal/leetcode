"""
DRILL: Sales With Product Names
TRAINS: sql-join-inner

Given the tables Sales and Product, return product_name, year and price for
every sale. Order by sale_id.

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
+---------+------------+------+----------+-------+
| sale_id | product_id | year | quantity | price |
+---------+------------+------+----------+-------+
| 1       | 100        | 2008 | 10       | 5000  |
| 2       | 100        | 2009 | 12       | 5000  |
| 7       | 200        | 2011 | 15       | 9000  |
+---------+------------+------+----------+-------+
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
+---------+------------+------+----------+-------+
| sale_id | product_id | year | quantity | price |
+---------+------------+------+----------+-------+
| 1       | 100        | 2008 | 10       | 5000  |
| 2       | 999        | 2009 | 1        | 10    |
+---------+------------+------+----------+-------+
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

    REQUIRED: join the two tables on product_id. Listing both tables without a
    join condition (a cross join filtered afterwards, or not at all) is the
    failure mode this drill exists to kill.

    Runner: sqlite3 in memory. Write portable SQL: CASE not IF, COALESCE,
    || for concatenation, strftime()/julianday()/date() for dates.
"""

import sqlite3

EXAMPLE_1 = """
CREATE TABLE Sales (sale_id INTEGER, product_id INTEGER, year INTEGER, quantity INTEGER, price INTEGER);
INSERT INTO Sales VALUES (1, 100, 2008, 10, 5000);
INSERT INTO Sales VALUES (2, 100, 2009, 12, 5000);
INSERT INTO Sales VALUES (7, 200, 2011, 15, 9000);
CREATE TABLE Product (product_id INTEGER, product_name TEXT);
INSERT INTO Product VALUES (100, 'Nokia');
INSERT INTO Product VALUES (200, 'Apple');
INSERT INTO Product VALUES (300, 'Samsung');
"""

EXAMPLE_2 = """
CREATE TABLE Sales (sale_id INTEGER, product_id INTEGER, year INTEGER, quantity INTEGER, price INTEGER);
INSERT INTO Sales VALUES (1, 100, 2008, 10, 5000);
INSERT INTO Sales VALUES (2, 999, 2009, 1, 10);
CREATE TABLE Product (product_id INTEGER, product_name TEXT);
INSERT INTO Product VALUES (100, 'Nokia');
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

print(run(EXAMPLE_1, sol.query()))  # [('Nokia', 2008, 5000), ('Nokia', 2009, 5000), ('Apple', 2011, 9000)]

# assert run(EXAMPLE_1, sol.query()) == [('Nokia', 2008, 5000), ('Nokia', 2009, 5000), ('Apple', 2011, 9000)]
# assert run(EXAMPLE_2, sol.query()) == [('Nokia', 2008, 5000)]
