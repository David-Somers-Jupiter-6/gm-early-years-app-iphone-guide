"""3.81 review: Contact your HV team, Support menu, Contacts. usage: contacts.py src out"""
import re, sys
s = open(sys.argv[1], encoding='utf-8').read()
_k = '#app #s5 :is(.wc-hv,.wc-nhs) .wc-tile{background:#005eb8 url('
_a = s.index(_k) + len(_k); NHS = s[_a:s.index(')', _a)]
def sec(i):
    m = re.search(r'<section class="screen[^"]*" id="%s".*?</section>' % re.escape(i), s, re.S); assert m, i; return m
def rep(i, a, b, n=1):
    global s
    m = sec(i); blk = m.group(0); assert blk.count(a) == n, (i, a[:80], blk.count(a))
    s = s[:m.start()] + blk.replace(a, b) + s[m.end():]

# Contact your Health Visiting team
rep('hv', '<h2 class="h2" tabindex="-1">How to contact your HV team</h2>', '<h2 class="h2" tabindex="-1">Contact your Health Visiting team</h2>')
rep('hv', '<p class="q-hint hv-how">Find your team’s contact details:</p>', '<p class="q-hint hv-how">Choose your area, then your team:</p>')
rep('hv', '<span class="hv-num" aria-hidden="true">1</span>Locality</label>', '<span class="hv-num" aria-hidden="true">1</span>Area</label>')
rep('hv', '<option value="">Choose a locality first</option>', '<option value="">Choose an area first</option>')
m = sec('hv'); n = m.group(0).count('<p class="hv-tap">Tap the <strong>contact number</strong> to <strong>call</strong>.</p>')
rep('hv', '<p class="hv-tap">Tap the <strong>contact number</strong> to <strong>call</strong>.</p>',
    '<p class="hv-tap">Tap the <strong>number</strong> to <strong>call</strong>. Say you need help signing in to the GM Early Years App.</p>', n)

# Support
rep('s4', '<p class="tc-lead">What is the problem?</p>', '<p class="tc-lead">What do you need help with?</p>')
rep('s4', '<span class="tc-s">Signing in, password, security codes</span><span class="tc-w fit-opt">Help from: <b>NHS login Support team</b></span>',
    '<span class="tc-s">Setting up, signing in, password, security codes</span>')
rep('s4', '<span class="tc-s">Activation Link, installing, sign-in problems</span>', '<span class="tc-s">Activation Link, installing the App, App codes</span>')
m = sec('s4').group(0); a = m.index('<span class="tc-tile">'); z = m.index('</span>', a) + 7
mm = sec('s4'); s = s[:mm.start()+a] + '<span class="tc-tile tc-nhsmark" aria-hidden="true"></span>' + s[mm.start()+z:]

# Contacts
rep('s5', '<em>For:</em> your App account – your details and Activation Link', '<em>For:</em> your App account details and your Activation Link')
rep('s5', '<em>For:</em> your NHS login – setting up, signing in, security codes', '<em>For:</em> setting up or signing in to NHS login, and security codes')
rep('s5', '<em>For:</em> problems with the App itself, once NHS login works', '<em>For:</em> problems with the App itself, after NHS login works')
TEAM = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='white' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E"
        "%3Ccircle cx='9' cy='8' r='3.2'/%3E%3Cpath d='M3 19c.8-3.4 3.2-5.2 6-5.2s5.2 1.8 6 5.2'/%3E%3Ccircle cx='16.5' cy='9' r='2.6'/%3E%3Cpath d='M16 13.9c2.6.1 4.3 1.8 5 4.6'/%3E%3C/svg%3E")
rep('s5-gmdp', '<p class="info-lead sp-lead">For GM Early Years App problems after NHS login works, such as an App verification-code error.</p>',
    '<p class="info-lead sp-lead">For problems with the GM Early Years App after NHS login works, such as an App code error.</p>')
rep('s5-gmdp', '<span>gmdp.support@greatermanchester-ca.gov.uk</span>', '<span class="sp-addr">gmdp.support@<wbr>greatermanchester-ca.gov.uk</span>')

css = ('#app #s4 .tc-nhsmark{background:#005eb8 url(%s) center/30px auto no-repeat!important}\n' % NHS +
       '#app #s5 .wc-hv .wc-tile{background:#005eb8 url("%s") center/26px 26px no-repeat!important}\n' % TEAM +
       '#app #s5-gmdp .sp-addr{overflow-wrap:normal!important;word-break:normal!important}\n')
s = s.replace('</style>', css + '</style>', 1)
open(sys.argv[2], 'w', encoding='utf-8').write(s); print('ok')
