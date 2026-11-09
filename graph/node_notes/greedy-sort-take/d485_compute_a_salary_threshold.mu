# REFERENCE: d485 EPI 13.12 Compute a salary threshold
class Solution
  def find_salary_cap(target_payroll: int, current_salaries: [int]) -> float
    salaries = sort(current_salaries)
    paid = 0
    for >i, s in salaries
      rest = len(salaries) - i
      if paid + s * rest >= target_payroll
        return (target_payroll - paid) / rest
      paid += s
    -1.0
