DRILL: Mint Writes
TRAINS: design-mint

Design Mint.com. A user connects a financial account; the service extracts its
transactions daily, categorises each one, computes monthly spending by
category, recommends a budget and notifies the user near or over budget.
Assume 10 million users, 30 million accounts, 5 billion transactions per
month, 500 million read requests per month, 50 bytes per transaction and
50,000 sellers.

Say what is done about the write load.

REQUIRED: the SQL scaling patterns, NoSQL considered, a month of transactions
kept in the database. One SQL master taking 2,000 writes per second is the
fail.

## Answer
