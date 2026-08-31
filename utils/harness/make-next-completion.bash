# bash completion for `make next ...` in this repo.
# source it from ~/.bashrc:  . ~/dev/leet/utils/harness/make-next-completion.bash
# After `make next`, tab offers the group names from graph/nodes.json and the
# switches (cram early assisted prepare graph why). Anywhere else, the make
# targets. Works on bash 3.2.

_leet_make_next() {
    local cur prev words groups switches root
    cur="${COMP_WORDS[COMP_CWORD]}"
    root="$PWD"
    while [ "$root" != "/" ] && [ ! -f "$root/graph/nodes.json" ]; do
        root=$(dirname "$root")
    done
    if [ "${COMP_WORDS[1]}" = "next" ] && [ -f "$root/graph/nodes.json" ]; then
        groups=$(sed -n 's/^ *"group": *"\([^"]*\)".*/\1/p' "$root/graph/nodes.json" | sort -u)
        switches="cram early assisted prepare graph why"
        COMPREPLY=( $(compgen -W "$groups $switches" -- "$cur") )
        return 0
    fi
    words=$(grep -o '^[a-zA-Z][a-zA-Z0-9_-]*:' "$root/Makefile" 2>/dev/null | tr -d ':' | sort -u)
    COMPREPLY=( $(compgen -W "$words" -- "$cur") )
}
complete -F _leet_make_next make
