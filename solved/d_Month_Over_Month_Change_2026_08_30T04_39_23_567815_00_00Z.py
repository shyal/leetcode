"""
DRILL: Month Over Month Change
TRAINS: sql-window-offset

Given the table `Revenue` with one row per consecutive month, return
`month`, `amount` and `change`: the `amount` minus the previous month's
`amount`. The first month has no previous month and its `change` is NULL. No
ordering required.

Table: Revenue

    +-------------+---------+
    | Column Name | Type    |
    +-------------+---------+
    | month       | varchar |
    | amount      | int     |
    +-------------+---------+
    month is the primary key, formatted 'YYYY-MM'. Months are consecutive with no gaps.

Example 1:

Input:
Revenue table:
+---------+--------+
| month   | amount |
+---------+--------+
| 2025-11 | 100    |
| 2025-12 | 120    |
| 2026-01 | 90     |
| 2026-02 | 90     |
+---------+--------+
Output:
+---------+--------+--------+
| month   | amount | change |
+---------+--------+--------+
| 2025-11 | 100    | null   |
| 2025-12 | 120    | 20     |
| 2026-01 | 90     | -30    |
| 2026-02 | 90     | 0      |
+---------+--------+--------+
Explanation: The year boundary between 2025-12 and 2026-01 is an ordinary previous month. Equal amounts give a change of 0.

Example 2:

Input:
Revenue table:
+---------+--------+
| month   | amount |
+---------+--------+
| 2026-05 | 40     |
+---------+--------+
Output:
+---------+--------+--------+
| month   | amount | change |
+---------+--------+--------+
| 2026-05 | 40     | null   |
+---------+--------+--------+
Explanation: A single month: change is NULL.

Constraints:

    1 <= number of rows <= 10^4

    REQUIRED: one pass over Revenue; the first row's change is NULL, not 0.

    FORBIDDEN: a self-join on 'the month before' (date arithmetic on a
    string, breaks across the year boundary).

    Runner: sqlite3 in memory. Write portable SQL: CASE not IF, COALESCE,
    || for concatenation, strftime()/julianday()/date() for dates.

---

Forgot: amount - lag(amount) over (order by month) as change

Assisted.

"""

from dsa.sql import SQLDrill


class Solution(SQLDrill):

    def query(self) -> str:
        return """
            select
                month,
                amount,
                amount - lag(amount) over (order by month) as change
            from Revenue
            ;
        """


EXAMPLE_1 = """
CREATE TABLE Revenue (month TEXT, amount INTEGER);
INSERT INTO Revenue VALUES ('2025-11', 100);
INSERT INTO Revenue VALUES ('2025-12', 120);
INSERT INTO Revenue VALUES ('2026-01', 90);
INSERT INTO Revenue VALUES ('2026-02', 90);
"""

EXAMPLE_2 = """
CREATE TABLE Revenue (month TEXT, amount INTEGER);
INSERT INTO Revenue VALUES ('2026-05', 40);
"""


sol = Solution()

sol.show(EXAMPLE_1)

assert sol.run(EXAMPLE_1) == [
    ("2025-11", 100, None),
    ("2025-12", 120, 20),
    ("2026-01", 90, -30),
    ("2026-02", 90, 0),
]
assert sol.run(EXAMPLE_2) == [("2026-05", 40, None)]
