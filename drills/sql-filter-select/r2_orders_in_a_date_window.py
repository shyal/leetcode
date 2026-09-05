"""
DRILL: Orders In A Date Window
TRAINS: sql-filter-select

Given the table `Orders`, return the `id` of every order whose `order_date`
is from 2024-03-01 to 2024-03-31, both days included. No ordering required.

Table: Orders

    +-------------+---------+
    | Column Name | Type    |
    +-------------+---------+
    | id          | int     |
    | order_date  | date    |
    +-------------+---------+
    id is the primary key.

Example 1:

Input:
Orders table:
+----+------------+
| id | order_date |
+----+------------+
| 1  | 2024-02-29 |
| 2  | 2024-03-01 |
| 3  | 2024-03-15 |
| 4  | 2024-03-31 |
| 5  | 2024-04-01 |
+----+------------+
Output:
+----+
| id |
+----+
| 2  |
| 3  |
| 4  |
+----+
Explanation: Both ends of the window are inside it; the day before and the day after are not.

Example 2:

Input:
Orders table:
+----+------------+
| id | order_date |
+----+------------+
| 7  | 2023-03-10 |
+----+------------+
Output:
+----+
+----+
Explanation: March of another year is outside the window.

Constraints:

    1 <= number of rows <= 10^4

    REQUIRED: one comparison that names both ends of the window.

    FORBIDDEN: a LIKE pattern on the date text; Python.

    Runner: sqlite3 in memory. Write portable SQL: CASE not IF, COALESCE,
    || for concatenation, strftime()/julianday()/date() for dates.
"""

from dsa.sql import SQLDrill


class Solution(SQLDrill):

    def query(self) -> str:
        return """

        """


EXAMPLE_1 = """
CREATE TABLE Orders (id INTEGER, order_date TEXT);
INSERT INTO Orders VALUES (1, '2024-02-29');
INSERT INTO Orders VALUES (2, '2024-03-01');
INSERT INTO Orders VALUES (3, '2024-03-15');
INSERT INTO Orders VALUES (4, '2024-03-31');
INSERT INTO Orders VALUES (5, '2024-04-01');
"""

EXAMPLE_2 = """
CREATE TABLE Orders (id INTEGER, order_date TEXT);
INSERT INTO Orders VALUES (7, '2023-03-10');
"""


sol = Solution()

sol.show(EXAMPLE_1)

# assert sol.run(EXAMPLE_1) == [(2,), (3,), (4,)]
# assert sol.run(EXAMPLE_2) == []
