"""3.81 review: Accessibility, About this guide. usage: about.py src out"""
import re, sys
s = open(sys.argv[1], encoding='utf-8').read()
def sec(i):
    m = re.search(r'<section class="screen[^"]*" id="%s".*?</section>' % re.escape(i), s, re.S); assert m, i; return m
def rep(i, a, b, n=1):
    global s
    m = sec(i); blk = m.group(0); assert blk.count(a) == n, (i, a[:80], blk.count(a))
    s = s[:m.start()] + blk.replace(a, b) + s[m.end():]
MAIL = '<a class="st-mail" href="mailto:gmdp.support@greatermanchester-ca.gov.uk">gmdp.support@<wbr><span class="nw">greatermanchester-ca.gov.uk</span></a>'

# Accessibility (Contacts page 5)
rep('a11y', '<span class="k">Accessibility</span><p>If this guide is hard to read or use, it is available in large print, easy-read and other formats or languages.</p><p>To ask for one, please contact the GMDP Support Team at <a href="mailto:gmdp.support@greatermanchester-ca.gov.uk">gmdp.support@greatermanchester-ca.gov.uk</a>.</p></div>',
    '<span class="k">Other formats</span><p>If this guide is hard to read or use, you can ask for it in <strong>large print</strong>, <strong>easy read</strong>, another language or another format.</p><p>To ask, email the GMDP Support Team:</p>' + MAIL + '</div>\n<p class="st-p a11y-zoom">Text too small? Use Safari’s <strong>aA</strong> button to make it bigger.</p>')

# About this guide menu
rep('s6', '<p class="lead">Information about this guide:</p>', '<p class="lead">You do not need these pages to sign in. They are here for reference.</p>')

# Accessibility statement: show which part of the statement each page is
for n, i in enumerate(['a11y-stmt', 'a11y-stmt-2', 'a11y-stmt-3', 'a11y-stmt-4'], 1):
    bars = ''.join('<i class="on"></i>' if k == n else '<i></i>' for k in range(1, 5))
    m = sec(i).group(0); pb = re.search(r'<div class="pbox">', m).group(0)
    rep(i, pb, '<div class="pbox tp-stg"><div class="stg"><span class="stg-b" aria-hidden="true">%s</span><span class="stg-t">Accessibility statement · %d of 4</span></div>' % (bars, n))

rep('a11y-stmt-2', '<p class="st-p">We believe this guide meets <strong>WCAG 2.2 AA</strong>, but it has not had a full independent audit yet. Until then, it is <strong>partially compliant</strong>.</p>',
    '<p class="st-p">This guide is <strong>partially compliant</strong> with <strong>WCAG 2.2 AA</strong>, because of the issues below. It has not yet had a full independent audit.</p>')
rep('a11y-stmt-2', '<span>Screenshots show text from the App and NHS login. Each has a written description, and the steps are written out.</span>',
    '<span>Screenshots are pictures, so the text in them cannot be made bigger. Each one has a written description, and every step is also written out.</span>')
rep('a11y-stmt-3', '<a class="st-mail" href="mailto:gmdp.support@greatermanchester-ca.gov.uk">gmdp.support@<wbr>greatermanchester-ca.gov.uk</a>', MAIL)

# Privacy
rep('privacy', '<span>No sign-in, no cookies and no tracking.</span>', '<span>No sign-in, cookies or tracking. NHS login and the App have their own privacy notices.</span>')
rep('privacy', '<span>The website host, GitHub, may keep technical details such as IP addresses.</span>', '<span>The website host, GitHub, may keep technical details such as IP addresses, as most websites do.</span>')
rep('privacy', 'Questions? Email <a href="mailto:gmdp.support@greatermanchester-ca.gov.uk">GMDP Support</a>.', 'Questions? Email the <a href="mailto:gmdp.support@greatermanchester-ca.gov.uk">GMDP Support Team</a>.')

css = ('#app .st-mail .nw{white-space:nowrap}#app .screen .st-mail{overflow-wrap:normal}\n'
       '#app #a11y .tip .st-mail{margin:6px 0 2px}#app #a11y .a11y-zoom{margin-top:14px}\n'
       '')
s = s.replace('</style>', css + '</style>', 1)
open(sys.argv[2], 'w', encoding='utf-8').write(s); print('ok')
