#!/bin/bash
# Usage: research/publish.sh "commit message" slug1 slug2 ...  (merge, mark ready, build, validate, push, GSC submit)
set -e
cd "$(dirname "$0")/.."
MSG="$1"; shift
(cd research && PYTHONIOENCODING=utf-8 python -X utf8 merge.py "$@" | tail -n "$#")
python -X utf8 - "$@" <<'PY'
import json,sys
f='data/site.json';s=json.load(open(f,encoding='utf-8'));S=set(sys.argv[1:])
for p in s['protocols']:
  for x in p['subs']:
    if x['slug'] in S: x['ready']=True
open(f,'w',encoding='utf-8').write(json.dumps(s,indent=2,ensure_ascii=False)+'\n')
PY
python -X utf8 build.py | tail -1
python -X utf8 - "$@" <<'PY'
import re,os,sys
bad=0
for f in os.listdir('docs'):
    if not f.endswith('.html'): continue
    t=open('docs/'+f,encoding='utf-8').read()
    for h in re.findall(r'href="([^"#:?]+\.html)',t):
        if not os.path.exists('docs/'+h): bad+=1; print('broken',f,h)
    for a in re.findall(r'amazon\.com/dp/[A-Z0-9]+[^"]*',t):
        if 'tag=themisreviews-20' not in a: bad+=1; print('notag',f)
for s in sys.argv[1:]:
    t=open(f'docs/{s}.html',encoding='utf-8').read()
    if '>None<' in t: bad+=1; print('None cell in',s)
print('problems',bad); sys.exit(1 if bad else 0)
PY
for i in 1 2 3; do rm -f .git/index.lock; git add -A && break; sleep 3; done
git commit -qm "$MSG

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
git push -q origin main
git log --oneline -1
