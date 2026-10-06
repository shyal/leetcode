DRILL: Mint
TRAINS: design-mint

Design Mint.com. A user connects a financial account; the service extracts
its transactions daily, categorises each one, computes monthly spending by
category, recommends a budget and notifies the user near or over budget.
Assume 10 million users, 30 million accounts, 5 billion transactions per
month, 500 million read requests per month, 50 bytes per transaction and
50,000 sellers. Write: (1) transactions per second, reads per second, new
content per month, and whether the system is read heavy or write heavy; (2)
the three cases in which transactions are extracted; (3) the extraction flow
from the request to the stored result, and why it has a queue; (4) how a
transaction gets its category and how large that structure is; (5) how the
budget avoids storing 100 million items; (6) what is done about the write
load.

REQUIRED: four facts, three triggers, the queued flow with the object store
and the two tables, the seller dictionary of about 12 MB, the template with
overrides, the scaling of writes. Extracting inside the request is the fail.

## Answer
