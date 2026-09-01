"""
DRILL: Song To Playlists
TRAINS: graph-inverted-index

Given playlists, where playlists[i] is the list of song ids on playlist i,
return a dict mapping each song id to the indexes of the playlists that
contain it, in increasing order.

Example 1:

Input: playlists = [[13, 11, 14], [11, 15]]
Output: {13: [0], 11: [0, 1], 14: [0], 15: [1]}
Explanation: song 11 is on playlists 0 and 1; every other song is on one
playlist.

Example 2:

Input: playlists = [[12], [12], [12]]
Output: {12: [0, 1, 2]}

Constraints:

    1 <= len(playlists) <= 500
    1 <= len(playlists[i]) <= 10^5
    sum(len(playlists[i])) <= 10^5
    0 <= song id < 10^6

    REQUIRED: must run in O(L) time, where L is the total number of song
    entries across all playlists. NO `song in playlist` membership scans.
"""


class Solution:

    def songToPlaylists(self, playlists: List[List[int]]) -> Dict[int, List[int]]:
        res = defaultdict(list)
        for i, playlist in enumerate(playlists):
            for song in playlist:
                res[song].append(i)
        return res


sol = Solution()

print(
    dict(sol.songToPlaylists([[13, 11, 14], [11, 15]]))
)  # {13: [0], 11: [0, 1], 14: [0], 15: [1]}

assert sol.songToPlaylists([[13, 11, 14], [11, 15]]) == {
    13: [0],
    11: [0, 1],
    14: [0],
    15: [1],
}
assert sol.songToPlaylists([[12], [12], [12]]) == {12: [0, 1, 2]}
assert sol.songToPlaylists([[19]]) == {19: [0]}
assert sol.songToPlaylists([[11, 12], [13, 14]]) == {11: [0], 12: [0], 13: [1], 14: [1]}
