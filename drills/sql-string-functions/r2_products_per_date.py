"""
DRILL: Products Sold Per Date
TRAINS: sql-string-functions, sql-group-aggregate

Given the table Activities, return for each sell_date: num_sold, the number of
distinct products sold that day, and products, the distinct product names
sorted lexicographically and joined with commas. Any row order.

Table: Activities

    +-------------+---------+
    | Column Name | Type    |
    +-------------+---------+
    | sell_date   | date    |
    | product     | varchar |
    +-------------+---------+
    No primary key; the same product can be sold several times on one date.

Example 1:

Input:
Activities table:
+------------+------------+
| sell_date  | product    |
+------------+------------+
| 2020-05-30 | Headphone  |
| 2020-06-01 | Pencil     |
| 2020-06-02 | Mask       |
| 2020-05-30 | Basketball |
| 2020-06-01 | Bible      |
| 2020-06-02 | Mask       |
| 2020-05-30 | T-Shirt    |
+------------+------------+
Output:
+------------+----------+------------------------------+
| sell_date  | num_sold | products                     |
+------------+----------+------------------------------+
| 2020-05-30 | 3        | Basketball,Headphone,T-Shirt |
| 2020-06-01 | 2        | Bible,Pencil                 |
| 2020-06-02 | 1        | Mask                         |
+------------+----------+------------------------------+
Explanation: Mask was sold twice on 2020-06-02 and is listed once.

Example 2:

Input:
Activities table:
+------------+---------+
| sell_date  | product |
+------------+---------+
| 2021-01-01 | Pen     |
| 2021-01-01 | Pen     |
| 2021-01-01 | Ink     |
+------------+---------+
Output:
+------------+----------+----------+
| sell_date  | num_sold | products |
+------------+----------+----------+
| 2021-01-01 | 2        | Ink,Pen  |
+------------+----------+----------+
Explanation: Pen twice, Ink once: two distinct products, listed in order.

Constraints:

    1 <= number of rows <= 10^4

    REQUIRED: products is built in SQL: distinct names, sorted, joined with
    commas. Duplicates in the list (Mask twice), or an unsorted list, are
    the failure mode this drill exists to kill. NO Python.

    Runner: sqlite3 in memory. Write portable SQL: CASE not IF, COALESCE,
    || for concatenation, strftime()/julianday()/date() for dates.
"""

from dsa.sql import SQLDrill


class Solution(SQLDrill):

    def query(self) -> str:
        return """

        """


EXAMPLE_1 = """
CREATE TABLE Activities (sell_date TEXT, product TEXT);
INSERT INTO Activities VALUES ('2020-05-30', 'Headphone');
INSERT INTO Activities VALUES ('2020-06-01', 'Pencil');
INSERT INTO Activities VALUES ('2020-06-02', 'Mask');
INSERT INTO Activities VALUES ('2020-05-30', 'Basketball');
INSERT INTO Activities VALUES ('2020-06-01', 'Bible');
INSERT INTO Activities VALUES ('2020-06-02', 'Mask');
INSERT INTO Activities VALUES ('2020-05-30', 'T-Shirt');
"""

EXAMPLE_2 = """
CREATE TABLE Activities (sell_date TEXT, product TEXT);
INSERT INTO Activities VALUES ('2021-01-01', 'Pen');
INSERT INTO Activities VALUES ('2021-01-01', 'Pen');
INSERT INTO Activities VALUES ('2021-01-01', 'Ink');
"""


sol = Solution()

sol.show(EXAMPLE_1)

# assert sol.run(EXAMPLE_1) == [('2020-05-30', 3, 'Basketball,Headphone,T-Shirt'), ('2020-06-01', 2, 'Bible,Pencil'), ('2020-06-02', 1, 'Mask')]
# assert sol.run(EXAMPLE_2) == [('2021-01-01', 2, 'Ink,Pen')]
