# REFERENCE: d534 EPI 18.7 Transform one string to another
class Solution:
    def transform_string(self, D, s, t):
        dist = {s: 0}
        q = deque([s])
        while q:
            word = q.popleft()
            if word == t:
                return dist[word]
            for i in range(len(word)):
                for ch in string.ascii_lowercase:
                    nxt = word[:i] + ch + word[i + 1:]
                    if nxt in D and nxt not in dist:
                        dist[nxt] = dist[word] + 1
                        q.append(nxt)
        return -1
