REFERENCE: d275 Query Cache Updates
SOURCE: System Design Primer, "Design a key-value cache to save the results of the most recent web server queries" https://github.com/donnemartin/system-design-primer/blob/master/solutions/system_design/query_cache/README.md

REQUIRED
- Update when the page contents change, when a page is removed or added, and
  when the page rank changes. The simplest handling is a time to live, TTL: a
  maximum time an entry stays in the cache.
