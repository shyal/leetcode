REFERENCE: d242 Shortest Path Between Users
SOURCE: System Design Primer, "Design the data structures for a social network" https://github.com/donnemartin/system-design-primer/blob/master/solutions/system_design/social_graph/README.md

REQUIRED
- 5 billion friend relationships: 100 million users * 50. 400 search
  requests per second.
- On one machine: breadth first search, the shortest path in an unweighted
  graph.
- Users are sharded across Person Servers, and a Lookup Service maps a
  person id to the Person Server that stores it.
- Client to Web Server to Search API to the User Graph Service, which asks
  the Lookup Service for the current user's Person Server and retrieves the
  user's friend_ids.
- It runs BFS from the current user; for each adjacent node id it must ask
  the Lookup Service again which Person Server stores that node.
- Four optimisations out of: a Memory Cache for person data; storing
  complete or partial BFS traversals in the cache; computing traversals
  offline in batch into a NoSQL Database; batching friend lookups that sit
  on the same Person Server, to reduce machine jumps; sharding Person
  Servers by location; two BFS searches at once, from the source and from
  the destination, then merging; starting from people with many friends; a
  limit on time or hops before asking the user whether to continue.
