-- QUERY: Verdicts With Dates
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
-- Return every verdict with the date it was recorded on, newest first. The
-- date lives in solves, the verdict in verdicts, and they share the
-- file column.
-- Columns: date, verdict.
--
-- REQUIRED: one JOIN ... ON. NO subquery.

select m.verdict, e.date
    from solves as e
    join verdicts as m on e.file = m.file
    order by e.date desc;