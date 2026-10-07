REFERENCE: d262 Crawler Scaled
SOURCE: System Design Primer, "Design a web crawler" https://github.com/donnemartin/system-design-primer/blob/master/solutions/system_design/web_crawler/README.md

REQUIRED
- Two scaling measures out of: a Memory Cache for popular queries; sharding
  and federation of the Reverse Index Service and the Document Service; the
  crawler keeps its own DNS lookup, refreshed periodically, since DNS lookup
  is a bottleneck; connection pooling; enough bandwidth.

ALSO TRUE
- Search: Query API parses the query, the Reverse Index Service finds and
  ranks matching documents, the Document Service returns titles and snippets.
