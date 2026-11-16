# URL: https://leetcode.com/problems/maximum-gap-between-stations/description/?envType=problem-list-v2&envId=vn57k9wr
#
# 4026. Maximum Gap Between Stations
#
# You are given two strings skill and station of lengths n and m, respectively.
#
# skill[i] represents the skill of worker i, and station[j] represents the skill supported by station j.
#
# You must assign every worker to a distinct station. Let j_i be the index of the station assigned to worker i. A valid assignment must satisfy:
#
# - station[j_i] == skill[i] for every 0 <= i < n.
# - The assigned station indices must be strictly increasing in worker order, meaning j_0 < j_1 < ... < j_{n - 1}.
#
# The gap of an assignment is the maximum difference between the station indices assigned to two consecutive workers. In other words, it is max(j_i - j_{i - 1}) over all 1 <= i < n.
#
# If there is only one worker, the gap is 0.
#
# Return the maximum possible gap among all valid assignments. It is guaranteed that at least one valid assignment exists.
#
# Example 1:
#
# Input: skill = "aa", station = "aaaa"
# Output: 3
# Explanation:
# - The two workers must be assigned to two different 'a' stations.
# - Assigning them to stations [0, 3] gives a gap of 3.
#
# Example 2:
#
# Input: skill = "xyz", station = "xyzz"
# Output: 2
# Explanation:
# - Assign worker 0 to station j = 0, and worker 1 to station j = 1.
# - To maximize the gap, assign worker 2 to station j = 3.
# - This gives the assignment [0, 1, 3] with gaps [1, 2], so the gap is 2.
#
# Example 3:
#
# Input: skill = "cbc", station = "cbcdbc"
# Output: 4
# Explanation:
# - Assign worker 0 to station j = 0, and worker 1 to station j = 1.
# - To maximize the gap, assign worker 2 to station j = 5.
# - This gives the assignment [0, 1, 5] with gaps [1, 4], so the gap is 4.
#
# Constraints:
#
#     skill.length == n
#     station.length == m
#     1 <= n <= m <= 10^5
#     skill and station consist of lowercase English letters.
#     It is guaranteed that a valid assignment exists for every worker.
#
# ---
# STAGE 1 of 3 - the approach. Write it in plain English under this line. Then run make solved.
#
# Input: skill = "cbc", station = "cbcdbc"
# 
# maybe we count the letters, like for c:
# 1 2  3
# cbcdbc
# 
# b:
#  1  2
# cbcdbc
# Learning


# mu 0.18

class Solution
  def maximumGap(skill: str, station: str) -> int
    j = -1
    early = [(j := station.index(c, j + 1)) for c in skill]
    j = len(station)
    late = [(j := station.rindex(c, 0, j)) for c in reversed(skill)][::-1]
    max([b - a for a, b in zip(early, late[1:])], default=0)


sol = Solution()

print(sol.maximumGap('aa', 'aaaa'))  # 3

# assert sol.maximumGap('aa', 'aaaa') == 3
# assert sol.maximumGap('xyz', 'xyzz') == 2
# assert sol.maximumGap('cbc', 'cbcdbc') == 4

# assert sol.maximumGap('a', 'a') == 0
# assert sol.maximumGap('a', 'z' * 99999 + 'a') == 0
# assert sol.maximumGap('abc', 'abcabcabcabcabcabcabcabcabcabc') == 28
# assert sol.maximumGap('aaaaa', 'aaaaaaaaaa') == 6
# assert sol.maximumGap('zzzzzzzzzz', 'z' * 100000) == 99991
# assert sol.maximumGap('abcabcabcabc', 'aabbcc' * 16666 + 'abc') == 99981
# assert sol.maximumGap('a' * 100000, 'a' * 100000) == 1
# assert sol.maximumGap('abc', 'xyzabcxyzabcxyzabc') == 13
# assert sol.maximumGap('abc', 'abc' * 33333 + 'a') == 99997
# assert sol.maximumGap('a', 'a' * 100000) == 0
# assert sol.maximumGap('ab', 'a' * 50000 + 'b' * 50000) == 99999
