"""
DRILL: Config Warning
TRAINS: py-logging

Given a config file name `filename`, log one warning that the file was
not found and return the line the logging module produced for it, in
the form LEVEL:logger:message. The logger is the root logger, the
message is "Warning:config file <filename> not found", and the
filename goes into the message through logging's own %s formatting,
not through an f-string.

Example 1:

Input: filename = "server.conf"
Output: "WARNING:root:Warning:config file server.conf not found"

Example 2:

Input: filename = "db.ini"
Output: "WARNING:root:Warning:config file db.ini not found"

Constraints:

    1 <= len(filename) <= 100

    REQUIRED: a logging.StreamHandler on an io.StringIO with a
    logging.Formatter of "%(levelname)s:%(name)s:%(message)s", added
    to logging.getLogger() for the call and removed after; the warning
    is logging.warning("...%s...", filename). NO print, NO f-string in
    the log call, NO building the line by hand.
"""

import io
import logging


class Solution:

    def warn(self, filename: str) -> str:
        pass


sol = Solution()

print(sol.warn("server.conf"))  # WARNING:root:Warning:config file server.conf not found

# assert sol.warn("server.conf") == "WARNING:root:Warning:config file server.conf not found"
# assert sol.warn("db.ini") == "WARNING:root:Warning:config file db.ini not found"
# assert sol.warn("a") == "WARNING:root:Warning:config file a not found"
# assert sol.warn("x") == sol.warn("x")
