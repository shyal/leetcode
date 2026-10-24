Design a web crawler. The service crawls a list of urls, builds a reverse
index from words to pages, and a static title and snippet for each page; a
user searches a term and sees the matching pages. Assume 1 billion links, each
crawled about once a week, so 4 billion crawled per month, 500 KB stored per
page, and 100 billion searches per month.

Name the two collections of links the crawler stores, what each holds, and
where they are stored.

REQUIRED: links_to_crawl ranked by popularity, crawled_links with page
signatures, a key-value store with the ranking in Redis sorted sets. A
single list of links is the fail.

## Answer
