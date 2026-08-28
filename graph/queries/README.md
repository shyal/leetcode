# graph/queries

SQL drills against the mirror (`graph/leet.db`, built by `make mirror`).
One file per sql node, numbered in prereq order, each header a real question
about the graph. The body is yours to write.

    make q            list the queries
    make q 07         run graph/queries/07_*.sql
    make q anti       run the one whose name contains 'anti'

Inside litecli: `.read graph/queries/07_sql-conditional-aggregate.sql`.
