DRILL: Shortest Path Between Users
TRAINS: design-social-graph

Design the data structures for a social network in which a user searches for
someone and sees the shortest path to that person. Assume 100 million users,
50 friends per user on average, 1 billion friend searches per month,
unweighted edges, and a graph that does not fit on one machine. Do not use a
graph database. Write: (1) the number of friend relationships and the
searches per second; (2) the algorithm when everything fits on one machine;
(3) how the users are spread over machines and how one is found; (4) the
request path, and what the search does for each node it visits; (5) four
optimisations.

REQUIRED: two numbers, BFS, Person Servers behind a Lookup Service, the
per-node lookup, four optimisations. Using Dijkstra on unweighted edges, or
assuming the graph is in one memory, is the fail.

## Answer
