DRILL: Social Graph Sharding
TRAINS: design-social-graph

Design the data structures for a social network in which a user searches for
someone and sees the shortest path to that person. Assume 100 million users,
50 friends per user on average, 1 billion friend searches per month,
unweighted edges, and a graph that does not fit on one machine. Do not use a
graph database.

Say how the users are spread over machines and how the machine holding a user
is found.

REQUIRED: Person Servers, the Lookup Service from person id to server.
Assuming the graph is in one memory is the fail.

## Answer
