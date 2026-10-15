"""
DRILL: Song To Playlists

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


# mu 0.10
# class Solution
#   def songToPlaylists(playlists: [[int]]) -> {int: [int]}
#     tolist = {:list}
#     for >i, playlist in playlists
#       for song in playlist
#         tolist[song] <- i
#     print_orig(tolist)
#     tolist

from collections import defaultdict


class Grid(list):
    """A list of rows that also takes a (row, col) pair as an index."""

    def __getitem__(self, k):
        if type(k) is tuple:
            return list.__getitem__(self, k[0])[k[1]]
        return list.__getitem__(self, k)

    def __setitem__(self, k, v):
        if type(k) is tuple:
            list.__getitem__(self, k[0])[k[1]] = v
        else:
            list.__setitem__(self, k, v)


class Solution:
    def songToPlaylists(self, playlists: list[list[int]]) -> dict[int, list[int]]:
        _in_playlists, playlists = playlists, Grid(playlists)
        _w_playlists = playlists
        try:
            tolist = defaultdict(list)
            for i, playlist in enumerate(playlists):
                for song in playlist:
                    tolist[song].append(i)
            print_orig(tolist)
            return tolist
        finally:
            _in_playlists[:] = _w_playlists


sol = Solution()
print(dict(sol.songToPlaylists([[13, 11, 14], [11, 15]])))
_l, _r = sol.songToPlaylists([[13, 11, 14], [11, 15]]), {13: [0], 11: [0, 1], 14: [0], 15: [1]}
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.songToPlaylists([[12], [12], [12]]), {12: [0, 1, 2]}
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.songToPlaylists([[19]]), {19: [0]}
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.songToPlaylists([[11, 12], [13, 14]]), {11: [0], 12: [0], 13: [1], 14: [1]}
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
