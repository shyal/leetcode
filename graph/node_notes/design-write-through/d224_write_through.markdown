REFERENCE: d224 Write Through
SOURCE: System Design Primer, "Write-through" https://github.com/donnemartin/system-design-primer#write-through

REQUIRED
- The application adds or updates the entry in the cache.
- The cache synchronously writes the entry to the data store.
- Return.
- The application uses the cache as its main data store; the cache is
  responsible for reading and writing to the database.
- The write is slow overall, but later reads of the data just written are
  fast, and data in the cache is not stale.
- Disadvantage: a new node, created after a failure or for scaling, caches
  nothing until an entry is updated in the database; cache-aside together
  with write-through mitigates this.
- Disadvantage: most data written might never be read; a TTL minimises this.

ALSO TRUE
- Users generally tolerate latency better when updating data than when
  reading it.
