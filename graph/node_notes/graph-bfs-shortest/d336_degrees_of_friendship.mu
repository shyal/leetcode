# REFERENCE: d336 Degrees of Friendship
class Solution
  def friend_distance(friends: [[int]], userA: int, userB: int) -> int
    dist = {userA: 0}
    q = deque([userA])
    while q
      u = q.popleft()
      if u == userB
        return dist[u]
      for >v, linked in friends[u]
        if linked and v not in dist
          dist[v] = dist[u] + 1
          q <- v
    -1
