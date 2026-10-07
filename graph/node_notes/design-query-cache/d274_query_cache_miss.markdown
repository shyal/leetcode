REFERENCE: d274 Query Cache Miss
SOURCE: System Design Primer, "Design a key-value cache to save the results of the most recent web server queries" https://github.com/donnemartin/system-design-primer/blob/master/solutions/system_design/query_cache/README.md

REQUIRED
- Miss: the Query API uses the Reverse Index Service to find and rank matching
  documents, the Document Service for titles and snippets, then updates the
  Memory Cache, placing the entry at the front of the LRU list.

ALSO TRUE
- The flow is cache-aside.
