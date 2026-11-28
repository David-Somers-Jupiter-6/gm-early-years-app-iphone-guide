"""Guide 3.94 (from 3.93) – Installing the App: new screenshots taken from the clips (David, 28 Nov: "Great idea. Yes please"),
so the picture shown after each clip matches it. Same green highlight style (box #B5E51D, arrow below).
Step 2 keeps its old screenshot (no clip). Step 3/4 wording now matches today's App Store (GMCA icon; Get button).
Highlights: scripts/assets/install/v394/draw_highlights.py (frames from ScreenRecording_11-28-2026_Combined_v2_Get.mp4).
usage: python3 make394.py v3.93.html v3.94.html [--embed CLIPS_DIR]   (--embed only for a 3.93 chat copy input; clip data is carried over)"""
import re, sys, os, io, base64
from PIL import Image
src, dst = sys.argv[1], sys.argv[2]
A = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'install', 'v394')
s = open(src, encoding='utf-8').read()

def rep(x, y, n=1):
    global s
    assert s.count(x) == n, (x[:90], s.count(x)); s = s.replace(x, y)

rep('content="Version 3.93. A screen-by-screen', 'content="Version 3.94. A screen-by-screen')
rep('>3.93 (iPhone edition)<', '>3.94 (iPhone edition)<')
rep('<span class="cv-ver">Version 3.93</span>', '<span class="cv-ver">Version 3.94</span>')
old = re.search(r'<div class="rr"><span class="rv">3\.89</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.93</span>', '<div class="rr"><span class="rv">3.94</span><span class="rd">28 Nov 2026</span><p>Installing the App: new screenshots that match the clips</p></div>\n<div class="rr"><span class="rv">3.93</span>')

# id: (file, y, et, eb, pb) in 417 x 902 px; crop heights (pb - y) kept as before so the pages do not change size
SHOTS = {'z-in06': ('shot06c.png', 0, 61, 163, 460),
         'z-in10': ('shot10c.png', 30, 53, 156, 600),
         'z-in13': ('shot13c.png', 0, 158, 259, 370),
         'z-in15': ('shot15c.png', 0, 156, 259, 370),
         'z-in17': ('shot17c.png', 0, 158, 259, 370),
         'z-in18': ('shot18c.png', 120, 386, 459, 720)}
for zid, (fn, y, et, eb, pb) in SHOTS.items():
    im = Image.open(os.path.join(A, fn)).convert('RGB'); w, h = im.size; assert (w, h) == (417, 902)
    buf = io.BytesIO(); im.save(buf, 'JPEG', quality=84, optimize=True, progressive=True)
    b64 = base64.b64encode(buf.getvalue()).decode()
    i = s.index(f'<label class="shot has-clip" for="{zid}"'); j = s.index('</label>', i)
    blk = s[i:j]
    blk, n1 = re.subn(r'style="--cw:417;--ch:\d+;--fw:417;--x:0;--y:\d+;--et:\d+;--eb:\d+;--pb:\d+;--ih:\d+"',
                      f'style="--cw:417;--ch:{pb - y};--fw:417;--x:0;--y:{y};--et:{et};--eb:{eb};--pb:{pb};--ih:{h}"', blk)
    blk, n2 = re.subn(r'src="data:image/jpeg;base64,[^"]+" width="417" height="\d+"', f'src="data:image/jpeg;base64,{b64}" width="417" height="{h}"', blk)
    assert n1 == 1 and n2 == 1, zid
    s = s[:i] + blk + s[j:]

# wording that matches today's App Store
rep('Look for <strong>GM Early Years</strong> with the ABC blocks icon.</p>',
    'Look for <strong>GM Early Years</strong> by Greater Manchester Early Years.</p>')
rep('<p>Next to <strong>GM Early Years</strong>, tap the <strong>Download</strong> button.</p>\n'
    '<div class="tip step-tip"><span class="k">Button says Get?</span><p>Tap <strong>Get</strong>. Your iPhone may ask for Face ID, Touch ID or your Apple ID password.</p></div>\n'
    '<div class="tap"><span class="lbl">Tap</span><span class="chip">Download</span></div>',
    '<p>Next to <strong>GM Early Years</strong>, tap <strong>Get</strong>. Your iPhone may ask for Face ID, Touch ID or your Apple ID password.</p>\n'
    '<div class="tip step-tip"><span class="k">Button shows a cloud?</span><p>You have had the App before. Tap the cloud.</p></div>\n'
    '<div class="tap"><span class="lbl">Tap</span><span class="chip">Get</span></div>')
rep('GM Early Years in the App Store results with the Download button highlighted', 'GM Early Years in the App Store results with the Get button highlighted', 2)
open(dst, 'w', encoding='utf-8').write(s); print('written', dst, len(s))
