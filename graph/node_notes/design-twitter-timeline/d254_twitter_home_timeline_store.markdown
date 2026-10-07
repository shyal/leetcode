REFERENCE: d254 Twitter Home Timeline Store
SOURCE: System Design Primer, "Design the Twitter timeline and search" https://github.com/donnemartin/system-design-primer/blob/master/solutions/system_design/twitter/README.md

REQUIRED
- Home timelines live in a Memory Cache, a Redis list, because 60,000 fanout
  writes per second would overload a relational database; the store must have
  fast writes.
- The user's own timeline is read from the SQL Database.
