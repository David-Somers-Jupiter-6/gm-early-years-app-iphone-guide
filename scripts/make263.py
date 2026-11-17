"""Guide 2.63 (from 2.62). Checklist summary (sum) - David, 17 Nov:
- Next always goes to Section 3 Signing in (s3). It is green only when all four answers are Yes;
  with any cross it stays blue (it used to go to Section 4 Troubleshooting).
- NHS login account cross: Get help opens "Set up NHS login" (s4-setup) (was s4-problems).
- Amber message: "Select Get help next to each cross." (removed "or Next for more help").
- No pages deleted (David: sort out "What stopped you signing in?" later).
usage: python3 make263.py v2.62.html v2.63.html
"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
def edit(pid, a, b, n=1):
    global s
    m = re.search(r'<section class="screen" id="%s".*?</section>' % re.escape(pid), s, re.S); blk = m.group(0)
    assert blk.count(a) == n, (pid, a[:90], blk.count(a))
    s = s[:m.start()] + blk.replace(a, b) + s[m.end():]

edit('sum', 'data-yes="s3" data-no="s4"', 'data-yes="s3" data-no="s3"')
edit('sum', '<a class="nav-btn nav-next go-no" href="#s4">', '<a class="nav-btn nav-next go-no" href="#s3">')
edit('sum', '<p class="sum-s">You do not have NHS login yet</p></div><a class="sum-help" href="#s4-problems">',
     '<p class="sum-s">You do not have NHS login yet</p></div><a class="sum-help" href="#s4-setup">')
edit('sum', '<p>Select <strong>Get help</strong> next to each cross, or <strong>Next</strong> for more help.</p>',
     '<p>Select <strong>Get help</strong> next to each cross.</p>')

rep('Carer role v2.62', 'Carer role v2.63'); rep('Version 2.62 iPhone', 'Version 2.63 iPhone')
rep('<div>Version 2.62</div>', '<div>Version 2.63</div>'); rep('>2.62 – REVIEW DRAFT', '>2.63 – REVIEW DRAFT')
old = re.search(r'<div class="rr"><span class="rv">2\.60</span>.*?</div>\n', s).group(0); s = s.replace(old, '')
rep('<div class="rr"><span class="rv">2.62</span>', '<div class="rr"><span class="rv">2.63</span><span class="rd">17 Nov 2026</span><p>Checklist summary: Next always goes to Signing in; NHS login Get help opens Set up NHS login</p></div>\n<div class="rr"><span class="rv">2.62</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
