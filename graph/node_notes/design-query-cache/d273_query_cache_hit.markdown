REFERENCE: d273 Query Cache Hit
SOURCE: System Design Primer, "Design a key-value cache to save the results of the most recent web server queries" https://github.com/donnemartin/system-design-primer/blob/master/solutions/system_design/query_cache/README.md

REQUIRED
- Hit: the Query API parses the query and checks the Memory Cache; the cache
  moves the entry to the front of the LRU list and returns the cached
  contents.
