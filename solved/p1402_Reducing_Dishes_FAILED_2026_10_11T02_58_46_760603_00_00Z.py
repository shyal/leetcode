"""
URL: https://leetcode.com/problems/reducing-dishes/description/?envType=problem-list-v2&envId=vn57k9wr

1402. Reducing Dishes

A chef has collected data on the satisfaction level of his n dishes. Chef can cook any dish in 1 unit of time.

Like-time coefficient of a dish is defined as the time taken to cook that dish including previous dishes multiplied by its satisfaction level i.e. time[i] * satisfaction[i].

Return the maximum sum of like-time coefficient that the chef can obtain after preparing some amount of dishes.

Dishes can be prepared in any order and the chef can discard some dishes to get this maximum value.

Example 1:

Input: satisfaction = [-1,-8,0,5,-9]
Output: 14
Explanation: After Removing the second and last dish, the maximum total like-time coefficient will be equal to (-1*1 + 0*2 + 5*3 = 14).
Each dish is prepared in one unit of time.

Example 2:

Input: satisfaction = [4,3,2]
Output: 20
Explanation: Dishes can be prepared in any order, (2*1 + 3*2 + 4*3 = 20)

Example 3:

Input: satisfaction = [-1,-4,-5]
Output: 0
Explanation: People do not like the dishes. No dish is prepared.

Constraints:

    n == satisfaction.length
    1 <= n <= 500
    -1000 <= satisfaction[i] <= 1000
---
so by default we get [-1 * 1, -8 * 2, 0 * 3, 5 * 4, -9 * 5]
or                   [-1 * i, -8 * i, 0 * i, 5 * i, -9 * i]

where i is the position in the array

We can clearly discard negative scores, though one has to wonder why -1 still showed up
and the reason is, we get a greater i for subsequent dishes

So in which cases does keeping a negative score outweigh not keeping it
that really is the question here, and with 500 it'll be costly taking a trial and error
approach, which smells like DP

if we simply iterate over the array, and take the max of keeping versus discarding, we'll
get to the max.. but no it's not that simple, because keeping versus discarding affects
future results, so maybe either recursion or 2D dp to explore the solution space

forgot about the swap requirement.. so solved the wrong question
remember: make sure you're answering the right question.
"""


# mu 0.7
# def maxSatisfaction(satisfaction: [int]) -> int
#   def score(i, j, s)
#     if i <= len(s) -1
#       if i < len(s) -1
#         s[i], s[i+1] = s[i+1], s[i]
#         swap = s[i] * j + score(i+1, j+1, s)
#         s[i], s[i+1] = s[i+1], s[i]
#       else
#         swap = 0
#       return max(max(s[i] * j + score(i+1, j+1, s), swap, score(i+1, j, s)), 0)
#     return 0
#   score(0, 1, satisfaction)

class Solution:
    def maxSatisfaction(self, satisfaction: list[int]) -> int:
        def score(i, j, s):
            if i <= len(s) - 1:
                if i < len(s) - 1:
                    s[i], s[i + 1] = s[i + 1], s[i]
                    swap = s[i] * j + score(i + 1, j + 1, s)
                    s[i], s[i + 1] = s[i + 1], s[i]
                else:
                    swap = 0
                return max(max(s[i] * j + score(i + 1, j + 1, s), swap, score(i + 1, j, s)), 0)
            return 0
        return score(0, 1, satisfaction)


sol = Solution()
print(sol.maxSatisfaction([-1, -8, 0, 5, -7]))
_l, _r = sol.maxSatisfaction([-1, -8, 0, 5, -9]), 14
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.maxSatisfaction([4, 3, 2]), 20
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.maxSatisfaction([-1, -4, -5]), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.maxSatisfaction([0, 0, 0, 0, 0]), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.maxSatisfaction([1, 2, 3, 4, 5]), 55
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"


# FAILED: walked away after 41m 55s; no working solution.
# Judge the move the defect is in as struggled, not clean. A move the code never reached gets no verdict.
