"""
DRILL: Next Day
TRAINS: sql-date-arithmetic

Given the table `Weather`, return `recordDate` and `next_day` for every
row: `next_day` is the calendar date one day after `recordDate`, as
'YYYY-MM-DD'. No ordering required.

Table: Weather

    +-------------+------+
    | Column Name | Type |
    +-------------+------+
    | recordDate  | date |
    +-------------+------+
    recordDate is the primary key.

Example 1:

Input:
Weather table:
+------------+
| recordDate |
+------------+
| 2015-01-30 |
| 2015-01-31 |
| 2015-02-28 |
+------------+
Output:
+------------+------------+
| recordDate | next_day   |
+------------+------------+
| 2015-01-30 | 2015-01-31 |
| 2015-01-31 | 2015-02-01 |
| 2015-02-28 | 2015-03-01 |
+------------+------------+
Explanation: The day after 31 January is 1 February; 2015 is not a leap year.

Example 2:

Input:
Weather table:
+------------+
| recordDate |
+------------+
| 2015-12-31 |
+------------+
Output:
+------------+------------+
| recordDate | next_day   |
+------------+------------+
| 2015-12-31 | 2016-01-01 |
+------------+------------+
Explanation: The day after the last day of the year is in the next year.

Constraints:

    1 <= number of rows <= 10^4

    REQUIRED: next_day comes from the engine's date arithmetic on
    recordDate.

    FORBIDDEN: string slicing; adding 1 to the day number (both break at a
    month end).

    Runner: sqlite3 in memory. Write portable SQL: CASE not IF, COALESCE,
    || for concatenation, strftime()/julianday()/date() for dates.
"""

from dsa.sql import SQLDrill


class Solution(SQLDrill):

    def query(self) -> str:
        return """
            select
                recordDate,
                date(recordDate, '+1 day') as next_day
            from Weather
            ;
        """


EXAMPLE_1 = """
CREATE TABLE Weather (recordDate TEXT);
INSERT INTO Weather VALUES ('2015-01-30');
INSERT INTO Weather VALUES ('2015-01-31');
INSERT INTO Weather VALUES ('2015-02-28');
"""

EXAMPLE_2 = """
CREATE TABLE Weather (recordDate TEXT);
INSERT INTO Weather VALUES ('2015-12-31');
"""


sol = Solution()

sol.show(EXAMPLE_1)

assert sol.run(EXAMPLE_1) == [
    ("2015-01-30", "2015-01-31"),
    ("2015-01-31", "2015-02-01"),
    ("2015-02-28", "2015-03-01"),
]
assert sol.run(EXAMPLE_2) == [("2015-12-31", "2016-01-01")]
