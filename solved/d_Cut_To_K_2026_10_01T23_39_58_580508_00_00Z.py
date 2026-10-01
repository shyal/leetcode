"""
DRILL: Cut To K
TRAINS: binary-search-on-answer

Given a list of chunks of non-negative integers and an integer k, return
exactly k chunks. Take the leftmost chunk holding two or more numbers, cut
it into its first number and the rest, and repeat until there are k chunks.
Keep the chunks in order.

Example 1:

Input: chunks = [[1, 2], [3], [4, 5]], k = 3
Output: [[1, 2], [3], [4, 5]]
Explanation: There are already 3 chunks, so nothing is cut.

Example 2:

Input: chunks = [[1, 2], [3], [4, 5]], k = 5
Output: [[1], [2], [3], [4], [5]]
Explanation: [1, 2] is cut first, then [4, 5].

Example 3:

Input: chunks = [[1], [2, 3], [4]], k = 4
Output: [[1], [2], [3], [4]]
Explanation: The only chunk holding two numbers is in the middle.

Constraints:

    1 <= len(chunks) <= 50
    1 <= the total count of numbers <= 1000
    0 <= each number <= 10^6
    len(chunks) <= k <= the total count of numbers

    REQUIRED: every returned chunk must be a run of one input chunk, in the
    original order. NO flattening the chunks into one list, NO merging two
    chunks, NO reordering, NO sorted. Returning anything other than exactly
    k chunks is a fail.
"""


# mu 0.7
# def cutToK(chunks: [[int]], k: int) -> [[int]]
#   while len chunks < k
#     for i, chunk in chunks
#       if len chunk > 1
#         chunks[i:i+1] = [[chunk[0]], chunk[1:]]
#         print_orig(chunks)
#         break
#   chunks

class Grid(list):
    """A list of rows that also takes a (row, col) pair as an index."""

    def __getitem__(self, k):
        if type(k) is tuple:
            return list.__getitem__(self, k[0])[k[1]]
        return list.__getitem__(self, k)

    def __setitem__(self, k, v):
        if type(k) is tuple:
            list.__getitem__(self, k[0])[k[1]] = v
        else:
            list.__setitem__(self, k, v)


class Solution:
    def cutToK(self, chunks: list[list[int]], k: int) -> list[list[int]]:
        _in_chunks, chunks = chunks, Grid(chunks)
        _w_chunks = chunks
        try:
            while len(chunks) < k:
                for i, chunk in enumerate(chunks):
                    if len(chunk) > 1:
                        chunks[i:i + 1] = [[chunk[0]], chunk[1:]]
                        print_orig(chunks)
                        break
            return chunks
        finally:
            _in_chunks[:] = _w_chunks


sol = Solution()
print(sol.cutToK([[1, 2], [3], [4, 5]], 4))
assert sol.cutToK([[1, 2], [3], [4, 5]], 3) == [[1, 2], [3], [4, 5]]
assert sol.cutToK([[1, 2], [3], [4, 5]], 4) == [[1], [2], [3], [4, 5]]
assert sol.cutToK([[1, 2], [3], [4, 5]], 5) == [[1], [2], [3], [4], [5]]
assert sol.cutToK([[1], [2, 3], [4]], 4) == [[1], [2], [3], [4]]
assert sol.cutToK([[5]], 1) == [[5]]
assert sol.cutToK([[1, 2, 3]], 2) == [[1], [2, 3]]
assert sol.cutToK([[1, 2, 3]], 3) == [[1], [2], [3]]
assert sol.cutToK([[0, 0], [0]], 3) == [[0], [0], [0]]
assert sol.cutToK([[7, 2, 5], [10, 8]], 5) == [[7], [2], [5], [10], [8]]
assert max((sum(c) for c in sol.cutToK([[7, 2, 5], [10, 8]], 2))) <= 18
assert max((sum(c) for c in sol.cutToK([[7, 2, 5], [10, 8]], 3))) <= 18
assert max((sum(c) for c in sol.cutToK([[7, 2, 5], [10, 8]], 4))) <= 18
assert max((sum(c) for c in sol.cutToK([[7, 2, 5], [10, 8]], 5))) <= 18
assert avoids(Solution, sorted)
