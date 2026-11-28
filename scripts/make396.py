"""Guide 3.96 (from 3.95) – step 1 clip holds 2 s on the opened App Store (David, 28 Nov). Clip from scripts/assets/install/v396/build_clips.py.
(3.95 note follows.) Installing the App clips now show the green highlight inside the video: the clip pauses on a
freeze-frame while the box (and arrow) fades in and holds about 2 s, the rest of the screen dimmed a little; idle stretches cut.
Clips built by scripts/assets/install/v395/build_clips.py into clips/. The clip URL carries ?v=3.96 so phones fetch the new clips.
usage: python3 make395.py v3.95.html v3.96.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(x, y, n=1):
    global s
    assert s.count(x) == n, (x[:90], s.count(x)); s = s.replace(x, y)
rep('content="Version 3.95. A screen-by-screen', 'content="Version 3.96. A screen-by-screen')
rep('>3.95 (iPhone edition)<', '>3.96 (iPhone edition)<')
rep('<span class="cv-ver">Version 3.95</span>', '<span class="cv-ver">Version 3.96</span>')
old = re.search(r'<div class="rr"><span class="rv">3\.91</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.95</span>', '<div class="rr"><span class="rv">3.96</span><span class="rd">28 Nov 2026</span><p>Installing the App: step 1 clip pauses on the opened App Store</p></div>\n<div class="rr"><span class="rv">3.95</span>')
rep("return base()+n+'.mp4?v=3.95';", "return base()+n+'.mp4?v=3.96';")
open(dst, 'w', encoding='utf-8').write(s); print('written', dst, len(s))
