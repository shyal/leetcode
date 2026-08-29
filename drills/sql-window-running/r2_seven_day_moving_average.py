"""
DRILL: Seven Day Moving Average
TRAINS: sql-window-running

Given the table Customer, return for every day that has six earlier days of
data: visited_on, amount (the total paid over that day and the six days before
it) and average_amount (that total divided by 7, rounded to 2 decimal places).
There is at least one customer every day. Order by visited_on.

Table: Customer

    +---------------+---------+
    | Column Name   | Type    |
    +---------------+---------+
    | customer_id   | int     |
    | name          | varchar |
    | visited_on    | date    |
    | amount        | int     |
    +---------------+---------+
    (customer_id, visited_on) is the primary key. Several customers can visit on one day.

Example 1:

Input:
Customer table:
+-------------+--------+------------+--------+
| customer_id | name   | visited_on | amount |
+-------------+--------+------------+--------+
| 1           | Jhon   | 2019-01-01 | 100    |
| 2           | Daniel | 2019-01-02 | 110    |
| 3           | Jade   | 2019-01-03 | 120    |
| 1           | Jhon   | 2019-01-04 | 130    |
| 2           | Daniel | 2019-01-05 | 110    |
| 3           | Jade   | 2019-01-06 | 140    |
| 1           | Jhon   | 2019-01-07 | 150    |
| 2           | Daniel | 2019-01-08 | 80     |
| 3           | Jade   | 2019-01-09 | 110    |
| 1           | Jhon   | 2019-01-10 | 130    |
| 3           | Jade   | 2019-01-10 | 150    |
+-------------+--------+------------+--------+
Output:
+------------+--------+----------------+
| visited_on | amount | average_amount |
+------------+--------+----------------+
| 2019-01-07 | 860    | 122.86         |
| 2019-01-08 | 840    | 120.0          |
| 2019-01-09 | 840    | 120.0          |
| 2019-01-10 | 1000   | 142.86         |
+------------+--------+----------------+
Explanation: The first full window ends on 2019-01-07. 2019-01-10 has two visits, 130 and 150, counted as one day of 280.

Example 2:

Input:
Customer table:
+-------------+------+------------+--------+
| customer_id | name | visited_on | amount |
+-------------+------+------------+--------+
| 1           | Ann  | 2020-03-01 | 10     |
| 1           | Ann  | 2020-03-02 | 10     |
| 1           | Ann  | 2020-03-03 | 10     |
| 1           | Ann  | 2020-03-04 | 10     |
| 1           | Ann  | 2020-03-05 | 10     |
| 1           | Ann  | 2020-03-06 | 10     |
| 1           | Ann  | 2020-03-07 | 10     |
+-------------+------+------------+--------+
Output:
+------------+--------+----------------+
| visited_on | amount | average_amount |
+------------+--------+----------------+
| 2020-03-07 | 70     | 10.0           |
+------------+--------+----------------+
Explanation: Exactly seven days: one row.

Constraints:

    1 <= number of rows <= 10^5

    REQUIRED: aggregate per day first (two visits on one day are one day),
    then a window with an explicit frame: SUM(amount) OVER (ORDER BY
    visited_on ROWS BETWEEN 6 PRECEDING AND CURRENT ROW). The default frame
    runs from the start of the partition, which gives a running total rather
    than a moving one; that is the failure mode this drill exists to kill.
    Rows without six preceding days are excluded.

    Runner: sqlite3 in memory. Write portable SQL: CASE not IF, COALESCE,
    || for concatenation, strftime()/julianday()/date() for dates.
"""

from dsa.sql import SQLDrill

EXAMPLE_1 = """
CREATE TABLE Customer (customer_id INTEGER, name TEXT, visited_on TEXT, amount INTEGER);
INSERT INTO Customer VALUES (1, 'Jhon', '2019-01-01', 100);
INSERT INTO Customer VALUES (2, 'Daniel', '2019-01-02', 110);
INSERT INTO Customer VALUES (3, 'Jade', '2019-01-03', 120);
INSERT INTO Customer VALUES (1, 'Jhon', '2019-01-04', 130);
INSERT INTO Customer VALUES (2, 'Daniel', '2019-01-05', 110);
INSERT INTO Customer VALUES (3, 'Jade', '2019-01-06', 140);
INSERT INTO Customer VALUES (1, 'Jhon', '2019-01-07', 150);
INSERT INTO Customer VALUES (2, 'Daniel', '2019-01-08', 80);
INSERT INTO Customer VALUES (3, 'Jade', '2019-01-09', 110);
INSERT INTO Customer VALUES (1, 'Jhon', '2019-01-10', 130);
INSERT INTO Customer VALUES (3, 'Jade', '2019-01-10', 150);
"""

EXAMPLE_2 = """
CREATE TABLE Customer (customer_id INTEGER, name TEXT, visited_on TEXT, amount INTEGER);
INSERT INTO Customer VALUES (1, 'Ann', '2020-03-01', 10);
INSERT INTO Customer VALUES (1, 'Ann', '2020-03-02', 10);
INSERT INTO Customer VALUES (1, 'Ann', '2020-03-03', 10);
INSERT INTO Customer VALUES (1, 'Ann', '2020-03-04', 10);
INSERT INTO Customer VALUES (1, 'Ann', '2020-03-05', 10);
INSERT INTO Customer VALUES (1, 'Ann', '2020-03-06', 10);
INSERT INTO Customer VALUES (1, 'Ann', '2020-03-07', 10);
"""


class Solution(SQLDrill):

    def query(self) -> str:
        return """

        """


sol = Solution()

sol.show(EXAMPLE_1)

# assert sol.run(EXAMPLE_1) == [('2019-01-07', 860, 122.86), ('2019-01-08', 840, 120.0), ('2019-01-09', 840, 120.0), ('2019-01-10', 1000, 142.86)]
# assert sol.run(EXAMPLE_2) == [('2020-03-07', 70, 10.0)]
