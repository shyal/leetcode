REFERENCE: d261 Crawler Recrawl
SOURCE: System Design Primer, "Design a web crawler" https://github.com/donnemartin/system-design-primer/blob/master/solutions/system_design/web_crawler/README.md

REQUIRED
- Recrawl: keep a timestamp of the last crawl per page; refresh every page
  after a default period, say one week, and frequently updated or popular
  sites sooner.

ALSO TRUE
- A Robots.txt file gives webmasters control of the crawl frequency.
