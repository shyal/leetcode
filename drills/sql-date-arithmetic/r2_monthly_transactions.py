"""
DRILL: Monthly Transactions
TRAINS: sql-date-arithmetic

Given the table Transactions, return for each month and country: trans_count,
approved_count, trans_total_amount and approved_total_amount. month is the
year and month as 'YYYY-MM'. Any row order.

Table: Transactions

    +-------------+---------+
    | Column Name | Type    |
    +-------------+---------+
    | id          | int     |
    | country     | varchar |
    | state       | varchar |
    | amount      | int     |
    | trans_date  | date    |
    +-------------+---------+
    id is the primary key. state is 'approved' or 'declined'.

Example 1:

Input:
Transactions table:
+-----+---------+----------+--------+------------+
| id  | country | state    | amount | trans_date |
+-----+---------+----------+--------+------------+
| 121 | US      | approved | 1000   | 2018-12-18 |
| 122 | US      | declined | 2000   | 2018-12-19 |
| 123 | US      | approved | 2000   | 2019-01-01 |
| 124 | DE      | approved | 2000   | 2019-01-07 |
+-----+---------+----------+--------+------------+
Output:
+---------+---------+-------------+----------------+--------------------+-----------------------+
| month   | country | trans_count | approved_count | trans_total_amount | approved_total_amount |
+---------+---------+-------------+----------------+--------------------+-----------------------+
| 2018-12 | US      | 2           | 1              | 3000               | 1000                  |
| 2019-01 | DE      | 1           | 1              | 2000               | 2000                  |
| 2019-01 | US      | 1           | 1              | 2000               | 2000                  |
+---------+---------+-------------+----------------+--------------------+-----------------------+
Explanation: December 2018 has two US transactions (one approved); January 2019 has one in each country.

Example 2:

Input:
Transactions table:
+----+---------+----------+--------+------------+
| id | country | state    | amount | trans_date |
+----+---------+----------+--------+------------+
| 1  | FR      | declined | 300    | 2020-02-01 |
| 2  | FR      | approved | 400    | 2020-02-29 |
+----+---------+----------+--------+------------+
Output:
+---------+---------+-------------+----------------+--------------------+-----------------------+
| month   | country | trans_count | approved_count | trans_total_amount | approved_total_amount |
+---------+---------+-------------+----------------+--------------------+-----------------------+
| 2020-02 | FR      | 2           | 1              | 700                | 400                   |
+---------+---------+-------------+----------------+--------------------+-----------------------+
Explanation: Both rows fall in 2020-02.

Constraints:

    1 <= number of rows <= 10^4

    REQUIRED: group on a month bucket derived from the date: strftime('%Y-%m',
    trans_date) in sqlite, DATE_FORMAT in MySQL, date_trunc in Postgres and
    Presto. Grouping on the raw date, or building the bucket in Python, is the
    failure mode this drill exists to kill.

    Runner: sqlite3 in memory. Write portable SQL: CASE not IF, COALESCE,
    || for concatenation, strftime()/julianday()/date() for dates.
"""

from dsa.sql import SQLDrill


class Solution(SQLDrill):

    def query(self) -> str:
        return """

        """


EXAMPLE_1 = """
CREATE TABLE Transactions (id INTEGER, country TEXT, state TEXT, amount INTEGER, trans_date TEXT);
INSERT INTO Transactions VALUES (121, 'US', 'approved', 1000, '2018-12-18');
INSERT INTO Transactions VALUES (122, 'US', 'declined', 2000, '2018-12-19');
INSERT INTO Transactions VALUES (123, 'US', 'approved', 2000, '2019-01-01');
INSERT INTO Transactions VALUES (124, 'DE', 'approved', 2000, '2019-01-07');
"""

EXAMPLE_2 = """
CREATE TABLE Transactions (id INTEGER, country TEXT, state TEXT, amount INTEGER, trans_date TEXT);
INSERT INTO Transactions VALUES (1, 'FR', 'declined', 300, '2020-02-01');
INSERT INTO Transactions VALUES (2, 'FR', 'approved', 400, '2020-02-29');
"""


sol = Solution()

sol.show(EXAMPLE_1)

# assert sol.run(EXAMPLE_1) == [('2018-12', 'US', 2, 1, 3000, 1000), ('2019-01', 'DE', 1, 1, 2000, 2000), ('2019-01', 'US', 1, 1, 2000, 2000)]
# assert sol.run(EXAMPLE_2) == [('2020-02', 'FR', 2, 1, 700, 400)]
