"""
Given a list grantsArray of grant amounts and a number newBudget, return
the cap. Every grant above the cap is lowered to the cap, every grant at
or below it is unchanged, and the lowered grants add up to exactly
newBudget. The cap is the largest number with that property, so the
fewest grants are lowered. When the grants already add up to at most
newBudget, return the largest grant.

Example 1:

Input: grantsArray = [2, 100, 50, 120, 1000], newBudget = 190
Output: 47
Explanation: the new grants are [2, 47, 47, 47, 47], which add up to
190. A cap of 50 keeps 50 and gives [2, 50, 50, 50, 50] = 202, too much.

Example 2:

Input: grantsArray = [2, 4], newBudget = 3
Output: 1.5
Explanation: the new grants are [1.5, 1.5]. The cap is below every
grant.

Example 3:

Input: grantsArray = [2, 4], newBudget = 10
Output: 4
Explanation: 2 + 4 = 6 is already within the budget, so nothing is
lowered and the largest grant is returned.

Constraints:

    0 <= len(grantsArray) <= 10^5
    0 <= grantsArray[i] <= 10^9
    0 <= newBudget <= 10^14
    The cap may be a fraction.

    REQUIRED: O(n log n) time. NO binary search on the cap. NO search
    by repeated trial of a value.
"""


class Solution:
    def find_grants_cap(self, grantsArray: list[int], newBudget: int) -> float:
        pass


sol = Solution()

print(sol.find_grants_cap([2, 100, 50, 120, 1000], 190))  # 47

# assert sol.find_grants_cap([2, 100, 50, 120, 1000], 190) == 47
# assert sol.find_grants_cap([2, 4], 3) == 1.5
# assert sol.find_grants_cap([2, 4], 10) == 4
# assert sol.find_grants_cap([2, 4, 6], 3) == 1
# assert sol.find_grants_cap([2, 100, 50, 120, 167], 400) == 128
# assert abs(sol.find_grants_cap([21, 100, 50, 120, 130, 110], 140) - 23.8) < 1e-9
# assert sol.find_grants_cap([210, 200, 150, 193, 130, 110, 209, 342, 117], 1530) == 211
# assert sol.find_grants_cap([], 10) == 0
# assert sol.find_grants_cap([7], 10) == 7
# assert sol.find_grants_cap([7], 3) == 3
# assert sol.find_grants_cap([7], 0) == 0
# assert sol.find_grants_cap([5, 5, 5], 15) == 5
# assert sol.find_grants_cap([5, 5, 5], 12) == 4
# assert sol.find_grants_cap([0, 0, 0], 0) == 0
# assert sol.find_grants_cap([10 ** 9] * 10 ** 5, 10 ** 14) == 10 ** 9
# assert sol.find_grants_cap([10 ** 9] * 10 ** 5, 5 * 10 ** 13) == 5 * 10 ** 8
# assert sol.find_grants_cap(list(range(1, 10 ** 5 + 1)), 3750025000) == 50000
