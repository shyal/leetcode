"""
DRILL: Fix Names
TRAINS: sql-string-functions

Given the table `Users`, return `user_id` and `name` with the name fixed so
that only the first character is upper case and the rest are lower case. No
ordering required.

Table: Users

    +----------------+---------+
    | Column Name    | Type    |
    +----------------+---------+
    | user_id        | int     |
    | name           | varchar |
    +----------------+---------+
    user_id is the primary key. name contains only letters.

Example 1:

Input:
Users table:
+---------+-------+
| user_id | name  |
+---------+-------+
| 1       | aLice |
| 2       | bOB   |
+---------+-------+
Output:
+---------+-------+
| user_id | name  |
+---------+-------+
| 1       | Alice |
| 2       | Bob   |
+---------+-------+

Example 2:

Input:
Users table:
+---------+------+
| user_id | name |
+---------+------+
| 3       | x    |
| 4       | ZOE  |
+---------+------+
Output:
+---------+------+
| user_id | name |
+---------+------+
| 3       | X    |
| 4       | Zoe  |
+---------+------+
Explanation: A single character is upper-cased; an all-caps name keeps only its first letter upper.

Constraints:

    1 <= number of rows <= 10^4
    1 <= length of name <= 40

    REQUIRED: the fixed name is built in SQL from the stored name.

    FORBIDDEN: the case change in Python; hard-coded names.

    Runner: sqlite3 in memory. Write portable SQL: CASE not IF, COALESCE,
    || for concatenation, strftime()/julianday()/date() for dates.
"""

from dsa.sql import SQLDrill


class Solution(SQLDrill):

    def query(self) -> str:
        return """

        """


EXAMPLE_1 = """
CREATE TABLE Users (user_id INTEGER, name TEXT);
INSERT INTO Users VALUES (1, 'aLice');
INSERT INTO Users VALUES (2, 'bOB');
"""

EXAMPLE_2 = """
CREATE TABLE Users (user_id INTEGER, name TEXT);
INSERT INTO Users VALUES (3, 'x');
INSERT INTO Users VALUES (4, 'ZOE');
"""


sol = Solution()

sol.show(EXAMPLE_1)

# assert sol.run(EXAMPLE_1) == [(1, 'Alice'), (2, 'Bob')]
# assert sol.run(EXAMPLE_2) == [(3, 'X'), (4, 'Zoe')]
