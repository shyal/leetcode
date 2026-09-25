# REFERENCE: d61 Department Top Three Salaries
class Solution(SQLDrill):
    def query(self):
        return """
        with ranked as (
            select departmentId, name, salary,
                   dense_rank() over (partition by departmentId order by salary desc) as rnk
            from Employee
        )
        select departmentId, name, salary
        from ranked
        where rnk <= 3
        """
