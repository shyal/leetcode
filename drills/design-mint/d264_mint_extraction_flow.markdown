Design Mint.com. A user connects a financial account; the service extracts its
transactions daily, categorises each one, computes monthly spending by
category, recommends a budget and notifies the user near or over budget.
Assume 10 million users, 30 million accounts, 5 billion transactions per
month, 500 million read requests per month, 50 bytes per transaction and
50,000 sellers.

Write the extraction flow from the request to the stored result, component by
component, and say why it has a queue.

REQUIRED: the Accounts API, the queue because extraction is slow, the
Transaction Extraction Service, raw logs in the object store, the Category and
Budget Services, the two SQL tables, the notification. Extracting inside the
request is the fail.

## Answer
