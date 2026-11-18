"""Guide 2.84 (from 2.83). Section 4 · Your Health Visiting team title boxes (David, 18 Nov):
 same design as the NHS login title boxes - a strip at the top with the NHS logo and "Health Visiting team",
 then the title and underline, on the NHS login blue. No NHS logo in the corner, no ABC blocks behind.
 Both Section 4 pages (hv, hv-confirm). Titles shortened to one line, as the strip says Health Visiting team:
 "Contact your team" and "Confirm your details" (Contents and Search keep the full names).
usage: python3 make284.py v2.83.html v2.84.html
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

BAND = '<div class="eyb eyb-nhs" aria-hidden="true"><i class="eym"></i><b>Health Visiting team</b></div>'
old = re.search(r'<div class="tp-card has-badge"><div class="tp-body"><h2 class="h2 tp-h" tabindex="-1">Contact your Health Visiting team</h2><span class="tp-n" aria-hidden="true">4</span></div><img alt="NHS" class="nhsbadge sm nhs-mark" src="[^"]+"/></div>', page('hv').group(0)).group(0)
edit('hv', old, '<div class="pbox eyx eyx-nhs eyx-hv">' + BAND + '<span class="tp-n" aria-hidden="true">4</span><h2 class="h2" tabindex="-1">Contact your team</h2></div>')
edit('hv-confirm', '<div class="pbox"><h2 class="h2" tabindex="-1">Confirm your NHS login contact details</h2></div>',
     '<div class="pbox eyx eyx-nhs eyx-hv">' + BAND + '<h2 class="h2" tabindex="-1">Confirm your details</h2></div>')
# the old Section 4 title box rules no longer match anything; remove them so they cannot come back into play
rep('#app .screen#hv:not(#contents) .tp-card .tp-body:not(.eyx),#app .screen#s5-hv:not(#contents) .pbox:not(.eyx){', '#app .screen#s5-hv:not(#contents) .pbox:not(.eyx){')
rep('#app .screen#hv-confirm:not(#contents) .pbox:not(.eyx){background:linear-gradient(135deg,#003087 0%,#005eb8 100%)!important}\n', '')

# About your account (David, 18 Nov): one highlight only, so the page reads in one flow
edit('acct', '<p class="info-lead">Your Health Visiting team sets up a GM Early Years App account for the <strong>child\'s mother</strong> or <strong>primary carer</strong>.</p>\n'
     '<div class="tip info-q"><p>In this guide, this person is called the <strong>account holder</strong>.</p></div>\n'
     '<ul class="facts acct-list"><li>Only the account holder can sign in.</li>'
     '<li>They use the same <strong>email address</strong> and <strong>password</strong> as their own NHS login account.</li></ul>\n'
     '<div class="amber info-q"><p>A partner or another family member cannot sign in to the account.</p></div>',
     '<p class="info-lead">Your Health Visiting team sets up a GM Early Years App account for the <strong>child\'s mother</strong> or <strong>primary carer</strong>.</p>\n'
     '<p class="info-lead acct-who">In this guide, we call this person the <strong>account holder</strong>.</p>\n'
     '<ul class="facts acct-list"><li>Only the account holder can sign in.</li>'
     '<li>They sign in with the same <strong>email address</strong> and <strong>password</strong> as their own NHS login.</li></ul>\n'
     '<div class="amber info-q"><p>A partner or another family member <strong>cannot</strong> sign in to the account.</p></div>')
rep('#acct .acct-list{margin-top:12px;margin-bottom:12px}', '#acct .acct-who{margin-top:10px}#acct .acct-list{margin-top:16px;margin-bottom:18px}')

# version
rep('Carer role v2.83', 'Carer role v2.84'); rep('Version 2.83 iPhone', 'Version 2.84 iPhone')
rep('<div>Version 2.83</div>', '<div>Version 2.84</div>'); rep('>2.83 – REVIEW DRAFT', '>2.84 – REVIEW DRAFT')
old = re.search(r'<div class="rr"><span class="rv">2\.81</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">2.83</span>', '<div class="rr"><span class="rv">2.84</span><span class="rd">18 Nov 2026</span><p>Your Health Visiting team title boxes have an NHS strip, like NHS login; About your account has one highlight</p></div>\n<div class="rr"><span class="rv">2.83</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
