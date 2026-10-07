REFERENCE: d258 Crawler Link Stores
SOURCE: System Design Primer, "Design a web crawler" https://github.com/donnemartin/system-design-primer/blob/master/solutions/system_design/web_crawler/README.md

REQUIRED
- links_to_crawl, ranked by site popularity, and crawled_links, the processed
  links with their page signatures; both in a key-value NoSQL Database, the
  ranking in Redis sorted sets.
