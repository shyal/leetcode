REFERENCE: d259 Crawler Loop
SOURCE: System Design Primer, "Design a web crawler" https://github.com/donnemartin/system-design-primer/blob/master/solutions/system_design/web_crawler/README.md

REQUIRED
- Loop: take the top ranked link; check crawled_links for an entry with a
  similar page signature.
- If a similar page exists, reduce the priority of the link, which prevents a
  cycle, and continue.
- Otherwise crawl the link: add a job to the Reverse Index Service queue; add
  a job to the Document Service queue for the title and snippet; generate the
  page signature; remove the link from links_to_crawl; insert the link and its
  signature into crawled_links.
