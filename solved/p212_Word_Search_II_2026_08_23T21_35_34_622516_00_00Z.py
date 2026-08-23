"""
URL: https://leetcode.com/problems/word-search-ii/description/?envType=problem-list-v2&envId=vn57k9wr

212. Word Search II

Given an m x n board of characters and a list of strings words, return all words on the board.

Each word must be constructed from letters of sequentially adjacent cells, where adjacent cells are horizontally or vertically neighboring. The same letter cell may not be used more than once in a word.

Example 1:

Input: board = [["o","a","a","n"],["e","t","a","e"],["i","h","k","r"],["i","f","l","v"]], words = ["oath","pea","eat","rain"]
Output: ["eat","oath"]

Example 2:

Input: board = [["a","b"],["c","d"]], words = ["abcb"]
Output: []

Constraints:

    m == board.length
    n == board[i].length
    1 <= m, n <= 12
    board[i][j] is a lowercase English letter.
    1 <= words.length <= 3 * 10^4
    1 <= words[i].length <= 10
    words[i] consists of lowercase English letters.
    All the strings of words are unique.

---

Ok i'm thinking this might be a multi source DFS problem, or maybe that's a brute force solution.

Since 1 <= words.length <= 3 * 104 we might need a TRIE as an optimization.

OK i've struggled on this problem long enough. I'm hitting bugs that are just getting in the way of
solving the problem.

I'm giving up. Lack of will at this point.

Doesn't pass all the tests on leetcode. Would likely hit a TLE too.

"""


class Solution:
    def findWords(self, board: List[List[str]], words: List[str]) -> List[str]:
        def dfs(row, col, depth, word):
            visited.add((row, col))
            if depth == len(word) - 1:
                return word[depth] == board[row][col]
            if not board[row][col] == word[depth]:
                return False
            for row_x, col_x in [
                [row - 1, col],
                [row, col + 1],
                [row + 1, col],
                [row, col - 1],
            ]:
                if (
                    0 <= row_x < len(board)
                    and 0 <= col_x < len(board[0])
                    and (row_x, col_x) not in visited
                ):
                    if dfs(row_x, col_x, depth + 1, word):
                        return True
            return False

        res = set([])
        for row in range(len(board)):
            for col in range(len(board[0])):
                for word in words:
                    visited = set([])
                    if dfs(row, col, 0, word):
                        res.add(word)
        return list(sorted(list(res)))


sol = Solution()

assert sol.findWords([["a"]], ["a"]) == ["a"]
assert sol.findWords([["a", "a"]], ["aa"]) == ["aa"]

print(
    sol.findWords(
        [
            ["o", "a", "a", "n"],
            ["e", "t", "a", "e"],
            ["i", "h", "k", "r"],
            ["i", "f", "l", "v"],
        ],
        ["oath", "pea", "eat", "rain"],
    )
)  # ["eat","oath"]


# assert sol.findWords(
#     [
#         ["a", "b", "c", "e"],
#         ["x", "x", "c", "d"],
#         ["x", "x", "b", "a"],
#     ],
#     ["abc", "abcd"],
# ) == ["abc", "abcd"]

assert sorted(
    sol.findWords(
        [
            ["o", "a", "a", "n"],
            ["e", "t", "a", "e"],
            ["i", "h", "k", "r"],
            ["i", "f", "l", "v"],
        ],
        ["oath", "pea", "eat", "rain"],
    )
) == sorted(["eat", "oath"])
assert sol.findWords([["a", "b"], ["c", "d"]], ["abcb"]) == []

assert sol.findWords([["a"]], ["b"]) == []
assert sol.findWords([["a", "a"], ["a", "a"]], ["aa", "aaa"]) == ["aa", "aaa"]
assert sol.findWords([["z"] * 12 for _ in range(12)], ["z" * 10]) == ["zzzzzzzzzz"]
assert sol.findWords(
    [["a", "b", "c"], ["d", "e", "f"], ["g", "h", "i"]],
    ["abc", "aei", "cfi", "beh", "defi"],
) == ["abc", "beh", "cfi", "defi"]
assert sol.findWords([["a", "b", "c"], ["d", "e", "f"], ["g", "h", "i"]], ["xyz"]) == []
assert sol.findWords([["a", "b"], ["c", "d"]], ["ab", "abcd", "abc"]) == ["ab"]
assert sol.findWords(
    [["a", "a", "a", "a"], ["a", "a", "a", "a"], ["a", "a", "a", "a"]],
    ["aaaa", "aaaaa"],
) == ["aaaa", "aaaaa"]
assert sol.findWords([["a"] * 12], ["a" * 10, "a" * 12]) == [
    "aaaaaaaaaa",
    "aaaaaaaaaaaa",
]
# assert sol.findWords([["a"]] * 12, ["a" * 10, "a" * 12]) == []
assert sol.findWords(
    [["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l"]],
    ["abcdefghijk", "abcdefghijkl"],
) == ["abcdefghijk", "abcdefghijkl"]
assert sol.findWords(
    [["a"] * 12 for _ in range(12)], ["a" * 10, "a" * 11, "a" * 12]
) == ["aaaaaaaaaa", "aaaaaaaaaaa", "aaaaaaaaaaaa"]
