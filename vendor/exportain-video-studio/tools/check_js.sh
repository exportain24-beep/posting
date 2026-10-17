#!/usr/bin/env bash
# Syntax-check the scripts inside the built scenes.html (run after build.sh). Usage: bash check_js.sh [project_dir]
cd "${1:-.}"; python3 - <<'PY'
import re,subprocess,tempfile
s=open('scenes.html',encoding='utf-8').read()
js='\n'.join(re.findall(r'<script>(.*?)</script>',s,re.S))
f=tempfile.NamedTemporaryFile('w',suffix='.js',delete=False,encoding='utf-8');f.write(js);f.close()
r=subprocess.run(['node','--check',f.name],capture_output=True,text=True)
print(r.stderr[:1500] or 'JS OK')
PY
grep -n '\${0}' js/*.js && echo "WARNING: \${0} placeholder left in JS (run: sed -i 's/\\\${0}+//g; s/\\\${0}||//g' js/3_a.js js/4_b.js)" || true
grep -nE "(tx|lat|kw|pill|icon|check|cross)\([0-9]+,\\$\{" js/3_a.js js/4_b.js 2>/dev/null | head -5 | sed 's/^/WARNING nested \${} as argument (write the bare expression): /' || true
