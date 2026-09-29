# REFERENCE: d175 After The Drop
class Solution:
    def afterTheDrop(self, nums):
        return [x <= nums[-1] for x in nums]
