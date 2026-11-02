# URL: https://leetcode.com/problems/repeated-dna-sequences/description/?envType=problem-list-v2&envId=vn57k9wr
#
# 187. Repeated DNA Sequences
#
# The DNA sequence is composed of a series of nucleotides abbreviated as 'A', 'C', 'G', and 'T'.
#
# For example, "ACGAATTCCG" is a DNA sequence.
#
# When studying DNA, it is useful to identify repeated sequences within the DNA.
#
# Given a string s that represents a DNA sequence, return all the 10-letter-long sequences (substrings) that occur more than once in a DNA molecule. You may return the answer in any order.
#
# Example 1:
#
# Input: s = "AAAAACCCCCAAAAACCCCCCAAAAAGGGTTT"
# Output: ["AAAAACCCCC","CCCCCAAAAA"]
#
# Example 2:
#
# Input: s = "AAAAAAAAAAAAA"
# Output: ["AAAAAAAAAA"]
#
# Constraints:
#
#     1 <= s.length <= 10^5
#     s[i] is either 'A', 'C', 'G', or 'T'.
#
# ---
# LEETCODE: Accepted (982 ms, 33.5 MB)

# mu 0.16

class Solution
  def findRepeatedDnaSequences(s: str) -> [str]
    counts = {:int}
    for i in 0..len(s) - 10
      counts[s[i:i+10]] += 1
    [k for k, v in counts.items() if v > 1]

sol = Solution()

print(sol.findRepeatedDnaSequences('AAAAACCCCCAAAAACCCCCCAAAAAGGGTTT'))  # ["AAAAACCCCC","CCCCCAAAAA"]

assert sorted(sol.findRepeatedDnaSequences('AAAAACCCCCAAAAACCCCCCAAAAAGGGTTT')) == sorted(['AAAAACCCCC', 'CCCCCAAAAA'])
assert sorted(sol.findRepeatedDnaSequences('AAAAAAAAAAAAA')) == sorted(['AAAAAAAAAA'])
