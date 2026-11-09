# REFERENCE: d524 EPI 17.5 Find the majority element
class Solution:
    def majority_search(self, stream):
        candidate, count = None, 0
        for s in stream:
            if count == 0:
                candidate = s
            count += 1 if s == candidate else -1
        return candidate
