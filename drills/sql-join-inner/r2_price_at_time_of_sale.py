"""
DRILL: Price At Time Of Sale
TRAINS: sql-join-inner

Given the tables `Prices` and `UnitsSold`, return each sale's `product_id`,
`purchase_date` and the `price` in force on that date: the price of the
product's range that `purchase_date` falls in. No ordering required.

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
+------------+---------------+-------+
| product_id | purchase_date | price |
+------------+---------------+-------+
| 1          | 2019-02-25    | 5     |
| 1          | 2019-03-01    | 20    |
| 2          | 2019-02-10    | 15    |
| 2          | 2019-03-22    | 30    |
+------------+---------------+-------+
Explanation: Product 1 has two ranges. The sale on 2019-02-25 falls in the first (price 5), the sale on 2019-03-01 on the first day of the second (price 20).

Example 2:

Input:
Prices table:
+------------+------------+------------+-------+
| product_id | start_date | end_date   | price |
+------------+------------+------------+-------+
| 3          | 2020-01-01 | 2020-06-30 | 9     |
| 3          | 2020-07-01 | 2020-12-31 | 11    |
+------------+------------+------------+-------+
UnitsSold table:
+------------+---------------+-------+
| product_id | purchase_date | units |
+------------+---------------+-------+
| 3          | 2020-06-30    | 4     |
+------------+---------------+-------+
Output:
+------------+---------------+-------+
| product_id | purchase_date | price |
+------------+---------------+-------+
| 3          | 2020-06-30    | 9     |
+------------+---------------+-------+
Explanation: The last day of the first range still takes the first price.

Constraints:

    1 <= rows in Prices <= 10^4
    1 <= rows in UnitsSold <= 10^4

    REQUIRED: one output row per sale; the join matches on the product AND
    on the date falling in the range.

    FORBIDDEN: a join on product_id alone (it pairs each sale with every
    range of its product); Python.

    Runner: sqlite3 in memory. Write portable SQL: CASE not IF, COALESCE,
    || for concatenation, strftime()/julianday()/date() for dates.
"""

from dsa.sql import SQLDrill


class Solution(SQLDrill):

    def query(self) -> str:
        return """

        """


EXAMPLE_1 = """
CREATE TABLE Prices (product_id INTEGER, start_date TEXT, end_date TEXT, price INTEGER);
INSERT INTO Prices VALUES (1, '2019-02-17', '2019-02-28', 5);
INSERT INTO Prices VALUES (1, '2019-03-01', '2019-03-22', 20);
INSERT INTO Prices VALUES (2, '2019-02-01', '2019-02-20', 15);
INSERT INTO Prices VALUES (2, '2019-02-21', '2019-03-31', 30);
CREATE TABLE UnitsSold (product_id INTEGER, purchase_date TEXT, units INTEGER);
INSERT INTO UnitsSold VALUES (1, '2019-02-25', 100);
INSERT INTO UnitsSold VALUES (1, '2019-03-01', 15);
INSERT INTO UnitsSold VALUES (2, '2019-02-10', 200);
INSERT INTO UnitsSold VALUES (2, '2019-03-22', 30);
"""

EXAMPLE_2 = """
CREATE TABLE Prices (product_id INTEGER, start_date TEXT, end_date TEXT, price INTEGER);
INSERT INTO Prices VALUES (3, '2020-01-01', '2020-06-30', 9);
INSERT INTO Prices VALUES (3, '2020-07-01', '2020-12-31', 11);
CREATE TABLE UnitsSold (product_id INTEGER, purchase_date TEXT, units INTEGER);
INSERT INTO UnitsSold VALUES (3, '2020-06-30', 4);
"""


sol = Solution()

sol.show(EXAMPLE_1)

# assert sol.run(EXAMPLE_1) == [(1, '2019-02-25', 5), (1, '2019-03-01', 20), (2, '2019-02-10', 15), (2, '2019-03-22', 30)]
# assert sol.run(EXAMPLE_2) == [(3, '2020-06-30', 9)]
