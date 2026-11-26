#!/usr/bin/env python3
"""Extract inline scripts and validate syntax with Node.js on the GitHub Actions runner."""
from pathlib import Path
import re, subprocess, tempfile

import sys
source=(Path(__file__).resolve().parents[1]/(sys.argv[1] if len(sys.argv)>1 else 'index.html')).read_text(encoding='utf-8')
scripts=re.findall(r'<script(?:\s[^>]*)?>(.*?)</script\s*>',source,re.I|re.S)
if not scripts:
    raise SystemExit('FAIL No inline JavaScript found')
for i,script in enumerate(scripts,1):
    with tempfile.NamedTemporaryFile(mode='w',suffix='.js',encoding='utf-8') as temp:
        temp.write(script)
        temp.flush()
        subprocess.run(['node','--check',temp.name],check=True)
    print(f'PASS JavaScript syntax block {i}')
