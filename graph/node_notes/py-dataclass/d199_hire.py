# REFERENCE: d199 Hire
@dataclass
class Employee:
    name: str
    dept: str
    salary: int


class Solution:
    def hire(self, name, dept, salary):
        return Employee(name, dept, salary)
