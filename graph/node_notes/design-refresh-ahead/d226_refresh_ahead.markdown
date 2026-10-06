REFERENCE: d226 Refresh Ahead
SOURCE: System Design Primer, "Refresh-ahead" https://github.com/donnemartin/system-design-primer#refresh-ahead

REQUIRED
- The cache automatically refreshes any recently accessed entry before it
  expires.
- It reduces latency, compared with read-through, if the cache can
  accurately predict which items will be needed in the future.
- Disadvantage: inaccurate prediction gives worse performance than no
  refresh-ahead at all.
