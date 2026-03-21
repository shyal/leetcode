"""
URL: https://leetcode.com/problems/group-anagrams/description/?envType=problem-list-v2&envId=vn57k9wr

49. Group Anagrams

Given an array of strings strs, group the anagrams together. You can return the answer in any order.


Example 1:

Input: strs = ["eat","tea","tan","ate","nat","bat"]

Output: [["bat"],["nat","tan"],["ate","eat","tea"]]

Explanation:

- There is no string in strs that can be rearranged to form "bat".

- The strings "nat" and "tan" are anagrams as they can be rearranged to form each other.

- The strings "ate", "eat", and "tea" are anagrams as they can be rearranged to form each other.

Example 2:

Input: strs = [""]

Output: [[""]]

Example 3:

Input: strs = ["a"]

Output: [["a"]]


Constraints:

- 1 <= strs.length <= 10^4

- 0 <= strs[i].length <= 100

- strs[i] consists of lowercase English letters.
"""

class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        groups = defaultdict(list)
        for s in strs:
            groups[tuple(sorted(s))].append(s)
        return list(groups.values())

sol = Solution()

# print(sol.groupAnagrams(["eat","tea","tan","ate","nat","bat"]))  # [["bat"],["nat","tan"],["ate","eat","tea"]]

assert sorted([sorted(group) for group in sol.groupAnagrams(["eat","tea","tan","ate","nat","bat"])]) == sorted([sorted(group) for group in [["bat"],["nat","tan"],["ate","eat","tea"]]])
assert sorted([sorted(group) for group in sol.groupAnagrams([""])]) == sorted([sorted(group) for group in [[""]]])
assert sorted([sorted(group) for group in sol.groupAnagrams(["a"])]) == sorted([sorted(group) for group in [["a"]]])
assert sorted([sorted(group) for group in sol.groupAnagrams(["", "", ""])] ) == sorted([sorted(group) for group in [["", "", ""]]])
assert sorted([sorted(group) for group in sol.groupAnagrams(["", "a"])] ) == sorted([sorted(group) for group in [[""], ["a"]]])
assert sorted([sorted(group) for group in sol.groupAnagrams(["abc", "abc", "abc"])] ) == sorted([sorted(group) for group in [["abc", "abc", "abc"]]])
assert sorted([sorted(group) for group in sol.groupAnagrams(["ab", "a", "ba"])] ) == sorted([sorted(group) for group in [["a"], ["ab", "ba"]]])
assert sorted([sorted(group) for group in sol.groupAnagrams(["aa", "aa", "a"])] ) == sorted([sorted(group) for group in [["a"], ["aa", "aa"]]])
assert sorted([sorted(group) for group in sol.groupAnagrams(["aab", "aba", "baa", "abb"])] ) == sorted([sorted(group) for group in [["aab", "aba", "baa"], ["abb"]]])
assert sorted([sorted(group) for group in sol.groupAnagrams(["abc", "def", "ghi"])] ) == sorted([sorted(group) for group in [["abc"], ["def"], ["ghi"]]])
assert sorted([sorted(group) for group in sol.groupAnagrams(["a", "b", "ab", "ba"])] ) == sorted([sorted(group) for group in [["a"], ["b"], ["ab", "ba"]]])
assert sorted([sorted(group) for group in sol.groupAnagrams(["race", "care", "acre", "face"])] ) == sorted([sorted(group) for group in [["race", "care", "acre"], ["face"]]])
assert sorted([sorted(group) for group in sol.groupAnagrams(["", "b", ""])] ) == sorted([sorted(group) for group in [["", ""], ["b"]]])