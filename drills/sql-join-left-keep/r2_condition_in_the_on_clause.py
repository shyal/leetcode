"""
DRILL: Average Selling Price With Date Ranges
TRAINS: sql-join-left-keep

Given the tables Prices and UnitsSold, return the average selling price of
each product, rounded to 2 decimal places: total money taken divided by total
units, where each unit is priced by the range its purchase_date falls in. A
product with no units sold has an average price of 0. Order by product_id.

Table: Prices

    +-------------+---------+
    | Column Name | Type    |
    +-------------+---------+
    | product_id  | int     |
    | start_date  | date    |
    | end_date    | date    |
    | price       | int     |
    +-------------+---------+
    (product_id, start_date, end_date) is the primary key. Ranges of one product do not overlap.

    Table: UnitsSold

    +---------------+---------+
    | Column Name   | Type    |
    +---------------+---------+
    | product_id    | int     |
    | purchase_date | date    |
    | units         | int     |
    +---------------+---------+
    Every purchase_date falls inside one of the product's ranges.

Example 1:

Input:
Prices table:
+------------+------------+------------+-------+
| product_id | start_date | end_date   | price |
+------------+------------+------------+-------+
| 1          | 2019-02-17 | 2019-02-28 | 5     |
| 1          | 2019-03-01 | 2019-03-22 | 20    |
| 2          | 2019-02-01 | 2019-02-20 | 15    |
| 2          | 2019-02-21 | 2019-03-31 | 30    |
| 3          | 2019-01-01 | 2019-12-31 | 9     |
+------------+------------+------------+-------+
UnitsSold table:
+------------+---------------+-------+
| product_id | purchase_date | units |
+------------+---------------+-------+
| 1          | 2019-02-25    | 100   |
| 1          | 2019-03-01    | 15    |
| 2          | 2019-02-10    | 200   |
| 2          | 2019-03-22    | 30    |
+------------+---------------+-------+
Output:
+------------+---------------+
| product_id | average_price |
+------------+---------------+
| 1          | 6.96          |
| 2          | 16.96         |
| 3          | 0             |
+------------+---------------+
Explanation: Product 1: (5 * 100 + 20 * 15) / 115 = 6.96. Product 2: (15 * 200 + 30 * 30) / 230 = 16.96. Product 3 sold nothing: 0.

Example 2:

Input:
Prices table:
+------------+------------+------------+-------+
| product_id | start_date | end_date   | price |
+------------+------------+------------+-------+
| 1          | 2020-01-01 | 2020-12-31 | 10    |
+------------+------------+------------+-------+
UnitsSold table:
+------------+---------------+-------+
| product_id | purchase_date | units |
+------------+---------------+-------+
+------------+---------------+-------+
Output:
+------------+---------------+
| product_id | average_price |
+------------+---------------+
| 1          | 0             |
+------------+---------------+
Explanation: No sales at all, so the only product averages 0.

Constraints:

    1 <= rows in Prices <= 10^4
    0 <= rows in UnitsSold <= 10^4
    price and units are integers; divide as a real number.

    REQUIRED: the date-range condition belongs in the ON clause of a LEFT
    JOIN. Putting it in WHERE turns the LEFT JOIN into an inner join and drops
    products with no sales; that is the failure mode this drill exists to
    kill.

    Runner: sqlite3 in memory. Write portable SQL: CASE not IF, COALESCE,
    || for concatenation, strftime()/julianday()/date() for dates.
"""

import sqlite3

EXAMPLE_1 = """
CREATE TABLE Prices (product_id INTEGER, start_date TEXT, end_date TEXT, price INTEGER);
INSERT INTO Prices VALUES (1, '2019-02-17', '2019-02-28', 5);
INSERT INTO Prices VALUES (1, '2019-03-01', '2019-03-22', 20);
INSERT INTO Prices VALUES (2, '2019-02-01', '2019-02-20', 15);
INSERT INTO Prices VALUES (2, '2019-02-21', '2019-03-31', 30);
INSERT INTO Prices VALUES (3, '2019-01-01', '2019-12-31', 9);
CREATE TABLE UnitsSold (product_id INTEGER, purchase_date TEXT, units INTEGER);
INSERT INTO UnitsSold VALUES (1, '2019-02-25', 100);
INSERT INTO UnitsSold VALUES (1, '2019-03-01', 15);
INSERT INTO UnitsSold VALUES (2, '2019-02-10', 200);
INSERT INTO UnitsSold VALUES (2, '2019-03-22', 30);
"""

EXAMPLE_2 = """
CREATE TABLE Prices (product_id INTEGER, start_date TEXT, end_date TEXT, price INTEGER);
INSERT INTO Prices VALUES (1, '2020-01-01', '2020-12-31', 10);
CREATE TABLE UnitsSold (product_id INTEGER, purchase_date TEXT, units INTEGER);
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

print(run(EXAMPLE_1, sol.query()))  # [(1, 6.96), (2, 16.96), (3, 0)]

# assert run(EXAMPLE_1, sol.query()) == [(1, 6.96), (2, 16.96), (3, 0)]
# assert run(EXAMPLE_2, sol.query()) == [(1, 0)]
