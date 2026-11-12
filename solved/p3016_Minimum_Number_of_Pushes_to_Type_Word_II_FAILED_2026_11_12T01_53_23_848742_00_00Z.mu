# URL: https://leetcode.com/problems/minimum-number-of-pushes-to-type-word-ii/description/?envType=problem-list-v2&envId=vn57k9wr
#
# 3016. Minimum Number of Pushes to Type Word II
#
# You are given a string word containing lowercase English letters.
#
# Telephone keypads have keys mapped with distinct collections of lowercase English letters, which can be used to form words by pushing them. For example, the key 2 is mapped with ["a","b","c"], we need to push the key one time to type "a", two times to type "b", and three times to type "c".
#
# It is allowed to remap the keys numbered 2 to 9 to distinct collections of letters. The keys can be remapped to any amount of letters, but each letter must be mapped to exactly one key. You need to find the minimum number of times the keys will be pushed to type the string word.
#
# Return the minimum number of pushes needed to type word after remapping the keys.
#
# An example mapping of letters to keys on a telephone keypad is given below. Note that 1, *, #, and 0 do not map to any letters.
#
# Example 1:
#
# Input: word = "abcde"
# Output: 5
# Explanation: The remapped keypad given in the image provides the minimum cost.
# "a" -> one push on key 2
# "b" -> one push on key 3
# "c" -> one push on key 4
# "d" -> one push on key 5
# "e" -> one push on key 6
# Total cost is 1 + 1 + 1 + 1 + 1 = 5.
# It can be shown that no other mapping can provide a lower cost.
#
# Example 2:
#
# Input: word = "xyzxyzxyzxyz"
# Output: 12
# Explanation: The remapped keypad given in the image provides the minimum cost.
# "x" -> one push on key 2
# "y" -> one push on key 3
# "z" -> one push on key 4
# Total cost is 1 * 4 + 1 * 4 + 1 * 4 = 12
# It can be shown that no other mapping can provide a lower cost.
# Note that the key 9 is not mapped to any letter: it is not necessary to map letters to every key, but to map all the letters.
#
# Example 3:
#
# Input: word = "aabbccddeeffgghhiiiiii"
# Output: 24
# Explanation: The remapped keypad given in the image provides the minimum cost.
# "a" -> one push on key 2
# "b" -> one push on key 3
# "c" -> one push on key 4
# "d" -> one push on key 5
# "e" -> one push on key 6
# "f" -> one push on key 7
# "g" -> one push on key 8
# "h" -> two pushes on key 9
# "i" -> one push on key 9
# Total cost is 1 * 2 + 1 * 2 + 1 * 2 + 1 * 2 + 1 * 2 + 1 * 2 + 1 * 2 + 2 * 2 + 6 * 1 = 24.
# It can be shown that no other mapping can provide a lower cost.
#
# Constraints:
#
#     1 <= word.length <= 10^5
#     word consists of lowercase English letters.
#
# ---
# 
# Take the counts, and map the most frequently used keys first.
# 
# 

# mu 0.17

class Solution
  def minimumPushes(word: str) -> int
    c = counter word
    print c
    n = len c
    if n <= 6
      return len word
    cost_dict = {:set}
    cost = {}
    for k, v in c.items()
      cost_dict[v].add(k)
    print_orig(cost_dict)
    cnt = 1
    while cost_dict
      max_freq = max(cost_dict)
      for i in 0..<8
        if cost_dict[max_freq]
          cost[cost_dict[max_freq].pop()] = cnt
      if not cost_dict[max_freq]
        del cost_dict[max_freq]
    print_orig(cost)
    sum for word: cost[_]

sol = Solution()

print(sol.minimumPushes('aabbccddeeffgghhiiiiii'))  # 24

# assert sol.minimumPushes('abcde') == 5
# assert sol.minimumPushes('xyzxyzxyzxyz') == 12
# assert sol.minimumPushes('aabbccddeeffgghhiiiiii') == 24

# assert sol.minimumPushes('a') == 1
# assert sol.minimumPushes('zzzzzzzzzz') == 10
# assert sol.minimumPushes('abcdefghijklmno') == 22
# assert sol.minimumPushes('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa') == 50
# assert sol.minimumPushes('abcdefghijklmnopqrstuvwxyz') == 56


# FAILED: walked away after 33m 31s; no working solution.
# Judge the move the defect is in as struggled, not clean. A move the code never reached gets no verdict.
