"""Home Screen icon: ABC blocks only, larger (David chose "New 2", 19 Nov 2026; replaces "B+F 1" with the GUIDE label).
Writes icon-source.svg and renders icon-180/192/512 + icon-maskable-512 PNGs into OUTDIR,
using the Archivo font embedded in the guide (so the letters match the guide's headings).
usage: python3 make_icons.py guide.html OUTDIR"""
import re, sys, os
from playwright.sync_api import sync_playwright
guide, out = sys.argv[1], sys.argv[2]; os.makedirs(out, exist_ok=True)
font = re.search(r"@font-face\{font-family:'Archivo';[^}]*\}", open(guide, encoding='utf-8').read()).group(0)
NAVY, MAG = '#16314f', '#a3124d'
def block(x, y, s, L):
    return (f'<rect x="{x}" y="{y+8}" width="{s}" height="{s}" rx="{s*.16:.0f}" fill="#000" opacity=".16"/>'
            f'<rect x="{x}" y="{y}" width="{s}" height="{s}" rx="{s*.16:.0f}" fill="#fff"/>'
            f'<text x="{x+s/2}" y="{y+s*.74:.0f}" text-anchor="middle" font-family="Archivo" font-weight="800" font-size="{s*.66:.0f}" fill="{MAG}">{L}</text>')
s, ax, ay, gap = 160, 176, 82, 20
GLYPH = block(ax, ay, s, 'A') + block(ax - s//2 - gap//2, ay + s + gap, s, 'B') + block(ax + s//2 + gap//2, ay + s + gap, s, 'C')
def svg(scale=1.0):
    g = GLYPH if scale == 1 else f'<g transform="translate(256 256) scale({scale}) translate(-256 -256)">{GLYPH}</g>'
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">'
            '<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#6c155c"/><stop offset="1" stop-color="#d01545"/></linearGradient></defs>'
            f'<rect width="512" height="512" fill="url(#g)"/>{g}</svg>')
open(os.path.join(out, 'icon-source.svg'), 'w').write('<!-- Text uses the Archivo font (weight 800), as embedded in the guide. -->\n' + svg())
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/usr/bin/google-chrome')
    for name, size, sc in [('icon-180.png', 180, 1), ('icon-192.png', 192, 1), ('icon-512.png', 512, 1), ('icon-maskable-512.png', 512, 0.78)]:
        pg = b.new_page(viewport={'width': size, 'height': size})
        pg.set_content(f'<style>{font}html,body{{margin:0}}svg{{display:block;width:{size}px;height:{size}px}}</style>{svg(sc)}')
        pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(300)
        assert pg.evaluate("document.fonts.check('800 100px Archivo')")
        pg.screenshot(path=os.path.join(out, name)); pg.close()
    b.close()
print('icons written to', out)
