# REFERENCE: d485 EPI 13.12 Compute a salary threshold
class Solution:
    def find_salary_cap(self, target_payroll, current_salaries):
        salaries = sorted(current_salaries)
        paid = 0
        for i, s in enumerate(salaries):
            rest = len(salaries) - i
            if paid + s * rest >= target_payroll:
                return (target_payroll - paid) / rest
            paid += s
        return -1.0
