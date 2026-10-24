Design the data structures for a social network in which a user searches for
someone and sees the shortest path to that person. Assume 100 million users,
50 friends per user on average, 1 billion friend searches per month,
unweighted edges, and a graph that does not fit on one machine. Do not use a
graph database.

Write the request path of a search, component by component, and say what the
search does for each node it visits.

REQUIRED: the Search API, the User Graph Service, the Lookup Service for the
current user, BFS with a Lookup Service call per adjacent node. Reading a
neighbour's friends without asking which server holds it is the fail.

## Answer
