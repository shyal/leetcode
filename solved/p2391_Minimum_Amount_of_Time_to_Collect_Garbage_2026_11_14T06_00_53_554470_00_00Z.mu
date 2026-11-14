# URL: https://leetcode.com/problems/minimum-amount-of-time-to-collect-garbage/description/?envType=problem-list-v2&envId=vn57k9wr
#
# 2391. Minimum Amount of Time to Collect Garbage
#
# You are given a 0-indexed array of strings garbage where garbage[i] represents the assortment of garbage at the iᵗʰ house. garbage[i] consists only of the characters 'M', 'P' and 'G' representing one unit of metal, paper and glass garbage respectively. Picking up one unit of any type of garbage takes 1 minute.
#
# You are also given a 0-indexed integer array travel where travel[i] is the number of minutes needed to go from house i to house i + 1.
#
# There are three garbage trucks in the city, each responsible for picking up one type of garbage. Each garbage truck starts at house 0 and must visit each house in order; however, they do not need to visit every house.
#
# Only one garbage truck may be used at any given moment. While one truck is driving or picking up garbage, the other two trucks cannot do anything.
#
# Return the minimum number of minutes needed to pick up all the garbage.
#
# Example 1:
#
# Input: garbage = ["G","P","GP","GG"], travel = [2,4,3]
# Output: 21
# Explanation:
# The paper garbage truck:
# 1. Travels from house 0 to house 1
# 2. Collects the paper garbage at house 1
# 3. Travels from house 1 to house 2
# 4. Collects the paper garbage at house 2
# Altogether, it takes 8 minutes to pick up all the paper garbage.
# The glass garbage truck:
# 1. Collects the glass garbage at house 0
# 2. Travels from house 0 to house 1
# 3. Travels from house 1 to house 2
# 4. Collects the glass garbage at house 2
# 5. Travels from house 2 to house 3
# 6. Collects the glass garbage at house 3
# Altogether, it takes 13 minutes to pick up all the glass garbage.
# Since there is no metal garbage, we do not need to consider the metal garbage truck.
# Therefore, it takes a total of 8 + 13 = 21 minutes to collect all the garbage.
#
# Example 2:
#
# Input: garbage = ["MMM","PGM","GP"], travel = [3,10]
# Output: 37
# Explanation:
# The metal garbage truck takes 7 minutes to pick up all the metal garbage.
# The paper garbage truck takes 15 minutes to pick up all the paper garbage.
# The glass garbage truck takes 15 minutes to pick up all the glass garbage.
# It takes a total of 7 + 15 + 15 = 37 minutes to collect all the garbage.
#
# Constraints:
#
#     2 <= garbage.length <= 10^5
#     garbage[i] consists of only the letters 'M', 'P', and 'G'.
#     1 <= garbage[i].length <= 10
#     travel.length == garbage.length - 1
#     1 <= travel[i] <= 100
#
# ---
# STAGE 1 of 3 - the approach. Write it in plain English under this line. Then run make solved.
# precompute the prefixes of travel, and build a range_sum function that gives the time it takes
# to travel from house x to house y
# then iterate over the garbage array 3 times (once for each type of true)
# and sum up the pickups and travel times
# STAGE 1: pass
# STAGE 2 of 3 - the pseudocode. Write one comment line for each step in the solve below. Then run make solved.
# LEETCODE: Accepted (178 ms, 37.2 MB)

# mu 0.18

class Solution

  def get_range(i, j)
    J = self.p[j]
    I = self.p[i-1] if i > 0 else 0
    J - I

  def garbageCollection(garbage: [str], travel: [int]) -> int
    ret res = 0
    self.p = [0] + [*scan(+, travel)]
    for T in 'PMG'
      last = 0
      for >i, G in garbage
        if T in G
          cnt = G.count(T)
          travel_time = self.get_range(last+1, i)
          res += cnt + travel_time
          last = i

sol = Solution()


print(sol.garbageCollection(['G', 'P', 'GP', 'GG'], [2, 4, 3]))  # 21
assert sol.garbageCollection(['G', 'P', 'GP', 'GG'], [2, 4, 3]) == 21
assert sol.garbageCollection(['MMM', 'PGM', 'GP'], [3, 10]) == 37
assert sol.garbageCollection(['M'], []) == 1
assert sol.garbageCollection(['M', 'M', 'M'], [1, 1]) == 5
assert sol.garbageCollection(['', '', ''], [1, 1]) == 0
assert sol.garbageCollection(['M', 'P', 'G'], [100, 100]) == 303
assert sol.garbageCollection(['MPG', 'MPG', 'MPG'], [1, 1]) == 15
assert sol.garbageCollection(['M' * 10] * 100000, [1] * 99999) == 1099999
assert sol.garbageCollection(['P' * 10, 'G' * 10], [100]) == 120
assert sol.garbageCollection(['G', 'G', 'G', 'G'], [1, 1, 1]) == 7
assert sol.garbageCollection(['M', 'P', 'G', 'M', 'P', 'G'], [1, 2, 3, 4, 5]) == 37
assert sol.garbageCollection(['M', 'P', 'G', 'M', 'P', 'G'], [100, 100, 100, 100, 100]) == 1206
assert sol.garbageCollection(['M', 'P', 'G', 'M', 'P', 'G'], [1, 1, 1, 1, 1]) == 18
assert sol.garbageCollection(['M' * 10, 'P' * 10, 'G' * 10], [1, 1]) == 33
