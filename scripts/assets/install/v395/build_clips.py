"""3.95: install clips with the green highlight (same style as the screenshots) inside the video.
Before each tap the video pauses on a freeze-frame while the highlight fades in and holds, with the rest of the
screen dimmed a little; idle stretches (identical frames) are cut so the clips stay short.
usage: python3 build_clips.py SOURCE.mp4 OUTDIR   (SOURCE = ScreenRecording_11-28-2026_Combined_v2_Get.mp4, 750x1624, 60 fps)"""
import sys, os, subprocess
import numpy as np
from PIL import Image, ImageDraw
SRC, OUT = sys.argv[1], sys.argv[2]; os.makedirs(OUT, exist_ok=True)
W, H, FPS = 750, 1624, 30
G = (181, 229, 29); LW = 7; DIM = 0.30          # dim the rest of the screen by up to 30 % while a highlight shows
FADE_IN, FADE_OUT = 0.30, 0.15

def mark(box, arrow=None, sl=46):
    """RGBA layer with the box (and arrow) plus the region kept bright."""
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    x0, y0, x1, y1 = box; d.rectangle([x0, y0, x1, y1], outline=G + (255,), width=LW)
    if arrow:
        cx, top, hh, hw, sw = arrow, y1 + (8 if sl < 46 else 10), 40, 94, 54
        d.polygon([(cx, top), (cx - hw / 2, top + hh), (cx + hw / 2, top + hh)], fill=G + (255,))
        d.rectangle([cx - sw / 2, top + hh - 1, cx + sw / 2, top + hh + sl], fill=G + (255,))
    a = np.asarray(im).astype(np.float32)
    keep = np.zeros((H, W), np.float32); keep[max(0, y0):y1 + 1, max(0, x0):x1 + 1] = 1   # inside the box stays bright
    return a[..., :3], a[..., 3:] / 255.0, keep[..., None]

APP = (42, 110, 189, 294); SEARCH = (32, 96, 600, 210); GET = (552, 284, 719, 369); RING = (636, 281, 724, 369); NHS = (40, 694, 709, 826)
M = {'app': mark(APP), 'search': mark(SEARCH), 'search+': mark(SEARCH, 230, 22), 'get': mark(GET, 636),
     'ring': mark(RING, 680), 'open': mark(GET, 636), 'nhs': mark(NHS)}

# segments: ('play', from, to, speed, highlight) or ('hold', at, seconds, highlight); times are source seconds
CLIPS = {
 'inst-1': [('play', 5.6, 7.45, 1, None), ('hold', 7.45, 2.2, 'app'), ('play', 7.45, 7.62, 1, 'app'), ('play', 7.62, 9.0, 1, None)],
 'inst-3': [('play', 9.6, 9.95, 1, None), ('hold', 9.95, 1.8, 'search'), ('play', 9.95, 16.4, 2, 'search'),
            ('play', 16.4, 19.4, 3, 'search'), ('play', 19.4, 20.45, 1, 'search'), ('hold', 20.45, 2.4, 'search+')],
 'inst-4': [('play', 20.6, 21.0, 1, None), ('hold', 21.0, 2.4, 'get'), ('play', 24.95, 25.35, 1, 'get'), ('play', 25.35, 26.2, 1, None)],
 'inst-5': [('play', 25.2, 25.5, 1, None), ('play', 25.5, 27.46, 1, 'ring'), ('hold', 27.46, 2.0, 'ring'),
            ('play', 27.46, 27.65, 1, 'ring'), ('play', 27.65, 28.6, 1, None)],
 'inst-6': [('play', 27.7, 28.1, 1, None), ('hold', 28.1, 2.4, 'open'), ('play', 32.25, 32.63, 1, 'open'), ('play', 32.63, 34.1, 1, None)],
 'inst-7': [('play', 35.0, 39.0, 1, None), ('play', 39.6, 40.95, 1, None), ('play', 41.0, 43.5, 1, None),
            ('play', 45.5, 46.95, 1, None), ('hold', 46.95, 3.0, 'nhs')],
}

def frames(segs):
    """yield (source time, highlight) for every output frame."""
    for s in segs:
        if s[0] == 'play':
            _, a, b, sp, hl = s; n = max(1, round((b - a) / sp * FPS))
            for i in range(n): yield a + i * sp / FPS, hl
        else:
            _, t, dur, hl = s
            for i in range(round(dur * FPS)): yield t, hl

for name, segs in CLIPS.items():
    plan = list(frames(segs))
    a0 = plan[0][0]; a1 = max(t for t, _ in plan) + 0.05
    dec = subprocess.Popen(['ffmpeg', '-v', 'error', '-ss', f'{a0:.3f}', '-to', f'{a1:.3f}', '-i', SRC, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                            '-vf', 'scale=418:904:flags=lanczos,format=yuv420p', '-an', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '22',
                            '-profile:v', 'high', '-level', '4.0', '-movflags', '+faststart', os.path.join(OUT, name + '.mp4')], stdin=subprocess.PIPE)
    cur, cur_t, idx = None, a0 - 1, 0
    alpha, shown = 0.0, None
    for t, hl in plan:
        while cur_t + 1e-6 < t - (1 / 120):                       # advance the decoder to the frame for time t (60 fps source)
            buf = dec.stdout.read(W * H * 3)
            if len(buf) < W * H * 3: break
            cur = np.frombuffer(buf, np.uint8).reshape(H, W, 3); cur_t = a0 + idx / 60; idx += 1
        f = cur.astype(np.float32)
        if hl: alpha = min(1.0, alpha + 1 / (FADE_IN * FPS)); shown = hl
        else: alpha = max(0.0, alpha - 1 / (FADE_OUT * FPS))
        if shown and alpha > 0:
            rgb, a, keep = M[shown]
            f = f * (1 - DIM * alpha * (1 - keep))                  # dim outside the box
            f = f * (1 - a * alpha) + rgb * a * alpha                # box and arrow
        enc.stdin.write(np.clip(f, 0, 255).astype(np.uint8).tobytes())
    enc.stdin.close(); enc.wait(); dec.kill()
    out = os.path.join(OUT, name + '.mp4'); print(name, f'{len(plan) / FPS:.1f}s', os.path.getsize(out))
