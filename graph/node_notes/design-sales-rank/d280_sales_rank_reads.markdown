REFERENCE: d280 Sales Rank Reads
SOURCE: System Design Primer, "Design Amazon's sales rank by category feature" https://github.com/donnemartin/system-design-primer/blob/master/solutions/system_design/sales_rank/README.md

REQUIRED
- Reads: a Memory Cache serves popular content and absorbs uneven traffic; at
  40,000 reads per second the SQL Read Replicas may not handle the cache
  misses, so further SQL scaling patterns are needed.
