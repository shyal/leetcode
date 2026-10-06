REFERENCE: d240 Web Crawler
SOURCE: System Design Primer, "Design a web crawler" https://github.com/donnemartin/system-design-primer/blob/master/solutions/system_design/web_crawler/README.md

REQUIRED
- 2 PB of stored page content per month: 500 KB * 4 billion. 1,600 write
  requests per second. 40,000 search requests per second.
- links_to_crawl, ranked by site popularity, and crawled_links, the
  processed links with their page signatures; both in a key-value NoSQL
  Database, the ranking in Redis sorted sets.
- Loop: take the top ranked link; check crawled_links for an entry with a
  similar page signature.
- If a similar page exists, reduce the priority of the link, which prevents
  a cycle, and continue.
- Otherwise crawl the link: add a job to the Reverse Index Service queue;
  add a job to the Document Service queue for the title and snippet;
  generate the page signature; remove the link from links_to_crawl; insert
  the link and its signature into crawled_links.
- Duplicate urls: with 1 billion links, a MapReduce that outputs only
  entries with a frequency of 1.
- Duplicate content: generate a signature from the contents of the page and
  compare signatures for similarity, with the Jaccard index or cosine
  similarity.
- Recrawl: keep a timestamp of the last crawl per page; refresh every page
  after a default period, say one week, and frequently updated or popular
  sites sooner.
- Two scaling measures out of: a Memory Cache for popular queries; sharding
  and federation of the Reverse Index Service and the Document Service; the
  crawler keeps its own DNS lookup, refreshed periodically, since DNS lookup
  is a bottleneck; connection pooling; enough bandwidth.

ALSO TRUE
- A Robots.txt file gives webmasters control of the crawl frequency.
- Search: Query API parses the query, the Reverse Index Service finds and
  ranks matching documents, the Document Service returns titles and
  snippets.
