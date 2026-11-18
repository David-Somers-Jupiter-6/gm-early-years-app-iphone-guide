"""Guide 2.89 (from 2.88). Section 3 page 1 "Before you sign in" (David, 18 Nov): the diagram was confusing.
 Swap to the worked example (mockup C), without the "Sign in to check your details" button, with the words first:
   1. Your details must be exactly the same in NHS login and the GM Early Years App.
   2. (space) Same details: you can sign in.  /  Different details: ask your HV team.
   3. (space) For example:  two quiet example account cards (made-up details) with "=" between.
 The cards are calmer than in the mockup (tinted headers, thin coloured top edge) so the text leads.
 The 2.87 diagram styles are removed.
usage: python3 make289.py v2.88.html v2.89.html
"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
def page(pid):
    m = re.search(r'<section class="screen(?: cover)?" id="%s".*?</section>' % re.escape(pid), s, re.S); assert m, pid; return m
def edit(pid, a, b, n=1):
    global s
    m = page(pid); blk = m.group(0)
    assert blk.count(a) == n, (pid, a[:90], blk.count(a))
    s = s[:m.start()] + blk.replace(a, b) + s[m.end():]

TICK = ('<svg viewBox="0 0 20 20" width="12" height="12" aria-hidden="true"><path d="M4.5 10.4l3.6 3.5 7.4-7.6" '
        'fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>')
CROSS = ('<svg viewBox="0 0 20 20" width="12" height="12" aria-hidden="true"><path d="M5.5 5.5l9 9M14.5 5.5l-9 9" '
         'fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round"/></svg>')
FIELDS = [('Given name', 'Charlotte'), ('Surname', 'Somers'), ('NHS number', '485 777 3456'),
          ('Mobile', '07700 900123'), ('Email', 'c.somers@<wbr>example.com')]
def card(cls, title):
    return ('<div class="exc %s"><div class="exc-h">%s</div>%s</div>'
            % (cls, title, ''.join('<div class="exc-r"><span class="exc-k">%s</span><span class="exc-v">%s</span></div>' % kv for kv in FIELDS)))
ALT = ('Example: in NHS login and in the GM Early Years App the details are the same – given name Charlotte, surname Somers, '
       'NHS number 485 777 3456, mobile 07700 900123, email c.somers@example.com.')
BODY = ('<p class="lead ex-lead">Your details must be <strong>exactly the same</strong> in <strong>NHS login</strong> and the <strong>GM Early Years App</strong>.</p>\n'
        '<ul class="ex-out">'
        '<li class="ex-ok"><span class="ex-i">' + TICK + '</span><span><strong>Same details:</strong> you can sign in.</span></li>'
        '<li class="ex-no"><span class="ex-i">' + CROSS + '</span><span><strong>Different details:</strong> ask your <a href="#hv">HV team</a>.</span></li>'
        '</ul>\n'
        '<p class="ex-for">For example:</p>\n'
        '<div class="exw" role="img" aria-label="' + ALT + '">' + card('exc-n', 'NHS login') + '<span class="exw-eq" aria-hidden="true">=</span>'
        + card('exc-a', 'GM Early Years App') + '</div>')
nhs = page('nhs').group(0)
i = nhs.find('<p class="lead mx-lead">'); j = nhs.find('</a>', nhs.find('<a class="match-go"', i)) + 4
edit('nhs', nhs[i:j], BODY)

# remove the 2.87 diagram styles (from its comment to the end of its print rule)
a = s.find('/* 2.87 Section 3 start page'); b = s.find('@media print{.match-go{display:none}}') + len('@media print{.match-go{display:none}}')
assert 0 < a < b and b - a < 6000, (a, b); s = s[:a] + s[b:].lstrip('\n')
assert 'mx-' not in s and 'match-go' not in s

CSS = '''/* 2.89 Section 3 page 1: worked example */
#app #nhs .ex-lead{color:var(--ink);margin:0}
#app #nhs .ex-out{list-style:none;margin:18px 0 0;padding:0}
#app #nhs .ex-out li{display:flex;align-items:flex-start;gap:10px;margin:0 0 8px;padding:0;color:var(--ink)}
#app #nhs .ex-out li:last-child{margin-bottom:0}
#app #nhs .ex-i{flex:0 0 22px;width:22px;height:22px;margin-top:2px;border-radius:50%;color:#fff;display:flex;align-items:center;justify-content:center}
#app #nhs .ex-ok .ex-i{background:#00703c}#app #nhs .ex-no .ex-i{background:#b3261e}
#app #nhs .ex-for{margin:20px 0 8px;color:var(--sub)}
#app #nhs .exw{display:grid;grid-template-columns:minmax(0,1fr) 12px minmax(0,1fr);align-items:center;gap:3px}
#app #nhs .exc{border:1px solid var(--line);border-radius:12px;overflow:hidden;background:var(--surface)}
#app #nhs .exc-h{font-family:var(--font-head);font-weight:700;font-size:13px;line-height:1.2;padding:5px 7px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
#app #nhs .exc-n{border-top:3px solid #005eb8}#app #nhs .exc-n .exc-h{color:#005eb8;background:rgba(0,94,184,.08)}
#app #nhs .exc-a{border-top:3px solid #c0174e}#app #nhs .exc-a .exc-h{color:#a3123f;background:rgba(192,23,78,.07)}
#app #nhs .exc-r{padding:2px 7px;border-top:1px solid var(--line)}
#app #nhs .exc-k{display:block;font-size:11.5px;line-height:1.2;color:var(--sub)}
#app #nhs .exc-v{display:block;font-size:13.5px;line-height:1.3;color:var(--ink);font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
#app #nhs .exc-r:last-child .exc-v{white-space:normal;overflow-wrap:normal}
@media screen and (max-height:600px){#app #nhs .ex-out{margin-top:12px}#app #nhs .ex-out li{margin-bottom:6px}#app #nhs .ex-for{margin:14px 0 6px}#app #nhs .exc-r{padding:1px 7px}}
@media screen and (max-width:340px){#app #nhs .exc-h{font-size:12px}}
#app #nhs .exw-eq{font-family:var(--font-head);font-weight:800;font-size:20px;color:var(--sub);text-align:center}
'''
rep('/* 2.88 Step 1:', CSS + '/* 2.88 Step 1:', 1)
_i = s.find('@media print{'); _css = s[s.rfind('<style', 0, _i):_i]
assert _css.count('{') == _css.count('}'), 'unbalanced CSS before @media print'
assert s.count('@media print{') == 1

rep('Carer role v2.88', 'Carer role v2.89'); rep('Version 2.88 iPhone', 'Version 2.89 iPhone')
rep('<div>Version 2.88</div>', '<div>Version 2.89</div>'); rep('>2.88 – REVIEW DRAFT', '>2.89 – REVIEW DRAFT')
old = re.search(r'<div class="rr"><span class="rv">2\.86</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">2.88</span>', '<div class="rr"><span class="rv">2.89</span><span class="rd">18 Nov 2026</span><p>Before you sign in: worked example in place of the diagram</p></div>\n<div class="rr"><span class="rv">2.88</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
