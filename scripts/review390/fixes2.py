"""3.90 part 2 – points 9, 11, 13, 14, 15, 16 and 17 of the problems-and-solutions doc (David, 25 Nov).
 9  Help pages: the main action in "What to do" is a full-width solid button (min 44 px); "Still stuck?" is outlined.
 11 One set of example details: the Question 5 example NHS number is 123 456 7890 (as in the step 7 screenshot);
    the screenshots' email (hotmail) and phone (…9985) are edited to c.somers@example.com / …0123 by
    example_details_images.py.
 13 "Contact your Health Visiting team" becomes "Find your Health Visiting team", with a line saying they don't need
    to call now.
 14 Step 1: "Open Safari to come back to this guide." as a 4th line; the filler sentence goes.
 15 "Signing in to NHS login" becomes "Check your NHS login details"; the tips of steps 2–6 and Install step 4 sit on
    their step pages (6 tip pages removed); Back/Next and page counts renumbered.
 16 NHS login help: says once, positively, who can help (lead on the menu and under "Who can help").
 17 Copy tidy-ups: step 3, step 5, Question 5 question, curly apostrophes.
usage: fixes2.py src out"""
import sys, re
s = open(sys.argv[1], encoding='utf-8').read()
def rep(x, y, n=1):
    global s
    c = s.count(x); assert c == n, (x[:110], c); s = s.replace(x, y)
def span(sid):
    i = re.search(r'<section class="screen[^"]*" id="%s"' % re.escape(sid), s).start(); j = s.index('</section>', i) + len('</section>'); return i, j
def in_sec(sid, x, y, n=1):
    global s
    i, j = span(sid); t = s[i:j]; c = t.count(x); assert c == n, (sid, x[:110], c)
    s = s[:i] + t.replace(x, y) + s[j:]
def sub_sec(sid, pat, y, n=1):
    global s
    i, j = span(sid); t, c = re.subn(pat, y, s[i:j]); assert c == n, (sid, pat, c); s = s[:i] + t + s[j:]
css = ''

# ---------- 9 ----------
css += '''
/* 3.90 (point 9) help pages: the main action is a full-width solid button; "Still stuck?" is the quieter outlined one */
#app .abc .abc-links{display:block!important;width:100%!important}
#app .abc .abc-links .abc-btn{display:flex!important;width:100%!important;box-sizing:border-box!important;justify-content:center!important;align-items:center!important;min-height:44px!important;border-radius:12px!important;text-align:center!important}
#app .screen .stuck a.stuck-a.stuck-a{background:#fff!important;background-image:none!important;color:#1d6fb8!important;box-shadow:inset 0 0 0 2px #1d6fb8!important}
#app .screen .stuck a.stuck-a.stuck-a svg{color:#1d6fb8!important}
@media (max-height:600px){#app .abc .abc-links{margin-top:4px!important}}
@media (prefers-color-scheme:dark){#app .screen .stuck a.stuck-a.stuck-a{background:transparent!important;color:#8cc2f0!important;box-shadow:inset 0 0 0 2px #8cc2f0!important}#app .screen .stuck a.stuck-a.stuck-a svg{color:#8cc2f0!important}}
'''

# ---------- 11 ----------
in_sec('ts4', 'NHS number 485 777 3456', 'NHS number 123 456 7890', 2)
in_sec('ts4', '<span class="exc-v">485 777 3456</span>', '<span class="exc-v">123 456 7890</span>', 4)
assert '485 777 3456' not in s

# ---------- 13 ----------
in_sec('hv', 'data-title="Contact your Health Visiting team" aria-label="Section 2: Contact your Health Visiting team"', 'data-title="Find your Health Visiting team" aria-label="Section 2: Find your Health Visiting team"')
in_sec('hv', '<h2 class="h2" tabindex="-1">Contact your Health Visiting team</h2>', '<h2 class="h2" tabindex="-1">Find your Health Visiting team</h2>')
i, j = span('hv'); t = s[i:j]; k = t.rindex('</div>\n<nav class="bnav"')
t = t[:k] + '<p class="hv-why">You do not need to call them now. Keep their number handy in case the sign-in check finds a problem.</p>\n' + t[k:]
s = s[:i] + t + s[j:]
in_sec('contents', '<span class="tt">Contact your Health Visiting team</span>', '<span class="tt">Find your Health Visiting team</span>')
in_sec('search', '<a class="srch-tp" href="#hv">Contact your Health Visiting team</a>', '<a class="srch-tp" href="#hv">Find your Health Visiting team</a>')
css += '''
/* 3.90 (point 13) Find your Health Visiting team: one line saying why */
#app #hv .hv-why{margin:14px 0 0!important;font-size:17px;line-height:1.35;color:var(--ink)}
''' + ''.join('#app #hv:has(#hvs-loc option[value="%s"]:checked):has(#hvs-team-%s option:checked:not([value=""])) .hv-why{display:none!important}\n' % (a, a) for a in ('Bury', 'Rochdale', 'Stockport')) + '''
'''

# ---------- 14 ----------
in_sec('step-1', '<p>Restarting first helps everything run smoothly.</p>\n<ul class="facts">', '<ul class="facts">')
in_sec('step-1', '<li>Hold the side button until you see the Apple logo.</li>\n</ul>', '<li>Hold the side button until you see the Apple logo.</li>\n<li>Open <strong>Safari</strong> to come back to this guide.</li>\n</ul>')

# ---------- 15 ----------
in_sec('s4-nhs', '<span class="tr-t">Signing in to NHS login</span>', '<span class="tr-t">Check your NHS login details</span>')
in_sec('step-a', 'data-title="Step 1 · Signing in to NHS login"', 'data-title="Step 1 · Check your NHS login details"')
in_sec('step-a', '<span class="vh">Step 1 of 7: </span>Signing in to NHS login</h2>', '<span class="vh">Step 1 of 7: </span>Check your NHS login details</h2>')
TIP = '<div class="tip step-tip"><span class="k">{k}</span><p>{p}</p></div>'
AMB = '<div class="amber step-tip"><span class="k">{k}</span><p>{p}</p></div>'
def add_tip(sid, after, html):
    in_sec(sid, after, after + '\n' + html)
add_tip('step-c', '<p>Type the <strong>Email address</strong> and <strong>Password</strong> you use for NHS login, then tap <strong>Continue</strong>.</p>',
        TIP.format(k='Password not accepted?', p='Tap <strong>Forgot password?</strong> on this page.'))
in_sec('step-d', '<p>If NHS login asks for a security code, it sends a 6-digit code by text message to the mobile number registered with your NHS login.</p>',
       '<p>If NHS login asks for a security code, it sends a 6-digit code by text message to the mobile number registered with your NHS login. If it does not ask, go on to <a href="#step-g">Step 6</a>.</p>\n'
       + AMB.format(k='Not your number?', p='Tap <strong>I cannot log in using my mobile phone</strong> on this page.'))
add_tip('step-e', '<p>You will receive a text message with your <span class="nw">6-digit</span> security code.</p>',
        TIP.format(k='Notification gone?', p='Open the <strong>Messages</strong> app and find the text from NHS login.'))
add_tip('step-f', '<p>Type the <span class="nw">6-digit</span> security code in the <strong>Security code</strong> box, then tap <strong>Continue</strong>.</p>',
        TIP.format(k='No code after a few minutes?', p='Tap <strong>Not received a security code?</strong> and use the newest code. Still nothing? See <a href="#s5-2">Contacts</a>.'))
add_tip('step-g', '<p>Please wait a moment while NHS login checks your details.</p>',
        TIP.format(k='Page not moving on?', p='After a few minutes, contact NHS login Support (see <a href="#s5-2">Contacts</a>).'))
add_tip('inst-4', '<p>Next to <strong>GM Early Years</strong>, tap the <strong>Download</strong> button.</p>',
        TIP.format(k='Button says Get?', p='Tap <strong>Get</strong>. Your iPhone may ask for Face ID, Touch ID or your Apple ID password.'))
GONE = ['step-c-tip', 'step-d-tip', 'step-e-tip', 'step-f-tip', 'step-g-tip', 'inst-4-tip']
for g in GONE:
    i, j = span(g)
    while s[j:j+1] == '\n': j += 1
    s = s[:i] + s[j:]
# Back / Next across the removed pages
links = {('step-c', 'next'): 'step-d', ('step-d', 'back'): 'step-c', ('step-d', 'next'): 'step-e', ('step-e', 'back'): 'step-d',
         ('step-e', 'next'): 'step-f', ('step-f', 'back'): 'step-e', ('step-f', 'next'): 'step-g', ('step-g', 'back'): 'step-f',
         ('step-g', 'next'): 'step-h', ('step-h', 'back'): 'step-g', ('inst-4', 'next'): 'inst-5', ('inst-5', 'back'): 'inst-4'}
for (sid, k), to in links.items():
    sub_sec(sid, r'(<a class="nav-btn nav-%s[^"]*" href="#)[^"]+(")' % k, r'\g<1>%s\2' % to)
for g in GONE:
    assert ('#' + g + '"') not in s and ("'" + g + "'") not in s, g
# page counts: "N / T" and "(page N of T)" in page order; "Page X of Y" within each section
ids = re.findall(r'<section class="screen[^"]*" id="([^"]+)"', s)
counted = [x for x in ids if x != 'search']; T = len(counted)
for n, sid in enumerate(counted, 1):
    if 'aria-label="Contents (page' in s[slice(*span(sid))]:
        sub_sec(sid, r'aria-label="Contents \(page \d+ of \d+\)"', f'aria-label="Contents (page {n} of {T})"')
    if 'class="count">' in s[slice(*span(sid))] and re.search(r'class="count">\d+ / \d+<', s[slice(*span(sid))]):
        sub_sec(sid, r'class="count">\d+ / \d+<', f'class="count">{n} / {T}<')
groups = {}
for sid in ids:
    m = re.search(r'data-sec="([^"]+)"', s[slice(*span(sid))]); 
    if m: groups.setdefault(m.group(1), []).append(sid)
for g, members in groups.items():
    have = [x for x in members if re.search(r'<span class="pos">Page \d+ of \d+</span>', s[slice(*span(x))])]
    for n, sid in enumerate(have, 1):
        sub_sec(sid, r'<span class="pos">Page \d+ of \d+</span>', f'<span class="pos">Page {n} of {len(have)}</span>')

# ---------- 16 ----------
in_sec('s4-nhs', '<p class="info-lead">GMDP Support cannot assist with NHS login account issues.</p>',
       '<p class="info-lead">NHS login is run by the NHS. Only its Support team can see or change your account.</p>')
NEWSUB = '<p class="abc-sub">Only they can see or change your NHS login account.</p>'
n16 = s.count('<p class="abc-sub">GMDP Support cannot see NHS login accounts.</p>')
s = s.replace('<p class="abc-sub">GMDP Support cannot see NHS login accounts.</p>', NEWSUB)
print('point 16: Who can help lines changed on', n16, 'pages')
in_sec('step-a', ' See <a href="#s4-nhs">NHS login account help</a>. GMDP Support cannot see NHS login accounts.</p>', ' See <a href="#s4-nhs">NHS login account help</a>.</p>')

# ---------- 17 ----------
in_sec('step-3', '<p>On the sign-in screen, tap <strong>Continue to NHS login</strong>. It is under <strong>Parents and carers sign in below</strong>. The buttons further down are for staff only.</p>',
       '<p>Under <strong>Parents and carers sign in below</strong>, tap <strong>Continue to NHS login</strong>. The buttons further down are for staff.</p>')
in_sec('step-5', 'then tap <strong>Continue</strong>. Forgotten your password? Tap <strong>Forgot password?</strong></p>',
       'then tap <strong>Continue</strong>. If you have forgotten your password, tap <strong>Forgot password?</strong> on that screen.</p>')
in_sec('ts4', '<p class="q-ask" id="ask-ts4">Did you give your Health Visiting team these same details?</p>', '<p class="q-ask" id="ask-ts4">Are your details the same in both accounts?</p>')
# curly apostrophes in page text (not in scripts or styles)
parts = re.split(r'(<script.*?</script>|<style.*?</style>)', s, flags=re.S)
k = 0
for idx in range(0, len(parts), 2):
    parts[idx], c = re.subn(r"(?<=[A-Za-z])'(?=[a-z])", '’', parts[idx]); k += c
s = ''.join(parts); print('apostrophes made curly:', k)

s = s.replace('</style>', css + '</style>', 1)
open(sys.argv[2], 'w', encoding='utf-8').write(s); print('ok', T, 'pages')
