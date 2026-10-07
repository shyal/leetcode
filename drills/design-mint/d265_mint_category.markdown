DRILL: Mint Category
TRAINS: design-mint

Design Mint.com. A user connects a financial account; the service extracts its
transactions daily, categorises each one, computes monthly spending by
category, recommends a budget and notifies the user near or over budget.
Assume 10 million users, 30 million accounts, 5 billion transactions per
month, 500 million read requests per month, 50 bytes per transaction and
50,000 sellers.

Say how a transaction gets its category and how large that structure is.

REQUIRED: the seller-to-category dictionary of about 12 MB, overrides for the
rest. A database lookup per transaction is the fail.

## Answer
