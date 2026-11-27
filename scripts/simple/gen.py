"""Build the GM Early Years App Simple guide (single self-contained HTML file).
usage: gen.py VERSION OUT.html [trial]"""
import json, base64, sys, html, os
HERE = os.path.dirname(os.path.abspath(__file__))

VERSION = sys.argv[1]
OUT = sys.argv[2]
TRIAL = len(sys.argv) > 3 and sys.argv[3] == 'trial'
A = json.load(open(os.path.join(HERE, 'assets/assets.json')))
HV = json.load(open(os.path.join(HERE, 'data/hv.json')))
NHS_BADGE = open(os.path.join(HERE, 'assets/nhs_badge.txt')).read()


def img64(path):
    return 'data:image/jpeg;base64,' + base64.b64encode(open(path, 'rb').read()).decode()


def esc(s):
    return html.escape(s, quote=True)


# ---------- icons ----------
def sv(body, size=20, sw=2):
    return (f'<svg viewBox="0 0 24 24" width="{size}" height="{size}" fill="none" stroke="currentColor" '
            f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{body}</svg>')


I_BACK = '<svg aria-hidden="true" viewBox="0 0 20 20" width="18" height="18"><path d="M16 10H5M9 5l-5 5 5 5" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
I_NEXT = '<svg aria-hidden="true" viewBox="0 0 20 20" width="18" height="18"><path d="M4 10h11M11 5l5 5-5 5" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
I_TICK = '<svg aria-hidden="true" viewBox="0 0 20 20" width="16" height="16"><path d="M4.5 10.5l3.5 3.5 7.5-8" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
I_CHEV = '<svg class="chev" aria-hidden="true" viewBox="0 0 20 20" width="16" height="16"><path d="M7.5 4.5L13 10l-5.5 5.5" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
I_EXT = '<svg viewBox="0 0 20 20" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M11 3h6v6M17 3l-8 8M14 12v4a1 1 0 01-1 1H4a1 1 0 01-1-1V7a1 1 0 011-1h4"/></svg>'
I_HELP = sv('<circle cx="12" cy="12" r="9"/><path d="M9.6 9.3a2.5 2.5 0 014.8.9c0 1.7-2.4 2.2-2.4 3.6"/><circle cx="12" cy="17.2" r=".6" fill="currentColor"/>', 24)
I_MSG = sv('<path d="M4 5h16v11H9l-5 4z"/>')
I_USER = sv('<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0116 0"/>')
I_USERS = sv('<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20a6.5 6.5 0 0113 0"/><path d="M16 4.6a3.5 3.5 0 010 6.8M18 14a6.5 6.5 0 013.5 6"/>')
I_PHONE = sv('<path d="M5 3h3l2 5-2.5 1.5a11 11 0 005 5L14 12l5 2v3a2 2 0 01-2 2A16 16 0 013 5a2 2 0 012-2z"/>', 20)
I_PIN = sv('<path d="M12 21s-6.5-6.2-6.5-11a6.5 6.5 0 0113 0c0 4.8-6.5 11-6.5 11z"/><circle cx="12" cy="10" r="2.4"/>', 18)
I_CLOCK = sv('<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>', 18)
I_MAIL = sv('<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3.5 6.5L12 13l8.5-6.5"/>', 20)
I_LOCK = sv('<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V8a4 4 0 018 0v3"/>', 20)
I_A11Y = sv('<circle cx="12" cy="4.5" r="1.8"/><path d="M5 8.5l7 1.5 7-1.5M12 10v5M9 21l3-6 3 6"/>', 22)
I_CARD = sv('<rect x="3" y="5" width="18" height="14" rx="2.5"/><circle cx="9" cy="11" r="2.3"/><path d="M5.8 16.2a3.4 3.4 0 016.4 0M14.5 10h4M14.5 13.5h3"/>', 22)
I_APP = sv('<rect x="6" y="2.5" width="12" height="19" rx="2.5"/><path d="M10.5 18.5h3"/>', 22)
I_SMS = sv('<path d="M4 5h16v11H9l-5 4z"/><path d="M8 9.5h8M8 12.5h5"/>', 22)
I_CONTACT = sv('<path d="M4 13v-1a8 8 0 0116 0v1"/><rect x="3" y="12.5" width="4.5" height="7" rx="1.6" fill="currentColor"/><rect x="16.5" y="12.5" width="4.5" height="7" rx="1.6" fill="currentColor"/>', 24)
I_SCREENS = sv('<rect x="2.5" y="4" width="13" height="9.5" rx="1.5"/><path d="M6.5 17h5M9 13.5V17"/><rect x="16" y="8" width="6" height="11.5" rx="1.5"/>', 22)
I_ZOOM = sv('<circle cx="10.5" cy="10.5" r="6"/><path d="M15 15l5 5M10.5 8v5M8 10.5h5"/>', 18, 2.4)
NHS_TI = '<span class="ti nhs" aria-hidden="true"><b>NHS</b></span>'

# ---------- pages ----------
pages = []  # (id, label, html)


def bnav(back=None, nxt=None, nxt_label='Next', help_btn=True, back_dyn=False, done=False, nxt_cls=''):
    b = ''
    if back:
        b += (f'<a class="btn btn-back" href="#{back}"' + (' data-back' if back_dyn else '') + f'>{I_BACK}Back</a>')
    if help_btn:
        b += f'<a class="btn-help" href="#help">{I_HELP}<span>Help</span></a>'
    else:
        b += '<span class="btn-gap" aria-hidden="true"></span>'
    if nxt:
        b += (f'<a class="btn btn-next{nxt_cls}" href="#{nxt}"' + (' data-done' if done else '') + f'>{nxt_label}{I_NEXT}</a>')
    return f'<nav class="bnav" aria-label="Page navigation">{b}</nav>'


def pbox(title, kicker, cls='', step=None, icon=''):
    st = ''
    if step:
        n, total = step
        st = '<div class="stepper" aria-hidden="true">' + ''.join(
            f'<span class="{"d" if i < n else ("c" if i == n else "")}"></span>' for i in range(1, total + 1)) + '</div>'
    vh = f'<span class="vh">Step {step[0]} of {step[1]}: </span>' if step else ''
    ic = f'<span class="hic" aria-hidden="true">{icon}</span>' if icon else ''
    return (f'<div class="pbox{(" " + cls) if cls else ""}{" has-ic" if icon else ""}">{st}<p class="kicker">{kicker}</p>'
            f'<h2 tabindex="-1">{vh}{title}</h2>{ic}</div>')


# 1. Cover
cover = f'''<section class="screen" id="cover" aria-label="Cover">
<div class="scroll">
  <div class="cv-band">
    <div class="cv-gmca" role="img" aria-label="GMCA: Greater Manchester Combined Authority"><div class="w">GMCA</div><div class="s"><div>Greater</div><div>Manchester</div><div>Combined</div><div>Authority</div></div></div>
    <img class="cv-ddd" src="{A['ddd']}" alt="Greater Manchester: Doing Digital Differently">
  </div>
  <div class="cv-photo"><img src="{A['photo']}" alt="A young child playing with colourful wooden stacking toys"></div>
  <div class="cv-sheet">
    <img class="cv-icon" src="{A['icon']}" alt="GM Early Years App" width="76" height="76">
    <p class="cv-k">For parents and carers <span class="cv-ver">Version {VERSION}</span></p>
    <h1 tabindex="-1">GM Early Years App</h1>
    <p class="cv-sub">Help signing in on your iPhone</p>
    <div class="cv-calm">
      <span class="ic" aria-hidden="true">{I_TICK}</span>
      <p><strong>Having trouble signing in?</strong>You are not on your own. We will help you, one step at a time.</p>
    </div>
    <p class="cv-fam"><span class="cv-fl"><span class="pin" aria-hidden="true"><svg viewBox="0 0 24 24" width="15" height="15"><path d="M12 21s-6.5-6.2-6.5-11a6.5 6.5 0 0 1 13 0c0 4.8-6.5 11-6.5 11z" fill="currentColor"/><circle cx="12" cy="10" r="2.4" fill="#fff"/></svg></span>For families in</span><span class="cv-c">Bury</span><span class="cv-c">Rochdale</span><span class="cv-c">Stockport</span></p>
  </div>
</div>
<nav class="bnav" aria-label="Page navigation">
  <a class="btn-help cover-a11y" href="#a11y">{I_A11Y}<span>Accessibility</span></a>
  <a class="btn btn-start" href="#before">Start {I_NEXT}</a>
</nav>
</section>'''
pages.append(('cover', 'Cover', cover))

# 2. Before you start
before = f'''<section class="screen" id="before" aria-label="Before you start">
<div class="scroll">
  {pbox('Before you start', 'Getting ready')}
  <p class="lead">You need these 3 things:</p>
  <ul class="need">
    <li><span class="ni" aria-hidden="true">{I_CARD}</span><div><strong>The account is for you</strong><span>It is for the child’s mother or primary carer.</span></div></li>
    <li><span class="ni" aria-hidden="true">{I_LOCK}</span><div><strong>Your own NHS login</strong><span>Not got one? <a href="https://help.login.nhs.uk/setupnhslogin" target="_blank" rel="noopener">Set up NHS login</a></span></div></li>
    <li><span class="ni" aria-hidden="true">{I_SMS}</span><div><strong>Your Activation Link</strong><span>It comes by text message.</span></div></li>
  </ul>
  <p class="tipline"><span class="ni sm" aria-hidden="true">{I_SCREENS}</span><span><strong>Tip:</strong> read this guide on another screen, like a computer. Then sign in on your iPhone.</span></p>
</div>
{bnav(back='cover', nxt='step-1')}
</section>'''
pages.append(('before', 'Before you start', before))

FOCUS = {'step2': '0.444', 'step3': '0.443', 'step5': '0.168', 'step7': '0.068', 'step8': '0.360', 'step10': '0.470', 'step12': '0.046', 'step15': '0.000'}
# 3-9. Steps
STEPS = [
    dict(t='Open your Activation Link', part='GM Early Years App', img='step2',
         do=['Open <strong>Messages</strong> and find the text about your GM Early Years App account.',
             'Tap the link in the text. The App sign-in screen opens.'],
         stuck=('No text with a link?', 'p-link')),
    dict(t='Tap Continue to NHS login', part='GM Early Years App', img='step3',
         do=['Under <strong>Parents and carers sign in below</strong>, tap <strong>Continue to NHS login</strong>.',
             'Do not use the buttons further down. They are for staff.'],
         stuck=('Sign-in screen not opening?', 'p-app')),
    dict(t='Sign in to NHS login', part='NHS login', img='step5',
         do=['Asked about cookies? Tap either choice.',
             'Type your NHS login email address and password.',
             'Tap <strong>Continue</strong>.'],
         stuck=('Cannot sign in?', 'p-nhs')),
    dict(t='Enter your security code', part='NHS login', img='step7',
         do=['Wait for a text from NHS login with a 6&#8209;digit code.',
             'Tap the code above your keyboard.',
             'Tap <strong>Continue</strong>.'],
         stuck=('Code not arrived?', 'p-code')),
    dict(t='Trust this device', part='NHS login', img='step8',
         do=['Your own iPhone? Choose <strong>Yes, trust this device</strong>. If not, choose <strong>Not now</strong>.',
             'Tap <strong>Continue</strong>.',
             'Wait while NHS login checks your details.'],
         stuck=('Error about your details?', 'p-match')),
    dict(t='Get your App code', part='GM Early Years App', img='step10',
         do=['Check the last digits shown are your mobile number.',
             'Tap <strong>Send Code</strong>.',
             'Wait for a text from <strong>msverify</strong>.'],
         stuck=('Not your number?', 'p-other')),
    dict(t='Enter your App code', part='GM Early Years App', img='step12',
         do=['Tap the code box.',
             'Tap the code above your keyboard. This is a new code, not the NHS login one.',
             'Tap <strong>Verify Code</strong>.'],
         stuck=('App not opening?', 'p-open')),
    dict(t='You are signed in', part='All done', img='step15',
         do=['If you see <strong>Assessment Forms Status</strong>, tap <strong>Close</strong>.',
             'You will see your details. That is everything.'],
         stuck=None),
]
for i, s in enumerate(STEPS, 1):
    sid = f'step-{i}'
    prev = 'before' if i == 1 else f'step-{i-1}'
    alt = open(os.path.join(HERE, f'shots/{s["img"]}.alt')).read()
    lis = ''.join(f'<li><span>{d}</span></li>' for d in s['do'])
    last = i == len(STEPS)
    if s['stuck']:
        q, pid = s['stuck']
        da = f' data-open="{pid}"' if pid else ''
        tail = f'<div class="stuck"><p><strong>Stuck here?</strong><span>{q}</span></p><a href="#help"{da}>Get help</a></div>'
    else:
        tail = f'<div class="done-card"><span class="ic" aria-hidden="true">{I_TICK}</span><p><strong>Well done!</strong>You can close this guide now.</p></div>'
    body = f'''<section class="screen" id="{sid}" aria-label="Step {i} of {len(STEPS)}">
<div class="scroll">
  {pbox(s['t'], f"Step {i} of {len(STEPS)} · {s['part']}", cls='ok' if last else '', step=(len(STEPS) + 1 if last else i, len(STEPS)))}
  <ol class="do">{lis}</ol>
  <button type="button" class="shot" aria-label="Show this screenshot full size"><img src="{img64(os.path.join(HERE, f'shots/{s["img"]}.jpg'))}" alt="{esc(alt)}" data-focus="{FOCUS[s['img']]}"><span class="zoomi" aria-hidden="true">{I_ZOOM}</span></button>
  {tail}
</div>
{bnav(back=prev, nxt='cover' if last else f'step-{i+1}', nxt_label='Finish' if last else 'Next')}
</section>'''
    body = body.replace(f'<span class="vh">Step {len(STEPS) + 1} of {len(STEPS)}: </span>', f'<span class="vh">Step {len(STEPS)} of {len(STEPS)}: </span>')
    pages.append((sid, s['t'], body))

# 10. Still not working?
PROBS = [
    ('p-link', f'<span class="ti hv" aria-hidden="true">{I_MSG}</span>', 'My Activation Link has not arrived', 'Your Health Visiting team',
     'Ask them to check your mobile number and send you a new link.', ('#contacts" data-hv="1', 'Find your Health Visiting team', False)),
    ('p-app', f'<span class="ti hv" aria-hidden="true">{I_APP}</span>', 'The link does not open the App', 'GMDP Support team',
     'Check the App is on your iPhone: search <strong>gm early years</strong> in the App Store. Then tap the link in the text again.', ('mailto:gmdp.support@greatermanchester-ca.gov.uk', 'Email GMDP Support', False)),
    ('p-nhs', NHS_TI, 'I cannot sign in to NHS login', 'NHS login Support',
     'Only NHS login can see or change your NHS login.', ('https://help.login.nhs.uk', 'NHS login help', True)),
    ('p-code', NHS_TI, 'My security code has not arrived', 'NHS login Support',
     'Wait a few minutes. If it still does not arrive, get help from NHS login.', ('https://help.login.nhs.uk/error-messages-support', 'Security code help', True)),
    ('p-match', f'<span class="ti hv" aria-hidden="true">{I_USER}</span>', 'My details do not match', 'Your Health Visiting team',
     'Ask them to make your App email and mobile match your NHS login.', ('#contacts" data-hv="1', 'Find your Health Visiting team', False)),
    ('p-other', f'<span class="ti hv" aria-hidden="true">{I_USERS}</span>', 'Someone else’s details were used', 'Your Health Visiting team',
     'Ask them to change the App account to your own email and mobile.', ('#contacts" data-hv="1', 'Find your Health Visiting team', False)),
    ('p-open', f'<span class="ti hv" aria-hidden="true">{I_APP}</span>', 'The App does not open after my code', 'GMDP Support team',
     'Wait a few minutes. Still stuck, or seeing an error? Email us with the step and any error message. Never send passwords or codes.', ('mailto:gmdp.support@greatermanchester-ca.gov.uk', 'Email GMDP Support', False)),
]
items = ''
for pid, ti, title, who, what, (href, label, ext) in PROBS:
    tgt = ' target="_blank" rel="noopener"' if ext else ''
    items += (f'<details id="{pid}"><summary>{ti}<span class="pt">{title}</span>{I_CHEV}</summary>'
              f'<div class="ans"><p class="who">Who can help<strong>{who}</strong></p><p class="what">{what}</p>'
              f'<a class="go{" nhs" if ext else ""}" href="{href}"{tgt}>{label}{(" " + I_EXT) if ext else ""}</a></div></details>')
helpp = f'''<section class="screen" id="help" aria-label="Still not working?">
<div class="scroll">
  {pbox('Still not working?', 'Help', cls='help', icon=I_HELP.replace('width="24" height="24"', 'width="24" height="24" style="color:#fff"'))}
  <p class="calm"><span class="ic" aria-hidden="true">{I_TICK}</span>Tap the problem that sounds like yours.</p>
  <div class="plist">{items}</div>
  <p class="note">Something else? <a href="#contacts" data-hv="1">Your Health Visiting team</a> can help.</p>
</div>
{bnav(back='cover', nxt='contacts', nxt_label='Contacts', help_btn=False, back_dyn=True)}
</section>'''
pages.append(('help', 'Still not working?', helpp))

# 11. Contacts
area_btns = ''.join(f'<button type="button" class="area" data-area="{a}" aria-pressed="false">{a}</button>' for a in ['Bury', 'Rochdale', 'Stockport'])
contacts = f'''<section class="screen" id="contacts" aria-label="Contacts">
<div class="scroll">
  {pbox('Contacts', 'Help', cls='help', icon=I_CONTACT.replace('stroke="currentColor"', 'stroke="#fff"').replace('fill="currentColor"', 'fill="#fff"'))}
  <div class="ccard">
    <div class="ch"><span class="ti hv" aria-hidden="true">{I_USER}</span><div><h3>Your Health Visiting team</h3><p>For your App account and Activation Link.</p></div></div>
    <p class="clabel" id="area-l"><span class="num" aria-hidden="true">1</span>Choose your area</p>
    <div class="areas" role="group" aria-labelledby="area-l">{area_btns}</div>
    <div class="teamwrap off">
      <p class="clabel" id="team-l"><span class="num" aria-hidden="true">2</span>Choose your team</p>
      <div class="sel"><select id="team" aria-labelledby="team-l" disabled><option value="">Choose your area first</option></select></div>
      <p class="ahint" id="ahint"></p>
    </div>
    <div class="team" id="teamcard" aria-live="polite" hidden></div>
  </div>
  <div class="ccard">
    <div class="ch">{NHS_TI}<div><h3>NHS login Support</h3><p>For your NHS login, password and security codes.</p></div></div>
    <a class="go nhs" href="https://help.login.nhs.uk/contact" target="_blank" rel="noopener">Contact NHS login {I_EXT}</a>
  </div>
</div>
{bnav(back='help', nxt='a11y', nxt_label='Next', help_btn=False, back_dyn=True)}
</section>'''
pages.append(('contacts', 'Contacts', contacts))

# 12. Accessibility and privacy
a11y = f'''<section class="screen" id="a11y" aria-label="Accessibility and privacy">
<div class="scroll">
  {pbox('Accessibility and privacy', 'About this guide', cls='help', icon=I_A11Y.replace('stroke="currentColor"', 'stroke="#fff"'))}
  <div class="ccard tight">
    <h3>Need this guide another way?</h3>
    <p>Ask for large print, easy read or another language. For bigger text, tap <strong>aA</strong> in Safari.</p>
    <a class="go" href="mailto:gmdp.support@greatermanchester-ca.gov.uk">{I_MAIL} Email GMDP Support</a>
  </div>
  <div class="ccard tight">
    <h3>Accessibility statement</h3>
    <p>Run by GMCA. Partially compliant with WCAG 2.2 AA. <a href="../{'../' if TRIAL else ''}#a11y-stmt">Read the full statement</a></p>
  </div>
  <div class="ccard tight">
    <h3>Your privacy</h3>
    <p>We do not collect any information about you. No sign-in, cookies or tracking.</p>
  </div>
</div>
{bnav(back='contacts', nxt='cover', nxt_label='Done', help_btn=False, back_dyn=True, done=True)}
</section>'''
pages.append(('a11y', 'Accessibility and privacy', a11y))

# ---------- team data for the script ----------
SHORT = {}
for a in ['Bury', 'Rochdale', 'Stockport']:
    pass
teams = {}
for t in HV['teams']:
    teams.setdefault(t['area'], []).append(dict(n=t['name'], a=t['addr'], tel=t['tel'][0][0][4:], td=t['tel'][0][1], h=t['hours'][0], m=t['maps']))
OPT = {
    'Bury': ['Bury Central (Town Centre)', 'Enhanced and SEND', 'Prestwich Township', 'Radcliffe', 'Ramsbottom, Tottington & North Manor', 'Whitefield and Unsworth'],
    'Rochdale': ['Heywood', 'Middleton', 'Pennines', 'Rochdale North', 'Rochdale South'],
    'Stockport': ['Adswood', 'Brinnington', 'Cheadle Heath and Edgeley', 'Cheadle Hulme and Bramhall', 'Family Nurse Partnership', 'Gatley and Heald Green', 'Hazel Grove', 'Heatons', 'Marple', 'Offerton and Stockport Central', 'Reddish', 'Woodley'],
}
for a in teams:
    assert len(teams[a]) == len(OPT[a])
    for t, o in zip(teams[a], OPT[a]):
        t['o'] = o
DATA = json.dumps(dict(teams=teams, hints=HV['hints']), ensure_ascii=False)

css = open(os.path.join(HERE, 'simple.css'), encoding='utf-8').read()
css = css.replace('{{FONT_ARCHIVO}}', A['font_archivo']).replace('{{FONT_SOURCE}}', A['font_source'])
js = open(os.path.join(HERE, 'simple.js'), encoding='utf-8').read().replace('/*DATA*/null', DATA)
icons = '../../icons/' if TRIAL else '../icons/'
title_app = 'EY Simple' if TRIAL else 'EY Sign-in'

doc = f'''<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#2d5161">
<meta name="color-scheme" content="light dark">
<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="{icons}icon-180.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="{title_app}">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<title>GM Early Years App – simple sign-in help</title>
<meta name="description" content="Simple guide version {VERSION}. Eight short steps to sign in to the GM Early Years App on an iPhone, and who can help if you get stuck.">
<meta name="author" content="GMDP Support Team, GMCA">
<style>
{css}
</style>
</head>
<body>
{chr(10).join(p[2] for p in pages)}
<div id="zoom" hidden role="dialog" aria-modal="true" aria-label="Screenshot, full size"><img alt=""><p>Tap anywhere to close</p></div>
<script>
{js}
</script>
</body>
</html>
'''
open(OUT, 'w', encoding='utf-8').write(doc)
print(OUT, len(doc), 'bytes,', len(pages), 'pages')
