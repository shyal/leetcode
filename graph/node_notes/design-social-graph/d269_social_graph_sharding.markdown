REFERENCE: d269 Social Graph Sharding
SOURCE: System Design Primer, "Design the data structures for a social network" https://github.com/donnemartin/system-design-primer/blob/master/solutions/system_design/social_graph/README.md

REQUIRED
- Users are sharded across Person Servers, and a Lookup Service maps a person
  id to the Person Server that stores it.
