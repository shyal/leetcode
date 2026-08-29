"""
DRILL: Paid Orders Per Customer
TRAINS: sql-join-left-keep, sql-group-aggregate

Given the tables Customers and Orders, return name and paid_orders for every
customer: the number of that customer's orders whose status is 'paid'. A
customer with no paid order shows 0. Any row order.

Table: Customers

    +-------------+---------+
    | Column Name | Type    |
    +-------------+---------+
    | id          | int     |
    | name        | varchar |
    +-------------+---------+
    id is the primary key.

Table: Orders

    +-------------+---------+
    | Column Name | Type    |
    +-------------+---------+
    | customer_id | int     |
    | status      | varchar |
    +-------------+---------+
    One row per order. customer_id refers to Customers.id. status is 'paid' or 'open'.

Example 1:

Input:
Customers table:
+----+-------+
| id | name  |
+----+-------+
| 1  | Ann   |
| 2  | Bob   |
| 3  | Cal   |
+----+-------+
Orders table:
+-------------+--------+
| customer_id | status |
+-------------+--------+
| 1           | paid   |
| 1           | open   |
| 1           | paid   |
| 2           | open   |
+-------------+--------+
Output:
+------+-------------+
| name | paid_orders |
+------+-------------+
| Ann  | 2           |
| Bob  | 0           |
| Cal  | 0           |
+------+-------------+
Explanation: Bob has one order but it is open; Cal has no orders. Both show 0.

Example 2:

Input:
Customers table:
+----+------+
| id | name |
+----+------+
| 5  | Dee  |
+----+------+
Orders table:
+-------------+--------+
| customer_id | status |
+-------------+--------+
| 5           | paid   |
+-------------+--------+
Output:
+------+-------------+
| name | paid_orders |
+------+-------------+
| Dee  | 1           |
+------+-------------+
Explanation: One customer, one paid order.

Constraints:

    1 <= number of rows in each table <= 10^4

    REQUIRED: every customer appears exactly once, and the status test must
    NOT be in the WHERE clause. A WHERE status = 'paid' drops Bob and Cal
    from the result; that is the failure mode this drill exists to kill.

    Runner: sqlite3 in memory. Write portable SQL: CASE not IF, COALESCE,
    || for concatenation, strftime()/julianday()/date() for dates.
"""

from dsa.sql import SQLDrill


class Solution(SQLDrill):

    def query(self) -> str:
        return """

        """


EXAMPLE_1 = """
CREATE TABLE Customers (id INTEGER, name TEXT);
INSERT INTO Customers VALUES (1, 'Ann');
INSERT INTO Customers VALUES (2, 'Bob');
INSERT INTO Customers VALUES (3, 'Cal');
CREATE TABLE Orders (customer_id INTEGER, status TEXT);
INSERT INTO Orders VALUES (1, 'paid');
INSERT INTO Orders VALUES (1, 'open');
INSERT INTO Orders VALUES (1, 'paid');
INSERT INTO Orders VALUES (2, 'open');
"""

EXAMPLE_2 = """
CREATE TABLE Customers (id INTEGER, name TEXT);
INSERT INTO Customers VALUES (5, 'Dee');
CREATE TABLE Orders (customer_id INTEGER, status TEXT);
INSERT INTO Orders VALUES (5, 'paid');
"""


sol = Solution()

sol.show(EXAMPLE_1)

# assert sol.run(EXAMPLE_1) == [('Ann', 2), ('Bob', 0), ('Cal', 0)]
# assert sol.run(EXAMPLE_2) == [('Dee', 1)]
