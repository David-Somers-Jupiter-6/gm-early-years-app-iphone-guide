"""Guide 2.93 (from 2.92). Team finder (David, 19 Nov): the instruction changed after a team was chosen,
 which looked like the page jumping. Now one layout that never changes:
   "Find your team's contact details:"   then two numbered labels over the menus: (1) Locality  (2) Health Visiting team
 The labels are visible on every screen (they were hidden on shorter ones); only the team card appears below.

 Also (David, 19 Nov):
 - About your account: three headings - Who will be set up with an account? / Who will be able to access the account? /
   Who will not be able to access the account? - with a reusable in-page heading style (.pg-h).
 - Section 4 page "Before you sign in" -> "Your account details", in a GM Early Years App title box (was NHS login).
 Team finder: same on Section 2 "Contact your HV team" and the Section 8 copy (which, as before, hides its one-line instruction once a team is chosen).
usage: python3 make293.py v2.92.html v2.93.html
"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)

OLD = ('<div class="q-hint hv-how"><div class="hv-how-full"><p class="hv-how-p">If you need to contact your Health Visiting team, you can find their contact details by:</p>'
       '<ul class="hv-how-l"><li>selecting your <strong>Locality</strong></li><li>then selecting your <strong>Health Visiting team</strong></li></ul></div>'
       '<p class="hv-how-short" aria-hidden="true">Select your <strong>Locality</strong>, then your <strong>Health Visiting team</strong>.</p></div>')
rep(OLD, '<p class="q-hint hv-how">Find your team’s contact details:</p>', 2)
N = '<span class="hv-num" aria-hidden="true">%d</span>'
for sid in ('hvs', 'hv'):
    rep('<label for="%s-loc">Locality</label>' % sid, '<label for="%s-loc">%sLocality</label>' % (sid, N % 1))
    rep('<label for="%s-team">Health Visiting team</label>' % sid, '<label for="%s-team">%s<span class="hv-lt-l">Health Visiting team</span><span class="hv-lt-s" aria-hidden="true">HV team</span></label>' % (sid, N % 2))
    rep('<select id="%s-loc"><option value="" selected>Locality</option>' % sid, '<select id="%s-loc"><option value="" selected>Choose</option>' % sid)

# remove what the old two-version instruction needed
rep('#app :is(#hv,#s5-hv) .hv-f>label{position:absolute!important;width:1px;height:1px;margin:-1px;padding:0;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;border:0}', '')
s, n = re.subn(r'#app #hv:has\(#hvs-loc option\[value="\w+"\]:checked\):has\(#hvs-team-\w+ option:not\(\[value=""\]\):checked\) \.hv-how-(?:full|short)\{display:(?:none|block)\}', '', s)
assert n == 6, n
assert 'hv-how-full' not in s and 'hv-how-short' not in s.replace('.hv-how-short', '')

def page(pid):
    m = re.search(r'<section class="screen(?: cover)?" id="%s".*?</section>' % re.escape(pid), s, re.S); assert m, pid; return m
def edit(pid, a, b, n=1):
    global s
    m = page(pid); blk = m.group(0)
    assert blk.count(a) == n, (pid, a[:90], blk.count(a))
    s = s[:m.start()] + blk.replace(a, b) + s[m.end():]
# About your account: three headings
acct = page('acct').group(0)
i = acct.find('<p class="info-lead">Your Health Visiting team sets up'); j = acct.find('</div>', acct.find('<div class="amber info-q">')) + 6
edit('acct', acct[i:j],
     '<h3 class="pg-h">Who will be set up with an account?</h3>\n'
     '<p class="info-lead">Your Health Visiting team sets up a GM Early Years App account for the <strong>child\'s mother</strong> or <strong>primary carer</strong>. In this guide, we call this person the <strong>account holder</strong>.</p>\n'
     '<h3 class="pg-h">Who will be able to access the account?</h3>\n'
     '<p class="info-lead">Only the <strong>account holder</strong>. They sign in with the same <strong>email address</strong> and <strong>password</strong> as their own NHS login.</p>\n'
     '<h3 class="pg-h">Who will not be able to access the account?</h3>\n'
     '<div class="amber info-q"><p>A partner or another family member <strong>cannot</strong> sign in to the account.</p></div>')
# Before you sign in -> Your account details, GM Early Years App title box
nhs = page('nhs').group(0)
box = re.search(r'<div class="pbox has-badge eyx eyx-nhs">.*?</div>(?=\n<div class="strip")', nhs, re.S).group(0)
edit('nhs', box, '<div class="pbox"><h2 class="h2" tabindex="-1">Your account details</h2></div>')
edit('nhs', 'data-title="Before you sign in to NHS login"', 'data-title="Your account details"')
edit('nhs', 'aria-label="Section 4: NHS login"', 'aria-label="Section 4: Your account details"')

CSS = '''/* 2.93 team finder: one short line + numbered labels over the two menus, same before and after choosing */
#app :is(#hv,#s5-hv) .hv-how{margin:0 0 12px!important}
#app :is(#hv,#s5-hv) .hv-f>label{display:flex;align-items:center;gap:7px;margin:0 0 6px;font-size:15px;font-weight:700;color:var(--ink);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
#app :is(#hv,#s5-hv) .hv-num{flex:0 0 20px;width:20px;height:20px;border-radius:50%;background:#005eb8;color:#fff;font:700 12px/1 var(--font-head);display:flex;align-items:center;justify-content:center}
#app :is(#hv,#s5-hv) .hv-f>label{line-height:20px}
#app :is(#hv,#s5-hv) .hv-lt-s{display:none}
@media screen and (max-width:340px){#app :is(#hv,#s5-hv) .hv-lt-l{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}#app :is(#hv,#s5-hv) .hv-lt-s{display:inline}}
@media screen and (max-width:369px){#app :is(#hv,#s5-hv) .hv-f>label{font-size:14px;gap:5px}#app :is(#hv,#s5-hv) .hv-num{flex-basis:18px;width:18px;height:18px;font-size:11px}}
@media screen and (max-height:700px){#app :is(#hv,#s5-hv) .hv-how{margin-bottom:10px!important}#app :is(#hv,#s5-hv) .hv-f>label{margin-bottom:4px}#app :is(#hv,#s5-hv) .hv-card{margin-top:10px!important}}
/* in-page headings (2.93), for information pages */
#app .screen .pg-h{margin:18px 0 6px;font-family:var(--font-head);font-weight:700;font-size:18px;line-height:1.3;color:var(--ink)}
#app .screen .pg-h:first-of-type{margin-top:2px}
#app #acct .info-lead{margin:0}
#app #acct .amber.info-q{margin-top:0}
@media screen and (max-height:600px){#app .screen .pg-h{margin-top:12px;margin-bottom:4px}}
@media screen and (max-height:600px),screen and (max-width:369px){#app :is(#hv,#s5-hv) .hv-how{margin-bottom:7px!important}#app :is(#hv,#s5-hv) .hv-f>label{margin-bottom:3px}#app :is(#hv,#s5-hv) .hv-card{margin-top:8px!important}}
'''
rep('/* 2.88 Step 1:', CSS + '/* 2.88 Step 1:', 1)
_i = s.find('@media print{'); _css = s[s.rfind('<style', 0, _i):_i]
assert _css.count('{') == _css.count('}'), 'unbalanced CSS before @media print'

rep('Carer role v2.92', 'Carer role v2.93'); rep('Version 2.92 iPhone', 'Version 2.93 iPhone')
rep('<div>Version 2.92</div>', '<div>Version 2.93</div>'); rep('>2.92 – REVIEW DRAFT', '>2.93 – REVIEW DRAFT')
old = re.search(r'<div class="rr"><span class="rv">2\.90</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">2.92</span>', '<div class="rr"><span class="rv">2.93</span><span class="rd">19 Nov 2026</span><p>Team finder labels; headings on About your account; Your account details page</p></div>\n<div class="rr"><span class="rv">2.92</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
