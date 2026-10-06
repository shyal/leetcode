"""
DRILL: Lines Of A File
TRAINS: py-with

Given the `path` of a text file, return its lines as a list of strings
without their line endings. The file is closed by the time the method
returns, whatever happened while reading it.

Example 1:

Input: a file holding "red\nblue\n"
Output: ["red", "blue"]

Example 2:

Input: an empty file
Output: []

Example 3:

Input: a file holding "one" with no newline at the end
Output: ["one"]

Constraints:

    The file has at most 10^5 lines.

    REQUIRED: open the file in a with statement and iterate the file
    object line by line. NO open() outside a with, NO f.close(), NO
    read() of the whole file.
"""

import os
import tempfile


class Solution:

    def lines(self, path: str) -> List[str]:
        pass


sol = Solution()

path = os.path.join(tempfile.mkdtemp(), "colours.txt")
written = open(path, "w").write("red\nblue\n")
print(sol.lines(path))  # ['red', 'blue']

# assert sol.lines(path) == ["red", "blue"]
# written = open(path, "w").write("")
# assert sol.lines(path) == []
# written = open(path, "w").write("one")
# assert sol.lines(path) == ["one"]
# written = open(path, "w").write("a\n\nb\n")
# assert sol.lines(path) == ["a", "", "b"]
