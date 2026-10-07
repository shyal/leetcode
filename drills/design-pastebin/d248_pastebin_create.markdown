DRILL: Pastebin Create
TRAINS: design-pastebin

Design a paste service. A user enters a block of text and gets a randomly
generated link; a user enters a link and views the paste; a paste can expire.
Assume 10 million paste writes and 100 million paste reads per month, text
only, and 1.27 KB stored per paste.

Write the path of a create request, component by component. Say where the text
is stored and where the metadata is stored.

REQUIRED: the components in order, the SQL row for the metadata, the object
store for the text. Storing the paste text in the SQL row is the fail.

## Answer
