#!/bin/bash
# The check of the stage judge (kg_stage) against the real model.
#
#   utils/rs/kg_stage/check.sh [RUNS] [PATTERN]
#
# Each file in cases/ is a current.mu at stage 1 or 2. The first word of its
# name is the verdict that the judge must give:
#   pass   the plan is correct and fast enough
#   slow   the plan is correct and too slow for the constraints
#   wrong  the plan is not correct (and the judge must not call it slow)
# Each case is judged RUNS times (default 1). PATTERN selects cases by name.
# The exit code is the number of runs with a different verdict.
cd "$(dirname "$0")/../../.." || exit 2
BIN=utils/rs/target/release/kg_stage
RUNS=${1:-1}
OUT=$(mktemp -d)
for f in utils/rs/kg_stage/cases/*${2:-}*.mu; do
  for r in $(seq "$RUNS"); do echo "$f $r"; done
done | xargs -P 8 -n 2 sh -c '
  name=$(basename "$0" .mu)
  "'"$BIN"'" --judge "$0" > "'"$OUT"'/$name.$1" 2> "'"$OUT"'/$name.$1.err" || echo "{\"verdict\": \"error\"}" > "'"$OUT"'/$name.$1"
'
bad=0
for f in utils/rs/kg_stage/cases/*${2:-}*.mu; do
  name=$(basename "$f" .mu)
  want=${name%%_*}
  for r in $(seq "$RUNS"); do
    got=$(sed -n 's/.*"verdict":"\([a-z]*\)".*/\1/p' "$OUT/$name.$r")
    ops=$(sed -n 's/.*"operations":\([0-9.e+]*\).*/\1/p' "$OUT/$name.$r")
    if [ "$got" = "$want" ]; then mark=ok; else mark=BAD; bad=$((bad + 1)); fi
    printf '%-4s %-34s want %-5s got %-5s ops %s\n' "$mark" "$name" "$want" "$got" "$ops"
    [ "$mark" = BAD ] && sed 's/^/       /' "$OUT/$name.$r" "$OUT/$name.$r.err"
  done
done
echo "$bad runs with a different verdict. Raw output: $OUT"
exit "$bad"
