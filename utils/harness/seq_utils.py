# seq_utils.py

from typing import Any, Sequence

from grid_utils import cells, table


def lcs(a: Sequence[Any], b: Sequence[Any], full: bool = False, type: Any = int) -> Any:
    """Longest common subsequence of a and b.

    Row i and column j of the table stand for the prefixes a[:i] and b[:j],
    so row 0 and column 0 are the empty prefix. With type=int (the default)
    each cell holds the length; with type=str, list or tuple it holds one
    LCS itself, built as that type. Plain lcs(a, b) is the last cell,
    dp[-1][-1]; full returns the whole table."""
    dp = table(len(a) + 1, len(b) + 1, fill=type())
    for i, j in cells(dp, start=1):
        x = a[i - 1]
        if x == b[j - 1]:
            one = 1 if type is int else x if type is str else type([x])
            dp[i][j] = dp[i - 1][j - 1] + one
        else:
            dp[i][j] = max(dp[i - 1][j], dp[i][j - 1], key=None if type is int else len)
    return dp if full else dp[-1][-1]
