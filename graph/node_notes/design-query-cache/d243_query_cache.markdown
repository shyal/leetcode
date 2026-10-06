REFERENCE: d243 Query Cache
SOURCE: System Design Primer, "Design a key-value cache to save the results of the most recent web server queries" https://github.com/donnemartin/system-design-primer/blob/master/solutions/system_design/query_cache/README.md

REQUIRED
- 4,000 requests per second; 2.7 TB of cache data per month: 270 bytes * 10
  billion.
- Least recently used, LRU: a doubly-linked list, where new items are added
  at the head and items to expire are removed from the tail, plus a hash
  table for fast lookup of each list node.
- Hit: the Query API parses the query and checks the Memory Cache; the cache
  moves the entry to the front of the LRU list and returns the cached
  contents.
- Miss: the Query API uses the Reverse Index Service to find and rank
  matching documents, the Document Service for titles and snippets, then
  updates the Memory Cache, placing the entry at the front of the LRU list.
- Update when the page contents change, when a page is removed or added, and
  when the page rank changes. The simplest handling is a time to live, TTL:
  a maximum time an entry stays in the cache.
- Each machine has its own cache: simple, but a low cache hit rate.
- Each machine has a copy of the cache: simple, but an inefficient use of
  memory.
- The cache is sharded across all machines: more complex, and the best
  option; machine = hash(query), with consistent hashing.

ALSO TRUE
- The flow above is cache-aside.
