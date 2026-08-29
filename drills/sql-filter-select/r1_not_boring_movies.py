"""
DRILL: Not Boring Movies
TRAINS: sql-filter-select

Given the table Cinema, return every row whose id is odd and whose description
is not 'boring'. Order the result by rating, highest first.

Table: Cinema

    +-------------+---------+
    | Column Name | Type    |
    +-------------+---------+
    | id          | int     |
    | movie       | varchar |
    | description | varchar |
    | rating      | float   |
    +-------------+---------+
    id is the primary key.

Example 1:

Input:
Cinema table:
+----+------------+-------------+--------+
| id | movie      | description | rating |
+----+------------+-------------+--------+
| 1  | War        | great 3D    | 8.9    |
| 2  | Science    | fiction     | 8.5    |
| 3  | irish      | boring      | 6.2    |
| 4  | Ice song   | Fantasy     | 8.6    |
| 5  | House card | Interesting | 9.1    |
+----+------------+-------------+--------+
Output:
+----+------------+-------------+--------+
| id | movie      | description | rating |
+----+------------+-------------+--------+
| 5  | House card | Interesting | 9.1    |
| 1  | War        | great 3D    | 8.9    |
+----+------------+-------------+--------+
Explanation: Ids 1, 3 and 5 are odd; 3 is boring, so 5 and 1 remain, highest rating first.

Example 2:

Input:
Cinema table:
+----+---------+-------------+--------+
| id | movie   | description | rating |
+----+---------+-------------+--------+
| 2  | Quiet   | boring      | 4.0    |
| 4  | Loud    | great       | 7.0    |
| 7  | Odd one | boring      | 9.9    |
+----+---------+-------------+--------+
Output:
+----+-------+-------------+--------+
| id | movie | description | rating |
+----+-------+-------------+--------+
+----+-------+-------------+--------+
Explanation: The only odd id is boring, so nothing is returned.

Constraints:

    1 <= number of rows <= 10^4
    0.0 <= rating <= 10.0

    REQUIRED: one SELECT with a WHERE and an ORDER BY. The filtering and the
    ordering must happen in SQL; pulling rows into Python and filtering there
    is the failure mode this drill exists to kill.

    Runner: sqlite3 in memory. Write portable SQL: CASE not IF, COALESCE,
    || for concatenation, strftime()/julianday()/date() for dates.
"""

from dsa.sql import SQLDrill

EXAMPLE_1 = """
CREATE TABLE Cinema (id INTEGER, movie TEXT, description TEXT, rating REAL);
INSERT INTO Cinema VALUES (1, 'War', 'great 3D', 8.9);
INSERT INTO Cinema VALUES (2, 'Science', 'fiction', 8.5);
INSERT INTO Cinema VALUES (3, 'irish', 'boring', 6.2);
INSERT INTO Cinema VALUES (4, 'Ice song', 'Fantasy', 8.6);
INSERT INTO Cinema VALUES (5, 'House card', 'Interesting', 9.1);
"""

EXAMPLE_2 = """
CREATE TABLE Cinema (id INTEGER, movie TEXT, description TEXT, rating REAL);
INSERT INTO Cinema VALUES (2, 'Quiet', 'boring', 4.0);
INSERT INTO Cinema VALUES (4, 'Loud', 'great', 7.0);
INSERT INTO Cinema VALUES (7, 'Odd one', 'boring', 9.9);
"""


class Solution(SQLDrill):

    def query(self) -> str:
        return """

        """


sol = Solution()

sol.show(EXAMPLE_1)

# assert sol.run(EXAMPLE_1) == [(5, 'House card', 'Interesting', 9.1), (1, 'War', 'great 3D', 8.9)]
# assert sol.run(EXAMPLE_2) == []
