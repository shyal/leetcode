Design a paste service. A user enters a block of text and gets a randomly
generated link; a user enters a link and views the paste; a paste can expire.
Assume 10 million paste writes and 100 million paste reads per month, text
only, and 1.27 KB stored per paste.

Write the path of a read request, component by component.

REQUIRED: the components in order, the lookup before the fetch, the error when
the url is missing. Fetching from the object store before the SQL lookup is
the fail.

## Answer
