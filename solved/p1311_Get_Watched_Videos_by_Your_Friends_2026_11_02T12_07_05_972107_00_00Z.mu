# URL: https://leetcode.com/problems/get-watched-videos-by-your-friends/description/?envType=problem-list-v2&envId=vn57k9wr
#
# 1311. Get Watched Videos by Your Friends
#
# There are n people, each person has a unique id between 0 and n-1. Given the arrays watchedVideos and friends, where watchedVideos[i] and friends[i] contain the list of watched videos and the list of friends respectively for the person with id = i.
#
# Level 1 of videos are all watched videos by your friends, level 2 of videos are all watched videos by the friends of your friends and so on. In general, the level k of videos are all watched videos by people with the shortest path exactly equal to k with you. Given your id and the level of videos, return the list of videos ordered by their frequencies (increasing). For videos with the same frequency order them alphabetically from least to greatest.
#
# Example 1:
#
# Input: watchedVideos = [["A","B"],["C"],["B","C"],["D"]], friends = [[1,2],[0,3],[0,3],[1,2]], id = 0, level = 1
# Output: ["B","C"]
# Explanation:
# You have id = 0 (green color in the figure) and your friends are (yellow color in the figure):
# Person with id = 1 -> watchedVideos = ["C"]
# Person with id = 2 -> watchedVideos = ["B","C"]
# The frequencies of watchedVideos by your friends are:
# B -> 1
# C -> 2
#
# Example 2:
#
# Input: watchedVideos = [["A","B"],["C"],["B","C"],["D"]], friends = [[1,2],[0,3],[0,3],[1,2]], id = 0, level = 2
# Output: ["D"]
# Explanation:
# You have id = 0 (green color in the figure) and the only friend of your friends is the person with id = 3 (yellow color in the figure).
#
# Constraints:
#
#     n == watchedVideos.length == friends.length
#     2 <= n < = 100
#     1 <= watchedVideos[i].length <= 100
#     1 <= watchedVideos[i][j].length <= 8
#     0 <= friends[i].length < n
#     0 <= friends[i][j] < n
#     0 <= id < n
#     1 <= level < n
#     if friends[i] contains j, then friends[j] contains i
#
# ---
# LEETCODE: Accepted (32 ms, 21.1 MB)

# mu 0.16

class Solution
  def watchedVideosByFriends(watchedVideos: [[str]], friends: [[int]], id: int, level: int) -> [str]
    G = {:list}
    for >i, f in friends
      G[i].extend(f)
    q = deque([[id, 0]])
    seen = set([])
    counts = {:int}
    while q
      node, dist = q.popleft()
      if node in seen
        continue
      if dist == level
        for vid in watchedVideos[node]
          counts[vid] += 1
      seen.add(node)
      for next in G[node]
        q <- (next, dist + 1)
    [k for k, v in sorted(counts.items(), key= x -> [x[1], x[0]], reverse=false)]

sol = Solution()

print(sol.watchedVideosByFriends([['A', 'B'], ['C'], ['B', 'C'], ['D']], [[1, 2], [0, 3], [0, 3], [1, 2]], 0, 1))  # ["B","C"]

assert sol.watchedVideosByFriends([['A', 'B'], ['C'], ['B', 'C'], ['D']], [[1, 2], [0, 3], [0, 3], [1, 2]], 0, 1) == ['B', 'C']
assert sol.watchedVideosByFriends([['A', 'B'], ['C'], ['B', 'C'], ['D']], [[1, 2], [0, 3], [0, 3], [1, 2]], 0, 2) == ['D']
assert sol.watchedVideosByFriends([['A']], [[]], 0, 1) == []
assert sol.watchedVideosByFriends([['A', 'A', 'B'], ['B', 'B', 'C'], ['C', 'C', 'C']], [[1], [0, 2], [1]], 0, 1) == ['C', 'B']
assert sol.watchedVideosByFriends([['A'], ['B'], ['C'], ['D'], ['E']], [[1], [0, 2], [1, 3], [2, 4], [3]], 0, 4) == ['E']
assert sol.watchedVideosByFriends([['A'], ['B'], ['C'], ['D'], ['E']], [[1], [0, 2], [1, 3], [2, 4], [3]], 0, 5) == []
assert sol.watchedVideosByFriends([['A'], ['B'], ['C'], ['D'], ['E']], [[1], [0, 2], [1, 3], [2, 4], [3]], 4, 1) == ['D']
assert sol.watchedVideosByFriends([['A', 'B'], ['A', 'B'], ['A', 'B'], ['A', 'B']], [[1, 2, 3], [0, 2, 3], [0, 1, 3], [0, 1, 2]], 0, 1) == ['A', 'B']
assert sol.watchedVideosByFriends([['A', 'B'], ['A', 'B'], ['A', 'B'], ['A', 'B']], [[1, 2, 3], [0, 2, 3], [0, 1, 3], [0, 1, 2]], 0, 2) == []
assert sol.watchedVideosByFriends([['A', 'B'], ['A', 'B'], ['A', 'B'], ['A', 'B']], [[1, 2, 3], [0, 2, 3], [0, 1, 3], [0, 1, 2]], 0, 3) == []
assert sol.watchedVideosByFriends([['A', 'B'], ['A', 'B'], ['A', 'B'], ['A', 'B']], [[1, 2, 3], [0, 2, 3], [0, 1, 3], [0, 1, 2]], 0, 4) == []
assert sol.watchedVideosByFriends([['A', 'B'], ['A', 'B'], ['A', 'B'], ['A', 'B']], [[1, 2, 3], [0, 2, 3], [0, 1, 3], [0, 1, 2]], 3, 1) == ['A', 'B']
assert sol.watchedVideosByFriends([['A', 'B'], ['B', 'C'], ['C', 'D'], ['D', 'E']], [[1], [0, 2], [1, 3], [2]], 0, 3) == ['D', 'E']
assert sol.watchedVideosByFriends([['A'] * 100] * 100, [list(1..<100) + [0]] + [[0] for _ in 1..<100], 0, 1) == ['A']
