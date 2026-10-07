REFERENCE: d238 Pastebin Numbers
SOURCE: System Design Primer, "Design Pastebin.com (or Bit.ly)" https://github.com/donnemartin/system-design-primer/blob/master/solutions/system_design/pastebin/README.md

REQUIRED
- 4 paste writes per second, 40 reads per second, 12.7 GB of new content per
  month: 1.27 KB * 10 million.

ALSO TRUE
- Handy conversion: 2.5 million seconds per month; 400 requests per second is
  1 billion per month.
