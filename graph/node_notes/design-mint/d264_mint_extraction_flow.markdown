REFERENCE: d264 Mint Extraction Flow
SOURCE: System Design Primer, "Design Mint.com" https://github.com/donnemartin/system-design-primer/blob/master/solutions/system_design/mint/README.md

REQUIRED
- Client to Web Server to Accounts API, which places a job on a Queue such as
  SQS or RabbitMQ, because extracting transactions can take a while and is
  done asynchronously.
- The Transaction Extraction Service pulls from the Queue, extracts the
  transactions from the financial institution and stores them as raw log files
  in the Object Store.
- It uses the Category Service to categorise each transaction and the Budget
  Service to compute aggregate monthly spending by category; the Budget
  Service uses the Notification Service when a user nears or exceeds the
  budget.
- It updates the SQL transactions table and the monthly_spending table, then
  notifies the user that the transactions are complete.
