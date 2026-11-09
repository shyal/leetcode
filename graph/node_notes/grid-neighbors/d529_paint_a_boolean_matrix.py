# REFERENCE: d529 EPI 18.2 Paint a Boolean matrix
class Solution:
    def flip_color(self, x, y, image):
        color = image[x][y]
        image[x][y] = not color
        q = deque([(x, y)])
        while q:
            r, c = q.popleft()
            for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if 0 <= nr < len(image) and 0 <= nc < len(image[0]) and image[nr][nc] == color:
                    image[nr][nc] = not color
                    q.append((nr, nc))
