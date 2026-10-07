REFERENCE: d276 Query Cache Layout
SOURCE: System Design Primer, "Design a key-value cache to save the results of the most recent web server queries" https://github.com/donnemartin/system-design-primer/blob/master/solutions/system_design/query_cache/README.md

REQUIRED
- Each machine has its own cache: simple, but a low cache hit rate.
- Each machine has a copy of the cache: simple, but an inefficient use of
  memory.
- The cache is sharded across all machines: more complex, and the best option;
  machine = hash(query), with consistent hashing.
