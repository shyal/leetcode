REFERENCE: d223 Cache Aside
SOURCE: System Design Primer, "Cache-aside" https://github.com/donnemartin/system-design-primer#cache-aside

REQUIRED
- Look for the entry in the cache, which misses.
- Load the entry from the database.
- Add the entry to the cache.
- Return the entry.
- The application reads and writes storage; the cache does not interact with
  storage directly.
- It is also called lazy loading: only requested data is cached, so the
  cache is not filled with data nobody asks for.
- Two disadvantages out of: each cache miss costs three trips, a noticeable
  delay; data becomes stale when it is updated in the database; when a node
  fails it is replaced by a new, empty node, which increases latency.
- Staleness is bounded by a time to live, TTL, that forces an update of the
  entry, or by using write-through.

ALSO TRUE
- Memcached is generally used this way.
