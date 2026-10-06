DRILL: Web Crawler
TRAINS: design-web-crawler

Design a web crawler. The service crawls a list of urls, builds a reverse
index from words to pages, and a static title and snippet for each page; a
user searches a term and sees the matching pages. Assume 1 billion links,
each crawled about once a week, so 4 billion crawled per month, 500 KB
stored per page, and 100 billion searches per month. Write: (1) the stored
content per month, the write requests per second and the searches per
second; (2) the two collections of links and where they are stored; (3) the
crawler loop, step by step; (4) how the crawler avoids an infinite loop, for
duplicate urls and for duplicate content; (5) how it decides when to crawl a
page again; (6) two measures that scale it.

REQUIRED: three numbers, links_to_crawl and crawled_links, the loop with the
signature check, both kinds of duplicate, the timestamp, two scaling
measures. Detecting duplicates by url alone is the fail.

## Answer
