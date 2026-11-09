# REFERENCE: d529 EPI 18.2 Paint a Boolean matrix
class Solution
  def flip_color(x: int, y: int, image: [[bool]])
    color = image[x][y]
    image[x][y] = not color
    q = deque([(x, y)])
    while q
      p = q.popleft()
      for n in nbrs(image, p, eq=color)
        image[n] = not color
        q <- n
