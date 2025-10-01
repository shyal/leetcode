"""
https://leetcode.com/problems/string-compression/description/

443. String Compression
Medium
Given an array of characters chars, compress it using the following algorithm:

Begin with an empty string s. For each group of consecutive repeating characters in chars:

If the group's length is 1, append the character to s.
Otherwise, append the character followed by the group's length.
The compressed string s should not be returned separately, but instead, be stored in the input character array chars. Note that group lengths that are 10 or longer will be split into multiple characters in chars.

After you are done modifying the input array, return the new length of the array.

You must write an algorithm that uses only constant extra space.

Note: The characters in the array beyond the returned length do not matter and should be ignored.


Example 1:

Input: chars = ["a","a","b","b","c","c","c"]
Output: Return 6, and the first 6 characters of the input array should be: ["a","2","b","2","c","3"]
Explanation: The groups are "aa", "bb", and "ccc". This compresses to "a2b2c3".
Example 2:

Input: chars = ["a"]
Output: Return 1, and the first character of the input array should be: ["a"]
Explanation: The only group is "a", which remains uncompressed since it's a single character.
Example 3:

Input: chars = ["a","b","b","b","b","b","b","b","b","b","b","b","b"]
Output: Return 4, and the first 4 characters of the input array should be: ["a","b","1","2"].
Explanation: The groups are "a" and "bbbbbbbbbbbb". This compresses to "ab12".
 

Constraints:

1 <= chars.length <= 2000
chars[i] is a lowercase English letter, uppercase English letter, digit, or symbol.


"""
from itertools import groupby
from itertools import chain


class Solution:
    def compress(self, chars: List[str]) -> int:
        a = [
            *chain(
                *[
                    (char, *str(count)) if count > 1 else (char)
                    for char, count in [(c, len([*it])) for c, it in groupby(chars)]
                ]
            )
        ]
        chars[: len(a)] = a
        return len(a)


sol = Solution()

chars = ["a", "a", "b", "b", "c", "c", "c"]
ret = sol.compress(chars)
assert ret == 6
assert chars[:ret] == ["a", "2", "b", "2", "c", "3"]

chars = ["a"]
ret = sol.compress(chars)
assert ret == 1
assert chars[:ret] == ["a"]

chars = ["a", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b"]
ret = sol.compress(chars)
assert ret == 4
assert chars[:ret] == ["a", "b", "1", "2"]

chars = ["a", "a", "b", "a"]
ret = sol.compress(chars)
assert chars[:ret] == ["a", "2", "b", "a"]

chars = ["a", "b", "a", "b", "a", "b"]
ret = sol.compress(chars)
assert chars[:ret] == ["a", "b", "a", "b", "a", "b"]

chars = ["a", "b", "b", "a"]
ret = sol.compress(chars)
assert chars[:ret] == ["a", "b", "2", "a"]

chars = ["a", "a", "a", "b", "b", "a", "a"]
ret = sol.compress(chars)
assert chars[:ret] == ["a", "3", "b", "2", "a", "2"]

chars = ["x"] * 12 + ["y"] + ["x"] * 3
ret = sol.compress(chars)
assert chars[:ret] == ["x", "1", "2", "y", "x", "3"]

