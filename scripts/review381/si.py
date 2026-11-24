"""3.81 review: Section 4 Signing in text and UX. usage: si.py src out"""
import re, sys
s = open(sys.argv[1], encoding='utf-8').read()
def sec(i):
    m = re.search(r'<section class="screen[^"]*" id="%s".*?</section>' % re.escape(i), s, re.S); assert m, i; return m
def rep(i, a, b, n=1):
    global s
    m = sec(i); blk = m.group(0); assert blk.count(a) == n, (i, a[:80], blk.count(a))
    s = s[:m.start()] + blk.replace(a, b) + s[m.end():]
def title(i, old, new):
    rep(i, '</span>%s</h2>' % old, '</span>%s</h2>' % new)
def tap(label): return '<div class="tap"><span class="lbl">Tap</span><span class="chip">%s</span></div>\n' % label
def tip(k, p, cls='tip'): return '<div class="%s step-tip"><span class="k">%s</span><p>%s</p></div>\n' % (cls, k, p)
SHOT = '<input type="checkbox" class="zt"'

# Page 1 – overview
LINK = '<svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><path d="M10 14a4.5 4.5 0 0 0 6.4 0l3-3a4.5 4.5 0 0 0-6.4-6.4l-1.2 1.2M14 10a4.5 4.5 0 0 0-6.4 0l-3 3a4.5 4.5 0 0 0 6.4 6.4l1.2-1.2" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>'
rep('s3', '<ol class="jr"', '<div class="step-body si-lead"><p>Follow the steps in order. Each step shows the screen you will see.</p></div>\n<ol class="jr"')
rep('s3', '<ul class="nd"><li>', '<ul class="nd"><li><span aria-hidden="true">%s</span>The text message with your Activation Link</li><li>' % LINK)
rep('s3', 'Your NHS login email address</li>', 'Your NHS login email address and password</li>')
s = s.replace('<li><span aria-hidden="true"><svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><circle cx="8" cy="12" r="4" fill="none" stroke="currentColor" stroke-width="2"/><path d="M12 12h9M18 12v3M21 12v2" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg></span>Your NHS login password</li>', '', 1)
rep('s3', 'Your iPhone, to get text messages', 'Your iPhone, with a mobile signal for text messages')

# Step 1
rep('step-1', '<p>Restarting first helps the sign-in go smoothly.</p>', '<p>Restarting first helps everything run smoothly.</p>')
rep('step-1', '<li>Turn off your iPhone.</li>\n<li>Wait at least 15 seconds.</li>\n<li>Turn your iPhone back on.</li>',
    '<li>Hold the side button and either volume button until you see the slider.</li>\n<li>Drag the slider to turn off. Wait 15 seconds.</li>\n<li>Hold the side button until you see the Apple logo.</li>')
rep('step-1', '<div class="tip step-tip"><span class="k">How to turn your iPhone off and on</span><p><strong>Off:</strong> on most iPhones, hold the side button and a volume button until the slider appears, then drag it. <strong>On:</strong> hold the side button until the Apple logo appears.</p></div>',
    tip('iPhone with a Home button?', 'Hold the side button only, then drag the slider.').strip())

# Step 2
rep('step-2', 'Open the <strong>Messages</strong> app and find the text message about your GM Early Years App account. Tap the link in the message.',
    'Open the <strong>Messages</strong> app. Find the text about your GM Early Years App account, then tap the link in it.')
rep('step-2', '<div class="tap">', tip('Cannot find the text?', 'See <a href="#s4-activation">Activation Link not received</a>.') + '<div class="tap">')

# Step 3
m = sec('step-3').group(0); p = re.search(r'<p>On the sign-in screen.*?</p>', m, re.S).group(0)
rep('step-3', p, '<p>On the sign-in screen, tap <strong>Continue to NHS login</strong>. It is under <strong>Parents and carers sign in below</strong>. The buttons further down are for staff only.</p>')

# Step 4
rep('step-4', 'Either choice is fine.</p>', 'Either is fine. It does not affect signing in.</p>')

# Step 5
title('step-5', 'Enter your credentials', 'Enter your email and password')
m = sec('step-5').group(0); p = re.search(r'<p>Type the.*?</p>', m, re.S).group(0)
rep('step-5', p, '<p>Type your <strong>NHS login</strong> email address and password, then tap <strong>Continue</strong>. Forgotten your password? Tap <strong>Forgot password?</strong></p>')

# Steps 6 and 7
title('step-6', 'Enter the security code', 'Wait for your security code')
m = sec('step-6').group(0); p = re.search(r'<p>NHS login may send.*?</p>', m, re.S).group(0)
rep('step-6', p, '<p>NHS login texts you a <strong>6-digit security code</strong>. It appears at the top of your screen. You do not need to tap it. Just tap <strong>Next</strong>.</p>')
title('step-7', 'Enter security code', 'Enter the security code')
rep('step-7', SHOT, tap('Continue') + SHOT)

# Step 8
m = sec('step-8').group(0); p = re.search(r'<p>If this is your own iPhone.*?</p>', m, re.S).group(0)
rep('step-8', p, '<p>Is this your own iPhone? Choose <strong>Yes, trust this device</strong> to get fewer codes next time. If not, choose <strong>Not now</strong>. Then tap <strong>Continue</strong>.</p>')

# Step 10
title('step-10', 'Send your verification code', 'Get your App code')
rep('step-10', '<p>The App shows the end of the mobile number on your App account. If it is yours, tap <strong>Send Code</strong>.</p>',
    '<p>The App shows the last few digits of your mobile number. If they match your number, tap <strong>Send Code</strong>.</p>')
rep('step-10', '<p>Contact your Health Visiting team.</p>', '<p>Do not tap Send Code. <a href="#hv">Contact your Health Visiting team</a>.</p>')

# Step 11 (tip page folded into step 12)
title('step-11', 'App verification code', 'Wait for your App code')
rep('step-11', '<p>The App sends you a text message with a <strong>verification code</strong>. The sender is shown as <strong>msverify</strong>.</p>',
    '<p>The App texts you a second code, from <strong>msverify</strong>. You do not need to tap it.</p>\n' +
    tip('Two different codes', 'This App code is not the same as the NHS login code from step 6.').strip())
rep('step-11', 'href="#step-11-tip"', 'href="#step-12"')
title('step-12', 'App verification code', 'Enter your App code')
rep('step-12', '<p>Type in the code from the <strong>msverify</strong> text message.</p>',
    '<p>Open the <strong>Messages</strong> app, find the text from <strong>msverify</strong>, then come back and type in the code.</p>')
rep('step-12', SHOT, tap('Verify Code') + SHOT)
rep('step-12', 'href="#step-11-tip"', 'href="#step-11"')

# Step 13 (tip page folded in)
m = sec('step-13').group(0); p = re.search(r'<p>When your code is accepted.*?</p>', m, re.S).group(0)
rep('step-13', p, '<p>When your code is accepted, the GM Early Years App opens. You will see <strong>Starting app…</strong> for a moment.</p>\n' +
    tip('Stuck on this screen?', 'If nothing happens after a few minutes, or you see an error, go to <a href="#s4">Support</a>.').strip())
rep('step-13', 'href="#step-13-tip"', 'href="#step-14"')

# Step 14
rep('step-14', 'It tells you if any forms need completing.', 'It shows if you have any forms to complete.')

# Styles: lead line on page 1
s = s.replace('</style>', '#app #s3 .si-lead{padding-top:0!important;padding-bottom:0!important;margin:10px 0 2px!important}#app #s3 .si-lead p{margin:0!important}\n</style>', 1)
# step 14 Back skipped the removed tip page
rep('step-14', 'href="#step-13-tip"', 'href="#step-13"')
# search titles
for i, t in [('step-5', 'Enter your email and password'), ('step-6', 'Wait for your security code'), ('step-7', 'Enter the security code'),
             ('step-10', 'Get your App code'), ('step-11', 'Wait for your App code'), ('step-12', 'Enter your App code')]:
    m = sec(i); blk = m.group(0); blk2, n = re.subn(r'data-title="Step (\d+) · [^"]*"', lambda x: 'data-title="Step %s · %s"' % (x.group(1), t), blk, count=1); assert n == 1, i
    s = s[:m.start()] + blk2 + s[m.end():]
# remove the two tip pages
for i in ['step-11-tip', 'step-13-tip']:
    m = re.search(r'<section class="screen[^"]*" id="%s".*?</section>\n?' % i, s, re.S); s = s[:m.start()] + s[m.end():]
assert 'step-11-tip' not in s and 'step-13-tip' not in s
open(sys.argv[2], 'w', encoding='utf-8').write(s)
print('ok')
