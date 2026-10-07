REFERENCE: d260 Crawler Duplicates
SOURCE: System Design Primer, "Design a web crawler" https://github.com/donnemartin/system-design-primer/blob/master/solutions/system_design/web_crawler/README.md

REQUIRED
- Duplicate urls: with 1 billion links, a MapReduce that outputs only entries
  with a frequency of 1.
- Duplicate content: generate a signature from the contents of the page and
  compare signatures for similarity, with the Jaccard index or cosine
  similarity.
