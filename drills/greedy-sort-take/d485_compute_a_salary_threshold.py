"""
EPI 13.12 Compute a salary threshold

Given a target payroll target_payroll and a list of salaries
current_salaries, return the cap c such that the capped salaries add up
to exactly target_payroll. A capped salary is min(salary, c). When the
salaries add up to exactly target_payroll, return the largest salary.
When the salaries add up to less than target_payroll, no cap works:
return -1.0.

Example 1:

Input: target_payroll = 180, current_salaries = [20, 80, 50, 110]
Output: 55.0
Explanation: 20 + 50 + 55 + 55 = 180.

Example 2:

Input: target_payroll = 300, current_salaries = [100, 100]
Output: -1.0

Example 3:

Input: target_payroll = 4, current_salaries = [3, 5]
Output: 2.0
Explanation: the cap is below every salary, and 2 + 2 = 4.

Constraints:

    1 <= len(current_salaries) <= 10^5
    0 <= current_salaries[i] <= 10^9
    0 <= target_payroll <= 10^14
    The cap may be a fraction.

    REQUIRED: O(n log n) time, where n is the length of
    current_salaries. NO binary search on the cap.
"""


class Solution:
    def find_salary_cap(self, target_payroll: int, current_salaries: list[int]) -> float:
        pass


sol = Solution()

print(sol.find_salary_cap(180, [20, 80, 50, 110]))  # 55.0

# assert sol.find_salary_cap(180, [20, 80, 50, 110]) == 55.0
# assert sol.find_salary_cap(300, [100, 100]) == -1.0
# assert sol.find_salary_cap(4, [3, 5]) == 2.0
# assert sol.find_salary_cap(10, [3, 7]) == 7.0
# assert sol.find_salary_cap(0, [5]) == 0.0
# assert sol.find_salary_cap(3, [5]) == 3.0
# assert sol.find_salary_cap(6, [5]) == -1.0
# assert sol.find_salary_cap(12, [5, 5, 5]) == 4.0
# assert sol.find_salary_cap(7, [1, 10, 10]) == 3.0
# assert sol.find_salary_cap(8, [1, 10, 10]) == 3.5
# assert abs(sol.find_salary_cap(10, [10, 10, 10]) - 10 / 3) < 1e-9
# assert sol.find_salary_cap(30, [10, 20, 0]) == 20.0
# assert sol.find_salary_cap(3750025000, list(range(1, 10 ** 5 + 1))) == 50000.0
# assert sol.find_salary_cap(10 ** 14, [10 ** 9] * 10 ** 5) == 10 ** 9
# assert sol.find_salary_cap(5 * 10 ** 13, [10 ** 9] * 10 ** 5) == 5 * 10 ** 8
# assert sol.find_salary_cap(10 ** 14, [10 ** 9] * (10 ** 5 - 1)) == -1.0
