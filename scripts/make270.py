"""Guide 2.70 (from 2.69). NHS login account issues pages (s4-nhs and its eight pages) get title box
option 6c (David, 17 Nov): a dark NHS blue band across the top reading "NHS login | Account issues",
an NHS blue title box, and a white circle with an icon for the page in the bottom right.
On screens <=600 px tall (iPhone SE in Safari) the icon is hidden and the band is slimmer so every page still fits.
The white NHS mark is scripts/nhsmark_white.png (cut from the NHS login logo already in the guide).
usage: python3 make270.py v2.69.html v2.70.html
"""
import re, sys, base64, os
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a)); s = s.replace(a, b)
MARK = 'data:image/png;base64,' + base64.b64encode(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'nhsmark_white.png'), 'rb').read()).decode()
P = {  # page: icon paths (24 x 24)
 's4-nhs':     '<circle cx="12" cy="8" r="4" fill="currentColor"/><path d="M4 20.5c.7-4.2 4-6.6 8-6.6s7.3 2.4 8 6.6z" fill="currentColor"/>',
 's4-setup':   '<circle cx="10" cy="8" r="4" fill="currentColor"/><path d="M2.5 20.5c.7-4.2 3.8-6.6 7.5-6.6 1.6 0 3 .4 4.2 1.2" fill="currentColor"/><path d="M18.5 13v8M14.5 17h8" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/>',
 's4-cannot':  '<rect x="5" y="10.5" width="14" height="10" rx="2" fill="currentColor"/><path d="M8 10.5V8a4 4 0 018 0v2.5" fill="none" stroke="currentColor" stroke-width="2"/>',
 's4-pw':      '<path d="M14.5 3.5a5 5 0 00-4.7 6.7L3.5 16.5V20h3.5v-2h2v-2h2l1.3-1.3A5 5 0 1014.5 3.5zm1.5 5a1.5 1.5 0 110-3 1.5 1.5 0 010 3z" fill="currentColor"/>',
 's4-code':    '<path d="M7 2.5h10a2 2 0 012 2v15a2 2 0 01-2 2H7a2 2 0 01-2-2v-15a2 2 0 012-2z" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M8.5 7.5h7v5h-4l-3 2.2z" fill="currentColor"/><circle cx="12" cy="18.3" r="1" fill="currentColor"/>',
 's4-email':   '<rect x="2.5" y="5" width="19" height="14" rx="2" fill="currentColor"/><path d="M3.5 6.5l8.5 6.3 8.5-6.3" fill="none" stroke="#fff" stroke-width="1.8" stroke-linejoin="round"/>',
 's4-pwchange':'<path d="M19.5 12a7.5 7.5 0 01-13.2 4.9M4.5 12a7.5 7.5 0 0113.2-4.9" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/><path d="M18.6 3.5v4.2h-4.2M5.4 20.5v-4.2h4.2" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/><circle cx="12" cy="12" r="2.2" fill="currentColor"/>',
 's4-mobile':  '<rect x="6" y="2.5" width="12" height="19" rx="2.4" fill="none" stroke="currentColor" stroke-width="2"/><path d="M10 5.5h4" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/><circle cx="12" cy="18" r="1.2" fill="currentColor"/>',
 's4-name':    '<rect x="2.5" y="5" width="19" height="14" rx="2" fill="none" stroke="currentColor" stroke-width="1.9"/><circle cx="8.5" cy="11" r="2.3" fill="currentColor"/><path d="M5 16.5c.4-2 1.8-3 3.5-3s3.1 1 3.5 3z" fill="currentColor"/><path d="M14 10h5M14 13.5h4" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>',
}
BAND = '<div class="tb-band" aria-hidden="true"><i class="tb-mark"></i><b>NHS login</b><span>Account issues</span></div>'
for pid, icon in P.items():
    i = s.find('<section class="screen" id="%s"' % pid); assert i > 0, pid
    a = s.find('<div class="pbox"><h2 class="h2" tabindex="-1">', i); assert 0 < a < i + 3000, pid
    old = '<div class="pbox"><h2 class="h2" tabindex="-1">'
    s = s[:a] + '<div class="pbox nhs-band">' + BAND + '<span class="tb-ic" aria-hidden="true"><svg viewBox="0 0 24 24" width="22" height="22">' + icon + '</svg></span><h2 class="h2" tabindex="-1">' + s[a + len(old):]
CSS = '''/* 2.70 NHS login account issues: title box with an NHS login band and a page icon (option 6c) */
#app .screen .pbox.nhs-band{background:linear-gradient(135deg,#005eb8 0%,#0b4f9c 100%)!important;padding-top:0!important}
.pbox.nhs-band .tb-band{position:absolute;left:0;right:0;top:0;height:30px;background:#003087;display:flex;align-items:center;gap:10px;padding:0 16px;color:#cfe3f7;font:700 12px/1 var(--font-body);letter-spacing:.08em;text-transform:uppercase;z-index:1}
.pbox.nhs-band .tb-mark{display:block;width:32px;height:13px;background:url(@@MARK@@) center/contain no-repeat}
.pbox.nhs-band .tb-band b{color:#fff;font-weight:700;text-transform:none;letter-spacing:.02em;font-size:13px}
.pbox.nhs-band .tb-band span{border-left:1px solid rgba(255,255,255,.35);padding-left:10px}
.pbox.nhs-band .tb-ic{position:absolute;right:14px;bottom:14px;width:40px;height:40px;border-radius:50%;display:grid;place-items:center;color:#005eb8;background:#fff;box-shadow:0 3px 8px rgba(0,0,0,.25);z-index:1}
#app .screen .pbox.nhs-band h2{max-width:calc(100% - 52px)}
@media (max-height:600px){#app .screen .pbox.nhs-band{padding-top:34px!important}.pbox.nhs-band .tb-band{height:26px}.pbox.nhs-band .tb-ic{display:none}#app .screen .pbox.nhs-band h2{max-width:100%}}
'''.replace('@@MARK@@', MARK)
rep('@media print{', CSS + '@media print{')
rep('Carer role v2.69', 'Carer role v2.70'); rep('Version 2.69 iPhone', 'Version 2.70 iPhone')
rep('<div>Version 2.69</div>', '<div>Version 2.70</div>'); rep('>2.69 – REVIEW DRAFT', '>2.70 – REVIEW DRAFT')
old = re.search(r'<div class="rr"><span class="rv">2\.67</span>.*?</div>\n', s).group(0); s = s.replace(old, '')
rep('<div class="rr"><span class="rv">2.69</span>', '<div class="rr"><span class="rv">2.70</span><span class="rd">17 Nov 2026</span><p>NHS login account issues pages: NHS login band and a page icon in the title box</p></div>\n<div class="rr"><span class="rv">2.69</span>')
open(dst, 'w', encoding='utf-8').write(s); print('written', dst)
