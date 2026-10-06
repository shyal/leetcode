REFERENCE: d238 Pastebin
SOURCE: System Design Primer, "Design Pastebin.com (or Bit.ly)" https://github.com/donnemartin/system-design-primer/blob/master/solutions/system_design/pastebin/README.md

REQUIRED
- 4 paste writes per second, 40 reads per second, 12.7 GB of new content per
  month: 1.27 KB * 10 million.
- Create: the Client sends the request to the Web Server, a reverse proxy,
  which forwards it to the Write API server.
- The Write API generates a unique url, checking the SQL Database for a
  duplicate and generating another if it is taken; saves a row to the SQL
  pastes table; saves the paste data to the Object Store; returns the url.
- The SQL Database works as a large hash table from the shortlink to the
  path of the paste file; the contents live in an Object Store such as S3.
- The link: take the MD5 hash of the user's IP address plus a timestamp,
  Base 62 encode it, keep the first 7 characters. 62^7 values cover the 360
  million shortlinks of 3 years.
- Read: Client to Web Server to Read API server, which looks the url up in
  the SQL Database; if it is there, it fetches the contents from the Object
  Store; otherwise it returns an error.
- Expiry: scan the SQL Database for entries whose expiration timestamp is
  older than now, and delete them or mark them expired.
- Scaled: a Memory Cache handles the popular content and the uneven traffic;
  SQL Read Replicas handle the cache misses; a single SQL Write Master-Slave
  handles 4 writes per second.

ALSO TRUE
- Base 62 encodes to [a-zA-Z0-9], which needs no escaping in a url; Base 64
  adds + and /.
- Page analytics need not be realtime: MapReduce over the Web Server logs
  gives the hit counts.
- Handy conversion: 2.5 million seconds per month; 400 requests per second
  is 1 billion per month.
- Scale iteratively: benchmark, profile for bottlenecks, address them
  weighing alternatives, repeat.
