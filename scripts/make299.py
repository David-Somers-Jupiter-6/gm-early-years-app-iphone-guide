"""Guide 2.99 (from 2.98). David, 19 Nov: Troubleshooting menus in the same style as Contact & support (from mockup):
 - s4: topic cards with icon tiles, a short line and "Help from:" (descriptions shortened; lead "What is the problem?")
 - s4-nhs: the eight options as an icon list
 - s4-reasons: three cards with icons
usage: python3 make299.py v2.98.html v2.99.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
def page(pid):
    m = re.search(r'<section class="screen(?: cover)?" id="%s".*?</section>' % re.escape(pid), s, re.S); assert m, pid; return m
def body_after_strip(pid, new):
    """replace everything between the page strip and the end of .scroll"""
    global s
    m = page(pid); blk = m.group(0)
    a = re.search(r'<div class="strip" aria-hidden="true">.*?</div></div>\n', blk, re.S); b = blk.index('</div>\n<nav class="bnav"')
    blk2 = blk[:a.end()] + new + '\n' + blk[b:]
    s = s[:m.start()] + blk2 + s[m.end():]
CHEV='<svg viewBox="0 0 20 20" width="18" height="18" aria-hidden="true"><path d="M7.5 4.5L13 10l-5.5 5.5" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>'
def I(d, sw=2): return f'<svg viewBox="0 0 24 24" width="24" height="24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">{d}</svg>'
IC = {
 'user':  I('<circle cx="12" cy="8" r="4"/><path d="M4 20c1.5-4 4.5-6 8-6s6.5 2 8 6"/>'),
 'link':  I('<path d="M10 14a4.5 4.5 0 006.4 0l3-3a4.5 4.5 0 00-6.4-6.4l-1.2 1.2"/><path d="M14 10a4.5 4.5 0 00-6.4 0l-3 3a4.5 4.5 0 006.4 6.4l1.2-1.2"/>'),
 'warn':  I('<path d="M12 3.5l9.5 16.5h-19z"/><path d="M12 10v4.5M12 17.3v.2"/>'),
 'head':  I('<path d="M4 13v-1a8 8 0 0116 0v1"/><rect x="3" y="12.5" width="4.5" height="7" rx="1.6" fill="currentColor"/><rect x="16.5" y="12.5" width="4.5" height="7" rx="1.6" fill="currentColor"/><path d="M19 19.5c0 1.5-2 2.5-5 2.5"/>'),
 'signin':I('<path d="M14 4h4a2 2 0 012 2v12a2 2 0 01-2 2h-4"/><path d="M4 12h11M11 8l4 4-4 4"/>'),
 'useradd':I('<circle cx="10" cy="8" r="4"/><path d="M3 20c1.3-3.7 4-5.6 7-5.6 1.2 0 2.4.3 3.4.8"/><path d="M18 14v6M15 17h6"/>'),
 'lock':  I('<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V8a4 4 0 018 0v3"/>'),
 'key':   I('<circle cx="8" cy="15" r="4"/><path d="M11 12l8-8M16 7l2.5 2.5M14 9l2 2"/>'),
 'code':  I('<path d="M4 5h16v11H9l-5 4z"/><path d="M8.5 10.5h.01M12 10.5h.01M15.5 10.5h.01" stroke-width="2.8"/>'),
 'mail':  I('<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3.5 6l8.5 7 8.5-7"/>'),
 'phone': I('<rect x="7" y="2.5" width="10" height="19" rx="2.2"/><path d="M11 18.5h2"/>'),
 'name':  I('<rect x="2.5" y="5" width="19" height="14" rx="2"/><circle cx="8.5" cy="11" r="2.2"/><path d="M5.5 16c.6-1.5 1.7-2.3 3-2.3s2.4.8 3 2.3M14 10h4.5M14 13.5h3"/>'),
 'neq':   I('<path d="M5 9.5h14M5 14.5h14M15.5 5l-7 14"/>'),
 'two':   I('<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c1.2-3.6 3.6-5.4 6.5-5.4s5.3 1.8 6.5 5.4"/><circle cx="17" cy="9" r="2.8"/><path d="M17.5 14.4c2 .3 3.4 1.9 4.2 4.6"/>'),
 'nope':  I('<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c1.2-3.6 3.6-5.4 6.5-5.4 1.4 0 2.6.4 3.7 1.2"/><circle cx="18" cy="17" r="3.8"/><path d="M15.4 19.6l5.2-5.2"/>'),
}
def card(c, ic, t, sub, who=None):
    w = f'<span class="tc-w">Help from: <b>{who}</b></span>' if who else ''
    return f'<a class="tc {c}" href="#"><span class="tc-tile">{IC[ic]}</span><span class="tc-t"><b>{t}</b><span class="tc-s">{sub}</span>{w}</span><span class="tc-c">{CHEV}</span></a>'
S4 = ('<p class="tc-lead">What is the problem?</p><nav class="tc-list">'
 + card('tc-nhs','user','NHS login account issues','Signing in, password, security codes','NHS login Support team')
 + card('tc-hv','link','Activation Link issues','Not received, or not working','your HV team')
 + card('tc-hv','neq','Common sign-in problems','Details differ, or a partner’s details','your HV team')
 + card('tc-gm','head','Still need help?','Contact the GMDP Support Team') + '</nav>')
def row(ic, t): return f'<a class="tr" href="#"><span class="tr-i">{IC[ic]}</span><span class="tr-t">{t}</span><span class="tc-c">{CHEV}</span></a>'
NHS = ('<p class="info-lead">GMDP Support cannot assist with NHS login account issues.</p><nav class="tr-list">'
 + row('signin','Signing in to NHS login') + row('useradd','Set up NHS login') + row('lock','Cannot sign in') + row('key','Forgotten your password')
 + row('code','Security code not arriving') + row('mail','Cannot get into your email') + row('phone','Mobile number problems') + row('name','My name has changed') + '</nav>')
RS = ('<p class="tc-lead">Choose the reason that matches your situation.</p><nav class="tc-list">'
 + card('tc-hv','neq','Details do not match','App account and NHS login are different')
 + card('tc-hv','two','Partner’s details used','Set up with a partner’s email or mobile')
 + card('tc-hv','nope','A partner is signing in','Only the named carer can sign in') + '</nav>')
def card2(c, ic, href, t, sub, who=None):
    return card(c, ic, t, sub, who).replace('href="#"', 'href="#%s"' % href, 1)
def row2(ic, href, t): return row(ic, t).replace('href="#"', 'href="#%s"' % href, 1)
S4 = ('<p class="tc-lead">What is the problem?</p>\n<nav aria-label="Troubleshooting contents" class="tc-list">'
 + card2('tc-nhs', 'user', 's4-nhs', 'NHS login account issues', 'Signing in, password, security codes', 'NHS login Support team')
 + card2('tc-hv', 'link', 's4-activation', 'Activation Link issues', 'Not received, or not working', 'your HV team')
 + card2('tc-hv', 'neq', 's4-reasons', 'Common sign-in problems', 'Details differ, or a partner’s details', 'your HV team')
 + card2('tc-gm', 'head', 's4-help', 'Still need help?', 'Contact the GMDP Support Team') + '</nav>')
NHSL = ('<p class="info-lead">GMDP Support cannot assist with NHS login account issues.</p>\n<nav aria-label="NHS login account issues" class="tr-list">'
 + row2('signin', 'step-a', 'Signing in to NHS login') + row2('useradd', 's4-setup', 'Set up NHS login') + row2('lock', 's4-cannot', 'Cannot sign in')
 + row2('key', 's4-pw', 'Forgotten your password') + row2('code', 's4-code', 'Security code not arriving') + row2('mail', 's4-email', 'Cannot get into your email')
 + row2('phone', 's4-mobile', 'Mobile number problems') + row2('name', 's4-name', 'My name has changed') + '</nav>')
RS = ('<p class="tc-lead">Choose the reason that matches your situation.</p>\n<nav aria-label="Common reasons for sign-in problems" class="tc-list">'
 + card2('tc-hv', 'neq', 's4-problems', 'Details do not match', 'App account and NHS login are different')
 + card2('tc-hv', 'two', 's4-1b', 'Partner’s details used', 'Set up with a partner’s email or mobile')
 + card2('tc-hv', 'nope', 's4-2', 'A partner is signing in', 'Only the named carer can sign in') + '</nav>')
# old menus must hold exactly these links before we replace them
for pid, links in [('s4', ['s4-nhs', 's4-activation', 's4-reasons', 's4-help']), ('s4-nhs', ['step-a', 's4-setup', 's4-cannot', 's4-pw', 's4-code', 's4-email', 's4-mobile', 's4-name']),
                   ('s4-reasons', ['s4-problems', 's4-1b', 's4-2'])]:
    got = re.findall(r'class="toc-row" href="#([^"]+)"', page(pid).group(0)); assert got == links, (pid, got)
body_after_strip('s4', S4); body_after_strip('s4-nhs', NHSL); body_after_strip('s4-reasons', RS)
for pid in ('s4', 's4-nhs', 's4-reasons'): assert 'toc-row' not in page(pid).group(0)
P = '#app :is(#s4,#s4-reasons)'; N = '#app #s4-nhs'
CSS = f'''/* 2.99 Troubleshooting menus: cards and icon list, in the Contact & support style */
{P} .tc-lead{{font-size:17px;line-height:1.4;color:var(--ink);margin:0 0 10px}}
{P} .tc-list{{display:block;margin:0;padding:0}}
{P} .tc{{display:flex;align-items:center;gap:11px;margin:0 0 7px;padding:9px 10px;border:1px solid var(--line);border-left-width:5px;border-radius:14px;background:var(--surface);text-decoration:none!important;box-shadow:0 1px 2px rgba(0,48,135,.08)}}
{P} .tc-nhs,{P} .tc-hv{{border-left-color:#005eb8}}{P} .tc-gm{{border-left-color:#c0174e}}
{P} .tc-tile{{flex:0 0 44px;height:44px;border-radius:10px;display:flex;align-items:center;justify-content:center;color:#fff}}
{P} .tc-nhs .tc-tile,{P} .tc-hv .tc-tile{{background:#005eb8}}{P} .tc-gm .tc-tile{{background:linear-gradient(135deg,#6c155c,#d01545)}}
{P} .tc-t{{flex:1;min-width:0}}
{P} .tc-t>b{{display:block;font-family:var(--font-head);font-size:16.5px;line-height:1.25;color:var(--ink)}}
{P} .tc-s{{display:block;font-size:15px;line-height:1.3;color:var(--sub);margin-top:2px;font-weight:400!important}}
{P} .tc-w{{display:block;font-size:14px;line-height:1.3;color:var(--sub);margin-top:3px;font-weight:400!important}}
{P} .tc-t .tc-w b{{display:inline;font-family:inherit;font-size:inherit;line-height:inherit;font-weight:700;color:#005eb8}}
{P} .tc-c{{flex:0 0 auto;color:var(--accent2);display:flex}}
{N} .tr-list{{display:block;border:1px solid var(--line);border-radius:14px;background:var(--surface);overflow:hidden;box-shadow:0 1px 2px rgba(0,48,135,.08)}}
{N} .tr{{display:flex;align-items:center;gap:12px;min-height:40px;padding:2px 10px;border-top:1px solid var(--line);text-decoration:none!important}}
{N} .tr:first-child{{border-top:0}}
{N} .tr-i{{flex:0 0 32px;height:32px;border-radius:50%;display:flex;align-items:center;justify-content:center;background:#e6effa;color:#005eb8}}{N} .tr-i svg{{width:19px;height:19px}}
{N} .tr-t{{flex:1;font-family:var(--font-head);font-weight:700;font-size:16.5px;line-height:1.25;color:var(--ink)}}
{N} .tc-c{{flex:0 0 auto;color:var(--accent2);display:flex}}
@media screen and (max-height:600px){{{N} .tr{{min-height:37px}}{N} .tr-i{{flex-basis:28px;height:28px}}{P} .tc-s{{display:none}}{P} .tc{{padding:7px 10px}}{P} .tc-tile{{flex-basis:38px;height:38px}}}}
@media screen and (max-width:369px){{#app #s4 .tc-s{{display:none}}}}
@media screen and (max-height:600px),screen and (max-width:369px){{{P} .tc-gm .tc-s{{display:block}}}}
'''
rep('/* 2.88 Step 1:', CSS + '/* 2.88 Step 1:', 1)
_i = s.find('@media print{'); _css = s[s.rfind('<style', 0, _i):_i]
assert _css.count('{') == _css.count('}'), 'unbalanced CSS before @media print'
rep('Carer role v2.98', 'Carer role v2.99'); rep('Version 2.98 iPhone', 'Version 2.99 iPhone')
rep('<div>Version 2.98</div>', '<div>Version 2.99</div>'); rep('>2.98 – REVIEW DRAFT', '>2.99 – REVIEW DRAFT')
old = re.search(r'<div class="rr"><span class="rv">2\.96</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">2.98</span>', '<div class="rr"><span class="rv">2.99</span><span class="rd">19 Nov 2026</span><p>Troubleshooting menus with icons, like Contact &amp; support</p></div>\n<div class="rr"><span class="rv">2.98</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
