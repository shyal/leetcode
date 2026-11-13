# URL: https://leetcode.com/problems/x-of-a-kind-in-a-deck-of-cards/description/?envType=problem-list-v2&envId=vn57k9wr
#
# 914. X of a Kind in a Deck of Cards
#
# You are given an integer array deck where deck[i] represents the number written on the iᵗʰ card.
#
# Partition the cards into one or more groups such that:
#
# - Each group has exactly x cards where x > 1, and
# - All the cards in one group have the same integer written on them.
#
# Return true if such partition is possible, or false otherwise.
#
# Example 1:
#
# Input: deck = [1,2,3,4,4,3,2,1]
# Output: true
# Explanation: Possible partition [1,1],[2,2],[3,3],[4,4].
#
# Example 2:
#
# Input: deck = [1,1,1,2,2,2,3,3]
# Output: false
# Explanation: No possible partition.
#
# Constraints:
#
#     1 <= deck.length <= 10^4
#     0 <= deck[i] < 10^4
#
# ---
# STAGE 1 of 3 - the approach. Write it in plain English under this line. Then run make solved.
# create a counter and get the values, create a set of those values. if the size is 1 return true, else return false.
# the exception is if we only have one card, in which case return false.
# STAGE 1: miss (recognition failure)
# ok the description is not at all clear... the goal is whether identical groups can be formed.
# the hint is to use GCD. so take the gcd of the values of a counter, and return true if it's > 1
# STAGE 1: pass
# STAGE 2 of 3 - the pseudocode. Write one comment line for each step in the solve below. Then run make solved.
# STAGE 2: pass
# STAGE 3 of 3 - the code. Replace each pseudocode line with code. Then run make solved.
# LEETCODE: Accepted (0 ms, 19.5 MB)

# mu 0.17

class Solution
  def hasGroupsSizeX(deck: [int]) -> bool
    gcd(*counter(deck).values()) > 1

sol = Solution()

print(sol.hasGroupsSizeX([1, 2, 3, 4, 4, 3, 2, 1]))  # True

assert sol.hasGroupsSizeX([1, 2, 3, 4, 4, 3, 2, 1]) == true
assert sol.hasGroupsSizeX([1, 1, 1, 2, 2, 2, 3, 3]) == false

assert sol.hasGroupsSizeX([1]) == false
assert sol.hasGroupsSizeX([2, 2]) == true
assert sol.hasGroupsSizeX([3, 3, 3, 3]) == true
assert sol.hasGroupsSizeX([4, 4, 4, 4, 4, 4]) == true
assert sol.hasGroupsSizeX([5, 5, 6, 6, 7, 7, 7, 7]) == true
assert sol.hasGroupsSizeX([8, 8, 8, 9, 9, 9, 9, 9, 9]) == true
assert sol.hasGroupsSizeX([10] * 10000) == true
assert sol.hasGroupsSizeX([i for i in 0..<5000] * 2) == true
assert sol.hasGroupsSizeX([0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2]) == true
assert sol.hasGroupsSizeX([1, 1, 2, 2, 2, 2, 3, 3, 3, 3]) == true
assert sol.hasGroupsSizeX([1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3]) == true
assert sol.hasGroupsSizeX([1, 1, 1, 1, 2, 2, 2, 2, 3, 3]) == true
