DRILL: Crawler Loop
TRAINS: design-web-crawler

Design a web crawler. The service crawls a list of urls, builds a reverse
index from words to pages, and a static title and snippet for each page; a
user searches a term and sees the matching pages. Assume 1 billion links, each
crawled about once a week, so 4 billion crawled per month, 500 KB stored per
page, and 100 billion searches per month.

Write the crawler loop, step by step, from taking a link to filing it as
crawled.

REQUIRED: the top ranked link, the signature check against crawled_links, the
lower priority on a match, the two queued jobs, the signature, the move from
links_to_crawl to crawled_links. Crawling a link before checking its signature
is the fail.

## Answer
