Design a web crawler. The service crawls a list of urls, builds a reverse
index from words to pages, and a static title and snippet for each page; a
user searches a term and sees the matching pages. Assume 1 billion links, each
crawled about once a week, so 4 billion crawled per month, 500 KB stored per
page, and 100 billion searches per month.

Say how the crawler decides when to crawl a page again.

REQUIRED: the timestamp of the last crawl, a default period, sooner for
popular or frequently updated sites. One fixed period for every page is the
fail.

## Answer
