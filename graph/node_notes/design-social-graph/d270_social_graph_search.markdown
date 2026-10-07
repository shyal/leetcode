REFERENCE: d270 Social Graph Search
SOURCE: System Design Primer, "Design the data structures for a social network" https://github.com/donnemartin/system-design-primer/blob/master/solutions/system_design/social_graph/README.md

REQUIRED
- Client to Web Server to Search API to the User Graph Service, which asks the
  Lookup Service for the current user's Person Server and retrieves the user's
  friend_ids.
- It runs BFS from the current user; for each adjacent node id it must ask the
  Lookup Service again which Person Server stores that node.
