# REFERENCE: d450 EPI 10.4 Compute the k closest stars
class Solution:
    def find_closest_k_stars(self, stars, k):
        heap = []
        for star in stars:
            maxheappush(heap, star)
            if len(heap) > k:
                maxheappop(heap)
        return heap
