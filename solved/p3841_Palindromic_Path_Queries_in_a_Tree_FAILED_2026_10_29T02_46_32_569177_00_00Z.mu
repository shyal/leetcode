# URL: https://leetcode.com/problems/palindromic-path-queries-in-a-tree/description/?envType=problem-list-v2&envId=vn57k9wr
#
# 3841. Palindromic Path Queries in a Tree
#
# You are given an undirected tree with n nodes labeled 0 to n - 1. This is represented by a 2D array edges of length n - 1, where edges[i] = [u_i, v_i] indicates an undirected edge between nodes u_i and v_i.
#
# You are also given a string s of length n consisting of lowercase English letters, where s[i] represents the character assigned to node i.
#
# You are also given a string array queries, where each queries[i] is either:
#
# - "update u_i c": Change the character at node u_i to c. Formally, update s[u_i] = c.
# - "query u_i v_i": Determine whether the string formed by the characters on the unique path from u_i to v_i (inclusive) can be rearranged into a palindrome.
#
# Return a boolean array answer, where answer[j] is true if the jth query of type "query u_i v_i"​​​​​​​ can be rearranged into a palindrome, and false otherwise.
#
# Example 1:
#
# Input: n = 3, edges = [[0,1],[1,2]], s = "aac", queries = ["query 0 2","update 1 b","query 0 2"]
# Output: [true,false]
# Explanation:
# - "query 0 2": Path 0 → 1 → 2 gives "aac", which can be rearranged to form "aca", a palindrome. Thus, answer[0] = true.
# - "update 1 b": Update node 1 to 'b', now s = "abc".
# - "query 0 2": Path characters are "abc", which cannot be rearranged to form a palindrome. Thus, answer[1] = false.
# Thus, answer = [true, false].
#
# Example 2:
#
# Input: n = 4, edges = [[0,1],[0,2],[0,3]], s = "abca", queries = ["query 1 2","update 0 b","query 2 3","update 3 a","query 1 3"]
# Output: [false,false,true]
# Explanation:
# - "query 1 2": Path 1 → 0 → 2 gives "bac", which cannot be rearranged to form a palindrome. Thus, answer[0] = false.
# - "update 0 b": Update node 0 to 'b', now s = "bbca".
# - "query 2 3": Path 2 → 0 → 3 gives "cba", which cannot be rearranged to form a palindrome. Thus, answer[1] = false.
# - "update 3 a": Update node 3 to 'a', s = "bbca".
# - "query 1 3": Path 1 → 0 → 3 gives "bba", which can be rearranged to form "bab", a palindrome. Thus, answer[2] = true.
# Thus, answer = [false, false, true].
#
# Constraints:
#
#     1 <= n == s.length <= 5 * 10^4
#     edges.length == n - 1
#     edges[i] = [u_i, v_i]
#     0 <= u_i, v_i <= n - 1
#     s consists of lowercase English letters.
#     The input is generated such that edges represents a valid tree.
#     1 <= queries.length <= 5 * 10^4
#     queries[i] = "update u_i c" or "query u_i v_i"
#     0 <= u_i, v_i <= n - 1
#     c is a lowercase English letter.
#
# ---
# 
# couldn't solve the TLE. will return to it later.

# mu 0.13

class Solution
  def palindromePath(n: int, edges: [[int]], s: str, queries: [str]) -> [bool]
    G = adjacency(edges, n, false, false)
    s = list(s)
    ret ans = []
    ch = {: -> {:int}}
    def bfs(ui, vi)
      q = deque([[ui, [ui]]])
      seen = set([])
      while q
        node, path = q.popleft()
        if node in seen
          continue
        if node == vi
          return counter([s[x] for x in path])
        seen.add(node)
        for next in G[node]
          if next not in seen
            q <- (next, path + [next])
    for query in queries
      q, a, b = query.split(' ')
      if q == 'update'
        ui, c = int(a), b
        s[ui] = c
      elif q == 'query'
        ui, vi = int(a), int(b)
        res = bfs(ui, vi)
        ans <- sum(odd(x) for x in res.values()) <= 1


sol = Solution()

print(sol.palindromePath(3, [[0, 1], [1, 2]], 'aac', ['query 0 2', 'update 1 b', 'query 0 2']))  # [True, False]

assert uses(Solution, adjacency)
assert sol.palindromePath(3, [[0, 1], [1, 2]], 'aac', ['query 0 2', 'update 1 b', 'query 0 2']) == [true, false]
assert sol.palindromePath(4, [[0, 1], [0, 2], [0, 3]], 'abca', ['query 1 2', 'update 0 b', 'query 2 3', 'update 3 a', 'query 1 3']) == [false, false, true]
assert sol.palindromePath(1, [], 'a', ['query 0 0']) == [true]
assert sol.palindromePath(2, [[0, 1]], 'aa', ['query 0 1']) == [true]
assert sol.palindromePath(2, [[0, 1]], 'ab', ['query 0 1']) == [false]
assert sol.palindromePath(5, [[0, 1], [1, 2], [2, 3], [3, 4]], 'abcde', ['query 0 4']) == [false]
assert sol.palindromePath(5, [[0, 1], [1, 2], [2, 3], [3, 4]], 'abcde', ['update 2 a', 'query 0 4']) == [false]
assert sol.palindromePath(5, [[0, 1], [1, 2], [2, 3], [3, 4]], 'aaaaa', ['query 0 4']) == [true]
assert sol.palindromePath(5, [[0, 1], [1, 2], [2, 3], [3, 4]], 'abcba', ['query 0 4']) == [true]
assert sol.palindromePath(3, [[0, 1], [1, 2]], 'aba', ['query 0 2', 'update 1 c', 'query 0 2']) == [true, true]
assert sol.palindromePath(4, [[0, 1], [1, 2], [1, 3]], 'abba', ['query 2 3', 'update 3 b', 'query 2 3']) == [true, true]
assert sol.palindromePath(6, [[0, 1], [0, 2], [1, 3], [1, 4], [2, 5]], 'abcdef', ['query 3 5', 'update 4 a', 'query 3 5']) == [false, false]
assert sol.palindromePath(7, [[0, 1], [0, 2], [1, 3], [1, 4], [2, 5], [2, 6]], 'aaaaaaa', ['query 3 6', 'update 6 b', 'query 3 6']) == [true, true]
# assert tle(sol.palindromePath, 3841)


# FAILED: walked away after 51m 4s; no working solution.
# Judge the move the defect is in as struggled, not clean. A move the code never reached gets no verdict.
