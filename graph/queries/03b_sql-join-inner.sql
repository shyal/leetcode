-- QUERY: Verdicts With Titles
-- TRAINS: sql-join-inner
--
-- Tables:
--
--     solves
--         file     TEXT
--         date     TEXT
--         problem  TEXT
--         assist   TEXT
--         note     TEXT
--
--     verdicts
--         file     TEXT
--         node_id  TEXT
--         verdict  TEXT
--
--     problems
--         num         TEXT
--         title       TEXT
--         difficulty  TEXT
--         source      TEXT
--         note        TEXT
--         banned      INTEGER
--
-- Return every verdict with the title of the problem it was recorded on.
-- verdicts reaches problems through solves: file matches
-- verdicts, problem matches problems.num.
-- Columns: title, verdict.
--
-- REQUIRED: two JOIN ... ON lines. NO subquery.

 select v.verdict, p.title
    from solves as s
    join verdicts as v on s.file = v.file
    join problems as p on s.problem = p.num;