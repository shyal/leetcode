# URL: https://leetcode.com/problems/minimum-deletions-to-make-character-frequencies-unique/description/?envType=problem-list-v2&envId=vn57k9wr
#
# 1647. Minimum Deletions to Make Character Frequencies Unique
#
# A string s is called good if there are no two different characters in s that have the same frequency.
#
# Given a string s, return the minimum number of characters you need to delete to make s good.
#
# The frequency of a character in a string is the number of times it appears in the string. For example, in the string "aab", the frequency of 'a' is 2, while the frequency of 'b' is 1.
#
# Example 1:
#
# Input: s = "aab"
# Output: 0
# Explanation: s is already good.
#
# Example 2:
#
# Input: s = "aaabbbcc"
# Output: 2
# Explanation: You can delete two 'b's resulting in the good string "aaabcc".
# Another way it to delete one 'b' and one 'c' resulting in the good string "aaabbc".
#
# Example 3:
#
# Input: s = "ceabaacb"
# Output: 2
# Explanation: You can delete both 'c's resulting in the good string "eabaab".
# Note that we only care about characters that are still in the string at the end (i.e. frequency of 0 is ignored).
#
# Constraints:
#
#     1 <= s.length <= 10^5
#     s contains only lowercase English letters.
#
# ---
# 
# aab -> 1,2
# aaabbbcc -> 2,3,3
# ceabaacb -> 3,2,2,1
# 
# take the counts, then make them monotonically decreasing, so that there are no repeats
# the tricky part is that doing so affects the smaller counts too.
# so 3 2 2 1 becomes 3 2 1 1 so now we have a repeat in 1 and have to do the same amount.
# what happens if we work with counts of counts: we get 3: 1, 2: 2, 1: 1.
# we could have a carry mechanism on the counts of counts, so let's use a better example:
# gggggfffffeeeeeddddcccbba
# we get 5,5,5,4,3,2,1
# counts of counts gives us: 5: 3, 4: 1, 3: 1, 2: 1, 1: 1
# which becomes: 5: 1, 4: 3, 3: 1, 2: 1, 1: 1
# which becomes: 5: 1, 4: 1, 3: 3, 2: 1, 1: 1
# which becomes: 5: 1, 4: 1, 3: 1, 2: 3, 1: 1
# which becomes: 5: 1, 4: 1, 3: 1, 2: 1, 1: 3
# which becomes: 5: 1, 4: 1, 3: 1, 2: 1, 1: 1
# each time we have a collision, we have to add those to the count again
# 
# mu 0.17

class Solution
  def minDeletions(s: str) -> int
    c = counter(counter(s).values())
    h = heap([(v, k) for k, v in c.items()], type=max)
    ret res = 0
    while h and h.peek()[0] > 1
      cnt, number = h.pop()
      del c[number]
      if number >= 1
        number -= 1
      cnt -= 1
      if cnt > 0
        res += cnt
      if c[number]
        vv, kk = h.pop()
        vv += cnt
        c[kk] = vv
        h.push((vv, kk))
      elif number
        h.push((cnt, number))
        c[number] = cnt


sol = Solution()

print(sol.minDeletions('aabcdee'))  # 4

assert sol.minDeletions('aab') == 0
assert sol.minDeletions('aaabbbcc') == 2
assert sol.minDeletions('ceabaacb') == 2
assert sol.minDeletions('a') == 0
assert sol.minDeletions('aaaaaa') == 0
assert sol.minDeletions('abcabcabcabc') == 3
assert sol.minDeletions('bbcebab') == 2
assert sol.minDeletions('aecbaed') == 4


# FAILED: walked away after 58m 1s; no working solution.
# Judge the move the defect is in as struggled, not clean. A move the code never reached gets no verdict.
