DRILL: Crawler Scaled
TRAINS: design-web-crawler

Design a web crawler. The service crawls a list of urls, builds a reverse
index from words to pages, and a static title and snippet for each page; a
user searches a term and sees the matching pages. Assume 1 billion links, each
crawled about once a week, so 4 billion crawled per month, 500 KB stored per
page, and 100 billion searches per month.

Give two measures that scale the crawler.

REQUIRED: two measures. Leaving DNS lookup to the operating system on every
crawl is the fail.

## Answer
