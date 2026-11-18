"""Guide 2.83 (from 2.82). Section 3 · NHS login tidy-up (David, 18 Nov):
 1. One-line titles on the NHS login pages (fit at 375 px wide; all but Step 8 also at 360 px).
 2. NHS login step title boxes the same as Section 6 Signing in: 110 px tall, title and underline in
    exactly the same place (the NHS login band stays on top; the progress bar sits under it).
    iPhone SE in Safari (compact mode, band hidden and label shown): same spacing as the Signing in boxes there.
 3. Wording: Section 3 start page and Step 8 note no longer send people back to the checklist
    (it now comes later); Step 4 no longer repeats its tip; Contact & support links worded the same;
    "NHS login Support team" spelled one way throughout.
usage: python3 make283.py v2.82.html v2.83.html
"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
def page(pid):
    m = re.search(r'<section class="screen" id="%s".*?</section>' % re.escape(pid), s, re.S); assert m, pid; return m
def edit(pid, a, b, n=1):
    global s
    m = page(pid); blk = m.group(0)
    assert blk.count(a) == n, (pid, a[:90], blk.count(a))
    s = s[:m.start()] + blk.replace(a, b) + s[m.end():]

# 1. titles: (page, number, new visible title); tips keep their step's title
STEPS = [('a', 1, 'Go to NHS login'), ('b', 2, 'Sign-in page opens'), ('c', 3, 'Email and password'),
         ('d', 4, 'Security code page'), ('e', 5, 'Get your security code'), ('f', 6, 'Enter the security code'),
         ('g', 7, 'Checking your details'), ('h', 8, 'Your NHS account page')]
for L, n, t in STEPS:
    for pid in ('step-' + L, 'step-' + L + '-tip'):
        if not re.search(r'id="%s"' % pid, s): continue
        blk = page(pid).group(0)
        h2 = re.search(r'<h2 tabindex="-1"><span class="vh">([^<]*)</span>([^<]*)</h2>', blk)
        pre = h2.group(1)
        newpre = pre.replace('Step %d: ' % n, 'Step %d of 8: ' % n)
        edit(pid, h2.group(0), '<h2 tabindex="-1"><span class="vh">%s</span>%s</h2>' % (newpre, t))
        dt = re.search(r'data-title="Step %d · ([^"]*)"' % n, blk)
        if pid == 'step-' + L:
            edit(pid, dt.group(0), 'data-title="Step %d · %s"' % (n, t))
edit('nhs-info', '<h2 class="h2" tabindex="-1">Information needed from NHS login</h2>', '<h2 class="h2" tabindex="-1">Information needed</h2>')
edit('nhs-info', '<b>NHS login</b><span>Information</span>', '<b>NHS login</b><span>Part a</span>')
edit('s4-signin', '<b>NHS login</b><span>Signing in</span>', '<b>NHS login</b><span>Part b</span>')

# 2. title boxes: same size and title position as Section 6 Signing in
NHSIDS = '#step-a,#step-b,#step-b-tip,#step-c,#step-c-tip,#step-d,#step-d-tip,#step-e,#step-e-tip,#step-f,#step-f-tip,#step-g,#step-g-tip,#step-h,#step-h-tip'
SEL = '#app .screen:is(%s):not(#contents) :is(.pbox,.tp-body).eyx.eyx-nhs:has(.stepper)' % NHSIDS
CSS = ('/* 2.83 NHS login step title boxes = Section 6 Signing in boxes (110 px, one-line title, same title and underline position) */\n'
       '%s{min-height:110px!important;padding-top:38px!important}\n'
       '%s .stepper.nhs-steps{margin-bottom:16px!important}\n'
       '@media (max-height:600px){%s{min-height:72px!important;padding-top:8px!important}%s .stepper.nhs-steps{margin-bottom:6px!important}}\n'
       % (SEL, SEL, SEL, SEL))
rep('@media print{', CSS + '@media print{')

# 3. wording
edit('s4-signin', '<p class="lead">Follow these illustrated steps to sign in to your own NHS login account using an iPhone or computer.</p>\n'
     '<p class="lead">If you can sign in, return to <a href="#c2">question 2 of the checklist</a> and continue. If you cannot sign in, use the <a href="#s4-cannot">NHS login recovery guidance</a>. GMDP Support cannot administer NHS login accounts.</p>',
     '<p class="lead">Follow these steps to sign in to your own NHS login account, on your iPhone or on a computer. You use the same email address and password for the GM Early Years App.</p>\n'
     '<p class="lead">If you cannot sign in, see <a href="#s4-nhs">NHS login account issues</a> in Section 7 · Troubleshooting.</p>\n'
     '<p class="lead nhs-only">(The GMDP Support team cannot assist with NHS login account issues, as they do not have access to NHS login accounts.)</p>')
edit('step-d', '<p>If NHS login asks for a security code, it will send a 6-digit code to the mobile number registered with NHS login. Check that the last digits shown are your own. If you cannot use that number, follow the recovery option on the NHS login screen.</p>',
     '<p>If NHS login asks for a security code, it sends a 6-digit code by text message to the mobile number registered with your NHS login.</p>')
edit('step-f-tip', 'please contact the NHS login Support Team (see <a href="#s5-2">Section 8</a>).',
     'please contact the NHS login Support team (see <a href="#s5-2">Section 8 · Contact &amp; support</a>).')
edit('step-g-tip', 'please contact the NHS login Support Team. See <a href="#s5-2">Section 8 · Contact &amp; support</a>.',
     'please contact the NHS login Support team (see <a href="#s5-2">Section 8 · Contact &amp; support</a>).')
edit('step-h-tip', ' See <a href="#s2">Checklist</a> at the start of this guide.</p>', '</p>')
edit('step-h-tip', '<p style="margin-top:14px">When you have signed in successfully, return to <a href="#c2">question 2 of the checklist</a> and answer “Yes”.</p>',
     '<p style="margin-top:14px">You have now signed in to NHS login. Tap <strong>Next</strong> to go to <a href="#hv">Section 4 · Contact your Health Visiting team</a>.</p>')
n = s.count('NHS login Support Team'); s = s.replace('NHS login Support Team', 'NHS login Support team'); print('Support Team -> team:', n)
rep('.lead.nhs-only{', '.lead.nhs-only{', 0)
rep('@media print{', '#s4-signin .lead.nhs-only{font-size:15px;color:var(--muted,#4c6272)}\n@media print{')

# 4. version
rep('Carer role v2.82', 'Carer role v2.83'); rep('Version 2.82 iPhone', 'Version 2.83 iPhone')
rep('<div>Version 2.82</div>', '<div>Version 2.83</div>'); rep('>2.82 – REVIEW DRAFT', '>2.83 – REVIEW DRAFT')
old = re.search(r'<div class="rr"><span class="rv">2\.80</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">2.82</span>', '<div class="rr"><span class="rv">2.83</span><span class="rd">18 Nov 2026</span><p>NHS login: one-line titles, title boxes match Signing in, wording updated</p></div>\n<div class="rr"><span class="rv">2.82</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
