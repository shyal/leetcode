REFERENCE: d272 Query Cache Eviction
SOURCE: System Design Primer, "Design a key-value cache to save the results of the most recent web server queries" https://github.com/donnemartin/system-design-primer/blob/master/solutions/system_design/query_cache/README.md

REQUIRED
- Least recently used, LRU: a doubly-linked list, where new items are added at
  the head and items to expire are removed from the tail, plus a hash table
  for fast lookup of each list node.
