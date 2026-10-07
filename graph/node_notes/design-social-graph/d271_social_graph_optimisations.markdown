REFERENCE: d271 Social Graph Optimisations
SOURCE: System Design Primer, "Design the data structures for a social network" https://github.com/donnemartin/system-design-primer/blob/master/solutions/system_design/social_graph/README.md

REQUIRED
- Four optimisations out of: a Memory Cache for person data; storing complete
  or partial BFS traversals in the cache; computing traversals offline in
  batch into a NoSQL Database; batching friend lookups that sit on the same
  Person Server, to reduce machine jumps; sharding Person Servers by location;
  two BFS searches at once, from the source and from the destination, then
  merging; starting from people with many friends; a limit on time or hops
  before asking the user whether to continue.
