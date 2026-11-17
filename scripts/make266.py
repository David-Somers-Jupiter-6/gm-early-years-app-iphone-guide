"""Guide 2.66 (from 2.65). Troubleshooting pages laid out as The issue / Who can help / What to do
(David, 17 Nov, from the approved mockups):
- s4-setup "Set up NHS login", s4-cannot "Cannot sign in": Who can help is the NHS login Support team,
  with "(The GMDP Support team cannot assist with NHS login account issues, as they do not have access
  to NHS login accounts.)" in brackets underneath. Links shown as buttons under What to do.
- s4-activation retitled "Activation Link not received" (also the h2 on s4-activation-2);
  three short checks and a "What to ask" box.
usage: python3 make266.py v2.65.html v2.66.html
"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
EXT='<svg aria-hidden="true" viewBox="0 0 20 20" width="18" height="18"><path d="M11 3h6v6M17 3l-8 8M14 11v5a1 1 0 01-1 1H4a1 1 0 01-1-1V7a1 1 0 011-1h5" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"/></svg>'
CHEV='<svg aria-hidden="true" viewBox="0 0 20 20" width="18" height="18"><path d="M7 4l6 6-6 6" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>'
IC_ISSUE='<span class="abc-ic ic-issue" aria-hidden="true">!</span>'
IC_WHO='<span class="abc-ic ic-who" aria-hidden="true"><svg viewBox="0 0 20 20" width="16" height="16"><circle cx="10" cy="6.5" r="3.2" fill="currentColor"/><path d="M3.5 17.5c.6-3.6 3.3-5.6 6.5-5.6s5.9 2 6.5 5.6z" fill="currentColor"/></svg></span>'
IC_DO='<span class="abc-ic ic-do" aria-hidden="true"><svg viewBox="0 0 20 20" width="16" height="16"><path d="M4 10h11M11 5l5 5-5 5" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg></span>'
def row(ic,k,body): return f'<div class="abc-row">{ic}<div><p class="abc-k">{k}</p>{body}</div></div>'
def ext(href,label): return f'<a class="sp-link abc-btn" href="{href}" rel="noopener" target="_blank">{EXT}<span><strong>{label}</strong></span></a>'
def intl(href,label): return f'<a class="sp-link abc-btn" href="{href}"><svg aria-hidden="true" viewBox="0 0 20 20" width="18" height="18"><path d="M4 10h11M11 5l5 5-5 5" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg><span><strong>{label}</strong></span></a>'
NHS_WHO='<p><strong>NHS login Support team</strong></p><p class="abc-sub">(The GMDP Support team cannot assist with NHS login account issues, as they do not have access to NHS login accounts.)</p>'
pages={
's4-setup':('Set up NHS login',
  row(IC_ISSUE,'The issue','<p>You need an NHS login to use the GM Early Years App.</p>')+
  row(IC_WHO,'Who can help',NHS_WHO)+
  row(IC_DO,'What to do','<p>Set up an NHS login. The NHS login guide explains what you need and how to set it up.</p>'),
  '<div class="hv-card sp-card abc-links">'+ext('https://help.login.nhs.uk/setupnhslogin','Set up an NHS login')+'</div>'),
's4-cannot':('Cannot sign in',
  row(IC_ISSUE,'The issue','<p>You cannot sign in to your NHS login. You need it to use the GM Early Years App.</p>')+
  row(IC_WHO,'Who can help',NHS_WHO)+
  row(IC_DO,'What to do','<p>Use the NHS login Help Centre. If you still cannot sign in, contact NHS login Support.</p>'),
  '<div class="hv-card sp-card abc-links">'+ext('https://help.login.nhs.uk','NHS login Help Centre')+ext('https://help.login.nhs.uk/contact','Contact NHS login Support')+'</div>'),
's4-activation':('Activation Link not received',
  row(IC_ISSUE,'The issue','<p>You need an Activation Link to open the App sign-in page. It is sent to you by text message.</p>')+
  row(IC_WHO,'Who can help','<p><strong>Your Health Visiting team</strong></p>')+
  row(IC_DO,'What to do','<ul class="abc-list"><li>Check your text messages.</li><li>Check it went to your own mobile number.</li><li>Still no link? Contact the team.</li></ul>'),
  '<div class="tip abc-ask"><span class="k">What to ask</span><p>Ask them to check your account has the right name and mobile number, and to send a new link.</p></div>'),
}
CSS='''
/* 2.66 Troubleshooting pages: The issue / Who can help / What to do */
.abc{display:flex;flex-direction:column;margin:2px 0 0}
.abc-row{display:grid;grid-template-columns:30px 1fr;column-gap:11px;align-items:start;padding:8px 0}
.abc-row+.abc-row{border-top:1px solid var(--line)}
.abc-row:first-child{padding-top:2px}
.abc-ic{width:30px;height:30px;border-radius:50%;display:grid;place-items:center;font-family:var(--font-head);font-weight:900;font-size:17px;line-height:1}
.ic-issue{background:var(--amberBg);color:var(--amberInk);box-shadow:inset 0 0 0 2px var(--hl)}
.ic-who{background:var(--accentSoft);color:var(--accent);box-shadow:inset 0 0 0 2px var(--accent)}
.ic-do{background:var(--accentFill,var(--accent));color:#fff}
#app .screen .abc-k{font-size:13px!important;font-weight:800;letter-spacing:.07em;text-transform:uppercase;color:var(--sub);line-height:1.2;margin:0 0 3px}
#app .screen .abc-row p:not(.abc-k){font-size:17px!important;line-height:1.38!important;color:var(--ink);margin:0}
#app .screen .abc-row p.abc-sub{font-size:15px!important;line-height:1.35!important;color:var(--sub);margin-top:1px}
.abc-list{list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:3px}
#app .screen .abc-list li{position:relative;padding-left:16px;font-size:17px!important;line-height:1.36!important;color:var(--ink)}
.abc-list li::before{content:"";position:absolute;left:2px;top:9px;width:6px;height:6px;border-radius:50%;background:var(--accent)}
.abc-links{margin:4px 0 0 41px!important;padding:2px 12px!important}
.abc-links .abc-btn{padding:9px 0!important;align-items:center}
.abc-links .abc-btn:first-child{border-top:0!important}
.abc-links .abc-btn+.abc-btn{border-top:1px solid rgba(29,111,184,.18)}
.abc-links .abc-btn strong{color:var(--accent2)!important}
.abc-ask{margin:6px 0 0 41px!important;padding:8px 12px!important}
#app .screen .abc-ask p{font-size:15px!important;line-height:1.38!important}
.abc-ask .k{font-size:13px;font-weight:800;letter-spacing:.07em;text-transform:uppercase}
@media (max-width:369px){.abc-row{padding:5px 0}.abc-links .abc-btn{padding:6px 0!important}}
'''

for pid,(title,abc,after) in pages.items():
    m = re.search(r'<section class="screen" id="%s".*?</section>' % re.escape(pid), s, re.S); sec = m.group(0)
    a = sec.find('</div></div>', sec.find('<div class="strip"')) + len('</div></div>')
    b = sec.find('</div>\n<nav class="bnav"'); assert a > 20 and b > a, pid
    new = sec[:a] + '\n<div class="abc">' + abc + '</div>\n' + after + '\n' + sec[b:]
    new = re.sub(r'(<h2 class="h2" tabindex="-1">)[^<]*', lambda x: x.group(1) + title, new, count=1)
    s = s[:m.start()] + new + s[m.end():]
rep('data-title="I have not received an Activation Link" aria-label="I have not received an Activation Link"',
    'data-title="Activation Link not received" aria-label="Activation Link not received"')
rep('aria-label="I have not received an Activation Link, continued">\n<div class="scroll">\n<div class="pbox"><h2 class="h2" tabindex="-1">I have not received an Activation Link</h2>',
    'aria-label="Activation Link not received, continued">\n<div class="scroll">\n<div class="pbox"><h2 class="h2" tabindex="-1">Activation Link not received</h2>')
rep('@media print{', CSS.strip() + '\n@media print{')

rep('Carer role v2.65', 'Carer role v2.66'); rep('Version 2.65 iPhone', 'Version 2.66 iPhone')
rep('<div>Version 2.65</div>', '<div>Version 2.66</div>'); rep('>2.65 – REVIEW DRAFT', '>2.66 – REVIEW DRAFT')
old = re.search(r'<div class="rr"><span class="rv">2\.63</span>.*?</div>\n', s).group(0); s = s.replace(old, '')
rep('<div class="rr"><span class="rv">2.65</span>', '<div class="rr"><span class="rv">2.66</span><span class="rd">17 Nov 2026</span><p>NHS login and Activation Link pages show the issue, who can help and what to do</p></div>\n<div class="rr"><span class="rv">2.65</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
