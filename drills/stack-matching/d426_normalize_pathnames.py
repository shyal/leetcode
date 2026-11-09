"""
EPI 8.4 Normalize pathnames

Given a Unix path, return the shortest path that names the same file.
Names in the path are separated by '/'. Several '/' in a row are the
same as a single '/'. The name '.' is the current directory and '..' is the parent
directory. A path that starts with '/' is absolute and its result
starts with '/'. A relative path keeps each leading '..' that it cannot
remove. The result has no '/' at the end, except the root "/" itself.

Example 1:

Input: path = "/usr/lib/../bin/./gcc"
Output: "/usr/bin/gcc"

Example 2:

Input: path = "a/./b/../../c/"
Output: "c"

Example 3:

Input: path = "../../x/.."
Output: "../.."
Explanation: x and the last '..' cancel. The two leading '..' stay.

Constraints:

    1 <= len(path) <= 2 * 10^5
    Each name is '.', '..', or letters and digits.
    An absolute path never goes above the root.
    The result of a relative path is never empty.

    REQUIRED: O(n) time. NO os.path, NO pathlib, NO regex.
"""


class Solution:
    def shortest_equivalent_path(self, path: str) -> str:
        pass


sol = Solution()

print(sol.shortest_equivalent_path("/usr/lib/../bin/./gcc"))  # /usr/bin/gcc

# assert sol.shortest_equivalent_path("/usr/lib/../bin/./gcc") == "/usr/bin/gcc"
# assert sol.shortest_equivalent_path("a/./b/../../c/") == "c"
# assert sol.shortest_equivalent_path("../../x/..") == "../.."
# assert sol.shortest_equivalent_path("/") == "/"
# assert sol.shortest_equivalent_path("//") == "/"
# assert sol.shortest_equivalent_path("/a/") == "/a"
# assert sol.shortest_equivalent_path("/a/..") == "/"
# assert sol.shortest_equivalent_path("/./.") == "/"
# assert sol.shortest_equivalent_path("a") == "a"
# assert sol.shortest_equivalent_path("a/b/../c") == "a/c"
# assert sol.shortest_equivalent_path("..") == ".."
# assert sol.shortest_equivalent_path("./a") == "a"
# assert sol.shortest_equivalent_path("x/../../y") == "../y"
# assert sol.shortest_equivalent_path("../a/../..") == "../.."
# assert sol.shortest_equivalent_path("/a//b////c/d//././/..") == "/a/b/c"
# assert sol.shortest_equivalent_path("/" + "a/" * 50000 + "../" * 50000) == "/"
# assert sol.shortest_equivalent_path("b/" * 40000 + "../" * 39999) == "b"
# assert sol.shortest_equivalent_path("../" * 50000 + "z") == "../" * 50000 + "z"
