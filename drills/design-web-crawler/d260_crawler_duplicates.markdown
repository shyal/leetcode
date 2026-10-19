DRILL: Crawler Duplicates
TRAINS: design-web-crawler

Design a web crawler. The service crawls a list of urls, builds a reverse
index from words to pages, and a static title and snippet for each page; a
user searches a term and sees the matching pages. Assume 1 billion links, each
crawled about once a week, so 4 billion crawled per month, 500 KB stored per
page, and 100 billion searches per month.

Say how the crawler avoids an infinite loop: how it removes duplicate urls,
and how it detects duplicate content.

REQUIRED: the MapReduce that outputs the urls with frequency 1, a content signature
compared by Jaccard index or cosine similarity. Detecting duplicates by url
alone is the fail.

## Answer
