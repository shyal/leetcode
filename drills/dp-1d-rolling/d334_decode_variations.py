"""
A letter is encoded as a number: "A" is "1", "B" is "2", and so on to
"Z" as "26". A message of uppercase letters is encoded by writing the
numbers of its letters one after the other, so "AZB" becomes "1262".
Given a string of digits S, return the number of messages that encode
to S.

Example 1:

Input: S = "1262"
Output: 3
Explanation: "AZB", "ABFB" and "LFB".

Example 2:

Input: S = "1270"
Output: 0
Explanation: no letter has the number 0 or 70, and "27" is more than 26.

Example 3:

Input: S = "26"
Output: 2
Explanation: "BF" and "Z".

Constraints:

    1 <= len(S) <= 100
    S holds digits only.

    REQUIRED: O(n) time, O(1) extra space. NO recursion, NO list of
    the messages.
"""


class Solution:
    def decodeVariations(self, S: str) -> int:
        pass


sol = Solution()

print(sol.decodeVariations("1262"))  # 3

# assert sol.decodeVariations("1262") == 3
# assert sol.decodeVariations("1270") == 0
# assert sol.decodeVariations("26") == 2
# assert sol.decodeVariations("127") == 2
# assert sol.decodeVariations("83778549129") == 2
# assert sol.decodeVariations("8254779486") == 2
# assert sol.decodeVariations("122231131122") == 120
# assert sol.decodeVariations("122212313113") == 126
# assert sol.decodeVariations("321121311231") == 65
# assert sol.decodeVariations("0") == 0
# assert sol.decodeVariations("7") == 1
# assert sol.decodeVariations("10") == 1
# assert sol.decodeVariations("20") == 1
# assert sol.decodeVariations("30") == 0
# assert sol.decodeVariations("100") == 0
# assert sol.decodeVariations("101") == 1
# assert sol.decodeVariations("1" * 100) == 573147844013817084101
