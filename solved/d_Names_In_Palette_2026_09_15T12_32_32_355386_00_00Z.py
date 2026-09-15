"""
DRILL: Names In Palette

Given a Color value palette and a list names of strings, each one of
"red", "green" or "blue", return the strings of names whose member is
held in palette, in the order they appear in names.

Example 1:

Input: palette = Color.red | Color.blue, names = ["green", "blue", "red"]
Output: ["blue", "red"]

Example 2:

Input: palette = Color(0), names = ["red", "green"]
Output: []
Explanation: palette holds no member.

Example 3:

Input: palette = Color.green, names = ["green", "green"]
Output: ["green", "green"]

Constraints:

    0 <= len(names) <= 1000
    names[i] is "red", "green" or "blue".

    REQUIRED: O(n). The membership test is on palette itself. NO
    conversion of palette to an int, a set or a list.
"""

from enum import Flag, auto


class Color(Flag):
    red = auto()
    green = auto()
    blue = auto()


class Solution:
    def present(self, palette: Color, names: list[str]) -> list[str]:
        res = []
        for n in names:
            if Color[n] in palette:
                res.append(n)
        return res


sol = Solution()

print(sol.present(Color.red | Color.blue, ["green", "blue", "red"]))  # ['blue', 'red']

# assert sol.present(Color.red | Color.blue, ["green", "blue", "red"]) == ["blue", "red"]
# assert sol.present(Color(0), ["red", "green"]) == []
# assert sol.present(Color.green, ["green", "green"]) == ["green", "green"]
# assert sol.present(Color.red | Color.green | Color.blue, ["blue", "red", "green"]) == ["blue", "red", "green"]
# assert sol.present(Color.red, []) == []
# assert sol.present(Color.blue, ["red", "green", "blue"]) == ["blue"]
# assert sol.present(Color.red | Color.green, ["blue"] * 1000) == []
