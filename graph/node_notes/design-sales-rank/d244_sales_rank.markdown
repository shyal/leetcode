REFERENCE: d244 Sales Rank
SOURCE: System Design Primer, "Design Amazon's sales rank by category feature" https://github.com/donnemartin/system-design-primer/blob/master/solutions/system_design/sales_rank/README.md

REQUIRED
- 400 transactions per second, 40,000 read requests per second, 40 GB of new
  content per month.
- The raw Sales API server log files are stored in a managed Object Store
  such as S3.
- MapReduce step 1: transform the data to (category, product_id),
  sum(quantity).
- MapReduce step 2: a distributed sort.
- The sorted result is inserted into an aggregate sales_rank table in a SQL
  Database, indexed on id, category_id and product_id.
- Read: Client to Web Server to Read API server, which reads the sales_rank
  table.
- Reads: a Memory Cache serves popular content and absorbs uneven traffic;
  at 40,000 reads per second the SQL Read Replicas may not handle the cache
  misses, so further SQL scaling patterns are needed.
- Writes: 400 per second may be tough for a single SQL Write Master-Slave,
  which also calls for further scaling, federation, sharding,
  denormalization, SQL tuning, or moving data to NoSQL.

ALSO TRUE
- Keep a limited period of data in the database and the rest in a data
  warehouse or the Object Store.
- 100:1 read to write ratio.
