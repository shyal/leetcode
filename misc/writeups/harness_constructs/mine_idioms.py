"""Measure the recurring multi-line idioms in solved/ and the lines a one-line construct would save.

Run from the repo root: python3 misc/writeups/harness_constructs/mine_idioms.py
Numbers in ../harness_constructs.md come from this on 2026-09-17.
"""
import ast, collections, glob, re, sys

code = {}
for f in sorted(glob.glob("solved/*.py")):
    src = open(f).read()
    try:
        tree = ast.parse(src)
    except SyntaxError:
        continue
    lines = src.splitlines()
    code[f] = "\n".join(
        "\n".join(lines[n.lineno - 1 : n.end_lineno])
        for n in tree.body
        if isinstance(n, (ast.ClassDef, ast.FunctionDef))
    )
def span(n): return n.end_lineno - n.lineno + 1
def src(n): return ast.unparse(n)
def is_name(n, s=None): return isinstance(n, ast.Name) and (s is None or n.id == s)
def stmts(body):
    for st in body:
        yield st
        for a in ('body','orelse','finalbody'):
            if hasattr(st,a) and isinstance(getattr(st,a), list): yield from stmts(getattr(st,a))
R = collections.defaultdict(lambda: {'files':set(),'drill':0,'prob':0,'now':0,'after':0,'ex':[]})
def hit(k, f, now, after, ex):
    r=R[k]; key=f.split('/')[-1].split('_20')[0]; r['files'].add(key)
    r['drill' if key.startswith('d_') else 'prob']+=1; r['now']+=now; r['after']+=after
    if len(r['ex'])<4: r['ex'].append((key, ex))
def rangecall(n): return isinstance(n, ast.Call) and is_name(n.func,'range')
for f, c in code.items():
    try: t = ast.parse(c)
    except SyntaxError: continue
    for fn in [n for n in ast.walk(t) if isinstance(n, ast.FunctionDef)]:
        body = fn.body
        for st in stmts(body):
            # M1 binary search
            if isinstance(st, ast.While):
                inner = list(stmts(st.body))
                mids = [x for x in inner if isinstance(x, ast.Assign) and '// 2' in src(x.value)]
                if mids:
                    mid = src(mids[0].targets[0])
                    moves = [x for x in inner if isinstance(x, ast.Assign) and re.fullmatch(rf'{mid}( [+-] 1)?', src(x.value))]
                    if len(moves) >= 2:
                        idx = any(re.search(r'\w+\[' + re.escape(mid) + r'\]', src(x)) for x in inner)
                        hit('M1 binary search loop (index)' if idx else 'M1 binary search loop (answer)', f, span(st)+1, 2, src(st).split('\n')[0])
            # M2 linked list walk
            if isinstance(st, ast.While) and st.body:
                last = st.body[-1]
                if isinstance(last, ast.Assign) and len(last.targets)==1 and is_name(last.targets[0]) and isinstance(last.value, ast.Attribute) and last.value.attr=='next' and is_name(last.value.value, last.targets[0].id) and is_name(st.test, last.targets[0].id):
                    hit('M2 linked-list walk', f, 3, 1, src(st).split('\n')[0])
            # M4/M5 bfs
            if isinstance(st, ast.While):
                s = src(st)
                if 'popleft()' in s and '.left' in s and '.right' in s:
                    hit('M4 tree level-order bfs', f, span(st)+1, 1, s.split('\n')[0])
                elif 'popleft()' in s and ('add(' in s or '= True' in s) and 'not in' in s or ('popleft()' in s and 'seen' in s):
                    hit('M5 graph bfs with seen', f, span(st)+2, 1, s.split('\n')[0])
            # M9 children pairs
            if isinstance(st, ast.If) and isinstance(st.test, ast.Attribute) and st.test.attr=='left' and len(st.body)==1 and isinstance(st.body[0], ast.Expr):
                hit('M9 if n.left: push / if n.right: push', f, 4, 1, src(st))
            # M10 digits
            if isinstance(st, ast.While):
                s = src(st)
                if '% ' in s and '//= ' in s and 'append' in s and span(st)<=4:
                    hit('M10 digit peel loop', f, span(st)+1, 1, s.replace('\n',' | '))
            # M12 rectangular nested range / M15 triangular
            if isinstance(st, ast.For) and len(st.body)==1 and isinstance(st.body[0], ast.For):
                a, b = st, st.body[0]
                if rangecall(a.iter) and rangecall(b.iter):
                    if len(a.iter.args)==1 and len(b.iter.args)==1 and src(a.target) not in src(b.iter):
                        hit('M12 rectangular nested range', f, 2, 1, src(a).split('\n')[0]+' / '+src(b).split('\n')[0])
                    elif len(b.iter.args)==2 and src(b.iter.args[0]) in (f'{src(a.target)} + 1', src(a.target)):
                        hit('M15 triangular nested range -> pairs(n)', f, 2, 1, src(a).split('\n')[0]+' / '+src(b).split('\n')[0])
            # M8 adjacency build: for u, v in edges: X[u].append(v) [; X[v].append(u)]
            if isinstance(st, ast.For) and isinstance(st.target, ast.Tuple) and len(st.target.elts)==2 and 1<=len(st.body)<=2:
                ok = True
                for x in st.body:
                    if not (isinstance(x, ast.Expr) and isinstance(x.value, ast.Call) and isinstance(x.value.func, ast.Attribute) and x.value.func.attr in ('append','add') and isinstance(x.value.func.value, ast.Subscript)):
                        ok = False
                if ok:
                    hit('M8 adjacency build loop', f, span(st)+1, 1, src(st).replace('\n',' | '))
        # M3 void tree dfs / M17 graph dfs
        for st in stmts(body):
            if isinstance(st, ast.FunctionDef) and len(st.args.args)>=1:
                rets = [x for x in ast.walk(st) if isinstance(x, ast.Return)]
                s = src(st)
                calls = [x for x in ast.walk(st) if isinstance(x, ast.Call) and is_name(x.func, st.name)]
                if calls and all(r.value is None for r in rets):
                    if '.left' in s and '.right' in s:
                        hit('M3 void tree dfs', f, 5, 1, s.split('\n')[0]+' ... '+str(span(st))+' lines')
                    elif 'seen' in s or 'visited' in s:
                        hit('M17 void graph dfs with seen', f, 5, 1, s.split('\n')[0]+' ... '+str(span(st))+' lines')
                elif calls and rets and any(r.value is not None for r in rets) and ('.left' in s and '.right' in s):
                    hit('M3b returning tree dfs (tree DP)', f, 0, 0, s.split('\n')[0])
        # M6/M7/M14 loop+return collapses
        names0 = {src(x.targets[0]) for x in body if isinstance(x, ast.Assign) and isinstance(x.value, ast.Constant) and x.value.value==0}
        namesL = {src(x.targets[0]) for x in body if isinstance(x, ast.Assign) and isinstance(x.value, ast.List) and not x.value.elts}
        namesI = {src(x.targets[0]) for x in body if isinstance(x, ast.Assign) and ('inf' in src(x.value) or src(x.value) in ('0','-1'))}
        for i, st in enumerate(body):
            if isinstance(st, ast.For) and i+1 < len(body) and isinstance(body[i+1], ast.Return) and body[i+1].value is not None:
                rv = src(body[i+1].value)
                inner = st.body
                if len(inner)==1 and isinstance(inner[0], ast.If) and not inner[0].orelse:
                    inner = inner[0].body
                if len(inner)==1:
                    x = inner[0]
                    if rv in names0 and isinstance(x, ast.AugAssign) and src(x.target)==rv:
                        hit('M6 count loop -> sum(genexp)', f, span(st)+2, 1, src(st).replace('\n',' | ')[:90])
                    if rv in namesL and isinstance(x, ast.Expr) and isinstance(x.value, ast.Call) and isinstance(x.value.func, ast.Attribute) and x.value.func.attr=='append' and src(x.value.func.value)==rv:
                        hit('M7 res/append/return -> comprehension', f, span(st)+2, 1, src(st).replace('\n',' | ')[:90])
                    if rv in namesI and isinstance(x, ast.Assign) and src(x.targets[0])==rv and isinstance(x.value, ast.Call) and is_name(x.value.func) and x.value.func.id in ('max','min') and src(x.value.args[0])==rv:
                        hit('M14 pure running max loop -> max(genexp)', f, span(st)+2, 1, src(st).replace('\n',' | ')[:90])
        if body and isinstance(body[-1], ast.Return) and body[-1].value is not None and src(body[-1].value) in namesL:
            rv = src(body[-1].value)
            inner_defs = [x for x in body if isinstance(x, ast.FunctionDef)]
            if inner_defs and any(f'{rv}.append(' in src(d) for d in inner_defs):
                hit('M7b nested def appends to res -> @as_list', f, 3, 1, fn.name)
        # M16 interval merge: X[-1][1] = max(
        for st in stmts(body):
            if isinstance(st, ast.Assign) and isinstance(st.targets[0], ast.Subscript) and '[-1]' in src(st.targets[0]) and isinstance(st.value, ast.Call) and is_name(st.value.func,'max'):
                hit('M16 interval merge', f, 6, 1, src(st))
        # M18 kahn
        s = src(fn)
        if ('indeg' in s or 'in_deg' in s) and 'popleft' in s:
            hit('M18 Kahn toposort', f, 12, 2, fn.name)
        # M19 dijkstra
        if 'heappop' in s and ('dist' in s) and 'heappush' in s:
            hit('M19 dijkstra', f, 10, 2, fn.name)
        # M20 backtracking choose/undo triple
        for st in stmts(body):
            if isinstance(st, ast.For):
                b = [x for x in st.body if not isinstance(x, ast.If)]
                if len(b)==3 and isinstance(b[0], ast.Expr) and 'append' in src(b[0]) and isinstance(b[2], ast.Expr) and 'pop()' in src(b[2]):
                    hit('M20 choose / recurse / undo', f, 3, 2, src(st).replace('\n',' | ')[:80])
rows = sorted(R.items(), key=lambda kv: -(kv[1]['now']-kv[1]['after']))
tot=0
print(f"{'uniq':>4} {'drill':>5} {'prob':>4} {'now':>5} {'after':>5} {'saved':>5}  construct")
for k, r in rows:
    print(f"{len(r['files']):4d} {r['drill']:5d} {r['prob']:4d} {r['now']:5d} {r['after']:5d} {r['now']-r['after']:5d}  {k}")
    tot += r['now']-r['after']
print('total saved', tot)
if len(sys.argv)>1:
    for k, r in rows:
        print('\n##', k)
        for e in r['ex']: print('   ', e)
