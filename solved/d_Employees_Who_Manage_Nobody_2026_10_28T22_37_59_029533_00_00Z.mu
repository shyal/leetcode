# Given the table `Employees`, return the `employee_id` of every employee who
# is not the manager of anyone. No ordering required.
#
# Table: Employees
#
#     +-------------+---------+
#     | Column Name | Type    |
#     +-------------+---------+
#     | employee_id | int     |
#     | name        | varchar |
#     | manager_id  | int     |
#     +-------------+---------+
#     employee_id is the primary key. manager_id is NULL for employees with no manager.
#
# Example 1:
#
# Input:
# Employees table:
# +-------------+------+------------+
# | employee_id | name | manager_id |
# +-------------+------+------------+
# | 1           | Ann  | null       |
# | 2           | Bob  | 1          |
# | 3           | Cal  | 1          |
# | 4           | Dee  | 3          |
# | 5           | Eve  | null       |
# +-------------+------+------------+
# Output:
# +-------------+
# | employee_id |
# +-------------+
# | 2           |
# | 4           |
# | 5           |
# +-------------+
# Explanation: Managers are 1 and 3. Everyone else manages nobody.
#
# Example 2:
#
# Input:
# Employees table:
# +-------------+------+------------+
# | employee_id | name | manager_id |
# +-------------+------+------------+
# | 1           | Ann  | null       |
# | 2           | Bob  | null       |
# +-------------+------+------------+
# Output:
# +-------------+
# | employee_id |
# +-------------+
# | 1           |
# | 2           |
# +-------------+
# Explanation: Nobody has a manager, so nobody is a manager.
#
# Constraints:
#
#     1 <= number of rows <= 10^4
#
#     REQUIRED: every employee who is nobody's manager is returned, and the
#     data contains NULL manager_ids.
#
#     FORBIDDEN: NOT IN against a list that can contain NULL: it returns
#     nothing, because x NOT IN (..., NULL) is never true.
#
#     Runner: sqlite3 in memory. Write portable SQL: CASE not IF, COALESCE,
#     || for concatenation, strftime()/julianday()/date() for dates.
#
# ---

# mu 0.13
from dsa.sql import SQLDrill

class Solution extends SQLDrill
  def query() -> str
    '''
    select
      e.employee_id
    from Employees as e
    left join Employees as m on e.employee_id = m.manager_id
    where m.employee_id is null
    ;
    '''

EXAMPLE_1 = "\nCREATE TABLE Employees (employee_id INTEGER, name TEXT, manager_id INTEGER);\nINSERT INTO Employees VALUES (1, 'Ann', NULL);\nINSERT INTO Employees VALUES (2, 'Bob', 1);\nINSERT INTO Employees VALUES (3, 'Cal', 1);\nINSERT INTO Employees VALUES (4, 'Dee', 3);\nINSERT INTO Employees VALUES (5, 'Eve', NULL);\n"

EXAMPLE_2 = "\nCREATE TABLE Employees (employee_id INTEGER, name TEXT, manager_id INTEGER);\nINSERT INTO Employees VALUES (1, 'Ann', NULL);\nINSERT INTO Employees VALUES (2, 'Bob', NULL);\n"

sol = Solution()

sol.show(EXAMPLE_1)

assert sol.run(EXAMPLE_1) == [(2,), (4,), (5,)]
assert sol.run(EXAMPLE_2) == [(1,), (2,)]
