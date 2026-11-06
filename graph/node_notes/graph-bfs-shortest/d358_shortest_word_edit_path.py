# REFERENCE: d358 Shortest Word Edit Path
class Solution:
    def shortestWordEditPath(self, source, target, words):
        unseen = set(words)
        queue = deque([(source, 0)])
        while queue:
            word, steps = queue.popleft()
            if word == target:
                return steps
            for i in range(len(word)):
                for c in "abcdefghijklmnopqrstuvwxyz":
                    nxt = word[:i] + c + word[i + 1 :]
                    if nxt in unseen:
                        unseen.remove(nxt)
                        queue.append((nxt, steps + 1))
        return -1
