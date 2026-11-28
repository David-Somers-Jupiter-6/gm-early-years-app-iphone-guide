"""Guide 3.95 (from 3.94) – Installing the App clips now show the green highlight inside the video: the clip pauses on a
freeze-frame while the box (and arrow) fades in and holds about 2 s, the rest of the screen dimmed a little; idle stretches cut.
Clips built by scripts/assets/install/v395/build_clips.py into clips/. The clip URL carries ?v=3.95 so phones fetch the new clips.
usage: python3 make395.py v3.94.html v3.95.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(x, y, n=1):
    global s
    assert s.count(x) == n, (x[:90], s.count(x)); s = s.replace(x, y)
rep('content="Version 3.94. A screen-by-screen', 'content="Version 3.95. A screen-by-screen')
rep('>3.94 (iPhone edition)<', '>3.95 (iPhone edition)<')
rep('<span class="cv-ver">Version 3.94</span>', '<span class="cv-ver">Version 3.95</span>')
old = re.search(r'<div class="rr"><span class="rv">3\.90</span>.*?</div>\n', s)
if old: s = s.replace(old.group(0), '')
rep('<div class="rr"><span class="rv">3.94</span>', '<div class="rr"><span class="rv">3.95</span><span class="rd">28 Nov 2026</span><p>Installing the App: clips pause to highlight what to tap</p></div>\n<div class="rr"><span class="rv">3.94</span>')
rep("return base()+n+'.mp4';", "return base()+n+'.mp4?v=3.95';")
open(dst, 'w', encoding='utf-8').write(s); print('written', dst, len(s))
