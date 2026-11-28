"""3.97: clip for the merged step 2 "Search for the App" (old steps 2 Tap Search + 3 Search for the App), as David asked:
 1. App Store Today screen with Search highlighted (the old step 2 screenshot - the recording opened straight on the Search tab), held ~2 s
 2. cross-fade into the recording; the search box is highlighted and the video pauses 1.5 s (screen dimmed only while paused)
 3. the search is typed (1.5x), then a 1.5 s pause on "gm early years"
 4. the results appear; pause 2.3 s with GM Early Years highlighted in the list
usage: python3 build_clip_search.py SOURCE.mp4 OUT.mp4   (SOURCE = ScreenRecording_11-28-2026_Combined_v2_Get.mp4, 750x1624, 60 fps)"""
import sys, os, subprocess
import numpy as np
from PIL import Image, ImageDraw
SRC, OUT = sys.argv[1], sys.argv[2]
HERE = os.path.dirname(os.path.abspath(__file__))
W, H, FPS = 750, 1624, 30
G = (181, 229, 29); LW = 7; DIM = 0.30; FADE_IN, FADE_OUT = 0.30, 0.15

def mark(box, draw=True):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    if draw: ImageDraw.Draw(im).rectangle(list(box), outline=G + (255,), width=LW)
    a = np.asarray(im).astype(np.float32)
    keep = np.zeros((H, W), np.float32); x0, y0, x1, y1 = box; keep[y0:y1 + 1, x0:x1 + 1] = 1
    return a[..., :3], a[..., 3:] / 255.0, keep[..., None]

# the old step 2 screenshot (417 x 904, highlight already drawn: box and arrow at x 340-407, y 768-881) scaled to 750 x 1624
today = np.asarray(Image.open(os.path.join(HERE, '..', 'shot09.png')).convert('RGB').resize((W, H), Image.LANCZOS)).astype(np.float32)
sx, sy = W / 417, H / 904
M = {'tab': mark((int(336 * sx), int(764 * sy), int(411 * sx), int(885 * sy)), draw=False),   # keep the drawn highlight bright
     'search': mark((32, 96, 600, 210)),
     'row': mark((28, 238, 548, 372))}

# plan: ('still', seconds, highlight) | ('xfade', source time, seconds) | ('play', from, to, speed, highlight) | ('hold', at, seconds, highlight)
PLAN = [('still', 0.5, None), ('still', 2.2, 'tab'), ('xfade', 9.62, 0.4),
        ('play', 9.62, 9.95, 1, None), ('hold', 9.95, 1.5, 'search'),
        ('play', 9.95, 16.45, 1.5, 'search'), ('hold', 16.45, 1.5, 'search'),
        ('play', 19.45, 20.45, 1, None), ('hold', 20.45, 2.3, 'row')]

def items():
    for p in PLAN:
        if p[0] == 'still':
            for _ in range(round(p[1] * FPS)): yield ('still', None, p[2], 0, True)
        elif p[0] == 'xfade':
            n = round(p[2] * FPS)
            for i in range(n): yield ('mix', p[1], None, (i + 1) / n, False)
        elif p[0] == 'play':
            _, a, b, sp, hl = p
            for i in range(round((b - a) / sp * FPS)): yield ('src', a + i * sp / FPS, hl, 0, False)
        else:
            _, t, d, hl = p
            for _ in range(round(d * FPS)): yield ('src', t, hl, 0, True)

a0 = 9.6
dec = subprocess.Popen(['ffmpeg', '-v', 'error', '-ss', f'{a0}', '-to', '21', '-i', SRC, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                        '-vf', 'scale=418:904:flags=lanczos,format=yuv420p', '-an', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '22',
                        '-profile:v', 'high', '-level', '4.0', '-movflags', '+faststart', OUT], stdin=subprocess.PIPE)
cur, cur_t, idx, alpha, shown, last_still, dim = None, a0 - 1, 0, 0.0, None, None, 0.0
def src_frame(t):
    global cur, cur_t, idx
    while cur is None or cur_t + 1e-6 < t - 1 / 120:
        buf = dec.stdout.read(W * H * 3)
        if len(buf) < W * H * 3: break
        cur = np.frombuffer(buf, np.uint8).reshape(H, W, 3); cur_t = a0 + idx / 60; idx += 1
    return cur.astype(np.float32)
n = 0
for kind, t, hl, mix, hold in items():
    dim = min(1.0, dim + 1 / (FADE_IN * FPS)) if (hl and hold) else max(0.0, dim - 1 / (FADE_IN * FPS))   # dim only while paused
    if hl: alpha = min(1.0, alpha + 1 / (FADE_IN * FPS)); shown = hl
    else: alpha = max(0.0, alpha - 1 / (FADE_OUT * FPS))
    if kind == 'still': f = today.copy()
    elif kind == 'mix': f = last_still * (1 - mix) + src_frame(t) * mix
    else: f = src_frame(t)
    if shown and alpha > 0 and kind != 'mix':
        rgb, a, keep = M[shown]
        f = f * (1 - DIM * min(alpha, dim) * (1 - keep)); f = f * (1 - a * alpha) + rgb * a * alpha
    if kind == 'still': last_still = f.copy()
    enc.stdin.write(np.clip(f, 0, 255).astype(np.uint8).tobytes()); n += 1
enc.stdin.close(); enc.wait(); dec.kill()
print(OUT, f'{n / FPS:.1f}s', os.path.getsize(OUT))
