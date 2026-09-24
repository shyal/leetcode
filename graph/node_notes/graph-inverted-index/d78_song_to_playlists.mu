# REFERENCE: d78 Song To Playlists
def songToPlaylists(playlists: [[int]]) -> {int: [int]}
  D = defaultdict(list)
  for i, playlist in playlists
    for song in playlist
      D[song] <- i
  D
