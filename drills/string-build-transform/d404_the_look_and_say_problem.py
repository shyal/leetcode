"""
EPI 6.7 The look-and-say problem

Given an integer n, return the n-th term of the look-and-say sequence.
The first term is "1". Each later term reads the previous term aloud,
group by group of equal consecutive digits: the count of the group and
then its digit.

Example 1:

Input: n = 4
Output: "1211"
Explanation: the terms are "1", "11" (one 1), "21" (two 1s), "1211"
(one 2, one 1).

Example 2:

Input: n = 1
Output: "1"

Example 3:

Input: n = 6
Output: "312211"
Explanation: term 5 is "111221": three 1s, two 2s, one 1.

Constraints:

    1 <= n <= 40

    REQUIRED: O(n * 2^n) time. NO itertools.groupby(), NO regex.
"""


class Solution:
    def look_and_say(self, n: int) -> str:
        pass


sol = Solution()

print(sol.look_and_say(4))  # 1211

# assert sol.look_and_say(4) == "1211"
# assert sol.look_and_say(1) == "1"
# assert sol.look_and_say(6) == "312211"
# assert sol.look_and_say(2) == "11"
# assert sol.look_and_say(3) == "21"
# assert sol.look_and_say(5) == "111221"
# assert sol.look_and_say(7) == "13112221"
# assert sol.look_and_say(8) == "1113213211"
# assert sol.look_and_say(9) == "31131211131221"
# assert sol.look_and_say(10) == "13211311123113112211"
# assert len(sol.look_and_say(30)) == 4462
# assert len(sol.look_and_say(40)) == 63138
# assert sol.look_and_say(40).startswith("13211321322113311213")
# assert sol.look_and_say(40).endswith("1312113211")
