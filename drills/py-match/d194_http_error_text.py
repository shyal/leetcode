"""
DRILL: HTTP Error Text
TRAINS: py-match

Given an HTTP status code `status`, return its text: "Bad request" for
400, "Not found" for 404, "I'm a teapot" for 418, "Not allowed" for 401
and 403, and "Something's wrong with the internet" for any other code.

Example 1:

Input: status = 404
Output: "Not found"

Example 2:

Input: status = 403
Output: "Not allowed"

Example 3:

Input: status = 500
Output: "Something's wrong with the internet"

Constraints:

    100 <= status <= 599

    REQUIRED: one match statement on status, one case per text, the two
    codes that share a text joined with | in one case, and case _ last.
    NO if, NO dict.
"""


class Solution:

    def http_error(self, status: int) -> str:
        pass


sol = Solution()

print(sol.http_error(404))  # Not found

# assert sol.http_error(404) == "Not found"
# assert sol.http_error(403) == "Not allowed"
# assert sol.http_error(500) == "Something's wrong with the internet"
# assert sol.http_error(400) == "Bad request"
# assert sol.http_error(418) == "I'm a teapot"
# assert sol.http_error(401) == "Not allowed"
# assert sol.http_error(200) == "Something's wrong with the internet"
