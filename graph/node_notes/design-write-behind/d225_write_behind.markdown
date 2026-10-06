REFERENCE: d225 Write Behind
SOURCE: System Design Primer, "Write-behind (write-back)" https://github.com/donnemartin/system-design-primer#write-behind-write-back

REQUIRED
- The application adds or updates the entry in the cache.
- The entry is written to the data store asynchronously.
- It improves write performance.
- Disadvantage: data can be lost if the cache goes down before its contents
  reach the data store.
- Disadvantage: it is more complex to implement than cache-aside or
  write-through.
