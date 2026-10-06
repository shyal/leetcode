REFERENCE: d241 Mint
SOURCE: System Design Primer, "Design Mint.com" https://github.com/donnemartin/system-design-primer/blob/master/solutions/system_design/mint/README.md

REQUIRED
- 2,000 transactions per second, 200 read requests per second, 250 GB of new
  content per month; write heavy, 10:1 write to read.
- Extract when the user first links the account, when the user manually
  refreshes it, and automatically each day for users active in the past 30
  days.
- Client to Web Server to Accounts API, which places a job on a Queue such
  as SQS or RabbitMQ, because extracting transactions can take a while and
  is done asynchronously.
- The Transaction Extraction Service pulls from the Queue, extracts the
  transactions from the financial institution and stores them as raw log
  files in the Object Store.
- It uses the Category Service to categorise each transaction and the Budget
  Service to compute aggregate monthly spending by category; the Budget
  Service uses the Notification Service when a user nears or exceeds the
  budget.
- It updates the SQL transactions table and the monthly_spending table, then
  notifies the user that the transactions are complete.
- Category: a seller-to-category dictionary seeded with the most popular
  sellers. 50,000 sellers at under 255 bytes each is about 12 MB of memory.
  Sellers not seeded are learned from the users' manual overrides.
- Budget: a generic budget template that allocates category amounts by
  income tier; only the categories a user overrides are stored.
- Writes: 2,000 per second is tough for a single SQL Write Master-Slave, so
  apply SQL scaling patterns, federation, sharding, denormalization, SQL
  tuning, and consider moving data to NoSQL; keep only a month of
  transactions in the database and the rest in a data warehouse or the
  Object Store.

ALSO TRUE
- MapReduce over the raw transaction files can categorise and aggregate,
  taking load off the database.
- Reads of summaries and recent transactions go through a Memory Cache,
  cache-aside.
